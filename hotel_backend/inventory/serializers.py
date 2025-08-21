from rest_framework import serializers
from .models import Product, Category, StockMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_detail', 'price', 
            'current_stock', 'minimum_stock', 'description',
            'stock_status', 'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class StockMovementSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    created_by_detail = serializers.StringRelatedField(source='created_by', read_only=True)
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_detail', 'movement_type', 'movement_type_display',
            'quantity', 'previous_stock', 'new_stock', 'reason', 
            'created_by', 'created_by_detail', 'created_at'
        ]
        read_only_fields = ['id', 'previous_stock', 'new_stock', 'created_by', 'created_at']

class StockAdjustmentSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    adjustment_type = serializers.ChoiceField(choices=[('increase', 'Aumentar'), ('decrease', 'Disminuir'), ('set', 'Establecer')])
    quantity = serializers.IntegerField(min_value=1)
    reason = serializers.CharField(max_length=100, required=False)
    
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Producto no encontrado")
        return value
