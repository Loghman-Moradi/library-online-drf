from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class BookSerializer(serializers.ModelSerializer):
    queryset = Comment.objects.all()
    new_price = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    rating = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'authors', 'genre', 'price', 'offers', 'new_price', 'cover_image',
                  'pdf_file', 'audio_file', 'comments', 'rating', 'average_rating']

    def get_new_price(self, obj):
        return obj.new_price


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']




# {
#     "message": "User found",
#     "user": "09184517699",
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4NTk3NDg2LCJpYXQiOjE3Mzg1OTcxODYsImp0aSI6ImQ2YjgzZjZjOTU2YjQ0NTdhNWUyMWVlYTRiY2UyYWQ1IiwidXNlcl9pZCI6NX0.G-Y6q27--8oMpVlzpFb7FE18iRJGvSRGuAb24oW_wwk",
#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODY4MzU4NiwiaWF0IjoxNzM4NTk3MTg2LCJqdGkiOiI3OTZlNjQ3ODNkNzQ0NWJlODg5MzI1MTU1YmY5NDFkYyIsInVzZXJfaWQiOjV9.pdlcWUUAWJJJ3E9fHXpq6i3stlsEvis7GZf_BACZMA4"
# }
















