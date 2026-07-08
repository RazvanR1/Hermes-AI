# Changelog - Hermes v8 Alpha 5 Core

## Added
- backend/actions_v8_registry.py
- backend/actions_v8_linux.py
- backend/actions_v8_runner.py
- backend/api/execution_v8.py
- install-alpha5-core.sh
- verify-alpha5-core.sh
- rollback-alpha5-core.sh

## Safety
- `linux.status`, `linux.disk`, `linux.memory`, `security.audit` sunt SAFE.
- `linux.apt_update` este SAFE.
- `linux.apt_upgrade_preview` este SAFE dry-run.
- Nu rulează `apt upgrade -y` real în acest release.
