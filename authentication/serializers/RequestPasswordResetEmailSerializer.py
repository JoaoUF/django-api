from rest_framework import serializers
from authentication.models import CustomUser

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']
