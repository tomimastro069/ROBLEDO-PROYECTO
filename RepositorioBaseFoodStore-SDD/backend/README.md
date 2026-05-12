# FoodStore Backend Structure

- **app/core/**: Core config, authentication, database utilities
  - `config.py`: Loads environment and settings
  - `database.py`: SQLModel integration
  - `auth.py`: JWT authentication
- **app/users/**: User-related APIs and logic (to be expanded)
- **orders/**: Order management service (lifecycle, state machine, external orchestration)
- **main.py**: Entrypoint

## Integrations
- **RabbitMQ**: Used for publishing domain events (`OrderCreated`, `OrderSubmitted`, etc.)
- **Prometheus**: Metrics available for order creation and error rates.
- **External Services**: Integrated with Inventory, Catalog, and Payment services via HTTP clients.

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install email-validator prometheus_client aio_pika
   ```
2. Setup your `.env` with microservices URLs and RabbitMQ broker URL.
3. Run development server:
   ```bash
   uvicorn main:app --reload
   ```
4. Access docs at:
   - OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health Check: [http://localhost:8000/api/v1/orders/health](http://localhost:8000/api/v1/orders/health)

## Automatic Database Creation
- On startup, tables are auto-generated using SQLModel (see `core/database.py`).
