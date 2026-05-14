# Design: Monorepo Structural Rules and SDD History

## 1. Context
During the initial development and migration phases, several files were generated outside of their designated domain constraints. Frontend boilerplate code ended up in the project root, testing scratchpads were committed to version control, and manual changelogs were maintained parallel to our SDD process.

## 2. Architectural Decisions

### ADR 1: Strict Separation of Concerns (Monorepo)
No application code, package managers (`package.json`, `requirements.txt`), or testing frameworks (`pytest.ini`) are allowed in the project root. 
- All frontend code must reside in `/frontend`.
- All backend code must reside in `/backend`.
Any violation of this rule creates execution ambiguity for SDD agents and IDEs.

### ADR 2: Deprecation of Manual Changelogs
We are officially deprecating `CHANGELOG.md` and `docs/CHANGES.md`. 
Under the SDD methodology, the `openspec/changes/archive` directory serves as the immutable, single source of truth for all historical modifications. Maintaining a parallel, manual Markdown file is redundant and prone to desynchronization.

### ADR 3: Ephemeral Scratch Space
The `backend/scratch` directory and similar temporary folders are strictly ephemeral. Files placed here (such as endpoint testing scripts or markdown problem statements) should not be committed to the main branch once the implementation is successfully merged and verified.
