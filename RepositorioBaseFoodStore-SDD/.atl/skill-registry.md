# Skill Registry

Generated: 24 Apr 2026  
Project: repositoriobasefoodstore-sdd  
Scope: SDD workflow + domain-specific assistance

## Available Skills

### OpenSpec Skills (Project-level)

These skills support the Spec-Driven Development workflow and are installed in `.agent/skills/` and `.agents/skills/`:

| Skill | Triggers | Purpose |
|-------|----------|---------|
| **openspec-explore** | `/openspec:explore <topic>` | Think through ideas, investigate problems, clarify requirements before committing to a change |
| **openspec-propose** | `/openspec:propose <description>` | Generate complete proposal (intent, scope, approach) with specs and tasks in one step |
| **openspec-apply-change** | `/openspec:apply` | Implement tasks from a change, write actual code following specs |
| **openspec-archive-change** | `/openspec:archive` | Finalize and archive a change after implementation is complete |
| **find-skills** | "how do I...", "find a skill..." | Discover and install agent skills for extended capabilities |

### System Skills (Global)

These are available system-wide from `~/.config/opencode/skills/`:

| Skill | Triggers | Purpose |
|-------|----------|---------|
| **sdd-init** | `sdd init` | Initialize SDD context — detect stack, conventions, testing (this phase) |
| **sdd-onboard** | orchestrator launch | Guided walkthrough of full SDD cycle using real codebase |
| **sdd-explore** | orchestrator launch | Explore ideas before committing to a change |
| **sdd-propose** | orchestrator launch | Create change proposal with intent, scope, approach |
| **sdd-spec** | orchestrator launch | Write specifications with requirements and scenarios |
| **sdd-design** | orchestrator launch | Create technical design with architecture decisions |
| **sdd-tasks** | orchestrator launch | Break down change into implementation task checklist |
| **sdd-apply** | orchestrator launch | Implement tasks from change following specs and design |
| **sdd-verify** | orchestrator launch | Validate implementation matches specs, design, tasks |
| **sdd-archive** | orchestrator launch | Sync delta specs and archive completed change |
| **go-testing** | Go tests, Bubbletea TUI | Go testing patterns and Bubbletea TUI testing (not applicable) |
| **skill-creator** | Create new AI skills | Create and document new agent skills following spec |
| **skill-registry** | `update skills`, `skill registry` | Create or update skill registry for project |
| **branch-pr** | Create PR, prepare review | PR creation workflow following issue-first enforcement |
| **issue-creation** | Create GitHub issue, report bug | Issue creation following issue-first enforcement |
| **judgment-day** | `judgment day`, `dual review` | Parallel adversarial review protocol with two judges |

## Project Configuration

### Persistence Mode
- **Active**: `openspec` (file-based, git-friendly)
- **Location**: `openspec/` folder (config.yaml, specs/, changes/, archive/)
- **Also Available**: Engram (persistent memory across sessions) for context

### Strict TDD Mode
- **Status**: ❌ Disabled
- **Reason**: Test infrastructure not yet scaffolded (backend/frontend templates not created)
- **Enable After**: Bootstrap backend/frontend with pytest (backend) and vitest (frontend)
- **Re-run**: `/sdd-init` to auto-detect test runner and re-enable Strict TDD

### Technology Stack

**Backend**:
- Framework: FastAPI (Python 3.11+)
- Database: PostgreSQL 15+ with Alembic migrations
- ORM: SQLModel (combines SQLAlchemy + Pydantic)
- Testing (recommended): pytest + pytest-asyncio

**Frontend**:
- Framework: React + TypeScript
- Bundler: Vite
- State: TanStack Query (server) + Zustand (client)
- Forms: TanStack Form
- Testing (recommended): Vitest + @testing-library/react

### Domain Knowledge

**System Actors**:
1. Cliente — End user, shopping
2. Administrador — Full system control
3. Gestor de Stock — Inventory management
4. Gestor de Pedidos — Order workflow
5. Sistema — Automated webhooks (MercadoPago IPN)

**Key Features**:
- RBAC authorization
- Hierarchical product categories
- Order FSM with state transitions
- MercadoPago payment integration (webhooks + IPN)
- Ingredient tracking + allergen identification
- Full order audit trail
- Admin metrics dashboard

**Requirements Documentation**: `docs/` folder (649+ lines)
- `docs/Descripcion.txt` — System overview, actors, stack
- `docs/Integrador.txt` — Architecture, ERD, patterns
- `docs/Historias_de_usuario.txt` — US-000 to US-076 with AC

## Recommended Workflow

1. **Explore** (`/openspec:explore`) — Clarify ideas around a feature
2. **Propose** (`/openspec:propose`) — Generate proposal + design + tasks
3. **Apply** (`/openspec:apply`) — Implement tasks incrementally
4. **Archive** (`/openspec:archive`) — Finalize and close the change

**Use Judgment Day** (`/judgment-day`) for critical changes requiring dual review.

## Next Steps

- [ ] Scaffold backend: Create `requirements.txt` with FastAPI, SQLModel, pytest
- [ ] Scaffold frontend: Create `package.json` with React, TypeScript, vitest
- [ ] Re-run `/sdd-init` to detect test infrastructure
- [ ] Begin with US-000 (setup infrastructure) using `/openspec:propose`
- [ ] Enable Strict TDD once test frameworks are detected

---

*For skill installation or questions, use `/find-skills`.*
