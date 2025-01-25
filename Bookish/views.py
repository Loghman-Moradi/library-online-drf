import os.path

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookApiView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['get'])
    def download_audio(self, request, pk=None):
        try:
            book = self.get_object()
            if book.audio_file:
                audio_url = request.build_absolute_uri(book.audio_file.url)
                return Response({"Audio_url": audio_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Audio File Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        try:
            book = self.get_object()
            if book.pdf_file:
                pdf_url = request.build_absolute_uri(book.pdf_file.url)
                return Response({"Pdf_url": pdf_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Pdf File Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthorsApiView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer







































