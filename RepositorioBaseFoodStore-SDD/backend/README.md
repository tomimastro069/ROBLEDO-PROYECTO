# Food Store — Backend

## Setup & Development

Para instalar y ejecutar el entorno de desarrollo local del backend, asegúrate de tener Python 3.11+ instalado y usa un entorno virtual.

```bash
# 1. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de base de datos

# 4. Correr migraciones de base de datos
alembic upgrade head

# 5. Levantar el servidor
uvicorn main:app --reload
```

## Arquitectura y Convenciones

> **⚠️ IMPORTANTE:**
> Este proyecto sigue reglas arquitectónicas estrictas (Feature-First, Unit of Work, etc.) dictadas por un enfoque de desarrollo guiado por IA (Spec-Driven Development).
> 
> Para conocer las convenciones del código, las librerías a usar, y los patrones de desarrollo que debe seguir el equipo y los agentes, **por favor consulta la documentación central en:**
> - `docs/AGENTS.md` (Para arquitectura de código, convenciones y reglas de orquestación)
> - `docs/Integrador.txt` (Para especificaciones técnicas, FSM de pedidos y requerimientos de dominio)
