from django.contrib import admin
from .models import Book, Author, Genre, Comment, Rating


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'authors', 'genre', 'publication_date', 'new_price']
    list_filter = ['authors', 'title']
    readonly_fields = ['new_price']

    def authors(self, obj):
        if hasattr(obj, 'authors') and hasattr(obj.authors, 'all'):
            return ",".join([author.name for author in obj.authors.all()])
        elif hasattr(obj, 'authors'):
            return obj.authors.name


    def new_price(self, obj):
        return obj.new_price

    new_price.short_description = 'New Price'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'bio']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book']
    list_filter = ['created_at', 'user', 'book']
    search_fields = ['message', 'user__username', 'book__title']
    raw_id_fields = ['user', 'book', 'parent']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'rate']
    list_filter = ['rate', 'book']
    search_fields = ['user__username', 'book__title']
    raw_id_fields = ['user', 'book']















