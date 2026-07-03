import base64
import json
import os
import ssl
import urllib.error
import urllib.request


def _load_env_file(path):
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    except FileNotFoundError:
        pass


def _config():
    _load_env_file("/home/hermes/.opnsense.env")
    _load_env_file("/home/hermes/.hermes/.env")

    url = os.getenv("OPNSENSE_URL", "https://192.168.1.1").rstrip("/")
    key = os.getenv("OPNSENSE_KEY", "")
    secret = os.getenv("OPNSENSE_SECRET", "")

    return url, key, secret


def _request(path):
    url, key, secret = _config()

    if not key or not secret:
        return {
            "ok": False,
            "error": "OPNsense API key/secret missing. Configure /home/hermes/.opnsense.env",
        }

    target = f"{url}{path}"
    auth = base64.b64encode(f"{key}:{secret}".encode()).decode()

    req = urllib.request.Request(
        target,
        headers={
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
        },
    )

    ctx = ssl._create_unverified_context()

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return {
                "ok": True,
                "status_code": resp.status,
                "data": json.loads(raw) if raw else {},
            }
    except urllib.error.HTTPError as e:
        return {
            "ok": False,
            "status_code": e.code,
            "error": e.read().decode("utf-8", errors="replace"),
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }


def firmware_status():
    return _request("/api/core/firmware/status")


def summary():
    fw = firmware_status()

    if not fw.get("ok"):
        return {
            "ok": False,
            "component": "opnsense",
            "error": fw.get("error"),
            "status_code": fw.get("status_code"),
        }

    data = fw.get("data", {}) or {}

    upgrade_packages = data.get("upgrade_packages") or []
    new_packages = data.get("new_packages") or []
    reinstall_packages = data.get("reinstall_packages") or []
    remove_packages = data.get("remove_packages") or []

    update_count = (
        len(upgrade_packages)
        + len(new_packages)
        + len(reinstall_packages)
        + len(remove_packages)
    )

    needs_reboot = str(data.get("needs_reboot", "0")) == "1"
    upgrade_needs_reboot = str(data.get("upgrade_needs_reboot", "0")) == "1"

    return {
        "ok": True,
        "component": "opnsense",
        "connection": data.get("connection"),
        "repository": data.get("repository"),
        "status": data.get("status"),
        "status_msg": data.get("status_msg"),
        "product_version": data.get("product_version"),
        "product_id": data.get("product_id"),
        "os_version": data.get("os_version"),
        "last_check": data.get("last_check"),
        "updates_count": update_count,
        "needs_reboot": needs_reboot,
        "upgrade_needs_reboot": upgrade_needs_reboot,
        "upgrade_packages": upgrade_packages,
        "new_packages": new_packages,
        "raw": data,
    }
