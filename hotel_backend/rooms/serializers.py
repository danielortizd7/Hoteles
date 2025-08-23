from rest_framework import serializers
from .models import Room, RoomType

class RoomTypeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'display_name', 'description', 'base_price_5h', 'created_at']
        read_only_fields = ['id', 'created_at']

class RoomTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['name', 'description', 'base_price_5h']

class RoomSerializer(serializers.ModelSerializer):
    room_type_detail = RoomTypeSerializer(source='room_type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'number', 'room_type', 'room_type_detail', 'status', 
            'status_display', 'floor', 'notes', 'is_available', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'room_type', 'floor', 'notes']
