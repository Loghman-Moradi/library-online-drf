from django.contrib import admin
from .models import LibraryUsers, Profile
from django.contrib.auth.admin import UserAdmin


@admin.register(LibraryUsers)
class LibraryUserAdmin(UserAdmin):
    ordering = ['phone']
    model = LibraryUsers
    list_display = ['id', 'phone', 'is_active', 'is_staff']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('phone', 'password')},
         ),
    )

    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('is_active', 'is_staff', 'is_superuser')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','first_name', 'last_name', 'bio']
    search_fields = ['user__phone', 'first_name', 'last_name', 'bio']
    list_filter = ['created_at', 'updated_at']
    raw_id_fields = ['user']














