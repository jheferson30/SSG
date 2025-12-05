---
title: "Plantilla de Auditoría de Documentación— SSG (Sistema de Seguridad para Gym)"
version: "v1.0"
date: "2025-11-08"
company: "GYM WORK"
project: "Plantilla de Auditoría de Documentación — API del Sistema de Gimnasio"
format: "Markdown"
---

# Objetivo

- Analizar y organizar la carpeta de documentación del proyecto **SSG (Smart System Gym)**, comprendiendo su estructura, manuales, diagramas, metadatos y relaciones entre archivos, con el fin de garantizar coherencia y detectar faltantes.

# Alcance

- Solo la ruta `<DOC_ROOT>` y sus subcarpetas. Usa rutas relativas y especifica el SO si es relevante.

# Parámetros (variables)

- `DOC_ROOT`: ruta absoluta de la carpeta de documentación.
- `DEPTH`: niveles de árbol a listar (sugerido: 3–5).
- `FILE_TYPES`: filtros opcionales por tipo (Markdown/Mermaid/SVG/JSON/otro).

# Estructura de Directorios (esperada)

# Estructura Sugerida de Carpeta

- `documentation/`
  - `README.md` (mapa y accesos rápidos al SSG)
  - `assets/`
    - `logo.svg`
    - `screenshots/` (capturas del sistema de acceso y gestión del gimnasio)
  - `manuales/`
    - `manual-de-usuario/index.md`
    - `manual-tecnico.md`
  - `capacitacion_aceptacion/`
    - `plan.md` (marco de capacitación para administradores y recepcionistas)
    - `plantillas/` (cronograma, casos de prueba, criterios de aceptación)
  - `diagrams/`
    - `Diagrama-de-Componentes-Arquitectura.png`
    - `Diagrama-de-Secuencia.png`
    - `diagrama-de-entidades.png`
 

# Inventario de Archivos con Metadatos

- Para cada archivo incluir:
  - `Nombre exacto`
  - `Extensión`
  - `Tipo` (Markdown/Mermaid/png/JSON/otro)
  - `Tamaño` (KB y MB)
  - `Fecha de última modificación`
  - `Ruta relativa`
- Señalar pares esperados `*.mmd` ↔ `*.png` en `diagrams/` y su correspondencia.

# Resumen de Contenidos por Documento

- Describe temas principales sin pegar el texto completo.
- Enumera secciones/capítulos clave y su jerarquía.
- Menciona elementos visuales destacados: diagramas y capturas (`assets/screenshots`) y su propósito.

# Patrones y Características Comunes

- Idioma predominante, formato (Markdown), numeración de secciones.
- Uso de alt text y consistencia de enlaces relativos.
- Presencia de front matter (title, version, date, company, project, format).
- Convenciones de nombres y ubicación de recursos.

# Relaciones entre Documentos

- Explica referencias cruzadas (p. ej., plan general ↔ plantillas ↔ ejemplos, manual de usuario ↔ assets/screenshots ↔ diagrams).
- Identifica duplicidades, complementarios y puntos de entrada (README).

# Diagramas (Mermaid)

- Lista diagramas presentes por tipo: arquitectura, ER, casos de uso, secuencia, despliegue, estados.
- Indica faltantes de pares `*.mmd`/`*.png`, obsolescencias o enlaces rotos.
- Sugiere diagramas adicionales según el dominio (ver “Plantillas de Diagramas”).

# Metadatos Relevantes

- Registra front matter y su consistencia: `title`, `version`, `date`, `company`, `project`, `format`.
- Observa timestamps por bloque para identificar cambios recientes.

# Inconsistencias o Faltantes

- Duplicidades, metadatos ausentes, referencias no existentes, falta de alt text, diagramas sin render o sin par.
- Recomendaciones de homogeneización (nombres, rutas, front matter).

# Salida Esperada

- Informe estructurado que permita: reconstruir la jerarquía, entender alcance y propósito, identificar documentos clave y listar acciones correctivas/recomendaciones.

---

# Estructura Sugerida de Carpeta

- `documentation/` (o `<DOC_ROOT>`)
  - `README.md` (mapa y accesos rápidos)
  - `assets/`
    - `logo.svg`
    - `screenshots/` (capturas con alt text)
  - `manuales/`
    - `manual-de-usuario/index.md`
    - `manual-tecnico.md`
  - `capacitacion_aceptacion/`
    - `plan.md` (marco general)
    - `plan-capacitacion-detallado.md` (9 elementos)
    - `plantillas/` (cronograma, casos de prueba, criterios, incidencias, RACI, protocolo, acta)
    - `ejemplos/` (cronograma, 10 casos, datos de prueba)
  - `diagrams/`
    - `componentes-arquitectura.mmd` + `componentes-arquitectura.svg`
    - `modelo-er.mmd` + `modelo-er.svg`
    - `uml-casos-uso.mmd` + `uml-casos-uso.svg`
    - `checkout-sequence.mmd` + `checkout-sequence.svg`
    - `deployment.mmd` + `deployment.svg`
  - `config/` (opcional, p. ej., `puppeteer-config.json`)

---

# Plantillas de Diagramas (Mermaid)

## Arquitectura por Componentes (`componentes-arquitectura.mmd`)

```
flowchart LR
  Browser[Usuario] --> Frontend[Frontend SPA]
  Frontend --> API[API Backend]
  API --> DB[(Base de Datos)]
  API --> Payments[Pasarela de Pago]
  API --> Storage[Almacenamiento]
```

## Modelo Entidad‑Relación (`modelo-er.mmd`)

```
erDiagram
  USER ||--o{ ORDER : places
  ORDER }o--o{ PRODUCT : contains
  USER {
    string id
    string email
    string role
  }
```

## Casos de Uso (`uml-casos-uso.mmd`)

```
flowchart LR
  actor(Usuario)
  actor --> (Iniciar sesión)
  actor --> (Buscar productos)
  actor --> (Gestionar carrito)
  actor --> (Pagar pedido)
```

## Secuencia de Checkout (`checkout-sequence.mmd`)

```
sequenceDiagram
  participant U as Usuario
  participant FE as Frontend
  participant BE as Backend
  participant PG as Pago
  U->>FE: Confirmar carrito
  FE->>BE: Crear orden
  BE->>PG: Procesar pago
  PG-->>BE: Resultado
  BE-->>FE: Confirmación
```

## Despliegue (`deployment.mmd`)

```
flowchart TB
  subgraph Cloud
    LB[Load Balancer] --> FE[Frontend (CDN)]
    LB --> BE[Backend Service]
    BE --> DB[(DB)]
    BE --> Cache[(Cache)]
  end
```

---

# Front Matter Estándar

```
---
title: "<Título del documento>"
version: "v1.0"
date: "<YYYY-MM-DD>"
company: "<Empresa>"
project: "<Proyecto>"
format: "Markdown"
---
```

---

# Checklist de Calidad

- Formato: todo en Markdown (si aplicas política “NADA DE PDF O WORD”).
- Accesibilidad: cada imagen con alt text descriptivo y título.
- Coherencia: enlaces relativos correctos; pares `.mmd`/`.svg` presentes; nombres consistentes.
- Metadatos: front matter uniforme en manuales y planes.
- Diagramas: renderizados actualizados; evita incrustar `.mmd` en producción si no hay render automático.
- Versionado: usa `version` y `date` coherentes; registra cambios en `README.md`.
- Duplicidades: consolidar documentos solapados.

---

# Uso del Prompt (Pasos)

1. Define `DOC_ROOT`, `DEPTH` y `FILE_TYPES` si deseas filtrar.
2. Lista estructura de directorios y genera inventario con metadatos.
3. Resume contenidos y señala elementos visuales (diagrams/screenshots).
4. Identifica patrones, relaciones y posibles inconsistencias.
5. Produce recomendaciones accionables y mapa de documentos clave.

---

# Notas

- Este documento es una plantilla general; ajusta módulos/diagramas según el dominio.
- Mantén los pares Mermaid/SVG actualizados para evitar fallos de render.