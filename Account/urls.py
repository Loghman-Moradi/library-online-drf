from django.urls import path
from . import views
from .views import ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'
urlpatterns = [
    path('send-otp/', views.SendOtpView.as_view(), name='send_otp_view'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify-otp-view'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', ProfileView.as_view(), name='profile-detail'),
]
