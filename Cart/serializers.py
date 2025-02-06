from rest_framework import serializers
from .models import *


class CartSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.phone

    def get_cart_items(self, obj):
        return CartSerializer(instance=obj.cart_items.all(), many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = '__all__'

    def get_book(self, obj):
        return obj.book.title
