# Design: Monorepo Scaffolding Structure

## Overview
Set up a maintainable monorepo with clear project separation, enabling backend and frontend teams to collaborate while sharing config and tooling as appropriate.

## Directory Structure
```
repo-root/
  backend/
    app/                 # Feature-first modules (e.g., users, products)
      users/
      core/
    main.py              # FastAPI entrypoint
    requirements.txt     # Python dependencies
    .env.example         # Backend environment variables example
    README.md            # Backend specific docs

  frontend/
    public/              # Static files
    src/                 # Feature-slice (FSD)
      features/
        users/
        core/
      app/
        index.js         # Main React entry
    package.json         # Frontend dependencies
    .env.example         # Frontend environment variables example
    README.md            # Frontend specific docs

  .gitignore             # Ignores shared/stack artifacts
  README.md              # Monorepo & onboarding
```

## Backend (FastAPI, feature-first)
- All source code under `backend/app/`, organized by domain/feature.
- Entrypoint: `backend/main.py`, importing from app modules.
- Python dependencies in `backend/requirements.txt`.
- .env handling and example file for local overrides.

## Frontend (React, FSD)
- All source under `frontend/src/features/` and `frontend/src/app/`.
- Entrypoint: `frontend/src/app/index.js`.
- UI split by slices/domains.
- React setup can be extended for state management/routing.

## Shared Tools/Files
- `.gitignore` in root for Python, Node, OS-specific ignores.
- `README.md` in root: onboarding, architecture overview, dev instructions.
- Each app gets its own `.env.example` + README.md.

## Example Files
- `backend/main.py`: Minimal FastAPI app.
- `frontend/src/app/index.js`: Minimal React rendering entrypoint.

## Extensibility
- Structure allows scaling with new features in both apps.
- Additional shared packages or tooling can be added under a future `shared/`.
