"""
Application layer - Casos de uso del dominio de usuarios
"""
from typing import Optional, Dict, Any, List
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from accounts.models import User
from ..domain.entities import UserRole, UserDomainRules, UserPermissions

class UserManagementService:
    """Servicio para gestión de usuarios"""
    
    @staticmethod
    def create_user(creator: User, user_data: Dict[str, Any]) -> tuple[bool, str, Optional[User]]:
        """Crear un nuevo usuario con validaciones de dominio"""
        try:
            # Obtener roles
            creator_role = UserRole(creator.role)
            target_role = UserRole(user_data.get('role', 'receptionist'))
            
            # Validar permisos
            is_valid, message = UserDomainRules.validate_user_creation(creator_role, target_role)
            if not is_valid:
                return False, message, None
            
            # Crear usuario
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=target_role.value,
                phone=user_data.get('phone', '')
            )
            
            return True, f"Usuario {user.username} creado exitosamente", user
            
        except Exception as e:
            return False, f"Error al crear usuario: {str(e)}", None
    
    @staticmethod
    def get_users_by_role(requester: User, role: Optional[str] = None) -> List[User]:
        """Obtener usuarios filtrados por rol según permisos"""
        requester_role = UserRole(requester.role)
        
        # Super admin ve todos
        if requester_role == UserRole.SUPER_ADMIN:
            queryset = User.objects.all()
        # Admin ve admins y recepcionistas
        elif requester_role == UserRole.ADMIN:
            queryset = User.objects.exclude(role='super_admin')
        # Recepcionista solo ve su perfil
        else:
            queryset = User.objects.filter(id=requester.id)
        
        # Filtrar por rol específico si se proporciona
        if role and role in [r.value for r in UserRole]:
            queryset = queryset.filter(role=role)
            
        return list(queryset)
    
    @staticmethod
    def update_user(modifier: User, target_user: User, update_data: Dict[str, Any]) -> tuple[bool, str]:
        """Actualizar usuario con validaciones"""
        try:
            modifier_role = UserRole(modifier.role)
            target_role = UserRole(target_user.role)
            
            # Validar permisos
            is_valid, message = UserDomainRules.validate_user_modification(modifier_role, target_role)
            if not is_valid:
                return False, message
            
            # Aplicar cambios
            for field, value in update_data.items():
                if hasattr(target_user, field) and field != 'password':
                    setattr(target_user, field, value)
            
            if 'password' in update_data:
                target_user.set_password(update_data['password'])
            
            target_user.save()
            return True, "Usuario actualizado exitosamente"
            
        except Exception as e:
            return False, f"Error al actualizar usuario: {str(e)}"

class AuthenticationService:
    """Servicio para autenticación y autorización"""
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> tuple[bool, str, Optional[User], Optional[str]]:
        """Autenticar usuario y generar token"""
        try:
            user = authenticate(username=username, password=password)
            if not user:
                return False, "Credenciales inválidas", None, None
            
            if not user.is_active:
                return False, "Usuario inactivo", None, None
            
            # Generar token
            token, created = Token.objects.get_or_create(user=user)
            
            return True, "Login exitoso", user, token.key
            
        except Exception as e:
            return False, f"Error en autenticación: {str(e)}", None, None
    
    @staticmethod
    def logout_user(user: User) -> tuple[bool, str]:
        """Cerrar sesión del usuario"""
        try:
            Token.objects.filter(user=user).delete()
            return True, "Logout exitoso"
        except Exception as e:
            return False, f"Error en logout: {str(e)}"
    
    @staticmethod
    def check_permission(user: User, permission: str) -> bool:
        """Verificar si el usuario tiene un permiso específico"""
        try:
            user_role = UserRole(user.role)
            return UserPermissions.has_permission(user_role, permission)
        except:
            return False

class SuperAdminSetupService:
    """Servicio para configuración inicial del super admin"""
    
    @staticmethod
    def create_initial_super_admin(user_data: Dict[str, Any]) -> tuple[bool, str, Optional[User]]:
        """Crear el primer super administrador del sistema"""
        try:
            # Verificar que no existe super admin
            if User.objects.filter(role='super_admin').exists():
                return False, "Ya existe un super administrador en el sistema", None
            
            # Crear super admin
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role='super_admin',
                phone=user_data.get('phone', '')
            )
            
            return True, "Super administrador creado exitosamente", user
            
        except Exception as e:
            return False, f"Error al crear super administrador: {str(e)}", None
