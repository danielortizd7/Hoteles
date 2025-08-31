from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RoomType(models.Model):
    """
    Modelo para tipos de habitaciones
    """
    
    nombre = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name='Tipo de habitación'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción'
    )
    precio_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Precio base'
    )
    precio_hora_adicional = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=5000,
        verbose_name='Precio por hora adicional'
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
        return self.nombre

class Room(models.Model):
    """
    Modelo para habitaciones individuales
    """
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('limpieza', 'En limpieza'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    
    numero = models.CharField(
        max_length=10, 
        unique=True,
        verbose_name='Número de habitación'
    )
    tipo_habitacion = models.ForeignKey(
        RoomType, 
        on_delete=models.CASCADE,
        verbose_name='Tipo de habitación'
    )
    estado = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='disponible',
        verbose_name='Estado'
    )
    precio_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=40000,
        verbose_name='Precio base'
    )
    precio_hora_adicional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5000,
        verbose_name='Precio por hora adicional'
    )
    descripcion = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción'
    )
    horas_base = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(24)],
        verbose_name='Horas base incluidas'
    )
    cobro_adicional = models.BooleanField(
        default=True,
        verbose_name='Cobrar horas adicionales'
    )
    piso = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=1,
        verbose_name='Piso'
    )
    notas = models.TextField(
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
        ordering = ['numero']
        
    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo_habitacion}"
    
    @property
    def is_available(self):
        return self.estado == 'disponible'
    
    def calcular_precio_total(self, horas_uso):
        """
        Calcula el precio total basado en las horas de uso
        """
        if horas_uso <= self.horas_base:
            return self.precio_base
        
        if self.cobro_adicional:
            horas_extras = horas_uso - self.horas_base
            return self.precio_base + (horas_extras * self.precio_hora_adicional)
        
        return self.precio_base
