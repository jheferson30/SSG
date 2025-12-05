---
title: "publicaciones — SSG (Sistema de Seguridad para Gym)"
version: "v1.0"
date: "2025-11-08"
company: "GYM WORK"
project: "Manual Técnico — API del Sistema de Gimnasio"
format: "Markdown"
---

# Objetivo
Establecer el proceso para generar salidas en formatos estándar (Markdown y PDF) y publicar la documentación del proyecto SSG en los repositorios designados o sitios de presentación.


# Generación de PDFs

```bash
# Instalar la herramienta
npm i -g md-to-pdf

# Generar los PDFs de tus manuales
md-to-pdf manuales/manual-tecnico.md --output pdf/manual-tecnico.pdf
md-to-pdf manuales/manual-de-usuario.md --output pdf/manual-de-usuario.pdf
md-to-pdf requisitos-del-sistema.md --output pdf/requisitos-del-sistema.pdf
md-to-pdf README.md --output pdf/README.pdf

```

# Publicación

- Guardar los archivos PDF generados en la carpeta /pdf/ del proyecto.

- Subirlos a la carpeta de entregas o compartirlos como documentación oficial del SSG.


# Control de calidad

- Verificar que los enlaces entre archivos funcionen.
- Revisar que las fechas, versiones y nombres de empresa estén actualizados.
- Asegurar que todos los archivos `.md` tengan portada (front matter) y título.
