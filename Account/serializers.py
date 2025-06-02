from rest_framework import serializers
from Orders.models import OrderItem
from .models import Profile
from Bookish.serializers import BookListSerializer
import re


class ProfileSerializer(serializers.ModelSerializer):
    purchased_books = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'purchased_books', 'first_name', 'last_name', 'bio', 'profile_image', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_purchased_books(self, obj):
        purchased_items = OrderItem.objects.filter(
            order__user=obj.user,
            order__is_paid=True
        ).select_related('book__genre').prefetch_related('book__authors')
        purchased_books = [item.book for item in purchased_items]
        return BookListSerializer(purchased_books, many=True).data


class LibraryUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError(
                "Invalid phone number format. Phone number must start with '09' and be 11 digits long.")
        return value



