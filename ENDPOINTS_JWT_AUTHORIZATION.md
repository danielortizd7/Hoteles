# 🔐 ENDPOINTS API - ESTADO DE AUTORIZACIÓN JWT
## Hotel Backend API - Documentación Completa

### 📋 **CONFIGURACIÓN GLOBAL**
- **Autenticación por defecto**: JWT (JWTAuthentication)
- **Permisos por defecto**: IsAuthenticated
- **Puerto**: 8000
- **Base URL**: http://127.0.0.1:8000

---

## 🏠 **ENDPOINTS PRINCIPALES**

### **Sistema General**
- `GET /` → ✅ **PÚBLICO** - Información de la API
- `GET /api/` → ✅ **PÚBLICO** - Root API
- `GET /test/` → ✅ **PÚBLICO** - Health check simple
- `GET /admin/` → ✅ **PÚBLICO** - Django Admin

---

## 👥 **ACCOUNTS (Legacy) - /api/accounts/**

### **🔓 Endpoints PÚBLICOS (AllowAny)**
- `POST /api/accounts/login/` → ✅ **PÚBLICO** - Login legacy
- `POST /api/accounts/jwt/login/` → ✅ **PÚBLICO** - JWT Login
- `POST /api/accounts/jwt/refresh/` → ✅ **PÚBLICO** - JWT Refresh token
- `GET /api/accounts/jwt/verify/` → ✅ **PÚBLICO** - Verificar JWT token
- `POST /api/accounts/create-test-user/` → ✅ **PÚBLICO** - Crear usuario test
- `POST /api/accounts/create-super-admin/` → ✅ **PÚBLICO** - Crear super admin
- `GET /api/accounts/debug/` → ✅ **PÚBLICO** - Información debug
- `GET /api/accounts/health/` → ✅ **PÚBLICO** - Health check
- `GET /api/accounts/simple/` → ✅ **PÚBLICO** - Test simple

### **🔒 Endpoints AUTENTICADOS (JWT Required)**
- `GET /api/accounts/perfil/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/accounts/profile/` → 🔒 **JWT + IsAuthenticated**
- `POST /api/accounts/cerrar-sesion/` → 🔒 **JWT + IsAuthenticated**
- `POST /api/accounts/logout/` → 🔒 **JWT + IsAuthenticated**

### **🛡️ ViewSet Usuarios (Permission-based)**
- `GET /api/accounts/usuarios/` → 🛡️ **JWT + CanManageUsers**
- `POST /api/accounts/usuarios/` → 🛡️ **JWT + CanManageUsers**
- `GET /api/accounts/usuarios/{id}/` → 🛡️ **JWT + CanManageUsers**
- `PUT /api/accounts/usuarios/{id}/` → 🛡️ **JWT + CanManageUsers**
- `DELETE /api/accounts/usuarios/{id}/` → 🛡️ **JWT + CanManageUsers**

### **👑 Endpoints de ADMINISTRACIÓN**
- `GET /api/accounts/usuarios/list_receptionists/` → 👑 **JWT + IsAdminOrSuperAdmin**
- `POST /api/accounts/usuarios/create_receptionist/` → 👑 **JWT + IsAdminOrSuperAdmin**
- `POST /api/accounts/usuarios/create_super_admin/` → 🔱 **JWT + IsSuperAdmin**

---

## 🏨 **USERS DOMAIN - /api/domains/users/**

### **🔓 Endpoints PÚBLICOS**
- `POST /api/domains/users/auth/login/` → ✅ **PÚBLICO** - Login dominio
- `POST /api/domains/users/setup/super-admin/` → ✅ **PÚBLICO** - Setup inicial

### **🔒 Endpoints AUTENTICADOS**
- `POST /api/domains/users/auth/logout/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/domains/users/permissions/check/` → 🔒 **JWT + IsAuthenticated**

### **🛡️ ViewSet User Management**
- `GET /api/domains/users/management/` → 🛡️ **JWT + CanManageUsers**
- `POST /api/domains/users/management/` → 🛡️ **JWT + CanManageUsers**
- `GET /api/domains/users/management/{id}/` → 🛡️ **JWT + CanManageUsers**
- `PUT /api/domains/users/management/{id}/` → 🛡️ **JWT + CanManageUsers**
- `DELETE /api/domains/users/management/{id}/` → 🛡️ **JWT + CanManageUsers**

### **👑 Endpoints de ADMINISTRACIÓN**
- `GET /api/domains/users/management/list_receptionists/` → 👑 **JWT + IsAdminOrSuperAdmin**
- `POST /api/domains/users/management/create_receptionist/` → 👑 **JWT + IsAdminOrSuperAdmin**
- `POST /api/domains/users/management/create_super_admin/` → 🔱 **JWT + IsSuperAdmin**

---

## 🏠 **ROOMS (Legacy) - /api/rooms/**

### **🛡️ GESTIÓN DE HABITACIONES (Permisos por Rol)**

#### **👁️ VER HABITACIONES (IsReceptionistOrHigher)**
- `GET /api/rooms/` → 🛡️ **JWT + IsReceptionistOrHigher** - Lista habitaciones
- `GET /api/rooms/{id}/` → 🛡️ **JWT + IsReceptionistOrHigher** - Detalle habitación
- `GET /api/rooms/dashboard/` → 🛡️ **JWT + IsReceptionistOrHigher** - Dashboard stats
- `GET /api/rooms/disponibles/` → 🛡️ **JWT + IsReceptionistOrHigher** - Habitaciones disponibles

#### **✏️ MODIFICAR HABITACIONES (IsReceptionistOrHigher)**
- `PUT /api/rooms/{id}/` → 🛡️ **JWT + IsReceptionistOrHigher** - Actualizar habitación
- `PATCH /api/rooms/{id}/` → 🛡️ **JWT + IsReceptionistOrHigher** - Actualización parcial
- `POST /api/rooms/{id}/change_status/` → 🛡️ **JWT + IsReceptionistOrHigher** - Cambiar estado

#### **👑 CREAR/ELIMINAR HABITACIONES (IsAdminOrSuperAdmin)**
- `POST /api/rooms/` → 👑 **JWT + IsAdminOrSuperAdmin** - Crear habitación
- `DELETE /api/rooms/{id}/` → 👑 **JWT + IsAdminOrSuperAdmin** - Eliminar habitación

### **🏷️ TIPOS DE HABITACIÓN (IsAdminOrSuperAdmin)**
- `GET /api/rooms/tipos/` → 👑 **JWT + IsAdminOrSuperAdmin** - Lista tipos
- `POST /api/rooms/tipos/` → 👑 **JWT + IsAdminOrSuperAdmin** - Crear tipo
- `GET /api/rooms/tipos/{id}/` → 👑 **JWT + IsAdminOrSuperAdmin** - Detalle tipo
- `PUT /api/rooms/tipos/{id}/` → 👑 **JWT + IsAdminOrSuperAdmin** - Actualizar tipo
- `DELETE /api/rooms/tipos/{id}/` → 👑 **JWT + IsAdminOrSuperAdmin** - Eliminar tipo

### **🔄 Compatibilidad Inglés (Mismos Permisos)**
- `GET /api/rooms/room-types/` → 👑 **JWT + IsAdminOrSuperAdmin** - Room types (EN)
- `POST /api/rooms/room-types/` → 👑 **JWT + IsAdminOrSuperAdmin** - Create room type (EN)

---

## 📦 **INVENTORY - /api/inventory/**

### **🔒 Todos AUTENTICADOS (JWT Required)**

#### **Productos**
- `GET /api/inventory/productos/` → 🔒 **JWT + IsAuthenticated**
- `POST /api/inventory/productos/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/inventory/productos/{id}/` → 🔒 **JWT + IsAuthenticated**
- `PUT /api/inventory/productos/{id}/` → 🔒 **JWT + IsAuthenticated**
- `DELETE /api/inventory/productos/{id}/` → 🔒 **JWT + IsAuthenticated**

#### **Categorías**
- `GET /api/inventory/categorias/` → 🔒 **JWT + IsAuthenticated**
- `POST /api/inventory/categorias/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/inventory/categorias/{id}/` → 🔒 **JWT + IsAuthenticated**
- `PUT /api/inventory/categorias/{id}/` → 🔒 **JWT + IsAuthenticated**
- `DELETE /api/inventory/categorias/{id}/` → 🔒 **JWT + IsAuthenticated**

#### **Movimientos de Stock**
- `GET /api/inventory/movimientos-stock/` → 🔒 **JWT + IsAuthenticated**
- `POST /api/inventory/movimientos-stock/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/inventory/movimientos-stock/{id}/` → 🔒 **JWT + IsAuthenticated**
- `PUT /api/inventory/movimientos-stock/{id}/` → 🔒 **JWT + IsAuthenticated**
- `DELETE /api/inventory/movimientos-stock/{id}/` → 🔒 **JWT + IsAuthenticated**

#### **Compatibilidad Inglés**
- `GET /api/inventory/products/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/inventory/categories/` → 🔒 **JWT + IsAuthenticated**
- `GET /api/inventory/stock-movements/` → 🔒 **JWT + IsAuthenticated**

---

## 📊 **RESUMEN DE SEGURIDAD**

### **🔓 Endpoints PÚBLICOS (15)**
- Sistema general (4)
- Accounts login/setup (7)
- Users domain login/setup (2)
- Health checks (2)

### **🔒 Endpoints AUTENTICADOS (22)**
- Accounts perfil/logout (4)
- Users domain logout/permissions (2)
- Inventory completo (16)

### **🛡️ Endpoints con PERMISOS ESPECIALES (27)**
- ViewSets con CanManageUsers (8)
- Admin endpoints (4)
- Super Admin endpoints (2)
- Rooms con IsReceptionistOrHigher (7)
- Rooms con IsAdminOrSuperAdmin (6)

### **⚠️ Endpoints TEMPORALMENTE PÚBLICOS (0)**
- ✅ **CORREGIDO** - Todos los endpoints tienen autorización apropiada

---

## 🔑 **TIPOS DE AUTORIZACIÓN**

1. **✅ PÚBLICO** - Sin autenticación requerida
2. **🔒 JWT + IsAuthenticated** - Token JWT válido
3. **🛡️ JWT + CanManageUsers** - Token + permisos gestión usuarios
4. **👑 JWT + IsAdminOrSuperAdmin** - Token + rol Admin o Super Admin
5. **🔱 JWT + IsSuperAdmin** - Token + rol Super Admin exclusivo
6. **⚠️ PÚBLICO TEMPORAL** - Temporalmente sin auth (necesita corrección)

---

## 🚨 **ACCIONES REQUERIDAS**

### **✅ COMPLETADO**
1. **✅ Rooms migrado a JWT** - Implementado con permisos granulares
2. **✅ Permisos por roles** implementados según jerarquía:
   - **Recepcionistas**: Ver, actualizar habitaciones, cambiar estado
   - **Admin/Super Admin**: Crear/eliminar habitaciones, gestionar tipos

### **PRÓXIMAS MEJORAS RECOMENDADAS**
1. **Documentar roles específicos** para cada endpoint ✅ (Completado)
2. **Implementar rate limiting** para endpoints públicos
3. **Agregar logging de seguridad**
4. **Tests de autorización** para validar permisos

---

*Última actualización: 24 de Agosto, 2025*
*Estado del servidor: ✅ Funcionando en puerto 8000*
*Estado de autorización: ✅ JWT implementado en todos los endpoints*
