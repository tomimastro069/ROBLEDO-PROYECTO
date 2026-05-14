# Food Store — Backend

## Visión General
Este proyecto conforma el motor (backend) de la plataforma Food Store, un e-commerce de productos alimenticios. Expone una API REST moderna que gestiona un catálogo completo con categorías jerárquicas, autenticación y autorización estricta basada en roles (RBAC), y una máquina de estados finitos que asegura la integridad en el ciclo de vida de cada pedido. A su vez, se encarga del procesamiento de pagos mediante la integración con webhooks (IPN) de MercadoPago.

## Stack Tecnológico
La arquitectura sigue un enfoque **Feature-First** (vertical) y está estructurada en capas estrictas (Router → Service → Unit of Work → Repository → Model) para garantizar separación de responsabilidades.
- **FastAPI**: Framework web asíncrono, con validación automática y alto rendimiento.
- **Python 3.11+**: Lenguaje base del backend.
- **PostgreSQL**: Base de datos relacional para integridad de los datos.
- **SQLModel**: ORM que fusiona de forma nativa SQLAlchemy y Pydantic.
- **Alembic**: Herramienta de migraciones de esquema.
- **Patrones Clave**: Unit of Work (transacciones atómicas), Snapshot (inmutabilidad de pedidos), Soft Delete e Idempotencia de pagos.

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
