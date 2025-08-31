from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer, RoomCreateSerializer, RoomTypeCreateSerializer, RoomStatusChangeSerializer
from accounts.permissions import IsReceptionistOrHigher, IsAdminOrSuperAdmin

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAdminOrSuperAdmin]  # Solo Admin y Super Admin pueden gestionar tipos
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RoomTypeCreateSerializer
        return RoomTypeSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('tipo_habitacion').all()
    serializer_class = RoomSerializer
    permission_classes = [IsReceptionistOrHigher]  # Recepcionistas y superiores pueden gestionar habitaciones
    
    def get_permissions(self):
        """
        Permisos específicos por acción
        """
        if self.action in ['create', 'destroy']:
            # Solo Admin y Super Admin pueden crear/eliminar habitaciones
            permission_classes = [IsAdminOrSuperAdmin]
        elif self.action in ['update', 'partial_update', 'cambio_estado']:
            # Recepcionistas y superiores pueden actualizar y cambiar estado
            permission_classes = [IsReceptionistOrHigher]
        else:
            # Ver habitaciones: todos los roles autenticados
            permission_classes = [IsReceptionistOrHigher]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RoomCreateSerializer
        elif self.action == 'cambio_estado':
            return RoomStatusChangeSerializer
        return RoomSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Crear habitación con respuesta optimizada en español
        """
        print("🔥 EJECUTANDO MÉTODO CREATE PERSONALIZADO")  # Debug temporal
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        
        print(f"🏠 Habitación creada: {room.numero}")  # Debug temporal
        
        # Crear respuesta optimizada en español
        response_data = {
            'id': room.id,
            'numero': room.numero,
            'estado': room.estado,
            'disponible': room.is_available,
            'fecha_creacion': room.created_at,
            
            # Información del tipo seleccionado
            'tipo_habitacion': {
                'id': room.tipo_habitacion.id,
                'nombre': room.tipo_habitacion.nombre,
                'descripcion': room.tipo_habitacion.description
            },
            
            # Precios y configuración (auto-cargados del tipo)
            'configuracion_precios': {
                'precio_base': room.precio_base,
                'precio_hora_adicional': room.precio_hora_adicional,
                'horas_incluidas': room.horas_base,
                'cobra_horas_extras': room.cobro_adicional
            }
        }
        
        print(f"📤 Enviando respuesta personalizada")  # Debug temporal
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[IsReceptionistOrHigher])
    def disponibles(self, request):
        """
        Endpoint para obtener solo habitaciones disponibles
        """
        available_rooms = self.queryset.filter(estado='disponible')
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsReceptionistOrHigher])
    def dashboard_stats(self, request):
        """
        Endpoint para obtener estadísticas del dashboard
        """
        # Contar habitaciones por estado
        stats = Room.objects.values('estado').annotate(count=Count('estado'))
        status_counts = {item['estado']: item['count'] for item in stats}
        
        # Contar por tipo de habitación
        type_stats = Room.objects.values('tipo_habitacion__nombre').annotate(count=Count('tipo_habitacion'))
        type_counts = {item['tipo_habitacion__nombre']: item['count'] for item in type_stats}
        
        # Totales
        total_rooms = Room.objects.count()
        available_rooms = status_counts.get('disponible', 0)
        occupied_rooms = status_counts.get('ocupada', 0)
        cleaning_rooms = status_counts.get('limpieza', 0)
        
        # Tasa de ocupación
        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
        
        return Response({
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'occupied_rooms': occupied_rooms,
            'cleaning_rooms': cleaning_rooms,
            'occupancy_rate': round(occupancy_rate, 2),
            'status_breakdown': status_counts,
            'type_breakdown': type_counts
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsReceptionistOrHigher], url_path='cambio-estado')
    def cambio_estado(self, request, pk=None):
        """
        Endpoint para cambiar el estado de una habitación
        URL: /api/rooms/{id}/cambio-estado/
        Body: {"estado": "ocupada"}
        """
        room = self.get_object()
        serializer = RoomStatusChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Capturar datos automáticamente
            new_status = serializer.validated_data['estado']
            registrado_por = request.user.username  # Del token JWT
            fecha_registro = timezone.now()  # Fecha actual
            estado_anterior = room.estado  # Para el log
            
            # Cambiar el estado
            room.estado = new_status
            room.save()
            
            # Aquí podrías registrar el historial de cambios en una tabla separada
            # RoomStatusHistory.objects.create(
            #     room=room,
            #     estado_anterior=estado_anterior,
            #     estado_nuevo=new_status,
            #     registrado_por=registrado_por,
            #     fecha_registro=fecha_registro
            # )
            
            return Response({
                'success': True,
                'message': f'Estado de habitación {room.numero} cambiado de {estado_anterior} a {new_status}',
                'cambio': {
                    'estado_anterior': estado_anterior,
                    'estado_nuevo': new_status,
                    'registrado_por': registrado_por,
                    'fecha_cambio': fecha_registro,
                    'usuario_completo': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
                },
                'habitacion': {
                    'id': room.id,
                    'numero': room.numero,
                    'estado': room.estado,
                    'disponible': room.is_available,
                    'tipo_habitacion': {
                        'id': room.tipo_habitacion.id,
                        'nombre': room.tipo_habitacion.nombre,
                        'descripcion': room.tipo_habitacion.description
                    },
                    'configuracion_precios': {
                        'precio_base': room.precio_base,
                        'precio_hora_adicional': room.precio_hora_adicional,
                        'horas_incluidas': room.horas_base,
                        'cobra_horas_extras': room.cobro_adicional
                    }
                }
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsReceptionistOrHigher])
    def disponibles(self, request):
        """
        Endpoint para obtener solo habitaciones disponibles
        """
        available_rooms = self.queryset.filter(estado='disponible')
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)
