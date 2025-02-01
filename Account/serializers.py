from rest_framework import serializers
from .models import LibraryUsers


class LibraryUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
