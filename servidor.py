import os
import sqlite3
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
CORS(app)
DB_NAME = "tareas.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    usuario = data['usuario'].strip()
    contrasena = data['contraseña']

    if not usuario or not contrasena:
        return jsonify({"error": "Campos vacíos"}), 400

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
        return jsonify({"error": "El usuario ya existe"}), 409

    conn.close()
    return jsonify({"mensaje": f"Usuario '{usuario}' registrado exitosamente"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    usuario = data['usuario'].strip()
    contrasena = data['contraseña']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    user_row = cursor.fetchone()
    conn.close()

    if user_row and check_password_hash(user_row['contrasena_hash'], contrasena):
        return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario}), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Bienvenido</title></head>
    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h1>¡Bienvenido al Gestor de Tareas!</h1>
        <p>API Flask operativa y conectada a SQLite.</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)