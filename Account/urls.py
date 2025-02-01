from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('send-otp/', views.SendOtpView.as_view(), name='send_otp_view'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify-otp-view'),
    # path('token-refresh/', views.RefreshTokenView.as_view(), name='token-refresh'),
]