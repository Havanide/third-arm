# Next Step

## Goal
Decide whether `POST /session/start` should also trigger the state-machine `session_start`
transition during Stage 1, or remain a pure session/bundle gate before handover.

## Scope
- Review current state-machine usage in the runtime flow
- Make the explicit decision
- If a transition is required: update router, tests, and openapi.yaml/docs accordingly
- Update DECISIONS_LOG.md with the decision and rationale

## Do not do
- Do not change other endpoints in this slice
- Do not pull Stage 1.5 vision or camera work
- Do not refactor session or handover flow beyond the transition decision

## Done when
- Decision made and recorded in DECISIONS_LOG.md
- If behaviour changes: runtime + tests + openapi.yaml updated
- If decision is "keep as-is": just record the decision in DECISIONS_LOG.md
- CURRENT_STATE.md and NEXT_STEP.md updated
