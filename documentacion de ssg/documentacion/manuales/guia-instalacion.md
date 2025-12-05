---
title: "Guía de Instalación y Configuración — GymWork API"
version: "v1.0"
date: "2025-11-08"
company: "GYM WORK"
project: "Instalación del Sistema de Gestión de Clientes"
format: "Markdown/PDF"
---

# 🎯 Objetivo

Proveer pasos claros para instalar, configurar y ejecutar la API **GymWork**, un sistema de gestión de clientes para gimnasios desarrollado con **Flask (Python)** y **MongoDB**, que permite registrar usuarios, generar recibos PDF y mostrar estadísticas.

---

# 🧩 Requisitos previos

### Software
- **Sistema operativo:** Windows 10/11, Linux o macOS.  
- **Python:** Versión 3.10 o superior.  
- **MongoDB:** Instalado y ejecutándose localmente en `mongodb://localhost:27017/`.  
- **Git:** Para clonar el repositorio (opcional).  

### Dependencias
Se instalarán automáticamente desde el archivo `requirements.txt`, pero incluyen:
- Flask  
- pymongo  
- fpdf  

---

# ⚙️ Instalación paso a paso

```bash
# 1️⃣ Clonar el proyecto (si está en un repositorio)
git clone https://github.com/usuario/gymwork-api.git
cd gymwork-api

# 2️⃣ Crear y activar un entorno virtual
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/macOS
source venv/bin/activate

# 3️⃣ Instalar dependencias
pip install flask pymongo fpdf


# Configuración

```dotenv
mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client["gymwork"]

```

# Verificación

- Abre MongoDB Compass y verifica que exista la base gymwork y la colección clientes.

- Ingresa un cliente de prueba desde la interfaz web.

- Genera un recibo PDF para confirmar que la carpeta recibos/ se crea correctamente.

- Comprueba que los clientes próximos a vencer aparezcan en la sección correspondiente.

# Despliegue (opcional)

```yaml
python app.py

// Luego, abre tu navegador y accede a

http://127.0.0.1:5000/

```

# Troubleshooting

| Problema                                     | Posible causa                      | Solución                                        |
| -------------------------------------------- | ---------------------------------- | ----------------------------------------------- |
| `pymongo.errors.ServerSelectionTimeoutError` | MongoDB no está iniciado           | Inicia MongoDB con `mongod` o verifica Compass. |
| `ModuleNotFoundError: flask`                 | Falta instalar dependencias        | Ejecuta `pip install -r requirements.txt`.      |
| Archivos PDF no se generan                   | Falta carpeta `recibos/`           | Crea manualmente la carpeta o revisa permisos.  |
| La web no carga                              | Puerto ocupado o error de sintaxis | Cambia el puerto o revisa el log del servidor.  |
