from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Product, Category, StockMovement
from .serializers import (
    ProductSerializer, CategorySerializer, StockMovementSerializer,
    StockAdjustmentSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        low_stock = self.request.query_params.get('low_stock', None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if low_stock and low_stock.lower() == 'true':
            queryset = queryset.filter(current_stock__lte=F('minimum_stock'))
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        """
        Endpoint para ajustar el stock de un producto
        """
        product = self.get_object()
        serializer = StockAdjustmentSerializer(data=request.data)
        
        if serializer.is_valid():
            adjustment_type = serializer.validated_data['adjustment_type']
            quantity = serializer.validated_data['quantity']
            reason = serializer.validated_data.get('reason', 'Ajuste manual')
            
            previous_stock = product.current_stock
            
            if adjustment_type == 'increase':
                new_stock = previous_stock + quantity
                movement_type = 'in'
            elif adjustment_type == 'decrease':
                new_stock = max(0, previous_stock - quantity)
                movement_type = 'out'
                quantity = previous_stock - new_stock  # Ajustar cantidad real
            else:  # set
                new_stock = quantity
                movement_type = 'adjustment'
                quantity = new_stock - previous_stock
            
            # Actualizar stock del producto
            product.current_stock = new_stock
            product.save()
            
            # Crear movimiento de stock
            StockMovement.objects.create(
                product=product,
                movement_type=movement_type,
                quantity=abs(quantity),
                previous_stock=previous_stock,
                new_stock=new_stock,
                reason=reason,
                created_by=request.user
            )
            
            return Response({
                'success': True,
                'message': f'Stock de {product.name} ajustado exitosamente',
                'product': ProductSerializer(product).data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Endpoint para obtener productos con stock bajo
        """
        low_stock_products = self.queryset.filter(current_stock__lte=F('minimum_stock'))
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related('product', 'created_by').all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product', None)
        
        if product:
            queryset = queryset.filter(product_id=product)
        
        return queryset
