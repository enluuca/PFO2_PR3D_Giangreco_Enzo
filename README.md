# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

Sistema de gestión y autenticación basado en API REST construido con Python, Flask y persistencia local en SQLite.

## Características
- **Seguridad:** Encriptación de contraseñas mediante hashing unidireccional (PBKDF2/SHA256 con salt) provisto por `werkzeug.security`.
- **Persistencia de Datos:** SQLite local integrado (`tareas.db`).
- **Endpoints REST:**
  - `POST /registro`: Alta de usuarios con validación de unicidad.
  - `POST /login`: Validación de credenciales contra hash criptográfico.
  - `GET /tareas`: Retorna la vista HTML de bienvenida del sistema.
- **Cliente interactivo:** CLI de consola para interacción directa vía HTTP.

---

## Requisitos de Instalación
- Python 3.8+
- Dependencias:
  ```bash
  pip install Flask requests