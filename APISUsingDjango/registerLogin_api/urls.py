from django.urls import path
from .views import UserDetailAPI, RegisterUserAPIView

urlpatterns = [
    path('reglogapi/user-details/', UserDetailAPI.as_view()),
    path('reglogapi/register/', RegisterUserAPIView.as_view())
]