from django.db import models
from django.conf import settings
from confessions.models import Confession


class Post(models.Model):
    """
    Konfessiya adminlari tomonidan joylangan postlar
    """
    confession = models.ForeignKey(
        Confession,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Konfessiya'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Muallif'
    )
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    content = models.TextField(verbose_name='Mazmun')
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True, verbose_name='Rasm')
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True, verbose_name='Video')
    is_pinned = models.BooleanField(default=False, verbose_name='Muhim (Pin)')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Postlar'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.confession.name}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.filter(is_active=True).count()


class Comment(models.Model):
    """
    Postlarga kommentlar
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Muallif'
    )
    content = models.TextField(verbose_name='Komment')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')

    class Meta:
        verbose_name = 'Komment'
        verbose_name_plural = 'Kommentlar'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} -> {self.post.title[:30]}"


class Like(models.Model):
    """
    Postlarga like qo'yish (faqat bir marta)
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Post'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Foydalanuvchi'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Like qo\'yilgan vaqt')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likelar'
        unique_together = ['post', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.post.title[:30]}"
