"""
URLs del dominio de usuarios
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .infrastructure.views import (
    UserManagementViewSet, 
    domain_login_view, 
    domain_logout_view,
    setup_super_admin,
    check_user_permissions
)

router = DefaultRouter()
router.register(r'management', UserManagementViewSet, basename='user-management')

urlpatterns = [
    # Rutas del ViewSet
    path('', include(router.urls)),
    
    # Autenticación
    path('auth/login/', domain_login_view, name='domain-login'),
    path('auth/logout/', domain_logout_view, name='domain-logout'),
    
    # Configuración inicial
    path('setup/super-admin/', setup_super_admin, name='setup-super-admin'),
    
    # Verificación de permisos
    path('permissions/check/', check_user_permissions, name='check-permissions'),
]
