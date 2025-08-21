from django.db import models
from django.conf import settings
from django.utils import timezone
from reservations.models import Reservation
from rooms.models import Room
from inventory.models import Product

class DailyReport(models.Model):
    """
    Modelo para reportes diarios del hotel
    """
    date = models.DateField(
        unique=True,
        verbose_name='Fecha'
    )
    total_rooms = models.IntegerField(
        verbose_name='Total de habitaciones'
    )
    occupied_rooms = models.IntegerField(
        verbose_name='Habitaciones ocupadas'
    )
    available_rooms = models.IntegerField(
        verbose_name='Habitaciones disponibles'
    )
    cleaning_rooms = models.IntegerField(
        verbose_name='Habitaciones en limpieza'
    )
    total_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Ingresos totales'
    )
    total_reservations = models.IntegerField(
        verbose_name='Total de reservaciones'
    )
    occupancy_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Tasa de ocupación (%)'
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
        verbose_name = 'Reporte Diario'
        verbose_name_plural = 'Reportes Diarios'
        ordering = ['-date']
        
    def __str__(self):
        return f"Reporte {self.date}"
    
    @classmethod
    def generate_daily_report(cls, date=None, user=None):
        """
        Genera un reporte diario automáticamente
        """
        if date is None:
            date = timezone.now().date()
        
        # Obtener estadísticas de habitaciones
        total_rooms = Room.objects.count()
        occupied_rooms = Room.objects.filter(status='occupied').count()
        available_rooms = Room.objects.filter(status='available').count()
        cleaning_rooms = Room.objects.filter(status='cleaning').count()
        
        # Calcular tasa de ocupación
        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
        
        # Calcular ingresos del día
        day_start = timezone.datetime.combine(date, timezone.datetime.min.time())
        day_end = timezone.datetime.combine(date, timezone.datetime.max.time())
        
        daily_reservations = Reservation.objects.filter(
            created_at__range=[day_start, day_end],
            status__in=['active', 'completed']
        )
        
        total_revenue = sum(r.paid_amount for r in daily_reservations)
        total_reservations = daily_reservations.count()
        
        # Crear o actualizar el reporte
        report, created = cls.objects.update_or_create(
            date=date,
            defaults={
                'total_rooms': total_rooms,
                'occupied_rooms': occupied_rooms,
                'available_rooms': available_rooms,
                'cleaning_rooms': cleaning_rooms,
                'total_revenue': total_revenue,
                'total_reservations': total_reservations,
                'occupancy_rate': occupancy_rate,
                'created_by': user,
            }
        )
        
        return report
