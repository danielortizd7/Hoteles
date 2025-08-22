# 🏨 Hotel MOTEL ECLIPSE - Backend API

Backend del sistema de gestión hotelera para MOTEL ECLIPSE, desarrollado con Django REST Framework.

## 🚀 Características

- **Gestión de Usuarios**: Sistema de autenticación con roles (admin/recepcionista)
- **Gestión de Habitaciones**: Control de estados, tipos y disponibilidad
- **Inventario**: Manejo de productos, categorías y movimientos de stock
- **API REST**: Endpoints en español e inglés para máxima compatibilidad
- **Base de Datos**: PostgreSQL con Supabase
- **Despliegue**: Configurado para Render

## 🛠 Tecnologías

- Django 5.1.2
- Django REST Framework 3.15.2
- PostgreSQL
- Supabase
- Gunicorn
- WhiteNoise

## 📊 API Endpoints

### Autenticación
- `POST /api/cuentas/login/` - Iniciar sesión
- `POST /api/usuarios/login/` - Iniciar sesión (español)
- `GET /api/cuentas/perfil/` - Perfil del usuario
- `POST /api/usuarios/cerrar-sesion/` - Cerrar sesión

### Habitaciones
- `GET /api/habitaciones/` - Lista de habitaciones
- `GET /api/habitaciones/tipos/` - Tipos de habitación
- `GET /api/habitaciones/dashboard/` - Estadísticas del dashboard
- `GET /api/habitaciones/disponibles/` - Habitaciones disponibles

### Inventario
- `GET /api/inventario/productos/` - Lista de productos
- `GET /api/inventario/categorias/` - Categorías
- `GET /api/inventario/movimientos-stock/` - Movimientos de stock
- `GET /api/inventario/productos/low_stock/` - Productos con stock bajo

### Usuarios
- `GET /api/usuarios/usuarios/` - Lista de usuarios
- `GET /api/cuentas/usuarios/` - Gestionar usuarios

## 🔧 Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/darkside-D77/Hoteles.git
cd Hoteles
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear archivo `.env`:
```env
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
DB_NAME=tu_db_name
DB_USER=tu_db_user
DB_PASSWORD=tu_db_password
DB_HOST=tu_db_host
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Migrar base de datos**
```bash
cd hotel_backend
python manage.py migrate
```

6. **Cargar datos iniciales**
```bash
python manage.py load_initial_data
```

7. **Ejecutar servidor**
```bash
python manage.py runserver
```

## 🌐 Despliegue en Render

### Variables de Entorno en Render:
```
SECRET_KEY=tu_secret_key_para_produccion
DEBUG=False
DATABASE_URL=postgresql://postgres.pmzfwxabqlbzpvkfinpr:Nirvana+1xJd7M@aws-1-sa-east-1.pooler.supabase.com:6543/postgres
ALLOWED_HOSTS=tu-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,http://localhost:3000
```

### Comandos de Build:
```bash
pip install -r requirements.txt
```

### Comando de Start:
```bash
cd hotel_backend && python manage.py migrate && python manage.py load_initial_data && gunicorn hotel_backend.wsgi:application
```

## 👥 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin   | admin123   | Administrador |
| martha  | martha123  | Recepcionista |

## 📱 Colección de Postman

Importa el archivo `Hotel_API_Final.postman_collection.json` para probar todos los endpoints.

## 🏗 Estructura del Proyecto

```
hotel_backend/
├── accounts/          # Gestión de usuarios y autenticación
├── rooms/            # Gestión de habitaciones
├── inventory/        # Gestión de inventario
├── reservations/     # Reservas (futuro)
├── reports/          # Reportes (futuro)
└── hotel_backend/    # Configuración principal
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

- GitHub: [@darkside-D77](https://github.com/darkside-D77)
- Proyecto: [https://github.com/darkside-D77/Hoteles](https://github.com/darkside-D77/Hoteles)
