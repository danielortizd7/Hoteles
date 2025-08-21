from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer, RoomCreateSerializer

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('room_type').all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RoomCreateSerializer
        return RoomSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """
        Endpoint para obtener estadísticas del dashboard
        """
        # Contar habitaciones por estado
        stats = Room.objects.values('status').annotate(count=Count('status'))
        status_counts = {item['status']: item['count'] for item in stats}
        
        # Contar por tipo de habitación
        type_stats = Room.objects.values('room_type__name').annotate(count=Count('room_type'))
        type_counts = {item['room_type__name']: item['count'] for item in type_stats}
        
        # Totales
        total_rooms = Room.objects.count()
        available_rooms = status_counts.get('available', 0)
        occupied_rooms = status_counts.get('occupied', 0)
        cleaning_rooms = status_counts.get('cleaning', 0)
        
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
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """
        Endpoint para cambiar el estado de una habitación
        """
        room = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Room.STATUS_CHOICES):
            return Response({
                'success': False,
                'message': 'Estado inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        room.status = new_status
        room.save()
        
        return Response({
            'success': True,
            'message': f'Estado de habitación {room.number} cambiado a {room.get_status_display()}',
            'room': RoomSerializer(room).data
        })
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Endpoint para obtener solo habitaciones disponibles
        """
        available_rooms = self.queryset.filter(status='available')
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)
