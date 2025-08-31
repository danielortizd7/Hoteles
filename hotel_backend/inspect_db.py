#!/usr/bin/env python3
"""
Script para inspeccionar la estructura de la tabla rooms_roomtype
"""
import sqlite3

def inspect_db():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Obtener información sobre la tabla rooms_roomtype
        cursor.execute("PRAGMA table_info(rooms_roomtype)")
        columns = cursor.fetchall()
        
        print("📋 Estructura de la tabla rooms_roomtype:")
        print("=" * 50)
        for column in columns:
            print(f"  {column[1]} ({column[2]}) - Null: {not column[3]} - Default: {column[4]}")
        
        # Obtener algunos registros si existen
        cursor.execute("SELECT COUNT(*) FROM rooms_roomtype")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total de registros: {count}")
        
        if count > 0:
            print("\n🔍 Primeros registros:")
            cursor.execute("SELECT * FROM rooms_roomtype LIMIT 3")
            records = cursor.fetchall()
            for record in records:
                print(f"  {record}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_db()
