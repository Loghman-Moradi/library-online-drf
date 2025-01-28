from rest_framework import serializers
from .models import LibraryUsers


class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUsers
        fields = ['phone']
