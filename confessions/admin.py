from django.contrib import admin
from .models import Confession, Subscription


@admin.register(Confession)
class ConfessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'admin', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'confession', 'subscribed_at']
    list_filter = ['confession', 'subscribed_at']
    search_fields = ['user__username', 'confession__name']
    readonly_fields = ['subscribed_at']
