# FoodStore Backend Structure

- **app/core/**: Core config, authentication, database utilities
  - `config.py`: Loads environment and settings
  - `database.py`: SQLModel integration
  - `auth.py`: JWT authentication
- **app/users/**: User-related APIs and logic (to be expanded)
- **main.py**: Entrypoint

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Setup your `.env` based on `.env.example`
3. Run development server:
   ```bash
   uvicorn main:app --reload
   ```
4. Access docs at:
   - OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Automatic Database Creation
- On startup, tables are auto-generated using SQLModel (see `core/database.py`).
