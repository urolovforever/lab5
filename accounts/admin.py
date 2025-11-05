from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_email_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_email_verified', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('role', 'is_email_verified')}),
    )
