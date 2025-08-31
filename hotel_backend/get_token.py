#!/usr/bin/env python3
"""
Script simple para obtener un nuevo token
"""
import requests
import json

def get_fresh_token():
    base_url = "http://127.0.0.1:8000"
    
    print("🔐 Obteniendo token fresco...")
    
    # Obtener token
    login_response = requests.post(f"{base_url}/api/token/", {
        "username": "admin",
        "password": "admin123"
    })
    
    print(f"Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data["access"]
        print(f"✅ Nuevo token obtenido:")
        print(f"📋 Access Token: {access_token}")
        print(f"\n🔗 Para usar en Postman:")
        print(f"Authorization: Bearer {access_token}")
        
        return access_token
    else:
        print(f"❌ Error: {login_response.text}")
        return None

if __name__ == "__main__":
    get_fresh_token()
