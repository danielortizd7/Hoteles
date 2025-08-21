from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login_view, logout_view, profile_view

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
]
