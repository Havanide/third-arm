# Third Arm — Execution Pack v0.15

## Repo skeleton
```text
third-arm/
├─ pyproject.toml
├─ README.md
├─ .env.example
├─ .gitignore
├─ configs/
│  ├─ app/
│  ├─ slots/
│  └─ calibration/
├─ docs/
│  ├─ api/
│  ├─ architecture/
│  └─ handoff/
├─ src/
│  └─ third_arm/
│     ├─ main.py
│     ├─ api/
│     ├─ core/
│     ├─ domain/
│     ├─ adapters/
│     ├─ logging/
│     ├─ storage/
│     └─ cli/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ replay/
│  └─ fixtures/
├─ scripts/
└─ sessions/
```

## Folder responsibilities
- `api/` — northbound REST + WS surface only.
- `domain/` — state machine, handover logic, slot/object semantics.
- `adapters/` — mock/hardware/vision/imu/semg integration points.
- `logging/` — session bundle writer, NDJSON trace, MCAP writer, replay reader.
- `configs/` — frozen runtime profiles.
- `tests/replay/` — regression against recorded sessions.

## Week 0 success gate
- repo bootstrapped;
- FastAPI app starts locally;
- `/health`, `/status`, `/ws/stream` work;
- session bundle is written to disk;
- mock arm can complete a `present_hold` scenario;
- replay artifacts are readable.

## Stage 1 launch basket
### Must-buy now
- Pi 5 class edge node + storage
- 24V power path
- motion core
- desktop dock
- E-stop
- physical trigger / footswitch
- printed source slots
- camera-ready bracket and cable path

### Buy-soon
- vision sensor
- IMU
- light / mounting refinements

### Defer
- sEMG primary path
- wearable mount hardware
- quick-change tool-side
- heavy scene-first compute
