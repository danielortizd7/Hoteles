#!/bin/bash
set -o errexit

# Script de build para Render
echo "🚀 Iniciando despliegue de Hotel MOTEL ECLIPSE Backend..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Navegar al directorio del proyecto Django
cd hotel_backend

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Aplicar migraciones
echo "🗄️ Aplicando migraciones de base de datos..."
python manage.py migrate

# Crear usuario administrador
echo "👤 Creando usuario administrador..."
python manage.py create_admin

# Cargar datos iniciales (solo si no existen)
echo "📊 Cargando datos iniciales..."
python manage.py load_initial_data

echo "✅ Despliegue completado exitosamente!"
