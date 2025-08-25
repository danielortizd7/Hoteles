from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, login_view, logout_view, profile_view,
    create_test_user, debug_info, health_check, simple_test, create_super_admin
)
from . import views as account_views

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
    path('create-super-admin/', create_super_admin, name='create-super-admin'),
    path('debug/', debug_info, name='debug'),
    path('health/', health_check, name='health'),
    path('simple/', simple_test, name='simple'),
]

# Añadir rutas JWT solo si disponible
if getattr(account_views, 'SIMPLEJWT_AVAILABLE', False):
    from .views import CustomTokenObtainPairView, TokenRefreshView, verify_token
    urlpatterns += [
        path('jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt-login'),
        path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
        path('jwt/verify/', verify_token, name='jwt-verify'),
    ]
