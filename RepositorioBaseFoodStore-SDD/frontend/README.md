# Food Store — Frontend

## Setup & Development

Para instalar y ejecutar el entorno de desarrollo local del frontend, asegúrate de tener Node.js instalado.

```bash
# 1. Instalar dependencias
npm install

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar el servidor de desarrollo
npm run dev

# 4. Construir para producción
npm run build
```

## Arquitectura y Convenciones

> **⚠️ IMPORTANTE:**
> Este proyecto sigue una arquitectura estricta (Feature-Sliced Design) dictada por un enfoque de desarrollo guiado por IA (Spec-Driven Development).
> 
> Para conocer la jerarquía de directorios permitida, las librerías a usar (Zustand, React nativo para formularios, Axios, Recharts), y los patrones de desarrollo que debe seguir el equipo y los agentes, **por favor consulta la documentación central en:**
> - `docs/AGENTS.md` (Para arquitectura FSD, convenciones frontend y reglas de orquestación)
> - `docs/Integrador.txt` (Para especificaciones técnicas y requerimientos de dominio)
