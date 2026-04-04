# Next Step

> **Prerequisite done:** Stage 1 smoke gate is in place (`pytest -m smoke`). Proceed to next feature slice.

## Goal
Add a narrow Stage 1 REST endpoint to inspect one bundle in detail without changing the existing operator flow.

## Scope
- Add `GET /artifacts/{session_id}`
- Return manifest-level metadata and bundle file inventory for one session
- Reuse existing storage/replay helpers where possible
- Add 200/404 automated tests
- Update checked-in OpenAPI and status docs

## Do not do
- Do not add download/export in this slice
- Do not add MCAP decoding or playback APIs
- Do not touch Stage 1.5 camera/vision work
- Do not refactor session/handover flow unless a bug requires it
- Do not expand the frozen Stage 1 operator contract

## Done when
- Existing `GET /artifacts` behavior still works
- `GET /artifacts/{session_id}` returns one bundle by session id
- Missing bundle returns 404
- Relevant tests pass
- `CURRENT_STATE.md` and `DECISIONS_LOG.md` are updated
