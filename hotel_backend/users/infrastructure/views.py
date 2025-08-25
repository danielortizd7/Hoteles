"""
Infrastructure layer - Controladores/Views del dominio de usuarios
"""
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from accounts.serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from accounts.permissions import IsSuperAdmin, IsAdminOrSuperAdmin, CanManageUsers

from ..application.services import (
    UserManagementService, 
    AuthenticationService, 
    SuperAdminSetupService
)

class UserManagementViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios usando servicios de dominio"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanManageUsers]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Obtener usuarios según permisos usando servicio de dominio"""
        return UserManagementService.get_users_by_role(self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Crear usuario usando servicio de dominio"""
        success, message, user = UserManagementService.create_user(
            creator=request.user,
            user_data=request.data
        )
        
        if success:
            return Response({
                'success': True,
                'message': message,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Actualizar usuario usando servicio de dominio"""
        user = self.get_object()
        success, message = UserManagementService.update_user(
            modifier=request.user,
            target_user=user,
            update_data=request.data
        )
        
        if success:
            return Response({
                'success': True,
                'message': message,
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrSuperAdmin])
    def by_role(self, request):
        """Obtener usuarios por rol"""
        role = request.query_params.get('role')
        users = UserManagementService.get_users_by_role(request.user, role)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminOrSuperAdmin])
    def create_receptionist(self, request):
        """Crear recepcionista"""
        data = request.data.copy()
        data['role'] = 'receptionist'
        
        success, message, user = UserManagementService.create_user(
            creator=request.user,
            user_data=data
        )
        
        if success:
            return Response({
                'success': True,
                'message': message,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsSuperAdmin])
    def create_admin(self, request):
        """Crear administrador (solo super admin)"""
        data = request.data.copy()
        data['role'] = 'admin'
        
        success, message, user = UserManagementService.create_user(
            creator=request.user,
            user_data=data
        )
        
        if success:
            return Response({
                'success': True,
                'message': message,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def domain_login_view(request):
    """Login usando servicio de dominio"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': 'Username y password son requeridos'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    success, message, user, token = AuthenticationService.authenticate_user(username, password)
    
    if success:
        login(request, user)
        return Response({
            'success': True,
            'token': token,
            'user': UserSerializer(user).data,
            'message': message
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': message
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def domain_logout_view(request):
    """Logout usando servicio de dominio"""
    success, message = AuthenticationService.logout_user(request.user)
    logout(request)
    
    return Response({
        'success': success,
        'message': message
    }, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def setup_super_admin(request):
    """Configurar super administrador inicial"""
    success, message, user = SuperAdminSetupService.create_initial_super_admin(request.data)
    
    if success:
        return Response({
            'success': True,
            'message': message,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'success': False,
            'message': message
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_user_permissions(request):
    """Verificar permisos del usuario actual"""
    permission = request.query_params.get('permission')
    
    if not permission:
        return Response({
            'error': 'Parámetro permission es requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    has_permission = AuthenticationService.check_permission(request.user, permission)
    
    return Response({
        'user': request.user.username,
        'role': request.user.role,
        'permission': permission,
        'has_permission': has_permission
    })
