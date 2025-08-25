"""
Domain layer - Entidades de negocio y reglas del dominio de usuarios
"""
from enum import Enum

class UserRole(Enum):
    """Roles disponibles en el sistema"""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"  
    RECEPTIONIST = "receptionist"

class UserPermissions:
    """Definición de permisos por rol"""
    
    ROLE_PERMISSIONS = {
        UserRole.SUPER_ADMIN: [
            'create_super_admin',
            'create_admin',
            'create_receptionist',
            'manage_all_users',
            'delete_users',
            'manage_system_settings',
            'view_all_data',
            'manage_rooms',
            'manage_inventory',
            'manage_reservations',
        ],
        UserRole.ADMIN: [
            'create_receptionist',
            'manage_receptionists',
            'view_admin_data',
            'manage_rooms',
            'manage_inventory', 
            'manage_reservations',
            'view_reports',
        ],
        UserRole.RECEPTIONIST: [
            'view_own_profile',
            'manage_rooms',
            'manage_inventory',
            'create_reservations',
            'view_reservations',
        ]
    }
    
    @classmethod
    def has_permission(cls, role: UserRole, permission: str) -> bool:
        """Verificar si un rol tiene un permiso específico"""
        return permission in cls.ROLE_PERMISSIONS.get(role, [])
    
    @classmethod
    def can_manage_user(cls, manager_role: UserRole, target_role: UserRole) -> bool:
        """Verificar si un rol puede gestionar a otro"""
        if manager_role == UserRole.SUPER_ADMIN:
            return True
        elif manager_role == UserRole.ADMIN:
            return target_role in [UserRole.ADMIN, UserRole.RECEPTIONIST]
        return False

class UserDomainRules:
    """Reglas de negocio del dominio de usuarios"""
    
    @staticmethod
    def validate_user_creation(creator_role: UserRole, target_role: UserRole) -> tuple[bool, str]:
        """Validar si se puede crear un usuario con el rol especificado"""
        if not UserPermissions.can_manage_user(creator_role, target_role):
            return False, f"El rol {creator_role.value} no puede crear usuarios con rol {target_role.value}"
        
        # Solo super admin puede crear otros super admins
        if target_role == UserRole.SUPER_ADMIN and creator_role != UserRole.SUPER_ADMIN:
            return False, "Solo super administradores pueden crear otros super administradores"
            
        return True, "Validación exitosa"
    
    @staticmethod
    def validate_user_modification(modifier_role: UserRole, target_role: UserRole) -> tuple[bool, str]:
        """Validar si se puede modificar un usuario"""
        if not UserPermissions.can_manage_user(modifier_role, target_role):
            return False, "Sin permisos para modificar este usuario"
            
        return True, "Modificación permitida"
