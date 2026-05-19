## Context

The repository base configuration (`docs/AGENTS.md`) serves as the strict source of truth for architecture and agent behavior. However, it currently diverges from the codebase in two ways: Tooling/Dependencies (missing skills, uninstalled libraries, wrong MCPs) and Architectural Reality (incorrect directory structures, omitted layers, hallucinated features). The code is already implemented, so the documentation MUST be bent to fit the code, regardless of whether the code's approach (Spanglish, lacking token refresh) is considered "correct" or not.

## Goals / Non-Goals

**Goals:**
- Align `docs/AGENTS.md` skill definitions with the folders in `.agents/skills`.
- Ensure MCP server documentation accurately reflects `opencode.json`.
- Fulfill frontend charting requirements by installing `recharts`.
- Update `docs/AGENTS.md` to mandate native React forms over TanStack Form.
- **Adjust `docs/AGENTS.md` to perfectly map the real backend structure** (`orders`, `products`, `app/core/`, etc.).
- **Adjust `docs/AGENTS.md` to perfectly map the real frontend structure** (insert `Widgets` into the FSD flow).
- **Correct documentation of existing functional features** (e.g., remove mentions of automatic token refresh).

**Non-Goals:**
- Changing backend or frontend application code or business logic (e.g., we will NOT implement token refresh, nor will we rename the backend folders to Spanish).

## Decisions

**1. Documentation Bows to Code**
- *Decision*: We will update `docs/AGENTS.md` to reflect the Spanglish directory names (`orders/` instead of `pedidos/`, `products/` instead of `productos/`), the correct path for `app/core/`, and the true behavior of the Axios interceptor (logout on 401).
- *Rationale*: The code is the ultimate source of truth. If the documentation describes an ideal state that doesn't exist, agents will hallucinate, look in the wrong directories, or write code for non-existent layers. 

**2. Pragmatic Form Architecture**
- *Decision*: We will NOT install or migrate to TanStack Form. Instead, we will update `docs/AGENTS.md` to mandate the use of native React state.
- *Rationale*: The current forms are already built, tested, and working perfectly.

**3. Frontend FSD Reality Check**
- *Decision*: Add the `Widgets` layer to the strict FSD flow rule in `docs/AGENTS.md`.
- *Rationale*: `frontend/src/widgets/` physically exists. If the orchestrator rules omit it, agents will be penalized or blocked from writing code there.

## Risks / Trade-offs

- **Risk**: Adding `recharts` could cause version conflicts.
  - *Mitigation*: We will use standard npm installs and ensure they align with React 18.