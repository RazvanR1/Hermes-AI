# Hermes v8 Events Core Fix 1

Fix pentru eroarea 500 la:

`POST /events/v8/emit-test`

Cauza probabilă: `backend/data/events_v8.json` creat ca root în timpul instalării, iar `hermes-api` rulează ca user `hermes`.

## Fix
- repară ownership pentru `backend/data`
- repară ownership pentru `events_v8.json`
- păstrează Event Bus persistent
