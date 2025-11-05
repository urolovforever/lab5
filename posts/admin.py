from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'confession', 'author', 'is_pinned', 'is_active', 'created_at']
    list_filter = ['confession', 'is_pinned', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'likes_count', 'comments_count']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']
