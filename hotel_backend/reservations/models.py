from django.db import models
from django.conf import settings
from rooms.models import Room
from django.utils import timezone

class Reservation(models.Model):
    """
    Modelo para reservaciones/ocupaciones de habitaciones
    """
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE,
        verbose_name='Habitación'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='Creado por'
    )
    guest_name = models.CharField(
        max_length=100,
        verbose_name='Nombre del huésped'
    )
    guest_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono del huésped'
    )
    check_in = models.DateTimeField(
        verbose_name='Check-in'
    )
    check_out = models.DateTimeField(
        verbose_name='Check-out'
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Monto total'
    )
    paid_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name='Monto pagado'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name='Estado'
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
        verbose_name = 'Reservación'
        verbose_name_plural = 'Reservaciones'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Reservación {self.id} - {self.guest_name} - {self.room}"
    
    @property
    def is_active(self):
        return self.status == 'active' and self.check_out > timezone.now()
    
    @property
    def pending_amount(self):
        return self.total_amount - self.paid_amount
    
    @property
    def duration_hours(self):
        duration = self.check_out - self.check_in
        return duration.total_seconds() / 3600
