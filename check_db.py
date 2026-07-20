import os
import sqlite3

print("======================================")
print("Directorio actual:", os.getcwd())
print("Base de datos:", os.path.abspath("caja_facil.db"))
print("Existe:", os.path.exists("caja_facil.db"))
print("======================================")

conn = sqlite3.connect("backend/caja_facil.db")
cursor = conn.cursor()

print("\n=== TABLAS ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"Total tablas: {len(tables)}")

for table in tables:
    print(table)
print("\n=== EMPRESAS ===")

cursor.execute("""
SELECT id, tax_id, business_name
FROM company
""")

rows = cursor.fetchall()

print(f"Total empresas: {len(rows)}")

for row in rows:
    print(row)

conn.close()