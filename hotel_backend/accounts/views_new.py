from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
import os

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
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

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def create_test_user(request):
    """
    Endpoint temporal para crear usuario de prueba
    """
    try:
        # Verificar si ya existe
        if User.objects.filter(username='admin').exists():
            return Response({
                'success': True,
                'message': 'Usuario admin ya existe',
                'user_count': User.objects.count()
            }, status=status.HTTP_200_OK)
        
        # Crear usuario admin
        user = User.objects.create_user(
            username='admin',
            email='admin@moteleclipse.com',
            password='admin123',
            first_name='Admin',
            last_name='Eclipse',
            role='admin'
        )
        
        return Response({
            'success': True,
            'message': 'Usuario admin creado exitosamente',
            'username': user.username,
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
