import jwt

from authentication.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer
from authentication.models import CustomUser
from authentication.renderers import CustomUserRender
from utils import Utils

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer
    render_classes=(CustomUserRender,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
        email_body = 'Hi ' + user.email + ' use link below to verify your email \n' + absurl
        data = {
            'email_body': email_body,
            'email_subject': 'Verify your account',
            'email_to': user.email
        }
        Utils.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',in_= openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email': 'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return Response({'email': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.filter(email=email)
            uidb64 = urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-resest-confirm', 
                kwargs = {'uidb64': uidb64, 'token': token}
            )
            absurl = 'http://' + current_site + relativeLink 
            email_body = 'Hi ' + user.email + 'Use link to reset your password' + absurl
            data = {
                'email_body': email_body,
                'email_subject': 'Reset your password',
                'email_to': user.email
            }
            Utils.send_email(data)
        return Response({'success':'We have sent you a link to reset your password'}, status= status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,requeset,uidb64,token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request new one'}, status= status.HTTP_400_BAD_REQUEST)

            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status= status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response({'error':'Token is not valid, please request new one'}, status= status.HTTP_400_BAD_REQUEST)

class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def path(self,request):
        serialier = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
