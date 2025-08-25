#!/bin/bash
set -o errexit

# Script de build para Render - Versión simplificada
echo "🚀 Iniciando despliegue de Hotel MOTEL ECLIPSE Backend..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Navegar al directorio del proyecto Django
cd hotel_backend

# Verificar que Django puede importar correctamente
echo "� Verificando configuración de Django..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Recopilar archivos estáticos
echo "� Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Aplicar migraciones
echo "🗄️ Aplicando migraciones de base de datos..."
python manage.py migrate

echo "✅ Despliegue completado exitosamente!"
