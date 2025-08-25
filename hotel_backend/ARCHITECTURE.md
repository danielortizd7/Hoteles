# Estructura del Proyecto por Dominios

Este proyecto utiliza **Domain-Driven Design (DDD)** para organizar el código por dominios de negocio.

## Estructura de Carpetas

```
hotel_backend/
├── my app/                          # Capa de dominios (arquitectura DDD)
│   ├── users/                       # Dominio de usuarios y roles
│   │   ├── domain/                  # Entidades y reglas de negocio
│   │   │   └── entities.py          # UserRole, UserPermissions, UserDomainRules
│   │   ├── application/             # Casos de uso y servicios
│   │   │   └── services.py          # UserManagementService, AuthenticationService
│   │   ├── infrastructure/          # Controladores y adaptadores
│   │   │   └── views.py             # UserManagementViewSet, login, logout
│   │   └── urls.py                  # Rutas del dominio
│   │
│   ├── rooms/                       # Dominio de habitaciones
│   │   ├── domain/
│   │   │   └── entities.py          # RoomStatus, RoomBusinessRules
│   │   ├── application/
│   │   │   └── services.py          # RoomManagementService
│   │   └── infrastructure/
│   │
│   ├── reservations/                # Dominio de reservas
│   ├── inventory/                   # Dominio de inventario
│   └── reports/                     # Dominio de reportes
│
├── accounts/                        # App legacy (mantener compatibilidad)
├── rooms/                           # App legacy
├── inventory/                       # App legacy
└── hotel_backend/                   # Configuración
```

## Capas por Dominio

### 1. Domain (Dominio)
- **Entidades**: Modelos de negocio puros
- **Reglas de negocio**: Lógica central del dominio
- **Value Objects**: Objetos inmutables
- **Enums**: Constantes del dominio

### 2. Application (Aplicación)
- **Servicios**: Casos de uso del dominio
- **DTOs**: Objetos de transferencia de datos
- **Interfaces**: Contratos para infraestructura

### 3. Infrastructure (Infraestructura)
- **Views**: Controladores REST
- **Serializers**: Validación y serialización
- **Repositories**: Acceso a datos
- **External Services**: APIs externas

## Dominios Implementados

### Users (Usuarios y Roles)
**Entidades principales:**
- `UserRole`: SUPER_ADMIN, ADMIN, RECEPTIONIST
- `UserPermissions`: Permisos por rol
- `UserDomainRules`: Validaciones de negocio

**Servicios:**
- `UserManagementService`: Crear, actualizar, listar usuarios
- `AuthenticationService`: Login, logout, verificar permisos
- `SuperAdminSetupService`: Configuración inicial

**Endpoints:**
```
POST /api/domains/users/setup/super-admin/     # Crear super admin inicial
POST /api/domains/users/auth/login/            # Login con dominio
POST /api/domains/users/auth/logout/           # Logout
GET  /api/domains/users/management/            # Listar usuarios
POST /api/domains/users/management/            # Crear usuario
GET  /api/domains/users/management/by_role/    # Filtrar por rol
POST /api/domains/users/management/create_receptionist/  # Crear recepcionista
POST /api/domains/users/management/create_admin/        # Crear admin (solo super admin)
GET  /api/domains/users/permissions/check/     # Verificar permisos
```

### Rooms (Habitaciones) - EN DESARROLLO
**Entidades:**
- `RoomStatus`: Estados de habitación
- `RoomBusinessRules`: Reglas de cambio de estado

**Servicios:**
- `RoomManagementService`: Gestión de habitaciones

### Reservations (Reservas) - PREPARADO
Estructura básica creada, listo para implementar.

### Inventory (Inventario) - PREPARADO  
Estructura básica creada, listo para implementar.

## Ventajas de esta Arquitectura

1. **Separación de responsabilidades**: Cada capa tiene su propósito
2. **Escalabilidad**: Fácil agregar nuevos dominios
3. **Mantenibilidad**: Cambios localizados por dominio
4. **Testabilidad**: Lógica de negocio independiente
5. **Reutilización**: Servicios reutilizables
6. **Compatibilidad**: Mantiene apps legacy funcionando

## Uso de los Nuevos Endpoints

### Configuración inicial (PRIMERA VEZ):
```bash
POST /api/domains/users/setup/super-admin/
{
  "username": "superadmin",
  "email": "super@hotel.com",
  "password": "superpassword123",
  "first_name": "Super",
  "last_name": "Admin"
}
```

### Login:
```bash
POST /api/domains/users/auth/login/
{
  "username": "superadmin",
  "password": "superpassword123"
}
```

### Crear administrador (como super admin):
```bash
POST /api/domains/users/management/create_admin/
Authorization: Token TU_TOKEN
{
  "username": "admin",
  "email": "admin@hotel.com",
  "password": "admin123",
  "first_name": "Admin",
  "last_name": "Hotel"
}
```

### Crear recepcionista (como admin o super admin):
```bash
POST /api/domains/users/management/create_receptionist/
Authorization: Token TU_TOKEN
{
  "username": "recepcionista1",
  "email": "recep@hotel.com",
  "password": "recep123",
  "first_name": "María",
  "last_name": "García"
}
```

## Migración Gradual

Los endpoints legacy siguen funcionando:
- `/api/accounts/` → Mantener para compatibilidad
- `/api/domains/users/` → Nueva arquitectura

Puedes migrar gradualmente o usar ambos sistemas en paralelo.
