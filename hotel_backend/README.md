# Hotel Backend API Documentation

## 🏨 Sistema de Gestión Hotelera - Backend

Este es el backend de un sistema de gestión hotelera desarrollado con Django REST Framework, diseñado para trabajar con Supabase como base de datos.

### 🚀 Características Principales

- **Gestión de Usuarios**: Sistema de autenticación con roles (Administrador, Recepcionista)
- **Gestión de Habitaciones**: Diferentes tipos de habitaciones (Estándar, Con Máquina del Amor, Suite)
- **Sistema de Inventario**: Control de productos con categorías y movimientos de stock
- **Sistema de Reservaciones**: Gestión de ocupación de habitaciones
- **Reportes**: Estadísticas y reportes diarios
- **API REST**: Endpoints completos para todas las funcionalidades

### 🛠️ Tecnologías Utilizadas

- **Django 5.1.2**: Framework web de Python
- **Django REST Framework**: Para la API REST
- **PostgreSQL**: Base de datos (Supabase)
- **django-cors-headers**: Para permitir CORS
- **python-decouple**: Para manejo de variables de entorno

### 📋 Configuración Inicial

1. **Instalar dependencias**:
```bash
pip install django-cors-headers djangorestframework psycopg2-binary python-decouple
```

2. **Configurar Supabase**:
```bash
python setup_supabase.py
```

3. **Aplicar migraciones**:
```bash
python manage.py migrate
```

4. **Cargar datos iniciales**:
```bash
python manage.py load_initial_data
```

5. **Ejecutar servidor**:
```bash
python manage.py runserver
```

### 🔗 Endpoints de la API

#### Autenticación (`/api/accounts/`)

- `POST /api/accounts/login/` - Iniciar sesión
- `POST /api/accounts/logout/` - Cerrar sesión
- `GET /api/accounts/profile/` - Obtener perfil del usuario actual
- `GET /api/accounts/users/` - Listar usuarios
- `POST /api/accounts/users/` - Crear nuevo usuario

#### Habitaciones (`/api/rooms/`)

- `GET /api/rooms/rooms/` - Listar habitaciones
- `POST /api/rooms/rooms/` - Crear habitación
- `GET /api/rooms/rooms/{id}/` - Detalle de habitación
- `PUT /api/rooms/rooms/{id}/` - Actualizar habitación
- `DELETE /api/rooms/rooms/{id}/` - Eliminar habitación
- `POST /api/rooms/rooms/{id}/change_status/` - Cambiar estado de habitación
- `GET /api/rooms/rooms/available/` - Habitaciones disponibles
- `GET /api/rooms/rooms/dashboard_stats/` - Estadísticas del dashboard
- `GET /api/rooms/room-types/` - Tipos de habitaciones

#### Inventario (`/api/inventory/`)

- `GET /api/inventory/products/` - Listar productos
- `POST /api/inventory/products/` - Crear producto
- `GET /api/inventory/products/{id}/` - Detalle de producto
- `PUT /api/inventory/products/{id}/` - Actualizar producto
- `DELETE /api/inventory/products/{id}/` - Eliminar producto
- `POST /api/inventory/products/{id}/adjust_stock/` - Ajustar stock
- `GET /api/inventory/products/low_stock/` - Productos con stock bajo
- `GET /api/inventory/categories/` - Categorías de productos
- `GET /api/inventory/stock-movements/` - Movimientos de stock

### 📊 Ejemplos de Uso

#### 1. Login
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 2. Obtener estadísticas del dashboard
```bash
curl -X GET http://localhost:8000/api/rooms/rooms/dashboard_stats/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### 3. Cambiar estado de habitación
```bash
curl -X POST http://localhost:8000/api/rooms/rooms/1/change_status/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "occupied"}'
```

#### 4. Ajustar stock de producto
```bash
curl -X POST http://localhost:8000/api/inventory/products/1/adjust_stock/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"adjustment_type": "increase", "quantity": 10, "reason": "Compra nueva"}'
```

### 🔐 Autenticación

La API utiliza Token Authentication. Después del login, incluye el token en todas las peticiones:

```
Authorization: Token YOUR_TOKEN_HERE
```

### 🏗️ Estructura del Proyecto

```
hotel_backend/
├── accounts/           # Gestión de usuarios y autenticación
├── rooms/             # Gestión de habitaciones
├── reservations/      # Sistema de reservaciones
├── inventory/         # Gestión de inventario
├── reports/           # Sistema de reportes
├── hotel_backend/     # Configuración principal
├── manage.py
├── .env              # Variables de entorno
├── setup_supabase.py # Script de configuración
└── README.md
```

### 🎯 Funcionalidades del Frontend Soportadas

Basado en las imágenes del frontend, el backend soporta:

1. **Panel de Control**:
   - Estadísticas de habitaciones (disponibles, ocupadas, en limpieza)
   - Ingresos del día
   - Tasa de ocupación

2. **Gestión de Usuarios**:
   - Roles: Administrador y Recepcionista
   - Información de contacto

3. **Gestión de Habitaciones**:
   - 3 tipos: Estándar, Con Máquina del Amor, Suite
   - Estados: Disponible, Ocupada, En Limpieza, Mantenimiento
   - Precios por tipo de habitación

4. **Inventario**:
   - Productos categorizados
   - Control de stock con alertas de stock bajo
   - Ajustes de inventario con historial

### 🔧 Configuración de Variables de Entorno

Ejemplo de archivo `.env`:

```env
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase Database Configuration
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db.your-project.supabase.co
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 🚨 Usuarios de Prueba

El comando `load_initial_data` crea los siguientes usuarios:

- **Administrador**: 
  - Usuario: `admin`
  - Contraseña: `admin123`
  - Rol: Administrador

- **Recepcionista**:
  - Usuario: `martha`
  - Contraseña: `martha123`
  - Rol: Recepcionista

### 📱 Integración con Frontend

Para conectar con tu frontend, asegúrate de:

1. Configurar CORS correctamente en `CORS_ALLOWED_ORIGINS`
2. Usar las URLs base: `http://localhost:8000/api/`
3. Incluir el token de autenticación en todas las peticiones
4. Manejar los códigos de respuesta HTTP apropiadamente

### 🐛 Solución de Problemas Comunes

1. **Error de conexión a la base de datos**:
   - Verifica las credenciales en el archivo `.env`
   - Asegúrate de que Supabase esté configurado correctamente

2. **Error de CORS**:
   - Verifica que tu URL del frontend esté en `CORS_ALLOWED_ORIGINS`

3. **Error 401 Unauthorized**:
   - Verifica que estés enviando el token de autenticación
   - Asegúrate de que el token sea válido

### 📄 Licencia

Este proyecto está desarrollado para fines educativos y de demostración.
