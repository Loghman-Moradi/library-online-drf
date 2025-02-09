from rest_framework import serializers
from .models import *


class CartSerializer(serializers.ModelSerializer):
    user_phone = serializers.SerializerMethodField()  
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'user_phone', 'cart_items', ]

    def get_user_phone(self, obj):
        if obj.user:
            return obj.user.phone
        return None

    def get_cart_items(self, obj):
        items = obj.cart_items.all()
        return CartItemSerializer(instance=items, many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = '__all__'

    def get_book(self, obj):
        return obj.book.title
