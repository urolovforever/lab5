from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, LikeSerializer
from confessions.models import Subscription


class IsConfessionAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: faqat konfessiya admini yoki superadmin post yarata oladi
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['confession_admin', 'superadmin']

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role == 'superadmin'


class PostViewSet(viewsets.ModelViewSet):
    """
    Postlar uchun CRUD operatsiyalari
    """
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    permission_classes = [IsConfessionAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Foydalanuvchining obuna bo'lgan konfessiyalaridan postlar
        """
        if not request.user.is_authenticated:
            return Response({'error': 'Tizimga kirishingiz kerak!'},
                            status=status.HTTP_401_UNAUTHORIZED)

        subscriptions = Subscription.objects.filter(user=request.user)
        confession_ids = subscriptions.values_list('confession_id', flat=True)
        posts = Post.objects.filter(confession_id__in=confession_ids, is_active=True)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Postga like qo'yish
        """
        post = self.get_object()
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            return Response({'message': 'Siz allaqachon like qo\'ygansiz!'},
                            status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, post=post)
        return Response({'message': 'Like qo\'yildi!'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        Postdan like ni olib tashlash
        """
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'error': 'Siz bu postga like qo\'ymagansiz!'},
                            status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'message': 'Like olib tashlandi!'})


class CommentViewSet(viewsets.ModelViewSet):
    """
    Kommentlar uchun CRUD operatsiyalari
    """
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        # Faqat muallif yoki post konfessiyasi admini o'chira oladi
        user = self.request.user
        if instance.author == user or instance.post.confession.admin == user or user.role == 'superadmin':
            instance.is_active = False
            instance.save()
        else:
            return Response({'error': 'Ruxsat berilmagan!'},
                            status=status.HTTP_403_FORBIDDEN)
