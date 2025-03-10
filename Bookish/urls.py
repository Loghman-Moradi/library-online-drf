from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    path('books/', views.BookListApiView.as_view(), name='bool_list_api'),
    path('book_detail/<int:pk>/', views.BookDetailApiView.as_view(), name='bool_detail_api'),
]