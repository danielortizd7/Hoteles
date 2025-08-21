from django.contrib import admin
from .models import Room, RoomType

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('get_name_display', 'base_price_5h', 'icon', 'created_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'status', 'floor', 'created_at')
    list_filter = ('status', 'room_type', 'floor', 'created_at')
    search_fields = ('number', 'notes')
    ordering = ('number',)
    
    list_editable = ('status',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('number', 'room_type', 'floor')
        }),
        ('Estado y Notas', {
            'fields': ('status', 'notes')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
