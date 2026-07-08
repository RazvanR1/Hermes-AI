#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/hermes/Hermes}"
SERVICE_NAME="${SERVICE_NAME:-hermes-api}"

cd "$PROJECT_DIR"

echo "[1/8] Git status..."
git status --short || true

echo "[2/8] Backup files..."
mkdir -p .hermes-backups
cp backend/actions_v8_linux.py ".hermes-backups/actions_v8_linux.py.alpha5-1.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true
cp /etc/sudoers.d/hermes-privrunner ".hermes-backups/sudoers.hermes-privrunner.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true
cp /usr/local/sbin/hermes-privrunner ".hermes-backups/hermes-privrunner.$(date +%Y%m%d-%H%M%S).bak" 2>/dev/null || true

echo "[3/8] Install privileged runner..."
install -o root -g root -m 0750 privrunner/hermes-privrunner /usr/local/sbin/hermes-privrunner

echo "[4/8] Configure sudoers allowlist..."
cat > /etc/sudoers.d/hermes-privrunner <<'EOF'
hermes ALL=(root) NOPASSWD: /usr/local/sbin/hermes-privrunner linux.apt_update
hermes ALL=(root) NOPASSWD: /usr/local/sbin/hermes-privrunner linux.apt_upgrade_preview
EOF
chmod 0440 /etc/sudoers.d/hermes-privrunner
visudo -cf /etc/sudoers.d/hermes-privrunner

echo "[5/8] Validate direct runner as hermes..."
su - hermes -c 'sudo -n /usr/local/sbin/hermes-privrunner linux.apt_upgrade_preview >/tmp/hermes-privrunner-test.out'
head -20 /tmp/hermes-privrunner-test.out || true

echo "[6/8] Validate Python imports..."
PYTHONPATH="$PROJECT_DIR/backend" python3 - <<'PY'
from api import execution_v8
from actions_v8_registry import list_actions
print("imports ok")
print(list_actions())
PY

echo "[7/8] Restart API..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l || true

echo "[8/8] Test API health..."
curl -fsS http://127.0.0.1:8088/execution/v8/health
echo
echo "Done."
