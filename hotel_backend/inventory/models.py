from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Category(models.Model):
    """
    Modelo para categorías de productos
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nombre de categoría'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    icon = models.CharField(
        max_length=50,
        default='📦',
        verbose_name='Icono'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        
    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Modelo para productos del inventario
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del producto'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Categoría'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio'
    )
    current_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock actual'
    )
    minimum_stock = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0)],
        verbose_name='Stock mínimo'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    @property
    def stock_status(self):
        if self.current_stock == 0:
            return 'out_of_stock'
        elif self.is_low_stock:
            return 'low_stock'
        else:
            return 'in_stock'

class StockMovement(models.Model):
    """
    Modelo para movimientos de inventario
    """
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('adjustment', 'Ajuste'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
        verbose_name='Tipo de movimiento'
    )
    quantity = models.IntegerField(
        verbose_name='Cantidad'
    )
    previous_stock = models.IntegerField(
        verbose_name='Stock anterior'
    )
    new_stock = models.IntegerField(
        verbose_name='Stock nuevo'
    )
    reason = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Motivo'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} - {self.quantity}"
