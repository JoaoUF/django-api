from authentication.views import RegisterView, VerifyEmail, LoginAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPassword
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="register"),
    path('verify-email/', VerifyEmail.as_view(), name="verify-email"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset-complete/', SetNewPassword.as_view(), name="password-reset-complete"),
    path('password-reset/<uuid64>/<token>/', PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
]
