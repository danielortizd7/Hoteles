from django.contrib import admin
from .models import Room, RoomType

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'precio_hora_adicional', 'icon', 'created_at')
    list_filter = ('nombre', 'created_at')
    search_fields = ('nombre', 'description')
    ordering = ('nombre',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo_habitacion', 'estado', 'precio_base', 'piso', 'created_at')
    list_filter = ('estado', 'tipo_habitacion', 'piso', 'created_at')
    search_fields = ('numero', 'descripcion', 'notas')
    ordering = ('numero',)
    
    list_editable = ('estado',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero', 'tipo_habitacion', 'piso', 'descripcion')
        }),
        ('Precios y Horas', {
            'fields': ('precio_base', 'precio_hora_adicional', 'horas_base', 'cobro_adicional')
        }),
        ('Estado y Notas', {
            'fields': ('estado', 'notas')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
