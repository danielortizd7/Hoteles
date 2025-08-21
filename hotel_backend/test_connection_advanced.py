#!/usr/bin/env python3
"""
Script para probar conexión usando connection string directo
"""

import psycopg2
import os
from pathlib import Path

# Cargar variables del .env
env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def test_connection_string():
    """Probar conexión usando connection string directo"""
    
    # Construir connection string exacto
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')
    
    # Probar diferentes formatos de connection string
    connection_strings = [
        f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require",
        f"postgresql://{user}:{password}@{host}:{port}/{database}",
        f"host={host} port={port} dbname={database} user={user} password={password} sslmode=require"
    ]
    
    for i, conn_str in enumerate(connection_strings):
        print(f"\n🔄 Probando método {i+1}...")
        if i < 2:
            print(f"Connection string: postgresql://{user}:****@{host}:{port}/{database}")
        else:
            print(f"Parameters: host={host} port={port} dbname={database} user={user}")
        
        try:
            if i < 2:
                # Usando connection string
                connection = psycopg2.connect(conn_str)
            else:
                # Usando parámetros separados
                connection = psycopg2.connect(
                    host=host,
                    port=port,
                    dbname=database,
                    user=user,
                    password=password,
                    sslmode='require'
                )
            
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            
            print("✅ ¡Conexión exitosa!")
            print(f"PostgreSQL version: {result[0][:50]}...")
            
            cursor.close()
            connection.close()
            
            return True, i+1
            
        except psycopg2.OperationalError as e:
            print(f"❌ Error: {e}")
            continue
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            continue
    
    return False, None

if __name__ == "__main__":
    success, method = test_connection_string()
    if success:
        print(f"\n🎉 La conexión funciona con el método {method}!")
        print("Ahora puedes ejecutar: python manage.py migrate")
    else:
        print("\n⚠️  Ningún método de conexión funcionó")
        print("Verifica:")
        print("1. Que la contraseña sea exacta")
        print("2. Que el usuario sea correcto para el pooler")
        print("3. Que el proyecto de Supabase esté activo")
