# Third Arm Status Update v0.19

**Date:** 2026-04-06
**Stage:** 1 (desktop-first, operator-triggered, mock hardware)
**Previous version:** v0.18

---

## What changed in v0.19

### docs/api/openapi.yaml — Stage 1 checked-in API contract synchronized

The `docs/api/openapi.yaml` has been corrected to match the checked-in Stage 1 contract
used for review. 8 implementation gaps were fixed, and validation/required-field details were tightened.

**Gaps corrected:**

| # | Item | Before | After |
|---|------|--------|-------|
| 1 | `HealthResponse` schema | `{status, version, ts}` | `{ok, ts, message}` |
| 2 | `StatusResponse` schema | missing `ts` field | `{ts, arm_state, session_id, uptime_s, mock_mode}` |
| 3 | `/arm/home` 202 response body | no schema | `{accepted: bool, new_state: str}` |
| 4 | `/session/start` errors | only 200, 409 | added 404 for unknown object_id / slot_id |
| 5 | `/handover/request` errors | only 202, 409 | added 404 for unknown object_id / slot_id |
| 6 | `ArtifactsResponse` | no `count` field | added `count: integer` |
| 7 | `/artifacts/{session_id}` | missing entirely | added with full response schema |
| 8 | New schemas | none | `ArtifactDetailResponse`, `PresenceFlags`, `BundleFileEntry`, `TraceSummary`, `ArmHomeResponse` |

**Additional alignment completed after review:**
- Added FastAPI `422 Validation Error` responses where body/path validation applies
- Marked POST request bodies as required
- Declared required response fields and nullable fields explicitly
- Clarified that checked-in `openapi.yaml` is authoritative, while runtime-generated `/docs` remains exploratory on endpoints without full response models

**Decision recorded:** `docs/api/openapi.yaml` remains hand-maintained in Stage 1 (see DECISIONS_LOG.md).

---

## Stage 1 documentation milestone status

All Stage 1 implementation deliverables and the checked-in API contract are now synchronized:
- Operator REST flow: complete
- Bundle/replay logging: complete and wired
- Session lifecycle hardening: complete
- E2E smoke gate: complete
- Bundle inspection endpoint: complete
- OpenAPI spec: complete and synced as checked-in contract (this version)

**Next slice:** Decide `POST /session/start` state requirement (IDLE vs READY only).

---

## Files not changed in v0.19

- `Third Arm Assembly Note v0.18.md` / v0.17 — no hardware change
- `Third Arm Procurement Note v0.18.md` / v0.16 — no BOM change
- Runtime code — no code changes in this slice (docs-only)
