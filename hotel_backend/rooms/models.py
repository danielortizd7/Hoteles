from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RoomType(models.Model):
    """
    Modelo para tipos de habitaciones
    """
    TYPE_CHOICES = [
        ('standard', 'Estándar'),
        ('love_machine', 'Con Máquina del Amor'),
        ('suite', 'Suite'),
    ]
    
    name = models.CharField(
        max_length=50, 
        choices=TYPE_CHOICES,
        unique=True,
        verbose_name='Tipo de habitación'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción'
    )
    base_price_5h = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Precio base 5h'
    )
    icon = models.CharField(
        max_length=50,
        default='🏠',
        verbose_name='Icono'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        verbose_name = 'Tipo de Habitación'
        verbose_name_plural = 'Tipos de Habitaciones'
        
    def __str__(self):
        return self.get_name_display()

class Room(models.Model):
    """
    Modelo para habitaciones individuales
    """
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('occupied', 'Ocupada'),
        ('cleaning', 'En Limpieza'),
        ('maintenance', 'Mantenimiento'),
    ]
    
    number = models.CharField(
        max_length=10, 
        unique=True,
        verbose_name='Número de habitación'
    )
    room_type = models.ForeignKey(
        RoomType, 
        on_delete=models.CASCADE,
        verbose_name='Tipo de habitación'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available',
        verbose_name='Estado'
    )
    floor = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Piso'
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Notas'
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
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'
        ordering = ['number']
        
    def __str__(self):
        return f"Habitación {self.number} - {self.room_type}"
    
    @property
    def is_available(self):
        return self.status == 'available'
