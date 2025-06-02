from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *


class BookListApiView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.select_related('genre').prefetch_related('authors')
    serializer_class = BookListSerializer


class BookDetailApiView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.select_related('genre').prefetch_related('authors', 'comments')
    serializer_class = BookDetailSerializer


class AuthorsApiView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer


class CommentApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        rating = serializer.save(user=self.request.user)
        rating.book.update_average_rating()































