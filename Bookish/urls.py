from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

app_name = "book"

router = SimpleRouter()
router.register(r'authors', views.AuthorsApiView, basename='author')
router.register(r'comments', views.CommentApiView, basename='comment')
router.register(r'ratings', views.RatingApiView, basename='rating')

urlpatterns = [
    path('books/', views.BookListApiView.as_view(), name='book_list_api'),
    path('book_detail/<int:pk>/', views.BookDetailApiView.as_view(), name='book_detail_api'),
    path('', include(router.urls)),
]

