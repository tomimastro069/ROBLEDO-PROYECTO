## 1. AGENTS.md Realignment (Tooling)

- [x] 1.1 In `docs/AGENTS.md`, rename the skill `fastapi-python` to `python-fastapi-development`.
- [x] 1.2 In `docs/AGENTS.md`, rename the skill `postgres` to `natural-language-postgres`.
- [x] 1.3 In `docs/AGENTS.md`, rename the skill `frontend-design` to `tailwind-design-system` and `dashboard-crud-page`.
- [x] 1.4 In `docs/AGENTS.md`, remove references to `documentation-writer` and `commit-changes-reporter`.
- [x] 1.5 In `docs/AGENTS.md`, update the `MCPs Configurados` section to list `context7`, `engram`, and `filesystem` instead of `devdocs-mcp`.

## 2. AGENTS.md Realignment (Architecture & Code Reality)

- [x] 2.1 In `docs/AGENTS.md`, replace the requirement for "TanStack Form" with a rule stating that forms must use native React state (Controlled Components) and existing hooks like `useFormModal`.
- [x] 2.2 In `docs/AGENTS.md`, update the backend directory tree to reflect the exact physical Spanglish names (`orders/`, `products/`, `categories/`, `app/users/`).
- [x] 2.3 In `docs/AGENTS.md`, update the backend architectural rules to clarify that `core` is located at `backend/app/core/`, modifying any import examples accordingly.
- [x] 2.4 In `docs/AGENTS.md`, update the Frontend FSD rule to explicitly include the `Widgets` layer (`Pages → Widgets → Features → Entities → Shared`).
- [x] 2.5 In `docs/AGENTS.md`, rewrite the Axios rule to remove "refresh automático" and state clearly that 401 errors result in `clearAuth()` and a redirect to login.

## 3. Frontend Dependencies

- [x] 3.1 Run `npm install recharts` in the `frontend` directory.
- [x] 3.2 Verify `frontend/package.json` now includes `recharts`.

## 4. README Refactoring

- [x] 4.1 Replace the `backend/README.md` contents with a streamlined entrypoint that links to `docs/AGENTS.md` and `docs/Integrador.txt` for architectural rules.
- [x] 4.2 Replace the `frontend/README.md` contents with a streamlined entrypoint that links to `docs/AGENTS.md` and `docs/Integrador.txt` for FSD architecture details.