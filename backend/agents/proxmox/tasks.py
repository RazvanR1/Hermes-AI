import os
import requests
import time

URL = os.getenv("PROXMOX_URL", "").rstrip("/")
TOKEN_ID = os.getenv("PROXMOX_TOKEN_ID", "")
TOKEN_SECRET = os.getenv("PROXMOX_TOKEN_SECRET", "")
VERIFY = os.getenv("PROXMOX_VERIFY_SSL", "false").lower() == "true"

HEADERS = {
    "Authorization": f"PVEAPIToken={TOKEN_ID}={TOKEN_SECRET}"
}


def wait_for_task(node: str, upid: str, timeout: int = 120):
    start = time.time()

    while time.time() - start < timeout:
        r = requests.get(
            f"{URL}/api2/json/nodes/{node}/tasks/{upid}/status",
            headers=HEADERS,
            verify=VERIFY,
            timeout=10,
        )

        if r.status_code != 200:
            return {
                "ok": False,
                "error": f"HTTP {r.status_code}"
            }

        data = r.json()["data"]

        if data.get("status") == "stopped":
            return {
                "ok": data.get("exitstatus") == "OK",
                "status": data.get("exitstatus"),
                "upid": upid,
            }

        time.sleep(2)

    return {
        "ok": False,
        "error": "Timeout waiting for task"
    }
