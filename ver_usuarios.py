import sqlite3

conn = sqlite3.connect("tareas.db")
cursor = conn.cursor()

cursor.execute("SELECT id, usuario, contrasena_hash FROM usuarios")
filas = cursor.fetchall()

print(f"{'ID':<4} | {'USUARIO':<15} | {'HASH'}")
print("-" * 80)
for fila in filas:
    print(f"{fila[0]:<4} | {fila[1]:<15} | {fila[2]}")

conn.close()