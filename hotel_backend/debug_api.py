#!/usr/bin/env python3
"""
Script para debuggear el endpoint /api/rooms/tipos/
"""
import requests
import json

def debug_api():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Debuggeando API...")
    
    # 1. Probar obtener token
    print("\n1️⃣ Probando obtener token...")
    try:
        login_response = requests.post(f"{base_url}/api/token/", {
            "username": "admin",
            "password": "admin123"
        }, timeout=5)
        
        print(f"   Status: {login_response.status_code}")
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data["access"]
            print(f"   ✅ Token obtenido: {token[:20]}...")
            
            # 2. Probar listar tipos de habitación
            print("\n2️⃣ Probando listar tipos...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            list_response = requests.get(f"{base_url}/api/rooms/tipos/", headers=headers, timeout=5)
            print(f"   Status: {list_response.status_code}")
            
            if list_response.status_code == 200:
                tipos = list_response.json()
                print(f"   ✅ Tipos encontrados: {len(tipos)}")
                
                # 3. Probar crear tipo
                print("\n3️⃣ Probando crear tipo...")
                new_tipo = {
                    "nombre": "Suite Test Debug",
                    "description": "Descripción de prueba",
                    "precio_base": 150000,
                    "precio_hora_adicional": 8000
                }
                
                create_response = requests.post(
                    f"{base_url}/api/rooms/tipos/",
                    headers=headers,
                    data=json.dumps(new_tipo),
                    timeout=5
                )
                
                print(f"   Status: {create_response.status_code}")
                if create_response.status_code == 201:
                    result = create_response.json()
                    print(f"   ✅ Tipo creado:")
                    print(f"   📝 Respuesta: {json.dumps(result, indent=2, ensure_ascii=False)}")
                else:
                    print(f"   ❌ Error al crear:")
                    print(f"   📝 Respuesta: {create_response.text}")
            else:
                print(f"   ❌ Error al listar:")
                print(f"   📝 Respuesta: {list_response.text}")
        else:
            print(f"   ❌ Error en token:")
            print(f"   📝 Respuesta: {login_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error de conexión: {e}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")

if __name__ == "__main__":
    debug_api()
