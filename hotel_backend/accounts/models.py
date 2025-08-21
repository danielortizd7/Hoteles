from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema hotelero
    """
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('receptionist', 'Recepcionista'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='receptionist',
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Teléfono'
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
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_receptionist(self):
        return self.role == 'receptionist'
