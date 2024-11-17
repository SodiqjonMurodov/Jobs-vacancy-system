from django.urls import path
from .views import UserThemeView, UserRegistrationAPIView

urlpatterns = [
    path('theme/', UserThemeView.as_view(), name='theme'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('register/confirm/', UserRegistrationAPIView.as_view(), name='user-confirm'),
]