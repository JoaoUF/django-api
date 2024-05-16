from rest_framework import serializers
from authentication.models import CustomUser

class EmailVerificationSerializer(serializers.ModelSerializer):
    token= serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']
