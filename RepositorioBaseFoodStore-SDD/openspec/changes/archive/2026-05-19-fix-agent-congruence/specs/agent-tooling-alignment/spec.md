## ADDED Requirements

### Requirement: Documentation reflects actual skill paths
The `docs/AGENTS.md` file MUST list only the agent skills that physically exist in the `.agents/skills/` directory. If a skill does not exist, it MUST be removed. If it has a different name, the documentation MUST reflect the exact folder name.

#### Scenario: Agent tries to load a skill
- **GIVEN** an agent orchestration workflow triggers skill loading
- **WHEN** the context requires a skill like FastAPI Python development
- **THEN** it resolves successfully because `docs/AGENTS.md` points to `python-fastapi-development`

### Requirement: Frontend forms use native React state
The documentation in `docs/AGENTS.md` MUST explicitly state that forms are built using native React state (Controlled Components) and custom hooks, and MUST NOT mandate TanStack Form.

### Requirement: Backend structure documentation matches reality
The `docs/AGENTS.md` file MUST accurately map the physical backend directory structure, using the existing Spanglish folder names (e.g., `orders/`, `products/`, `categories/`) and noting that `core/` is located at `backend/app/core/`.

#### Scenario: Agent creates a new order endpoint
- **GIVEN** an agent needs to add logic to orders
- **WHEN** it reads the structural guidelines in `docs/AGENTS.md`
- **THEN** it correctly targets `backend/orders/` instead of `backend/pedidos/`

### Requirement: Frontend FSD rules include Widgets
The documentation in `docs/AGENTS.md` MUST include the `Widgets` layer in the FSD flow rule (`Pages → Widgets → Features → Entities → Shared`).

### Requirement: Axios documentation reflects actual implementation
The `docs/AGENTS.md` file MUST state that the Axios interceptor handles 401s by clearing auth and redirecting to login, and MUST NOT claim that it performs automatic token refresh.

#### Scenario: Agent builds an API interaction
- **GIVEN** an agent is writing a new API call
- **WHEN** the agent reviews networking rules
- **THEN** it understands that 401s result in a hard logout, matching the actual `axiosInstance.ts` code

### Requirement: MCP configuration references actual installed servers
The `docs/AGENTS.md` file MUST accurately reflect the global `opencode.json` MCP server list (Context7, Engram, Filesystem).

### Requirement: README files delegate architecture to docs
The `backend/README.md` and `frontend/README.md` MUST serve as quick-start entrypoints only, and MUST delegate architectural definitions to `docs/AGENTS.md`.