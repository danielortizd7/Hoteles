from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login_view, logout_view, profile_view, create_test_user, debug_info, health_check, simple_test

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('perfil/', profile_view, name='perfil'),
    path('cerrar-sesion/', logout_view, name='cerrar-sesion'),
    # Compatibilidad
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    # Endpoints temporales para debug
    path('create-test-user/', create_test_user, name='create-test-user'),
    path('debug/', debug_info, name='debug'),
    path('health/', health_check, name='health'),
    path('simple/', simple_test, name='simple'),
]
