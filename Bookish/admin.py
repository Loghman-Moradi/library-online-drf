from django.contrib import admin
from .models import Book, Author, Genre, Comment, Rating


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'authors', 'genre', 'publication_date', 'new_price']
    list_filter = ['authors', 'title']
    readonly_fields = ['new_price']

    def new_price(self, obj):
        return obj.new_price

    new_price.short_description = 'New Price'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'bio']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']















