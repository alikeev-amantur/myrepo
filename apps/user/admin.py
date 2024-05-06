from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'role', 'is_staff','max_establishments']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'date_of_birth', 'avatar', 'role','max_establishments')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_blocked', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'name']
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
