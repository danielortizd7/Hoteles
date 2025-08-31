#!/usr/bin/env python3
"""
Script para probar las respuestas en español de la API de tipos de habitación
"""
import requests
import json

def test_spanish_api():
    base_url = "http://127.0.0.1:8000"
    
    # Obtener token
    print("🔐 Obteniendo token de acceso...")
    login_response = requests.post(f"{base_url}/api/token/", {
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Error al obtener token: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()["access"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Crear tipo de habitación
    print("\n🏠 Creando tipo de habitación en español...")
    room_type_data = {
        "nombre": "Suite Presidencial",
        "description": "Suite de lujo con vista al mar",
        "precio_base": 250000,
        "precio_hora_adicional": 15000
    }
    
    create_response = requests.post(
        f"{base_url}/api/room-types/",
        headers=headers,
        data=json.dumps(room_type_data)
    )
    
    print(f"📤 Respuesta del servidor:")
    print(f"Status: {create_response.status_code}")
    
    if create_response.status_code == 201:
        response_data = create_response.json()
        print("✅ Tipo de habitación creado exitosamente!")
        print(f"📝 Respuesta en JSON:")
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        
        # Verificar que el campo es 'nombre' y no 'name'
        if 'nombre' in response_data:
            print(f"✅ Campo 'nombre' encontrado: {response_data['nombre']}")
        else:
            print("❌ Campo 'nombre' no encontrado en la respuesta")
            
        if 'name' in response_data:
            print("⚠️ Advertencia: Aún se encontró campo 'name' en inglés")
        else:
            print("✅ No se encontró campo 'name' en inglés")
            
    else:
        print(f"❌ Error al crear tipo de habitación: {create_response.status_code}")
        print(create_response.text)
    
    # Listar tipos de habitación
    print("\n📋 Listando tipos de habitación...")
    list_response = requests.get(f"{base_url}/api/room-types/", headers=headers)
    
    if list_response.status_code == 200:
        room_types = list_response.json()
        print(f"✅ Se encontraron {len(room_types)} tipos de habitación:")
        for room_type in room_types:
            print(f"  - ID: {room_type['id']}, Nombre: {room_type.get('nombre', 'NO ENCONTRADO')}")
    else:
        print(f"❌ Error al listar tipos: {list_response.status_code}")

if __name__ == "__main__":
    test_spanish_api()
