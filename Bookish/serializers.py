from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Orders.models import OrderItem
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Comment
        fields = ['user', 'book', 'message']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def validate(self, attrs):
        user = self.context['request'].user
        book = attrs['book']

        if Rating.objects.filter(user=user, book=book).exists():
            raise ValidationError("You have already rated this book.")
        return attrs

    class Meta:
        model = Rating
        fields = ['user', 'book', 'rate']


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'new_price', 'average_rating']


class BookDetailSerializer(serializers.ModelSerializer):
    new_price = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    rating = RatingSerializer(many=True, read_only=True)
    audio_file = serializers.SerializerMethodField()
    pdf_file = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'authors', 'genre', 'price', 'offers', 'new_price', 'cover_image',
                  'audio_file', 'pdf_file', 'comments', 'rating', 'average_rating']

    def get_new_price(self, obj):
        return obj.new_price

    def check_order(self, user, book):
        if user.is_anonymous:
            return False
        return OrderItem.objects.filter(
            order__user=user,
            book=book,
            order__is_paid=True,
        ).exists()

    def get_audio_file(self, obj):
        request = self.context.get('request')
        user = request.user

        if obj.audio_file:
            if obj.price > 0 and not self.check_order(user, obj):
                return None
            return request.build_absolute_uri(obj.audio_file.url)
        return None

    def get_pdf_file(self, obj):
        request = self.context.get('request')
        user = request.user

        if obj.pdf_file:
            if obj.price > 0 and not self.check_order(user, obj):
                return None
            return request.build_absolute_uri(obj.pdf_file.url)
        return None


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']




# {
#     "message": "User found",
#     "user": "09214249950",
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQzMjc3NTU1LCJpYXQiOjE3NDE0NjMxNTUsImp0aSI6ImFlMTM4YzgyZWU4ZjRmNTQ5ZmViNDMxMzc5NDBhOGIwIiwidXNlcl9pZCI6MX0.acrSjayab0qXlqoeE1nvzIuH0acN3VzQilL8H31yJSc",
#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0Mzg4MjM1NSwiaWF0IjoxNzQxNDYzMTU1LCJqdGkiOiJkMDQzNTYxMjBjZDU0NWZjYjc0NjFkYTg1MGZlY2U1NSIsInVzZXJfaWQiOjF9.kDxSC9s6m045Nibs3nInqLbrKY4RKq1uLZNLMSd0IAg"
# }















