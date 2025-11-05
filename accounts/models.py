from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with additional fields
    Roles: 'user', 'confession_admin', 'superadmin'
    """
    ROLE_CHOICES = [
        ('user', 'Oddiy foydalanuvchi'),
        ('confession_admin', 'Konfessiya admini'),
        ('superadmin', 'SuperAdmin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Roli'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    is_email_verified = models.BooleanField(default=False, verbose_name='Email tasdiqlangan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
