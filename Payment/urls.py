from django.urls import path
from .views import PaymentView, PaymentVerifyView


app_name = 'payment'
urlpatterns = [
    path('payment/request/', PaymentView.as_view(), name='payment-request'),
    path('payment/verify/', PaymentVerifyView.as_view(), name='payment-verify'),
]