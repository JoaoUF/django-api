from authentication.views import RegisterView, VerifyEmail, LoginAPIView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="register"),
    path('verify-email/', VerifyEmail.as_view(), name="verify-email"),
]
