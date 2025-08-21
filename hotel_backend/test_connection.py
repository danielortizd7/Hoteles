#!/usr/bin/env python3
"""
Script para probar la conexión a Supabase directamente
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

def test_connection():
    """Probar conexión directa a Supabase"""
    
    # Configuración
    config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'sslmode': 'require'
    }
    
    print("🔄 Probando conexión a Supabase...")
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print(f"User length: {len(config['user'])}")
    print(f"Password: {'*' * len(config['password'])}")
    print()
    
    # Verificar que el usuario tenga el formato correcto
    if '.' not in config['user']:
        print("⚠️  ADVERTENCIA: El usuario no contiene un punto (.). Para pooler debe ser: postgres.xxxxx")
    
    try:
        # Crear connection string manual para debug
        conn_string = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?sslmode=require"
        print(f"Connection string: postgresql://{config['user']}:****@{config['host']}:{config['port']}/{config['database']}?sslmode=require")
        print()
        
        # Intentar conexión
        connection = psycopg2.connect(**config)
        cursor = connection.cursor()
        
        # Probar una consulta simple
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        
        print("✅ ¡Conexión exitosa!")
        print(f"PostgreSQL version: {result[0]}")
        
        # Probar crear una tabla de prueba
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            INSERT INTO test_connection (message) VALUES ('Conexión Django exitosa!');
        """)
        
        connection.commit()
        print("✅ Tabla de prueba creada y datos insertados correctamente")
        
        # Limpiar
        cursor.execute("DROP TABLE test_connection;")
        connection.commit()
        print("✅ Tabla de prueba eliminada")
        
        cursor.close()
        connection.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 La conexión funciona correctamente!")
        print("Ahora puedes ejecutar: python manage.py migrate")
    else:
        print("\n⚠️  Verifica tu configuración de Supabase")
        print("1. Verifica que el host sea correcto")
        print("2. Verifica que la contraseña sea correcta")
        print("3. Verifica que tu IP esté en la whitelist de Supabase")
