## Change Archived: auth-api

**Fecha**: 2026-05-09
**Estado**: Completado Manualmente (Rate Limit fallback)

### Specs Synced
| Domain | Action | Details |
|--------|--------|---------|
| auth | Updated | Added REST API Endpoints requirement and scenarios. |

### Archive Contents
- proposal.md ✅
- specs/ ✅
- design.md ✅
- tasks.md ✅ (7/7 tasks complete)

### Source of Truth Updated
- `openspec/specs/auth/spec.md` ahora refleja los endpoints REST oficiales.

### Notas
Se eliminó la lógica legacy en `backend/app/core/auth.py` y se centralizó todo en el nuevo router.
