import requests
import sys

BASE_URL = "http://localhost:5000"

def menu():
    print("\n--- CLIENTE CONSOLA - GESTIÓN DE TAREAS ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Consultar vista web de tareas (GET /tareas)")
    print("4. Salir")
    return input("Selecciona una opción: ").strip()

def registrar():
    usuario = input("Nombre de usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    
    try:
        res = requests.post(f"{BASE_URL}/registro", json={"usuario": usuario, "contraseña": contrasena})
        print(f"[{res.status_code}] {res.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de ejecutar servidor.py.")

def login():
    usuario = input("Nombre de usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    
    try:
        res = requests.post(f"{BASE_URL}/login", json={"usuario": usuario, "contraseña": contrasena})
        print(f"[{res.status_code}] {res.json()}")
        if res.status_code == 200:
            print("\nAcceso concedido. Puedes abrir en tu navegador: http://localhost:5000/tareas")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor.")

def ver_tareas():
    try:
        res = requests.get(f"{BASE_URL}/tareas")
        print(f"[{res.status_code}] Contenido HTML recibido correctamente ({len(res.text)} bytes).")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor.")

def main():
    while True:
        opcion = menu()
        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("Cerrando cliente...")
            sys.exit(0)
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()