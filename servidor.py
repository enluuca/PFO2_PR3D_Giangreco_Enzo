from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "tareas.db"

# --- Inicialización de la Base de Datos SQLite ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabla de Usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    """)
    # Tabla de Tareas (para extender funcionalidades)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    conn.commit()
    conn.close()

# Conexión auxiliar
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- Endpoints ---

# 1. Registro de Usuarios (POST /registro)
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"error": "Faltan campos requeridos ('usuario', 'contraseña')"}), 400

    usuario = data['usuario'].strip()
    contrasena = data['contraseña']

    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña no pueden estar vacíos"}), 400

    # Hasheo seguro de contraseña
    contrasena_hash = generate_password_hash(contrasena)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
            (usuario, contrasena_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "El nombre de usuario ya se encuentra registrado"}), 409

    conn.close()
    return jsonify({"mensaje": f"Usuario '{usuario}' registrado exitosamente"}), 201

# 2. Inicio de Sesión (POST /login)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"error": "Faltan campos requeridos ('usuario', 'contraseña')"}), 400

    usuario = data['usuario'].strip()
    contrasena = data['contraseña']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    user_row = cursor.fetchone()
    conn.close()

    # Verificación del hash de la contraseña
    if user_row and check_password_hash(user_row['contrasena_hash'], contrasena):
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": usuario,
            "status": "autorizado"
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# 3. Gestión de Tareas (GET /tareas)
@app.route('/tareas', methods=['GET'])
def tareas():
    plantilla_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Panel de Tareas</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f8; margin: 0; padding: 40px; display: flex; justify-content: center; }
            .card { background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; width: 100%; padding: 24px; text-align: center; }
            h1 { color: #1f2937; margin-bottom: 8px; }
            p { color: #4b5563; font-size: 16px; }
            .badge { display: inline-block; background-color: #10b981; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 14px; font-weight: bold; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Bienvenido al Gestor de Tareas!</h1>
            <p>Has accedido satisfactoriamente a la interfaz central de la API.</p>
            <span class="badge">Servidor Operativo</span>
        </div>
    </body>
    </html>
    """
    return render_template_string(plantilla_html)

if __name__ == '__main__':
    init_db()
    print("Base de datos SQLite inicializada. Servidor corriendo en http://localhost:5000")
    app.run(port=5000, debug=True)