from rest_framework import serializers

from core_api.models import AccessToken


class GetStatsSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate_access_token(self, value):
        try:
            access_token = AccessToken.objects.get(token=value)
            if access_token.used_count >= 3:
                raise serializers.ValidationError('access token is used')
            return value
        except AccessToken.DoesNotExist:
            raise serializers.ValidationError('access token not exist')
