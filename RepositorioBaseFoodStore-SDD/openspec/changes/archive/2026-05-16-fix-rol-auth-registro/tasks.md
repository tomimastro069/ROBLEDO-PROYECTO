# Tasks: Auth Registration Role Fix

- [x] Import `Role` enum in `backend/auth/service.py`.
- [x] Implement role lookup logic in `AuthService.register`.
- [x] Assign `role_id` to the new user before commit.
- [x] Refactor `AuthService.login` to remove hardcoded role fallback.
- [x] Refactor `AuthService.refresh` for consistency.
- [x] Verify registration flow with a new user.
