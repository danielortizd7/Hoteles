from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'productos', ProductViewSet, basename='productos')
router.register(r'categorias', CategoryViewSet, basename='categorias')
router.register(r'movimientos-stock', StockMovementViewSet, basename='movimientos-stock')

# Router para compatibilidad en inglés
router_en = DefaultRouter()
router_en.register(r'products', ProductViewSet)
router_en.register(r'categories', CategoryViewSet)
router_en.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Compatibilidad con URLs en inglés
    path('', include(router_en.urls)),
]
