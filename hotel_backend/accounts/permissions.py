from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Permiso personalizado para super administradores únicamente.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_super_admin
        )

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permiso para administradores y super administradores.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'super_admin']
        )

class IsReceptionistOrHigher(permissions.BasePermission):
    """
    Permiso para recepcionistas, administradores y super administradores.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['receptionist', 'admin', 'super_admin']
        )

class CanManageUsers(permissions.BasePermission):
    """
    Permiso para gestionar usuarios (crear, editar, eliminar).
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.can_manage_users
        )

class CanCreateAdmins(permissions.BasePermission):
    """
    Permiso para crear administradores (solo super admin).
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.can_create_admins
        )

def role_required(*allowed_roles):
    """
    Decorador para vistas que requieren roles específicos.
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'detail': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if request.user.role not in allowed_roles:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'detail': 'Insufficient permissions'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
