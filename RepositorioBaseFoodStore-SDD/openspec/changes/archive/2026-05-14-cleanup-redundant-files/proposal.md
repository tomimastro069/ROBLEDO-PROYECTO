# Proposal: Cleanup Redundant Files and Legacy Artifacts

## 1. Intent
The project repository has accumulated significant technical debt in the form of redundant tracking files, obsolete reports, and legacy frontend artifacts located in the wrong directories. 

The goal of this change is to strictly enforce the structural conventions of the SDD (Spec-Driven Development) monorepo architecture by removing all orphan code and outdated documentation.

## 2. Scope
This cleanup will target the following areas:
- **Root Directory Cleanup**: Removing the misplaced `src/` folder, `package.json`, and related testing configurations (`pytest.ini`) from the project root. These belong exclusively in the `/frontend` or `/backend` workspaces.
- **Manual Changelogs**: Deleting manual changelog files (`CHANGELOG.md`, `docs/CHANGES.md`) since our history is now managed natively through SDD artifacts in `openspec/changes`.
- **Obsolete Reports**: Removing old synchronization and gap analysis reports from `docs/reports`, `docs/map`, and `openspec/` that no longer reflect the system's current state.
- **Scratch and Temp Files**: Cleaning up temporary frontend testing files and `conftest.py` remnants from `backend/scratch/` and the backend root.

## 3. Benefits
- **Reduced Cognitive Load**: Developers (and AI agents) will no longer be confused by duplicate `src` folders or outdated `package.json` files.
- **Single Source of Truth**: Forcing reliance on the `openspec` tracking system rather than maintaining manual changelog files.
- **Structural Integrity**: Ensuring a clean root directory containing only orchestration tools (`.claude`, `engram`, `.opencode`) and the primary monorepo applications (`frontend`, `backend`).
