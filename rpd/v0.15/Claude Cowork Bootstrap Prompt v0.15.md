Ты работаешь на локальном Mac и должен создать ПУСТОЙ, НО ПРАВИЛЬНО СКЕЛЕТИЗИРОВАННЫЙ проект для разработки robotics/edge-сервиса под названием `third-arm`.

Важно:
- НЕ нужно реализовывать бизнес-логику полностью.
- НЕ нужно писать кинематику, vision pipeline, EMG/IMU обработку и реальный hardware control.
- Нужно создать структуру репозитория, базовые файлы, placeholders, stubs и минимально рабочий FastAPI shell.
- Все изменения делай локально в новой папке проекта.
- После создания покажи дерево файлов и кратко опиши, что создано.
- Если какой-то файл спорный, создай его как placeholder с TODO и docstring, а не выдумывай лишнюю реализацию.

Контекст проекта:
- Проект: «Третья рука».
- Это modular supernumerary arm для intent-driven handover.
- Stage 1 = desktop-first.
- Сервер не входит в safety-critical loop.
- Northbound contract: REST + WebSocket как база, MQTT позже.
- Logging/replay обязателен с самого начала.
- Stage 1 должен быть operator-triggered.
- Stage 1 camera-ready, но camera-on не обязателен в первом working skeleton.
- Нужно заложить архитектурный рост до Stage 1.5 / Stage 2 / Stage 3.

Создай репозиторий со следующей структурой на /Desktop:

```text
third-arm/
├─ pyproject.toml
├─ README.md
├─ .env.example
├─ .gitignore
├─ configs/
│  ├─ app/
│  │  ├─ default.yaml
│  │  ├─ dev.yaml
│  │  └─ stage1_desktop.yaml
│  ├─ slots/
│  │  ├─ stage1_slots.yaml
│  │  └─ stage1_objects.yaml
│  └─ calibration/
│     └─ placeholder.yaml
├─ docs/
│  ├─ api/
│  │  ├─ openapi.yaml
│  │  └─ asyncapi.yaml
│  ├─ architecture/
│  └─ handoff/
├─ src/
│  └─ third_arm/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ api/
│     │  ├─ __init__.py
│     │  ├─ deps.py
│     │  ├─ routers/
│     │  │  ├─ __init__.py
│     │  │  ├─ health.py
│     │  │  ├─ status.py
│     │  │  ├─ session.py
│     │  │  ├─ arm.py
│     │  │  ├─ handover.py
│     │  │  └─ artifacts.py
│     │  ├─ ws/
│     │  │  ├─ __init__.py
│     │  │  └─ stream.py
│     │  └─ schemas/
│     │     ├─ __init__.py
│     │     ├─ common.py
│     │     ├─ commands.py
│     │     ├─ events.py
│     │     ├─ telemetry.py
│     │     └─ faults.py
│     ├─ core/
│     │  ├─ __init__.py
│     │  ├─ settings.py
│     │  ├─ ids.py
│     │  ├─ clock.py
│     │  └─ errors.py
│     ├─ domain/
│     │  ├─ __init__.py
│     │  ├─ contracts.py
│     │  ├─ policies.py
│     │  ├─ object_model.py
│     │  ├─ slot_model.py
│     │  ├─ state_machine.py
│     │  ├─ session_service.py
│     │  └─ handover_service.py
│     ├─ adapters/
│     │  ├─ __init__.py
│     │  ├─ mock_arm/
│     │  │  ├─ __init__.py
│     │  │  └─ driver.py
│     │  ├─ hardware/
│     │  │  ├─ __init__.py
│     │  │  ├─ arm_driver.py
│     │  │  ├─ gpio_trigger.py
│     │  │  ├─ estop.py
│     │  │  └─ power_monitor.py
│     │  ├─ vision/
│     │  │  ├─ __init__.py
│     │  │  ├─ camera_stub.py
│     │  │  └─ observation_stub.py
│     │  └─ intent/
│     │     ├─ __init__.py
│     │     ├─ imu_stub.py
│     │     └─ semg_stub.py
│     ├─ logging/
│     │  ├─ __init__.py
│     │  ├─ bundle_writer.py
│     │  ├─ trace_writer.py
│     │  ├─ mcap_writer.py
│     │  ├─ manifest.py
│     │  └─ replay_reader.py
│     ├─ storage/
│     │  ├─ __init__.py
│     │  ├─ files.py
│     │  └─ paths.py
│     └─ cli/
│        ├─ __init__.py
│        ├─ run_dev.py
│        ├─ export_bundle.py
│        └─ replay_session.py
├─ tests/
│  ├─ unit/
│  │  └─ test_imports.py
│  ├─ integration/
│  │  └─ test_health.py
│  ├─ replay/
│  │  └─ test_bundle_smoke.py
│  └─ fixtures/
├─ scripts/
│  ├─ dev.sh
│  ├─ format.sh
│  ├─ seed_stage1_configs.py
│  └─ validate_bundle.py
└─ sessions/
   └─ .gitkeep
```

Что нужно реализовать минимально:
1. `pyproject.toml` с базовыми зависимостями:
   - fastapi
   - uvicorn
   - pydantic
   - pydantic-settings
   - pyyaml
   - pytest
   - mcap
2. `main.py`:
   - создает FastAPI app
   - подключает routers
   - подключает один WebSocket endpoint `/ws/stream`
3. routers:
   - `/health`
   - `/status`
   - `/session/start`
   - `/session/stop`
   - `/arm/home`
   - `/handover/request`
   - `/artifacts`
   Пока можно вернуть stub/no-op responses.
4. `settings.py`:
   - базовая модель настроек
   - чтение из `.env`
5. `state_machine.py`:
   - перечисление согласованных состояний:
     `boot, self_check, idle, homing, ready, task_arming, acquire, lift, present, transfer_wait, release, retract, task_complete, task_aborted, safe_stop, fault, recovering, shutdown`
   - пока без сложной логики, но со skeleton transitions / TODO
6. `slot_model.py` и `object_model.py`:
   - минимальные dataclass/pydantic-модели
7. `mock_arm/driver.py`:
   - stub driver с методами вроде `home()`, `start_handover()`, `safe_stop()`
8. `bundle_writer.py`:
   - создает папку сессии
   - пишет placeholder `manifest.json`
   - пишет placeholder `session_trace.ndjson`
   - создает placeholder для `telemetry.mcap`
9. YAML examples:
   - `stage1_desktop.yaml`
   - `stage1_slots.yaml`
   - `stage1_objects.yaml`
10. README:
   - кратко объясняет проект
   - как поставить зависимости
   - как запустить dev server
   - какие endpoints уже есть
11. scripts:
   - `dev.sh` для локального запуска
   - `seed_stage1_configs.py` для генерации/проверки example config
   - `validate_bundle.py` для smoke-проверки структуры bundle

Важно:
- Используй понятные имена, docstrings и TODO-комментарии.
- Не придумывай лишнюю глубину реализации.
- Код должен запускаться локально на Mac.
- После генерации:
  1) покажи дерево файлов,
  2) перечисли созданные зависимости,
  3) перечисли, что пока intentionally left as stub,
  4) предложи следующий минимальный шаг разработки.
