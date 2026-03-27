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
