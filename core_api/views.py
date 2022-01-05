import random
from django.db.models import F
import hmac
import hashlib
import json

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ekatagp.models import PaymentForm
from ekatagp.utils import create_payment_form

from core_api.serializers import GetStatsSerializer
from core_api.tasks import task_create_stats_snapshot
from core_api.utils import get_or_create_access_token
from core_api.models import AccessToken


class InitiatePayment(APIView):
    """
    This API will be used to initiate a payment for revealing stats
    """

    def post(self, request, format=None):
        amount = round(random.uniform(1, 2), 2)
        form_id = create_payment_form(amount)
        if form_id:
            task_create_stats_snapshot.delay(form_id)
            return Response({'form_id': form_id})
        return Response(
            {'error': 'no_form_id'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessView(APIView):
    """
        This API will be used when a payment is completed
    """

    def post(self, request):
        message = f"{request.data['payment_id']}" + \
            f"{request.data['wallet_address']}" + \
            f"{request.data['currency_name']}"
        signature = hmac.new(
            settings.EKATA_GATEWAY_PROCESSOR_PROJECT_API_SECRET.encode(),
            message.encode(),
            hashlib.sha256).hexdigest()
        if signature == request.data['signature']:
            try:
                form = PaymentForm.objects.get(form_id=request.data['form_id'])
                form.is_payment_success = True
                form.payment_payload = json.dumps(request.data)
                form.save()
                statssnapshot = form.statssnapshot
                stats = statssnapshot.get_stats_as_json()
                currency_name = request.data['currency_name']
                stats[f'{currency_name}_payment_count'] += 1
                statssnapshot.stats = json.dumps(stats)
                statssnapshot.save()
                access_token = get_or_create_access_token(form.statssnapshot)
                return Response({
                    'access_token': access_token,
                })
            except PaymentForm.DoesNotExist:
                return Response(
                    {'error': 'Payment form not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'payment not processed'},
            status=status.HTTP_304_NOT_MODIFIED
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
