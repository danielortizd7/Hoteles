from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from .permissions import IsSuperAdmin, IsAdminOrSuperAdmin, CanManageUsers, CanCreateAdmins
try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    SIMPLEJWT_AVAILABLE = True
except ImportError:  # Paquete no instalado aún
    SIMPLEJWT_AVAILABLE = False
import os

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanManageUsers]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filtrar usuarios según permisos del usuario actual"""
        user = self.request.user
        if user.is_super_admin:
            return User.objects.all()
        elif user.is_admin:
            # Admin puede ver admins y recepcionistas, no super admins
            return User.objects.exclude(role='super_admin')
        else:
            # Recepcionistas solo ven su propio perfil
            return User.objects.filter(id=user.id)
    
    def get_permissions(self):
        """Permisos dinámicos según la acción"""
        if self.action == 'create':
            permission_classes = [CanManageUsers]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [CanManageUsers]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrSuperAdmin])
    def by_role(self, request):
        """Obtener usuarios filtrados por rol"""
        role = request.query_params.get('role')
        if role and role in ['super_admin', 'admin', 'receptionist']:
            users = self.get_queryset().filter(role=role)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'Rol inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminOrSuperAdmin])
    def create_receptionist(self, request):
        """Endpoint específico para crear recepcionistas"""
        data = request.data.copy()
        data['role'] = 'receptionist'  # Forzar rol
        serializer = UserCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': f'Recepcionista {user.username} creado exitosamente',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsSuperAdmin])
    def create_admin(self, request):
        """Endpoint específico para crear administradores (solo super admin)"""
        data = request.data.copy()
        data['role'] = 'admin'  # Forzar rol
        serializer = UserCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': f'Administrador {user.username} creado exitosamente',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

if SIMPLEJWT_AVAILABLE:
    class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        """Extiende la respuesta JWT con datos de usuario."""
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token['username'] = user.username
            token['role'] = user.role
            return token

        def validate(self, attrs):
            data = super().validate(attrs)
            data['user'] = UserSerializer(self.user).data
            return data

    class CustomTokenObtainPairView(TokenObtainPairView):
        serializer_class = CustomTokenObtainPairSerializer

    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def verify_token(request):
        """Endpoint sencillo para verificar un JWT válido."""
        return Response({
            'valid': True,
            'user': UserSerializer(request.user).data
        })

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    API endpoint para login de usuarios
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login exitoso'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    API endpoint para logout de usuarios
    """
    try:
        # Eliminar el token del usuario
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({
            'success': True,
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error al hacer logout'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    """
    API endpoint para obtener el perfil del usuario actual
    """
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'user': serializer.data
    }, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_super_admin(request):
    """
    Endpoint para crear el primer super administrador (solo si no existe ninguno)
    """
    try:
        # Verificar si ya existe un super admin
        if User.objects.filter(role='super_admin').exists():
            return Response({
                'success': False,
                'message': 'Ya existe un super administrador en el sistema'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear super admin
        data = request.data.copy()
        data['role'] = 'super_admin'
        
        # Validaciones básicas
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return Response({
                    'success': False,
                    'error': f'Campo {field} es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='super_admin',
            phone=data.get('phone', '')
        )
        
        return Response({
            'success': True,
            'message': 'Super administrador creado exitosamente',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
def create_test_user(request):
    """
    Endpoint temporal para crear usuario de prueba (DEPRECATED - usar create_super_admin)
    """
    try:
        # Verificar si ya existe
        if User.objects.filter(username='admin').exists():
            return Response({
                'success': True,
                'message': 'Usuario admin ya existe',
                'user_count': User.objects.count()
            }, status=status.HTTP_200_OK)
        
        # Crear usuario admin con rol admin (no super_admin)
        user = User.objects.create_user(
            username='admin',
            email='admin@moteleclipse.com',
            password='admin123',
            first_name='Admin',
            last_name='Eclipse',
            role='admin'  # Cambiar a admin normal
        )
        
        return Response({
            'success': True,
            'message': 'Usuario admin creado exitosamente',
            'username': user.username,
            'role': user.role,
            'user_count': User.objects.count()
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'user_count': User.objects.count()
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def debug_info(request):
    """
    Endpoint para información de debug
    """
    try:
        users_count = User.objects.count()
        users_list = list(User.objects.values_list('username', flat=True)[:10])
        
        return Response({
            'success': True,
            'users_count': users_count,
            'users_list': users_list,
            'debug': True,
            'message': 'Debug endpoint funcionando correctamente'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'debug': True,
            'message': 'Error en debug endpoint'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Endpoint simple para verificar que la API funciona
    """
    return Response({
        'status': 'OK',
        'message': 'API funcionando correctamente',
        'timestamp': '2025-08-22'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def simple_test(request):
    """
    Endpoint ultra simple sin decoradores
    """
    return JsonResponse({
        'test': 'OK',
        'simple': True,
        'debug': os.environ.get('DEBUG', 'NOT_SET'),
        'allowed_hosts': os.environ.get('ALLOWED_HOSTS', 'NOT_SET'),
        'database_url': 'SET' if os.environ.get('DATABASE_URL') else 'NOT_SET',
        'django_settings': os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT_SET')
    })
