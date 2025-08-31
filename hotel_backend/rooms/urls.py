from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomTypeViewSet

# Router principal
router = DefaultRouter()
router.register(r'tipos', RoomTypeViewSet, basename='tipos-habitacion')
router.register(r'', RoomViewSet, basename='habitaciones')  # Registrar habitaciones en la raíz

urlpatterns = [
    # Incluir todas las rutas del router
    path('', include(router.urls)),
]
