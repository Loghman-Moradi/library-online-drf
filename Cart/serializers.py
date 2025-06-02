from rest_framework import serializers
from Bookish.serializers import BookListSerializer
from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['id', 'book', 'quantity', 'price']
        read_only_fields = ['book', 'price']

    def get_book(self, obj):
        return obj.book.title

    def get_price(self, obj):
        return obj.price


class CartSerializer(serializers.ModelSerializer):
    user_phone = serializers.SerializerMethodField()
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'user_phone', 'cart_items', 'total_price']
        read_only_fields = ['user', 'session_id']

    def get_user_phone(self, obj):
        if obj.user:
            return obj.user.phone
        return None

    def get_cart_items(self, obj):
        items = obj.cart_items.all()
        return CartItemSerializer(instance=items, many=True).data

    def get_total_price(self, obj):
        return obj.total_price


