---
title: "Componente Backend — API GYMWORK"
version: "v1.0"
date: "2025-11-09"
project: "Sistema SSG / GYMWORK"
format: "Markdown"
---

# Objetivo
Proveer servicios backend para la gestión de usuarios, membresías y pagos del gimnasio, incluyendo la generación de recibos en PDF y control de vencimientos.

# Alcance
Aplica a las funciones del servidor Flask (Python) que interactúan con la base de datos MongoDB, gestionan el flujo de usuarios, planes, pagos y vencimientos.

---

## Descripción general del componente

- **Nombre oficial:** SSG GYMWORK
- **Propósito:** Gestionar la lógica del gimnasio (clientes, pagos, membresías, recibos PDF).
- **Responsabilidades:** CRUD de clientes, manejo de fechas de vencimiento, generación de recibos y alertas de usuarios próximos a vencer.
- **Posición en la arquitectura:** Backend del sistema (conecta frontend con MongoDB).
- **Estado y criticidad:** Stable / Critical.

```mermaid
flowchart LR
  UI[Frontend GYMWORK] --> API[Flask API]
  API --> DB[(MongoDB)]
  API --> PDF[Generador de Recibos]
  
  
  ```


## Requisitos previos

- Sistema operativo: Windows 10+ / Linux / macOS

- Python: ≥ 3.10

- MongoDB: ≥ 6.0

- Dependencias: Flask, PyMongo, FPDF

- Permisos: Lectura/escritura en clientes dentro de la BD gymwork.

- Variables de entorno:

    - FLASK_ENV=development

    - MONGO_URI=mongodb://localhost:27017/gymwork

## Instrucciones de instalación/configuración

- Clonar el proyecto

```bash
# Clonar el proyecto
git clone https://github.com/usuario/gymwork-api.git
cd gymwork-api
```

- Crear entorno virtual

```yaml
python -m venv .venv
.\.venv\Scripts\activate
```

- Instalar dependencias

```yaml

pip install flask pymongo fpdf
```

- Inicio:

```bash
python app.py
```

## Parámetros y opciones configurables

| Parámetro    | Tipo   | Default                      | Obligatorio | Descripción         |
| ------------ | ------ | ---------------------------- | ----------- | ------------------- |
| `MONGO_URI`  | string | `mongodb://localhost:27017/` | Sí          | Conexión a MongoDB  |
| `PORT`       | number | `5000`                       | No          | Puerto de ejecución |
| `SECRET_KEY` | string | `mi_clave_super_secreta_123` | Sí          | Clave interna Flask |

- **Ejemplo de archivo de entorno**:

   - Visualizar página principal

```bash
GET /inicio
```
  - Muestra lista de usuarios, días restantes y próximos vencimientos.

## Ejemplos de uso básico y avanzado

- Básico (Registrar cliente):

```bash
POST /agregar_cliente

```
- Campos:

  - cedula

  - nombre

  - telefono

  - fecha_inicio

  - fecha_fin

  - forma_pago

  - valor_pagar

- Avanzado (Generar recibo PDF):

```typescript
GET /recibo/<cedula>
```
- Devuelve un archivo PDF con los datos del cliente.

## Consideraciones de seguridad

- Consideraciones de seguridad

  - El archivo .env no debe subirse al repositorio.

  - Sanitizar todos los datos recibidos desde formularios.

  - Limitar acceso a rutas de administración.

  - Asegurar conexión con MongoDB (auth o localhost).

  - Proteger SECRET_KEY y posibles tokens futuros.



# Variantes por Tipo de Componente

## Backend API / Microservicio

Descripción general

- Nombre del componente: API Flask — Sistema de gestión de gimnasio (SSG)

- Propósito: Permitir el registro, control de usuarios, pagos y acceso mediante huella.

- Lenguaje y Framework: Python 3.13 + Flask

- Base de datos: MongoDB

### Endpoints

| Método | Ruta                     | Descripción                                       |
| ------ | ------------------------ | ------------------------------------------------- |
| `GET`  | `/`                      | Página principal o ruta de inicio                 |
| `GET`  | `/usuarios`              | Muestra los usuarios registrados                  |
| `POST` | `/agregar_usuario`       | Registra un nuevo usuario (recepcionista)         |
| `POST` | `/editar_usuario/<id>`   | Actualiza información de un usuario               |
| `POST` | `/eliminar_usuario/<id>` | Elimina un usuario                                |
| `GET`  | `/usuarios_por_vencer`   | Muestra usuarios con mensualidad próxima a vencer |
| `GET`  | `/generar_recibo/<id>`   | Genera un recibo PDF del pago                     |


Ejemplos de consumo (pruebas con cURL)

```bash
# Verificar que la API está activa
curl -sS http://localhost:5000/

# Ver usuarios registrados
curl -sS http://localhost:5000/usuarios

# Agregar un usuario
curl -sS -X POST http://localhost:5000/agregar_usuario \
     -H "Content-Type: application/json" \
     -d "{\"nombre\": \"Carlos Pérez\", \"cedula\": \"12345\", \"valor_pagar\": 50000, \"forma_pago\": \"efectivo\"}"

```

### Configuración y entorno

```yaml
server:
  port: 5000
  debug: true
  secret_key: "mi_clave_super_secreta_123"

database:
  engine: "MongoDB"
  host: "localhost"
  port: 27017
  name: "gimnasio"

security:
  cors: true
  auth_method: "credencial / huella digital"

```

### Base de Datos — MongoDB

Descripción general

 - Nombre de la base de datos: gimnasio

 - Tipo: No relacional (MongoDB)

 - Colecciones principales:

 - usuarios

 - pagos

 - entrenadores

```yaml
erDiagram
  USUARIO {
    string _id
    string nombre
    string cedula
    string telefono
    string forma_pago
    number valor_pagar
    date fecha_registro 
    }

  PAGO {
    string _id
    string id_usuario
    number valor
    date fecha_pago
    }

  ENTRENADOR {
    string _id
    string nombre
    string especialidad
  }

  USUARIO ||--o{ PAGO : realiza
  ENTRENADOR ||--o{ USUARIO : entrena

```

Conexión a la base de datos (en Flask)

```yaml
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["gimnasio"]

```


# Checklist de Calidad del Componente

- Title, versión y fecha actualizados
- Instrucciones de instalación verificadas
- Parámetros configurables documentados
- Ejemplos reales probados
- Seguridad y roles definidos
- Diagrama incluido


# Notas

- Mantén los pares Mermaid/SVG actualizados para evitar fallos de render.
- Esta guía busca ser técnica pero accesible; ajusta ejemplos al lenguaje del componente.