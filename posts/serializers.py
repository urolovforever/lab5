from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserSerializer
from confessions.serializers import ConfessionSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment model uchun serializer
    """
    author_info = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_info', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    """
    Like model uchun serializer
    """
    user_info = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'user_info', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """
    Post model uchun serializer
    """
    author_info = UserSerializer(source='author', read_only=True)
    confession_info = ConfessionSerializer(source='confession', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'confession', 'confession_info', 'author', 'author_info', 'title',
                  'content', 'image', 'video', 'is_pinned', 'is_active', 'likes_count',
                  'comments_count', 'is_liked', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Yangi post yaratish uchun (faqat confession admin)
    """
    class Meta:
        model = Post
        fields = ['confession', 'title', 'content', 'image', 'video', 'is_pinned']

    def validate(self, attrs):
        # Check if user is admin of the confession
        request = self.context.get('request')
        confession = attrs.get('confession')

        if request.user.role == 'superadmin':
            return attrs

        if request.user.role == 'confession_admin' and confession.admin == request.user:
            return attrs

        raise serializers.ValidationError("Siz bu konfessiyaga post joylay olmaysiz!")

    def validate_image(self, value):
        if value and value.size > 5242880:  # 5MB
            raise serializers.ValidationError("Rasm hajmi 5MB dan oshmasligi kerak!")
        return value

    def validate_video(self, value):
        if value and value.size > 52428800:  # 50MB
            raise serializers.ValidationError("Video hajmi 50MB dan oshmasligi kerak!")
        return value
