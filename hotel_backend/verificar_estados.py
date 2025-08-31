#!/usr/bin/env python3
"""
Script para verificar los estados disponibles en el modelo Room
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/c/Users/PC/Desktop/BackendHoltel/hotel_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_backend.settings')
django.setup()

from rooms.models import Room

def verificar_estados():
    print("🏠 Estados disponibles en el modelo Room:")
    print("=" * 50)
    
    for value, display in Room.STATUS_CHOICES:
        print(f"  Valor interno: '{value}' → Display: '{display}'")
    
    print("\n✅ Estados que puedes usar en la API:")
    print("  - 'disponible' (se mostrará como 'Disponible')")
    print("  - 'ocupada' (se mostrará como 'Ocupada')")
    print("  - 'limpieza' (se mostrará como 'En limpieza')")
    print("  - 'mantenimiento' (se mostrará como 'Mantenimiento')")
    
    print("\n📋 Ejemplo de JSON para cambio de estado:")
    print('  {"estado": "disponible"}')
    print('  {"estado": "ocupada"}')
    print('  {"estado": "limpieza"}')
    print('  {"estado": "mantenimiento"}')

if __name__ == "__main__":
    verificar_estados()
