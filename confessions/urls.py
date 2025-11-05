from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfessionViewSet

router = DefaultRouter()
router.register(r'confessions', ConfessionViewSet, basename='confession')

urlpatterns = [
    path('', include(router.urls)),
]
