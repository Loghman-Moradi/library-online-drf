from rest_framework import serializers


class LibraryUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
