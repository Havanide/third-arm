# Decisions Log

## 2026-03-25
- Decision: Stage 1 remains desktop-first, operator-triggered, and mock-hardware-first.
- Reason: Keep the earliest executable loop narrow and benchable before hardware and sensing complexity.
- Affects: API scope, adapters, roadmap sequencing, procurement timing.

## 2026-03-27
- Decision: Bundle/replay logging is mandatory in the Stage 1 runtime path.
- Reason: The first trustworthy operator loop is `start -> handover -> stop -> artifacts`; replay artifacts must exist before moving to later slices.
- Affects: `SessionService`, `HandoverService`, `BundleWriter`, artifact flow, tests.

## 2026-03-27
- Decision: Preserve the existing Stage 1 response shapes and keep bundle discovery through `GET /artifacts`.
- Reason: Avoid silent API drift and keep the bundle/replay integration slice narrow.
- Affects: session/handover routers, OpenAPI, integration tests.

## 2026-03-27
- Decision: Session lifecycle failures must leave the runtime recoverable until bundle close succeeds.
- Reason: Hidden active sessions and half-finalized bundles are not acceptable failure modes for Stage 1 replay logging.
- Affects: session rollback behavior, bundle close semantics, targeted tests.

## 2026-04-04
- Decision: Stage 1 e2e smoke path is a mandatory merge gate for all PRs targeting main.
- Reason: The baseline operator flow (home → session → handover → stop → artifacts) must
  remain stable as subsequent slices are added. A labelled `smoke` marker and dedicated CI
  step make the gate explicit and machine-enforced.
- Affects: pytest marker config, CI workflow, AGENTS.md process rules.

## 2026-04-04
- Decision: `GET /artifacts/{session_id}` must validate session ids and degrade honestly on broken bundles.
- Reason: Stage 1 inspection is for operator debugging before hardware bring-up; broken bundles inside the session root must remain inspectable, while unsafe path-style ids must never escape the configured storage root.
- Affects: artifact router lookup rules, inspection response contract, integration tests, RPD wording.

## 2026-04-06
- Decision: `docs/api/openapi.yaml` remains hand-maintained in Stage 1.
- Reason: Runtime schema generation requires a live app process; hand-maintained YAML is
  reviewable in PRs and serves as the authoritative contract reference without infra dependency.
  FastAPI `/docs` and `/redoc` remain available for interactive exploration, but can remain
  broader or less precise for endpoints without explicit runtime response models.
- Affects: docs workflow, PR review practice for API contract changes, expectations around generated vs checked-in OpenAPI.

## 2026-04-06
- Decision: `POST /session/start` requires explicit `READY` state in Stage 1.
- Reason: The operator flow is already `home -> session/start`; allowing direct start from `IDLE` kept the precondition ambiguous and hid setup mistakes. Stage 1 should fail loudly instead of auto-homing or guessing operator intent.
- Affects: session router precondition, 409 error contract, integration tests, Stage 1 operator flow docs, RPD.

## 2026-04-06
- Decision: `POST /session/start` is a pure session/bundle gate; `POST /handover/request` is the task lifecycle entry point (READY → TASK_ARMING via `session_start` trigger).
- Reason: Separates operator intent (open session) from arm motion (task lifecycle). Keeps session/start lightweight and allows multiple handovers per session without re-entering the lifecycle gate each time.
- Affects: `HandoverService`, `StateMachine` trigger sequence, session router, trace events.

## 2026-04-06
- Decision: Stage 1 mock auto-returns arm to READY after each handover (`task_done` → `home_cmd` → `home_complete` → READY).
- Reason: Allows multiple handovers per session without operator re-homing. Physical home confirmation will gate this transition in Stage 1.5+.
- Affects: `HandoverService` post-handover sequence, `StateMachine`, trace events (`task_lifecycle_completed`), integration tests.
