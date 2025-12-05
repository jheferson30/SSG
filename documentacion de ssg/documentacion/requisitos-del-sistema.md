---
title: "Requisitos del Sistema y Dependencias — SSG (Sistema de Seguridad para Gym)"
version: "v1.0"
date: "2025-11-08"
company: "GYM WORK"
project: "API del Sistema de seguridad de Gimnasio"
format: "Markdown"
---

# Plataformas Soportadas

- **Sistemas Operativos:** Windows 10/11 (recomendado), macOS 13+.  
- **Navegadores Compatibles:** Google Chrome, Microsoft Edge, Mozilla Firefox.  
- **Servidor Web:** Local o remoto con soporte para Flask (Python) y MongoDB.

# Runtimes y Lenguajes

- **Python:** `>= 3.11` (requerido para ejecutar la API con Flask).  
- **JavaScript (Frontend):** para la interfaz visual y conexión con la API.  
- **HTML5 / CSS3:** para estructura y diseño del front-end.  

# Bases de Datos

- **MongoDB:** base de datos principal para gestionar usuarios, entrenadores, sesiones y pagos.  
- **Compass (opcional):** herramienta visual para administrar colecciones y registros.

# Dependencias Externas
 
- **Servicio de email:** SMTP (por ejemplo Gmail o SendGrid) para confirmaciones y notificaciones. "proximo" 
- **Generación de PDF:** `fpdf` (Python) para emitir recibos o facturas.  
- **Framework principal:** Flask (para la API y endpoints del sistema).

# Recursos Mínimos del Servidor o PC

| Recurso | Mínimo | Recomendado |
|----------|---------|-------------|
| CPU | 2 núcleos | 4 núcleos |
| RAM | 4 GB | 8 GB |
| Almacenamiento | 10 GB libres | 20 GB libres |
| Resolución de pantalla | 1366x768 | 1920x1080 |

# Puertos y Red

- **Puerto principal del servidor Flask:** `5000`  
- **Puerto de MongoDB:** `27017`  
- **Soporte para CORS:** habilitado para permitir acceso desde el frontend.  
- **Seguridad:** se recomienda usar HTTPS en entornos productivos.  

# Observabilidad y Monitoreo

- **Logs:** generados desde Flask con control de errores HTTP.  
- **Métricas opcionales:** seguimiento de usuarios, pagos y sesiones.  
- **Respaldo de base de datos:** mediante exportaciones (`mongodump` o backups automáticos).  

# Notas Adicionales

- Antes de ejecutar el sistema, verificar que Python y MongoDB estén correctamente instalados.  
- En entornos de producción, se recomienda configurar variables de entorno seguras (`.env`).  
- Para generar recibos PDF, asegúrate de tener instalada la librería `fpdf`.  
