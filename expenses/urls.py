from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpeneseListAPIView.as_view(), name= 'expenses'),
    path('<int:id>', views.ExpeneseDetailAPIView.as_view(), name= 'expense'),
]
