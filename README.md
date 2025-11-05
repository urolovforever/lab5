# Diniy Konfessiyalar Platformasi - Backend

Django REST Framework asosida qurilgan backend API.

## O'rnatish

1. Virtual environment yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

2. Kerakli paketlarni o'rnating:
```bash
pip install -r requirements.txt
```

3. Migratsiyalarni bajaring:
```bash
python manage.py migrate
```

4. Superuser yarating:
```bash
python manage.py createsuperuser
```

5. Serverni ishga tushiring:
```bash
python manage.py runserver
```

## API Endpoints

### Autentifikatsiya
- `POST /api/auth/users/register/` - Ro'yxatdan o'tish
- `POST /api/auth/users/login/` - Tizimga kirish
- `GET /api/auth/users/me/` - Joriy foydalanuvchi ma'lumotlari
- `PUT /api/auth/users/update_profile/` - Profilni yangilash
- `POST /api/auth/users/change_password/` - Parolni o'zgartirish

### JWT Token
- `POST /api/token/` - Token olish
- `POST /api/token/refresh/` - Tokenni yangilash

### Konfessiyalar
- `GET /api/confessions/` - Barcha konfessiyalar ro'yxati
- `GET /api/confessions/{id}/` - Bitta konfessiya ma'lumotlari
- `POST /api/confessions/` - Yangi konfessiya yaratish (superadmin)
- `GET /api/confessions/{id}/get_posts/` - Konfessiya postlari
- `POST /api/confessions/{id}/subscribe/` - Obuna bo'lish
- `POST /api/confessions/{id}/unsubscribe/` - Obunani bekor qilish
- `GET /api/confessions/my_subscriptions/` - Mening obunalarim

### Postlar
- `GET /api/posts/` - Barcha postlar
- `GET /api/posts/{id}/` - Bitta post
- `POST /api/posts/` - Yangi post yaratish (confession admin)
- `GET /api/posts/feed/` - Mening feedim (obuna bo'lgan konfessiyalar)
- `POST /api/posts/{id}/like/` - Like qo'yish
- `POST /api/posts/{id}/unlike/` - Like ni olib tashlash

### Kommentlar
- `GET /api/comments/` - Barcha kommentlar
- `POST /api/comments/` - Komment yozish
- `DELETE /api/comments/{id}/` - Kommentni o'chirish

## Admin Panel

Admin panelga kirish: http://localhost:8000/admin/

## Texnologiyalar

- Django 5.2.7
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1
- django-cors-headers 4.9.0
- Pillow 12.0.0
- SQLite (development)
