# Third Arm — Handoff Context v0.15

## Что это за проект
«Третья рука» — это модульная супернумерарная конечность для **intent-driven handover**.
Цель проекта — пройти путь:
- **Stage 1**: desktop-first proof of usefulness;
- **Stage 1.5**: observation overlay;
- **Stage 2**: continuous hybrid vision;
- **Stage 3**: modular wearable/desktop platform с multimodal intent.

## Главная идея
Это не общий манипулятор «на все случаи». Первая ценность — **подача объекта человеку в нужный момент и в понятной зоне handover**.

## Текущее состояние проекта
Архитектурная часть стабилизирована.
Текущая рабочая версия пакета документов: **v0.15**.

## Ключевые цели ближайшего этапа
1. Поднять mono-repo skeleton.
2. Поднять FastAPI edge skeleton.
3. Реализовать session bundle writer.
4. Реализовать state machine stub.
5. Подключить mock arm.
6. Только затем идти в hardware bring-up.

## Актуальные артефакты
- `01_PRD_Third_Arm_Master_v0_15.docx`
- `02_TechSpec_Architecture_C4_v0_15.docx`
- `03_BOM_Budget_Printables_v0_15.docx`
- `04_Project_Log_and_Open_Questions_v0_15.docx`

## Важные ограничения
- Нельзя ломать edge-first принцип.
- Сервер не участвует в safety-critical loop.
- Stage 1 должен остаться operator-triggered.
- Stage 1 camera-ready, но camera-on не является блокером первой демонстрации.
- Нельзя выкидывать structured slot model ради «умной» vision-first схемы раньше времени.
- Нельзя удалять старую важную информацию из документов; новые решения добавляются поверх истории.

## Предпочтительный стиль общения и работы
- Прямо, без лишнего оптимизма.
- Не соглашаться автоматически с гипотезами пользователя.
- Оспаривать слабые решения прагматично.
- Держать фокус на полезном прототипе, а не на красивой фантазии.
