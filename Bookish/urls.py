from os.path import basename

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = "book"
router = DefaultRouter()
router.register(r'books', views.BookApiView)
router.register(r'authors', views.AuthorsApiView)
router.register(r'comment', views.CommentApiView)
router.register(r'rating', views.RatingApiView)


urlpatterns = [
    path('', include(router.urls)),

]