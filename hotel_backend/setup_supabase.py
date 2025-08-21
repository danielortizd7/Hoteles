#!/usr/bin/env python3
"""
Script para configurar el backend del Hotel con Supabase
Ejecuta este script después de crear tu proyecto en Supabase
"""

import os
import sys
from pathlib import Path

def get_supabase_config():
    """Solicita al usuario la configuración de Supabase"""
    print("🏨 Configuración del Backend Hotel - Supabase")
    print("=" * 50)
    print()
    
    print("Por favor, proporciona la información de tu proyecto Supabase:")
    print("(Puedes encontrar esta información en: Settings > Database > Connection info)")
    print()
    
    db_host = input("🌐 Host de la base de datos (ej: db.xxx.supabase.co): ").strip()
    db_name = input("📊 Nombre de la base de datos (ej: postgres): ").strip() or "postgres"
    db_user = input("👤 Usuario (ej: postgres): ").strip() or "postgres"
    db_password = input("🔐 Contraseña: ").strip()
    db_port = input("🚪 Puerto (default: 5432): ").strip() or "5432"
    
    print()
    print("Frontend Configuration:")
    frontend_url = input("🌍 URL del frontend (ej: http://localhost:3000): ").strip() or "http://localhost:3000"
    
    return {
        'DB_HOST': db_host,
        'DB_NAME': db_name,
        'DB_USER': db_user,
        'DB_PASSWORD': db_password,
        'DB_PORT': db_port,
        'FRONTEND_URL': frontend_url
    }

def update_env_file(config):
    """Actualiza el archivo .env con la configuración proporcionada"""
    env_path = Path('.env')
    
    env_content = f"""# Django Configuration
SECRET_KEY=django-insecure-6g!4+3u+0lx84wcuwr4ocylkt7t1f@zz$jk=+=y4h-isrsrg5(
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,{config['DB_HOST']}

# Supabase Database Configuration
DB_NAME={config['DB_NAME']}
DB_USER={config['DB_USER']}
DB_PASSWORD={config['DB_PASSWORD']}
DB_HOST={config['DB_HOST']}
DB_PORT={config['DB_PORT']}

# CORS Configuration
CORS_ALLOWED_ORIGINS={config['FRONTEND_URL']},http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
"""
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ Archivo .env actualizado exitosamente!")

def main():
    print("🚀 Iniciando configuración del backend...")
    print()
    
    # Verificar que estamos en el directorio correcto
    if not Path('manage.py').exists():
        print("❌ Error: Este script debe ejecutarse desde el directorio del proyecto Django")
        print("   (donde se encuentra el archivo manage.py)")
        sys.exit(1)
    
    # Obtener configuración de Supabase
    config = get_supabase_config()
    
    # Actualizar archivo .env
    update_env_file(config)
    
    print()
    print("🎉 ¡Configuración completada!")
    print()
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py migrate")
    print("2. Ejecuta: python manage.py load_initial_data")
    print("3. Ejecuta: python manage.py runserver")
    print()
    print("🌐 Tu API estará disponible en: http://localhost:8000/api/")
    print("🔧 Panel de administración: http://localhost:8000/admin/")
    print()
    print("👤 Usuarios de prueba que se crearán:")
    print("   - Administrador: admin / admin123")
    print("   - Recepcionista: martha / martha123")

if __name__ == "__main__":
    main()
