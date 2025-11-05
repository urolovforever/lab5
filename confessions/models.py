from django.db import models
from django.conf import settings


class Confession(models.Model):
    """
    Diniy konfessiyalar modeli (16 ta konfessiya)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nomi')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    icon = models.ImageField(upload_to='confession_icons/', blank=True, null=True, verbose_name='Ikonka')
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_confessions',
        limit_choices_to={'role': 'confession_admin'},
        verbose_name='Admin'
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')

    class Meta:
        verbose_name = 'Konfessiya'
        verbose_name_plural = 'Konfessiyalar'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Foydalanuvchilar konfessiyalarga obuna bo'lish modeli
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Foydalanuvchi'
    )
    confession = models.ForeignKey(
        Confession,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Konfessiya'
    )
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Obuna bo\'lgan vaqt')

    class Meta:
        verbose_name = 'Obuna'
        verbose_name_plural = 'Obunalar'
        unique_together = ['user', 'confession']
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.user.username} -> {self.confession.name}"
