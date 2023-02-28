from django.urls import path, include
from .views import GenerateOtpAPI,VerifyOtpAPI
urlpatterns = [
    path('generateOTP/', GenerateOtpAPI.as_view()),
    path('verifyOTP/',VerifyOtpAPI.as_view()),
]