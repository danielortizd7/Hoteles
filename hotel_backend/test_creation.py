#!/usr/bin/env python3
"""
Script para probar la creación de tipos de habitación
"""
import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("🔐 Obteniendo token...")
    # Obtener token
    login_response = requests.post(f"{base_url}/api/token/", {
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code == 200:
        token = login_response.json()["access"]
        print(f"✅ Token obtenido: {token[:20]}...")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Probar crear tipo de habitación
        print("\n🏠 Creando tipo de habitación...")
        new_tipo = {
            "nombre": "Estandar 4",
            "description": "Habitación amplia con sala de estar",
            "precio_base": 20000,
            "precio_hora_adicional": 5000
        }
        
        create_response = requests.post(
            f"{base_url}/api/rooms/tipos/",
            headers=headers,
            data=json.dumps(new_tipo)
        )
        
        print(f"📤 Status: {create_response.status_code}")
        
        if create_response.status_code == 201:
            result = create_response.json()
            print("✅ ¡Tipo de habitación creado exitosamente!")
            print(f"📝 Respuesta:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error:")
            print(f"📝 Respuesta: {create_response.text}")
    else:
        print(f"❌ Error obteniendo token: {login_response.status_code}")
        print(login_response.text)

if __name__ == "__main__":
    test_api()
