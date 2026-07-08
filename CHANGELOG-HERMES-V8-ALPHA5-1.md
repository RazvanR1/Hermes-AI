# Changelog - Hermes v8 Alpha 5.1

## Added
- `/usr/local/sbin/hermes-privrunner`
- sudoers rule pentru userul `hermes`
- integrare în `actions_v8_linux.py`

## Safety
- Allowlist strict în privileged runner.
- Nu există shell liber.
- Nu există comenzi arbitrare.
- Nu se rulează apt upgrade automat.
