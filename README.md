# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

**Materia:** Programación sobre Redes  
**Tecnologías:** Python, Flask, SQLite, Werkzeug, HTML/CSS  
**Despliegue de Documentación:** GitHub Pages  

---

## Descripción del Proyecto
Este proyecto consiste en una **API REST** desarrollada con Flask que implementa autenticación básica, almacenamiento de contraseñas hasheadas y persistencia relacional con **SQLite**. Además, cuenta con un cliente interactivo por consola (CLI) y un sitio estático alojado en **GitHub Pages** que documenta la arquitectura, endpoints y evidencia de pruebas del sistema.

---

## Estructura del Repositorio

```text
├── capturas/
│   ├── registro.png     # Captura de pantalla: prueba exitosa de POST /registro
│   ├── login.png        # Captura de pantalla: prueba exitosa de POST /login
│   └── tareas.png       # Captura de pantalla: vista web GET /tareas
├── servidor.py          # API REST Flask con endpoints y lógica SQLite
├── cliente.py           # Cliente interactivo de consola
├── index.html           # Documentación visual servida vía GitHub Pages
├── README.md            # Guía de instalación, ejecución y respuestas conceptuales
└── tareas.db            # Base de datos SQLite (se autogenera al iniciar servidor.py)

Instalación y Requisitos Previos
Asegúrate de tener instalado Python 3.8+.

Instala las dependencias necesarias ejecutando en tu terminal:

Bash
pip install Flask requests flask-cors
(Nota: sqlite3 y werkzeug.security forman parte de la biblioteca estándar de Python y de las dependencias nativas de Flask).

Instrucciones de Ejecución
1. Iniciar el Servidor API
Abre una terminal en la raíz del proyecto y ejecuta:

Bash
python servidor.py
El script inicializará la base de datos tareas.db de forma automática si no existe.

El servicio quedará escuchando en http://localhost:5000.

2. Ejecutar el Cliente de Consola
En una segunda terminal, corre:

Bash
python cliente.py
Selecciona las opciones del menú numérico para:

Registrar un usuario (POST /registro).

Iniciar sesión (POST /login).

Comprobar la respuesta del servicio web (GET /tareas).

Respuestas Conceptuales
1. ¿Por qué hashear contraseñas?
Irreversibilidad (Unidireccionalidad): Un algoritmo criptográfico de hash convierte una clave en texto plano en una cadena alfanumérica de longitud fija imposible de revertir matemáticamente.

Mitigación frente a fugas de datos: Si la base de datos tareas.db sufre un acceso no autorizado o filtración, los atacantes solo obtienen cadenas de hashes inutilizables y no las contraseñas reales.

Protección contra ataques por Rainbow Tables: Al implementar funciones de hasheo con salt automático (como PBKDF2 en werkzeug.security), dos contraseñas idénticas producen hashes distintos, invalidando ataques basados en diccionarios precomputados.

2. Ventajas de usar SQLite en este proyecto
Serverless (Sin Servidor): No requiere instalar, configurar ni mantener un proceso o servicio de fondo dedicado (como PostgreSQL o MySQL).

Portabilidad: Toda la base de datos (tablas, índices y registros) reside en un único archivo (tareas.db), permitiendo trasladar, clonar o respaldar el proyecto sin configuraciones de red adicionales.

Librería nativa: Se integra mediante el módulo estándar sqlite3 de Python, eliminando la necesidad de controladores externos y agilizando las pruebas locales y académicas.

Visualización en GitHub Pages
La documentación del proyecto, junto con las evidencias de funcionamiento y capturas de terminal, está publicada en GitHub Pages a través del archivo