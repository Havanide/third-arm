# AGENTS.md — Third Arm

## Project mode
Third Arm is developed in staged mode:
Stage 1 -> Stage 1.5 -> Stage 2 -> Stage 3

Current focus: Stage 1 desktop-first prototype.

Do not pull Stage 2/3 complexity into Stage 1 unless explicitly requested.

## Core constraints
- Desktop-first
- Operator-triggered in Stage 1
- Camera-ready in Stage 1
- Observation overlay in Stage 1.5
- Continuous vision in Stage 2
- Multimodal / hybrid in Stage 3
- Shared arm core + different base modules
- Northbound: REST + WebSocket
- MQTT only as later extension
- Logging / replay bundle is mandatory
- Object slot model and state machine are already agreed
- Preserve architectural invariants when changing BOM or substitutes

## Runbook
- Create env: `python -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -e ".[dev]"`
- Run dev server: `bash scripts/dev.sh`
- Alternative run: `uvicorn third_arm.main:app --reload --host 0.0.0.0 --port 8080`

## Workflow
- Work only in feature branches, never directly in `main`
- Keep changes scoped to the current implementation slice
- Prefer narrow PRs
- Update docs when behavior, contracts, architecture, or procurement meaningfully changes
- After code changes, run tests before finishing
- Prepare a PR-ready summary
- After every merge to `main`, send a short state-sync block in chat using this template:

```md
## State sync after merge

PR:
- <link>
- <title>

Merge:
- branch: <feature branch>
- merge commit: <sha>

Что изменилось по поведению:
- ...

Что изменилось в API / state machine / contracts:
- ...

Что изменилось в документации:
- PRD: yes/no
- Architecture Spec: yes/no
- Procurement: yes/no
- Assembly PDF: yes/no
- другие файлы: ...

Проверки:
- pytest: pass/fail
- CI: pass/fail
- smoke path: pass/fail
- ручная проверка: ...

Что НЕ сделано:
- ...

Открытые вопросы / риски:
- ...

Отклонение от плана:
- none / есть

Рекомендуемый следующий шаг от Claude/Codex:
- ...
```

## Required before finishing a task
1. Code changes complete
2. Relevant tests pass
3. Documentation updated if needed
4. Short change summary prepared
5. Suggested PR title prepared
6. Known risks listed

## Testing expectations
- At minimum run the project-relevant automated tests for the touched slice
- Prefer adding or updating tests for behavior changes
- Before proposing merge, prefer a full `pytest` run unless the task is strictly docs-only

## Documentation expectations
When relevant, update:
- `docs/status/CURRENT_STATE.md`
- `docs/status/NEXT_STEP.md`
- `docs/status/OPEN_QUESTIONS.md`
- `docs/decisions/DECISIONS_LOG.md`

Main user-facing documents are maintained separately in office/PDF format, but repo markdown status files must remain current.

## What requires explicit agreement
- State-machine changes
- Slot/object model changes
- Frozen API contract changes
- Architecture changes beyond the current slice
- Procurement-impacting substitutions
- Pulling Stage 1.5/2/3 features into Stage 1

## PR format
- Narrow title tied to one implementation slice
- Short behavior summary
- Tests run
- Risks / follow-ups
- No hidden scope creep

## What not to do
- Do not redesign architecture without explicit reason
- Do not introduce Stage 2/3 features into Stage 1 by default
- Do not silently change frozen contracts
- Do not remove historical context from docs unless explicitly asked
- Do not expand scope just because a refactor looks attractive

## Preferred output format for task completion
Return:
- changed files
- behavior summary
- tests run
- risks / follow-ups
- PR title
- PR description draft
