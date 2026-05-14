# Food Store — Frontend

## Visión General
Food Store es un sistema de comercio electrónico diseñado para la venta de productos alimenticios. Esta interfaz de usuario (frontend) proporciona la plataforma para que los clientes exploren el catálogo, gestionen su carrito y realicen compras de forma intuitiva. Además, ofrece interfaces especializadas para la administración: gestión de inventarios, procesamiento de pedidos y visualización de métricas (diseñado para perfiles Admin, Gestor de Stock y Gestor de Pedidos).

## Stack Tecnológico
El frontend sigue la arquitectura **Feature-Sliced Design (FSD)**, separando estrictamente el estado del servidor y del cliente, y está construido con:
- **React + TypeScript**: Base de la aplicación para un desarrollo robusto y tipado.
- **Vite**: Bundler y entorno de desarrollo ultra rápido.
- **Zustand**: Gestión del estado puramente del cliente (carrito, sesión persistida en localStorage, UI).
- **TanStack Query**: Gestión y sincronización del estado del servidor (caching, fetching asíncrono).
- **Tailwind CSS**: Sistema de estilos basado en utilidades y diseño responsivo.
- **MercadoPago.js**: Tokenización segura de tarjetas en el cliente (cumplimiento PCI DSS SAQ-A).

---

## 🤖 Desarrollo Guiado por IA (Metodología)

Este proyecto no se construyó bajo el paradigma tradicional de escritura manual de código, sino que está desarrollado utilizando **Inteligencia Artificial** bajo la metodología **SDD (Spec-Driven Development)** mediante herramientas de orquestación (`opsx`).

Todo el ciclo de vida del código está estructurado en flujos guiados:
1. **Explore**: Investigación profunda y diseño arquitectónico del problema.
2. **Propose**: Definición explícita de intención, alcance y diseño de los cambios requeridos.
3. **Apply**: Implementación guiada, atómica y trazable de las tareas definidas.
4. **Archive**: Cierre del ciclo y persistencia del cambio en el historial del proyecto.

### Ecosistema IA del Repositorio
Para que este desarrollo autónomo y cooperativo sea posible, el repositorio hace uso de un entorno específico de persistencia y configuración:
- **`.claude` / `.opencode`**: Contienen las configuraciones, skills e instrucciones del sistema de los agentes orquestadores.
- **`engram`**: Motor de memoria persistente que la IA consulta para recuperar el contexto entre sesiones, evitando pérdida de información y garantizando decisiones coherentes a lo largo del tiempo.
- **`openspec`**: Directorio donde residen absolutamente todas las especificaciones (`specs`) y el historial completo de cambios (`changes`) archivados. Es la fuente de la verdad para el ciclo de vida del desarrollo.
