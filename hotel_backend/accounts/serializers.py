from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'phone', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        # Validar permisos de creación según rol
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            target_role = attrs.get('role')
            current_user = request.user
            
            # Solo super admin puede crear otros super admins
            if target_role == 'super_admin' and not current_user.is_super_admin:
                raise serializers.ValidationError("Solo super administradores pueden crear otros super administradores")
            
            # Solo super admin puede crear admins
            if target_role == 'admin' and not current_user.can_create_admins:
                raise serializers.ValidationError("Solo super administradores pueden crear administradores")
            
            # Admin y super admin pueden crear recepcionistas
            if target_role == 'receptionist' and not current_user.can_manage_users:
                raise serializers.ValidationError("No tienes permisos para crear usuarios")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas')
            if not user.is_active:
                raise serializers.ValidationError('Usuario inactivo')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Debe proporcionar username y password')
        
        return attrs
