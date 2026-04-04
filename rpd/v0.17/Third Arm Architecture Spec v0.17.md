# Third Arm Architecture Spec v0.17

## Scope of this version
This version adds a process and verification constraint, not a new runtime subsystem.

## Architecture delta vs v0.16
- `test_full_session_handover_flow` is the single authoritative Stage 1 smoke path
- It is labeled with `@pytest.mark.smoke`
- CI runs `pytest -m smoke -v` before the full suite
- The smoke path is intended to be enforced as a required GitHub check for `main`

## Verified runtime path
The smoke path exercises the current Stage 1 architecture end-to-end:
- FastAPI lifespan startup
- state machine home transition
- session lifecycle
- handover service on mock hardware
- bundle writer close/finalization
- artifact listing

## Isolation properties
- sessions dir is redirected to test-local `tmp_path`
- the flow uses `MockArmDriver`
- no external hardware, no network dependency, no shared runtime artifacts

## What did not change
- No architecture refactor
- No new adapters
- No event bus work
- No camera pipeline
- No real arm driver integration
- No MQTT

## Merge-gate intent
The purpose of this version is to keep one stable software acceptance path intact while later slices are added.
That gate is meaningful only if:
- CI runs it explicitly
- GitHub requires the corresponding checks before merge

Current state:
- CI runs the smoke step before the full suite
- GitHub `main` requires `test (3.10)` and `test (3.11)`
- therefore the smoke path is now enforced before merge
