from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("cart_page/", views.CartPageView.as_view(), name="cart_page"),
    path("add_to_cart/<int:book_id>/", views.AddCartView.as_view(), name="add_to_cart"),
    path("delete_cart/<int:pk>/", views.DeleteCartItemView.as_view(), name="delete_cart_item"),
    path("clear_cart/", views.ClearCartView.as_view(), name="clear_cart"),
]