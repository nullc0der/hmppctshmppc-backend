from django.db.models import F

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from payment_processor.models import Payment
from payment_processor.utils import create_payment, check_payment

from core_api.serializers import InitiatePaymentSerializer, GetStatsSerializer
from core_api.tasks import task_create_stats_snapshot
from core_api.utils import get_or_create_access_token
from core_api.models import AccessToken


class InitiatePayment(APIView):
    """
    This API will be used to initiate a payment for revealing stats
    """

    def post(self, request, format=None):
        serializer = InitiatePaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_info = create_payment(
                serializer.validated_data['currency'])
            if payment_info['wallet_address']:
                task_create_stats_snapshot.delay(payment_info['payment_id'])
                return Response(payment_info)
            return Response(
                {'error': 'unknown error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckPaymentCompleted(APIView):
    """
    This API will be used to check if payment is completed
    """

    def post(self, request, format=None):
        try:
            payment = Payment.objects.get(
                payment_id=request.data.get('payment_id', ''))
            if check_payment(payment):
                access_token = get_or_create_access_token(
                    payment.statssnapshot)
                return Response({
                    'access_token': access_token,
                    'tx_ids': payment.get_tx_ids_as_json(),
                    'amount_received': payment.amount_received
                })
            return Response(
                {'error': 'payment not processed'},
                status=status.HTTP_304_NOT_MODIFIED
            )
        except Payment.DoesNotExist:
            return Response(
                {'error': 'payment id not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class GetStats(APIView):
    """
    This API will be used to get stats
    """

    def post(self, request, format=None):
        serializer = GetStatsSerializer(data=request.data)
        if serializer.is_valid():
            access_token = AccessToken.objects.get(
                token=serializer.validated_data['access_token'])
            # TODO: Research(IMP) also transaction.atomic
            access_token.used_count = F('used_count') + 1
            access_token.save()
            return Response({
                'stats': access_token.stats_snapshot.get_stats_as_json(),
                'created_on': access_token.stats_snapshot.created_on
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
