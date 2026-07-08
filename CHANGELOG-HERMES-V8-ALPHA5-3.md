# Changelog - Hermes v8 Alpha 5.3

## Added
- `backend/operator_v8.py`
- `backend/api/operator_v8.py`
- `/operator/v8/chat`
- `/operator/v8/health`

## Purpose
Pregătește integrarea cu:
- Mission Control chat UI
- Telegram bot

## Safety
Endpointul nu execută direct acțiuni CONFIRM.
Creează misiuni și le trimite către fluxul de Approval.
