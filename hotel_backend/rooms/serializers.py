from rest_framework import serializers
from .models import Room, RoomType

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'nombre', 'description', 'precio_base', 'precio_hora_adicional', 'created_at']
        read_only_fields = ['id', 'created_at']

class RoomTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['nombre', 'description', 'precio_base', 'precio_hora_adicional']
        
    def to_representation(self, instance):
        """Personalizar la respuesta para mostrar todos los campos relevantes"""
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'description': instance.description,
            'precio_base': instance.precio_base,
            'precio_hora_adicional': instance.precio_hora_adicional,
            'created_at': instance.created_at
        }

class RoomSerializer(serializers.ModelSerializer):
    tipo_habitacion_detail = RoomTypeSerializer(source='tipo_habitacion', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    politica_horas = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'numero', 'tipo_habitacion', 'tipo_habitacion_detail', 'estado', 
            'estado_display', 'precio_base', 'precio_hora_adicional', 'descripcion',
            'horas_base', 'cobro_adicional', 'politica_horas', 'piso', 'notas', 
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_politica_horas(self, obj):
        return {
            'horas_base': obj.horas_base,
            'cobro_adicional': obj.cobro_adicional
        }

class RoomCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ['numero', 'tipo_habitacion', 'estado', 'piso', 'notas']
    
    def create(self, validated_data):
        # Auto-cargar datos del tipo de habitación
        room_type = validated_data['tipo_habitacion']
        
        # Auto-cargar precio base del tipo de habitación
        validated_data['precio_base'] = room_type.precio_base
        
        # Auto-cargar precio hora adicional del tipo de habitación  
        validated_data['precio_hora_adicional'] = room_type.precio_hora_adicional
        
        # Auto-cargar descripción del tipo de habitación
        validated_data['descripcion'] = room_type.description
        
        # Valores por defecto
        validated_data['horas_base'] = 3
        validated_data['cobro_adicional'] = True
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        politica_horas = validated_data.pop('politica_horas', None)
        
        # Actualizar política de horas si se proporciona
        if politica_horas:
            instance.horas_base = politica_horas.get('horas_base', instance.horas_base)
            instance.cobro_adicional = politica_horas.get('cobro_adicional', instance.cobro_adicional)
        
        return super().update(instance, validated_data)

class RoomStatusChangeSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=Room.STATUS_CHOICES)
    # Los campos registrado_por y fecha_registro se capturarán automáticamente
