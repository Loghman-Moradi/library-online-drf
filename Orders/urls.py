from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('view_order/', views.OrderPageView.as_view(), name='view_order_page'),
    path('create_order/', views.OrderCreateView.as_view(), name='create_order'),
    path('apply_coupon/', views.ApplyCouponView.as_view(), name='apply_coupon'),
]