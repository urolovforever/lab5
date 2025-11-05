from rest_framework import serializers
from .models import Confession, Subscription
from accounts.serializers import UserSerializer


class ConfessionSerializer(serializers.ModelSerializer):
    """
    Confession model uchun serializer
    """
    admin_info = UserSerializer(source='admin', read_only=True)
    subscribers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Confession
        fields = ['id', 'name', 'slug', 'description', 'icon', 'admin', 'admin_info',
                  'is_active', 'subscribers_count', 'posts_count', 'is_subscribed',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_posts_count(self, obj):
        return obj.posts.filter(is_active=True).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, confession=obj).exists()
        return False


class ConfessionCreateSerializer(serializers.ModelSerializer):
    """
    Yangi konfessiya yaratish uchun (faqat superadmin)
    """
    class Meta:
        model = Confession
        fields = ['name', 'slug', 'description', 'icon', 'admin']


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Subscription model uchun serializer
    """
    user_info = UserSerializer(source='user', read_only=True)
    confession_info = ConfessionSerializer(source='confession', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_info', 'confession', 'confession_info', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']
