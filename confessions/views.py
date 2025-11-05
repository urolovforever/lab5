from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Confession, Subscription
from .serializers import ConfessionSerializer, ConfessionCreateSerializer, SubscriptionSerializer
from posts.models import Post
from posts.serializers import PostSerializer


class ConfessionViewSet(viewsets.ModelViewSet):
    """
    Konfessiyalar uchun CRUD operatsiyalari
    """
    queryset = Confession.objects.filter(is_active=True)
    serializer_class = ConfessionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_posts']:
            return [permissions.AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConfessionCreateSerializer
        return ConfessionSerializer

    @action(detail=True, methods=['get'])
    def get_posts(self, request, pk=None):
        """
        Konfessiyaning barcha postlarini olish
        """
        confession = self.get_object()
        posts = Post.objects.filter(confession=confession, is_active=True)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """
        Konfessiyaga obuna bo'lish
        """
        confession = self.get_object()
        user = request.user

        if Subscription.objects.filter(user=user, confession=confession).exists():
            return Response({'message': 'Siz allaqachon obuna bo\'lgansiz!'},
                            status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.create(user=user, confession=confession)
        return Response({'message': 'Muvaffaqiyatli obuna bo\'ldingiz!'})

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        """
        Konfessiyadan obunani bekor qilish
        """
        confession = self.get_object()
        user = request.user

        subscription = Subscription.objects.filter(user=user, confession=confession).first()
        if not subscription:
            return Response({'error': 'Siz bu konfessiyaga obuna bo\'lmagansiz!'},
                            status=status.HTTP_400_BAD_REQUEST)

        subscription.delete()
        return Response({'message': 'Obuna bekor qilindi!'})

    @action(detail=False, methods=['get'])
    def my_subscriptions(self, request):
        """
        Foydalanuvchining obunalari
        """
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True, context={'request': request})
        return Response(serializer.data)
