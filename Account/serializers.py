from rest_framework import serializers
from Bookish.models import BookPurchase
from Orders.models import OrderItem
from .models import Profile
from Bookish.serializers import BookListSerializer


class ProfileSerializer(serializers.ModelSerializer):
    purchased_books = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'purchased_books', 'first_name', 'last_name', 'bio', 'profile_image', 'created_at', 'updated_at']

    def get_purchased_books(self, obj):
        purchased_items = OrderItem.objects.filter(order__user=obj.user, order__is_paid=True)
        purchased_books = [item.book for item in purchased_items]
        return BookListSerializer(purchased_books, many=True).data


class LibraryUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)


