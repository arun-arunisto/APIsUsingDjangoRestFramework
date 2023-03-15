from django.urls import path
from .views import ListCreateSongsView, TrackDetailView, LoginView, RegisterUsers


urlpatterns = [
    path('tracks/', ListCreateSongsView.as_view(),name="tracks-list-view"),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name="tracks-detail-view"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/register/", RegisterUsers.as_view(), name="auth-register")
]