#!/usr/bin/env python3
"""
Script para probar el endpoint de cambio de estado en español
"""
import requests
import json

def test_cambio_estado():
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
        
        # Cambiar estado de la habitación 7
        print("\n🏠 Cambiando estado de habitación 7...")
        cambio_data = {
            "estado": "ocupada"
        }
        
        # Usar el nuevo endpoint en español (solo estado)
        change_response = requests.post(
            f"{base_url}/api/rooms/7/cambio-estado/",
            headers=headers,
            data=json.dumps(cambio_data)
        )
        
        print(f"📤 Status: {change_response.status_code}")
        
        if change_response.status_code == 200:
            result = change_response.json()
            print("✅ ¡Estado cambiado exitosamente!")
            print(f"📝 Respuesta:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error:")
            print(f"📝 Respuesta: {change_response.text}")
            
        # Verificar el estado actual de la habitación
        print("\n🔍 Verificando estado actual...")
        get_response = requests.get(f"{base_url}/api/rooms/7/", headers=headers)
        if get_response.status_code == 200:
            room_data = get_response.json()
            print(f"📊 Estado actual: {room_data.get('estado')}")
            print(f"🏠 Disponible: {room_data.get('disponible')}")
        
    else:
        print(f"❌ Error obteniendo token: {login_response.status_code}")
        print(login_response.text)

if __name__ == "__main__":
    test_cambio_estado()
