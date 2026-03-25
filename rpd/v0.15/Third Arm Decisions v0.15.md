# Third Arm — Decisions and Invariants v0.15

## Product / roadmap
- Один продукт в стадиях **Stage 1 → 1.5 → 2 → 3**.
- **Stage 1 = desktop-first**.
- Mount на тело проектируется после живого настольного прототипа.
- Vision обязателен к **Stage 2**.
- sEMG не является обязательным входом Stage 1/1.5; это поздний multimodal слой.

## Architecture invariants
- Общий **arm core** + разные **base modules**.
- Interface contract v1.0:
  - жесткий фланец,
  - 24V rail,
  - внешний CAN-ready bus,
  - отдельный safety loop.
- Сервер не идет в actuator bus.
- Edge работает offline-first.
- Northbound:
  - REST + WebSocket как базовый контракт,
  - MQTT как расширение.

## Stage 1
- Payload: **300 г nominal / 500 г stretch**.
- Objects: **кружка, фонарик, мячик**.
- Handover режим Stage 1: основной — `present_hold`.
- Structured slot model frozen.
- Stage 1 state machine frozen (вариант B).
- Logging/replay:
  - Stage 1 = session bundle Variant 2,
  - Stage 2 = richer Variant 3.

## Input / sensing
- Stage 1 = operator-triggered.
- Обязательны:
  - Web UI / локальный UI,
  - physical trigger,
  - E-stop.
- Stage 1 camera-ready.
- IMU — ранний side-channel.
- sEMG — later / parallel R&D.

## Procurement rule
- Рыночные замены разрешены, если не ломают архитектурные инварианты.
- Любая замена, которая меняет:
  - bus strategy,
  - rail voltage,
  - safety loop,
  - edge-first control policy,
  требует отдельного пересогласования.
