from rest_framework import serializers
from .models import *


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_items', 'coupon_used', 'coupon', 'is_paid', 'created_at', 'subtotal']

    def get_order_items(self, obj):
        items = obj.order_items.all()
        return OrderItemSerializer(items, many=True).data

    def get_subtotal(self, obj):
        return obj.subtotal


class OrderItemSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'quantity', 'final_price']

    def create(self, validated_data):
        validated_data['quantity'] = 1
        return super().create(validated_data)

    def get_final_price(self, obj):
        return obj.final_price




