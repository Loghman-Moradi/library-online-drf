from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("cart_page/", views.CartPageView.as_view(), name="cart_page"),
    path("add_to_cart/<int:book_id>/", views.AddCartView.as_view(), name="add_to_cart"),
    path("delete_cart/<int:pk>/", views.DeleteCartView.as_view(), name="delete_cart"),
    path("delete_whole_cartitems/", views.DeleteWholeCart.as_view(), name="delete_whole_cartitems"),
]