from django.contrib import admin
from .models import LibraryUsers
from django.contrib.auth.admin import UserAdmin


@admin.register(LibraryUsers)
class LibraryUserAdmin(UserAdmin):
    ordering = ['phone']
    model = LibraryUsers
    list_display = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )

    readonly_fields = ('date_joined',)
