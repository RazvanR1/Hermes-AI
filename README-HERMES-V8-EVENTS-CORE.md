# Hermes v8 Events Core

Adaugă Event Bus pentru Hermes.

## Include

- `backend/event_bus_v8.py`
- `backend/mission_events_v8.py`
- `backend/api/events_v8.py`

## API

- `GET /events/v8/health`
- `GET /events/v8/list`
- `GET /events/v8/mission/{mission_id}`
- `POST /events/v8/emit-test`

## Scop

Pregătește UI live, Telegram notifications și audit log pentru:
- mission created
- mission approved
- mission running
- step started
- step finished
- mission completed
- mission failed
