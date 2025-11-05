from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    UserUpdateSerializer, ChangePasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchilar uchun CRUD operatsiyalari
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['register', 'login']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Yangi foydalanuvchi ro'yxatdan o'tkazish
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Ro\'yxatdan o\'tdingiz! Email manzilingizni tasdiqlang.',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Foydalanuvchi tizimga kirishi
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username va password talab qilinadi!'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Tizimga muvaffaqiyatli kirdingiz!',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        return Response({'error': 'Username yoki parol xato!'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Joriy foydalanuvchi ma'lumotlarini olish
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """
        Foydalanuvchi profilini yangilash
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profil yangilandi!', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Parolni o'zgartirish
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Eski parol xato!'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
