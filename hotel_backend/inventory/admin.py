from django.contrib import admin
from .models import Product, Category, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'current_stock', 'minimum_stock', 'stock_status', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    list_editable = ('price', 'current_stock', 'minimum_stock')
    
    def stock_status(self, obj):
        if obj.current_stock == 0:
            return "Sin Stock"
        elif obj.is_low_stock:
            return "Stock Bajo"
        else:
            return "Stock OK"
    
    stock_status.short_description = "Estado del Stock"

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'previous_stock', 'new_stock', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name', 'reason')
    ordering = ('-created_at',)
    
    readonly_fields = ('product', 'movement_type', 'quantity', 'previous_stock', 'new_stock', 'reason', 'created_by', 'created_at')
