# Hermes v8 Alpha 5.3 - Operator Chat Gateway

Adaugă un endpoint unic pentru conversații:

- `POST /operator/v8/chat`

Acesta este endpointul care va putea fi folosit de:
- Mission Control UI
- Telegram bot
- CLI
- alte integrări

## Ce face acum

Pentru mesaje de tip:
- `repornește VM 111`
- `restart VM 111`
- `reset VM 111`
- `pornește VM 111`
- `oprește VM 111`
- `status VM 111`
- `status LXC 202`

creează automat o misiune cu acțiunea corectă.

Acțiunile SAFE pot fi executate ulterior prin runner.
Acțiunile CONFIRM ajung în pending approval.
