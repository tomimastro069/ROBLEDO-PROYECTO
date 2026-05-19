## Why

The agent orchestration rules in `docs/AGENTS.md` do not match the actual state of the repository. Skill names are misaligned with `.agents/skills`, documented frontend dependencies are missing, and MCP configuration is outdated. Furthermore, the structural documentation in `docs/AGENTS.md` hallucinated ideal states rather than reflecting the real code: it assumes Spanish directory names when the codebase uses Spanglish (`orders/`, `products/`), assumes `core` is at the root instead of `app/core/`, hallucinated an automatic JWT refresh feature that doesn't exist, and omitted the `widgets` layer from the frontend FSD rules. This incongruence prevents agents from successfully resolving paths and executing tasks consistently.

## What Changes

- Update `docs/AGENTS.md` to map to existing skills (`python-fastapi-development`, `natural-language-postgres`, `tailwind-design-system`, `dashboard-crud-page`, `betterauth-fastapi-jwt-bridge`).
- Remove references to non-existent skills (`documentation-writer`, `commit-changes-reporter`) from `docs/AGENTS.md`.
- Update the MCP configuration reference in `docs/AGENTS.md` from `devdocs-mcp` to `context7`, `engram`, and `filesystem`.
- Add `recharts` to the frontend `package.json` to enable dashboard charts.
- Update `docs/AGENTS.md` to explicitly state that frontend forms use native React state (Controlled Components) and custom hooks like `useFormModal`, removing the mandate for TanStack Form.
- **NEW**: Correct the backend directory tree in `docs/AGENTS.md` to reflect reality (`orders/`, `products/`, `categories/`, `app/users/`, `app/core/`).
- **NEW**: Correct the frontend FSD flow in `docs/AGENTS.md` to include `Widgets` (`Pages → Widgets → Features → Entities → Shared`).
- **NEW**: Correct the Axios networking rules in `docs/AGENTS.md` to state that 401s clear auth and redirect to login, rather than claiming "automatic refresh".
- Refactor `backend/README.md` and `frontend/README.md` to serve as simple entrypoints that explicitly defer architectural and pattern documentation to `docs/AGENTS.md`.

## Capabilities

### New Capabilities
- `agent-tooling-alignment`: Fixes documentation and dependency incongruences to restore full alignment between the stated AI workflows and the repository reality, strictly honoring existing code patterns over theoretical ideals.

### Modified Capabilities
- 

## Impact

- **Affected Files**: `docs/AGENTS.md`, `backend/README.md`, `frontend/README.md`, `frontend/package.json`.
- **Systems**: AI agent workflows, orchestration, and skill resolution. No production application logic is affected. The documentation is downgraded/adjusted to match the actual implemented architecture (Spanglish, missing refresh, specific directory locations).