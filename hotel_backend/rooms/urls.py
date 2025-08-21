from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomTypeViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomTypeViewSet

# Router para URLs en español
router = DefaultRouter()
router.register(r'tipos', RoomTypeViewSet, basename='tipos-habitacion')

# Router para compatibilidad en inglés
router_en = DefaultRouter()
router_en.register(r'rooms', RoomViewSet)
router_en.register(r'room-types', RoomTypeViewSet)

urlpatterns = [
    # URLs principales de habitaciones (sin router para evitar conflictos)
    path('', RoomViewSet.as_view({'get': 'list', 'post': 'create'}), name='habitaciones-list'),
    path('<int:pk>/', RoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='habitaciones-detail'),
    path('<int:pk>/change_status/', RoomViewSet.as_view({'post': 'change_status'}), name='habitaciones-change-status'),
    path('dashboard/', RoomViewSet.as_view({'get': 'dashboard_stats'}), name='dashboard'),
    path('disponibles/', RoomViewSet.as_view({'get': 'available'}), name='disponibles'),
    
    # Incluir tipos de habitación
    path('', include(router.urls)),
    
    # Compatibilidad con URLs en inglés
    path('', include(router_en.urls)),
]
