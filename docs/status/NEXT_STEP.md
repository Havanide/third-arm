# Next Step

## Goal
Decide and implement the `POST /session/start` state requirement: should it require explicit
READY state, or continue to accept both IDLE and READY?

## Scope
- Review the open question in OPEN_QUESTIONS.md
- Make the explicit decision
- If READY is required: update session router, tests, and openapi.yaml accordingly
- Update DECISIONS_LOG.md with the decision and rationale

## Do not do
- Do not change other endpoints in this slice
- Do not pull Stage 1.5 vision or camera work
- Do not refactor session or handover flow beyond the state check

## Done when
- Decision made and recorded in DECISIONS_LOG.md
- If behaviour changes: session router updated + tests pass + openapi.yaml updated
- If decision is "keep as-is": just record the decision in DECISIONS_LOG.md
- CURRENT_STATE.md and NEXT_STEP.md updated
