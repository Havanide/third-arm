# Third Arm — Week 0 Task List v0.15

## Task 0.1 — Bootstrap repo
**Purpose:** создать чистый mono-repo.
**Deliverable:** репозиторий с папками, `pyproject.toml`, `README.md`, `.env.example`.
**Done:** репозиторий открывается и устанавливается локально.

## Task 0.2 — FastAPI app shell
**Purpose:** поднять минимальный edge service.
**Deliverable:** `main.py` + registered routers.
**Done:** локально отвечают `/health` и `/status`.

## Task 0.3 — WebSocket stream shell
**Purpose:** подготовить live channel для событий.
**Deliverable:** `/ws/stream` с heartbeat/status frames.
**Done:** локальный клиент получает frames.

## Task 0.4 — Settings and config loading
**Purpose:** централизовать runtime config.
**Deliverable:** `settings.py`, loader YAML configs.
**Done:** приложение читает `configs/app/stage1_desktop.yaml`.

## Task 0.5 — Slot/Object model loader
**Purpose:** завести structured workspace.
**Deliverable:** модели + parser/validator для slots/objects.
**Done:** `stage1_slots.yaml` и `stage1_objects.yaml` грузятся без ошибок.

## Task 0.6 — State machine stub
**Purpose:** реализовать согласованный lifecycle.
**Deliverable:** state machine with approved states and transitions.
**Done:** сценарий проходит до `task_complete` на mock arm.

## Task 0.7 — Mock arm adapter
**Purpose:** отладить control plane без железа.
**Deliverable:** mock adapter с predictible responses.
**Done:** `handover.request` приводит к правдоподобной последовательности событий.

## Task 0.8 — Session bundle writer
**Purpose:** не потерять replay/debug backbone.
**Deliverable:** writer для `manifest.json`, `session_trace.ndjson`, `telemetry.mcap`, snapshots.
**Done:** после одной session создается bundle корректной структуры.

## Task 0.9 — Integration smoke test
**Purpose:** связать API, state machine, mock arm и replay.
**Deliverable:** тест `session.start -> arm.home -> handover.request -> task_complete`.
**Done:** тест проходит локально и bundle валиден.

## Task 0.10 — Launch basket map
**Purpose:** привязать Week 0 к закупке.
**Deliverable:** список must-buy now с реальными market substitutes.
**Done:** есть список на закупку без архитектурных дыр.
