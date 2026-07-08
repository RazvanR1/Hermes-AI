# Hermes v8 Alpha 5.1 - Privileged Runner

Adaugă un runner privilegiat controlat pentru acțiuni Linux care au nevoie de root.

## Ce face

- API-ul Hermes rămâne pe user `hermes`.
- Acțiunile root se rulează prin scriptul `/usr/local/sbin/hermes-privrunner`.
- Scriptul acceptă doar acțiuni allowlist.
- În acest release, acțiunea reală permisă este:
  - `linux.apt_update`
- `linux.apt_upgrade_preview` rămâne fără root.
- NU rulează `apt upgrade -y`.

## Test

```bash
./verify-alpha5-1.sh
```
