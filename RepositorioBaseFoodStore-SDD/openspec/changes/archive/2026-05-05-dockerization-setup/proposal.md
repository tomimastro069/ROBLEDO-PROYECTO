# Proposal: Dockerization Setup

## Intent
Standardize the development and deployment environment using Docker. This ensures consistency across different machines, simplifies dependency management (especially for PostgreSQL), and provides a production-like environment for development.

## Scope

### In Scope
- `backend/Dockerfile`: Multi-stage build for FastAPI application.
- `frontend/Dockerfile`: Multi-stage build for Vite + React application.
- `docker-compose.yml`: Orchestration for backend, frontend, and PostgreSQL services.
- `.env.docker`: Specific environment variables for the containerized environment.
- Root `Makefile` or scripts for common Docker commands (optional).

### Out of Scope
- CI/CD pipeline integration (GitHub Actions, etc.).
- Production server provisioning (Terraform, Ansible).
- Kubernetes manifests.

## Capabilities

### New Capabilities
- `infrastructure-docker`: Provides the ability to run the entire stack using a single command (`docker-compose up`).

### Modified Capabilities
- None

## Approach
- Use **multi-stage builds** to keep image sizes small.
- Use **official lightweight images** (e.g., `python:3.11-slim` or `alpine`, `node:20-alpine`).
- Use **Docker volumes** for backend and frontend source code to enable hot-reloading during development.
- Configure a **dedicated network** in `docker-compose` for service-to-service communication.
- Use **PostgreSQL official image** with persistent volume for data.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `/` | New | `docker-compose.yml` and shared config. |
| `backend/` | New | `Dockerfile` and `.dockerignore`. |
| `frontend/` | New | `Dockerfile` and `.dockerignore`. |
| `.env` | Modified | Added/updated variables for DB connection via Docker service names. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Build time | Med | Use multi-stage builds and cache layers efficiently. |
| Port conflicts | Low | Allow port configuration via `.env`. |
| Image size | Low | Use slim/alpine base images. |

## Rollback Plan
- Delete the newly created Dockerfiles and `docker-compose.yml`.
- Revert any changes to `.env` files.
- The project remains runnable locally via `pip` and `npm` as before.

## Dependencies
- Docker and Docker Compose installed on the host machine.

## Success Criteria
- [ ] Backend service starts and is accessible at `localhost:8000`.
- [ ] Frontend service starts and is accessible at `localhost:5173`.
- [ ] Backend can successfully connect to the containerized PostgreSQL database.
- [ ] Changes in source code are reflected inside the containers (Hot-Reloading).
