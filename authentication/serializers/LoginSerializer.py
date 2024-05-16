from rest_framework import serializers
from authentication.models import CustomUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user=auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account not activated')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'tokens': user.tokens
        }
        return super().validate(attrs)
