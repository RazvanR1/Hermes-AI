import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Lipsește variabila {name}")
    return value

def headers():
    return {
        "Authorization": f"Bearer {env('TRUENAS_API_KEY')}",
        "Content-Type": "application/json",
    }

def api(method, path, data=None):
    url = f"{env('TRUENAS_URL').rstrip('/')}/api/v2.0{path}"
    r = requests.request(
        method,
        url,
        headers=headers(),
        json=data,
        verify=False,
        timeout=20,
    )
    r.raise_for_status()
    if not r.text:
        return {}
    return r.json()

def system_info():
    return api("GET", "/system/info")

def pools():
    return api("GET", "/pool")

def disks():
    return api("GET", "/disk")

def datasets():
    return api("GET", "/pool/dataset")

def shares_smb():
    return api("GET", "/sharing/smb")

def alerts():
    return api("GET", "/alert/list")

def smart_tests():
    return api("GET", "/smart/test")

def scrub_tasks():
    return api("GET", "/pool/scrub")

def snapshots():
    return api("GET", "/zfs/snapshot")

def health():
    info = system_info()
    pools_data = pools()
    alerts_data = alerts()
    disks_data = disks()

    return {
        "system": {
            "hostname": info.get("hostname"),
            "version": info.get("version"),
            "uptime": info.get("uptime"),
            "memory_gb": round(info.get("physmem", 0) / 1024 / 1024 / 1024, 1),
            "cores": info.get("cores"),
            "loadavg": info.get("loadavg"),
        },
        "pools": [
            {
                "name": p.get("name"),
                "status": p.get("status"),
                "path": p.get("path"),
                "healthy": p.get("healthy"),
                "warning": p.get("warning"),
                "scan": p.get("scan"),
                "topology": p.get("topology"),
            }
            for p in pools_data
        ],
        "alerts": [
            {
                "level": a.get("level"),
                "klass": a.get("klass"),
                "formatted": a.get("formatted"),
                "dismissed": a.get("dismissed"),
            }
            for a in alerts_data
        ],
        "disks": [
            {
                "name": d.get("name"),
                "serial": d.get("serial"),
                "model": d.get("model"),
                "size": d.get("size"),
                "type": d.get("type"),
                "rotationrate": d.get("rotationrate"),
                "temperature": d.get("temperature"),
            }
            for d in disks_data
        ],
    }


def health_summary():
    info = system_info()
    pools_data = pools()
    alerts_data = alerts()

    return {
        "system": {
            "hostname": info.get("hostname"),
            "version": info.get("version"),
            "uptime": info.get("uptime"),
            "memory_gb": round(info.get("physmem", 0) / 1024 / 1024 / 1024, 1),
            "cores": info.get("cores"),
            "loadavg": info.get("loadavg"),
        },
        "pools": [
            {
                "name": p.get("name"),
                "status": p.get("status"),
                "healthy": p.get("healthy"),
                "warning": p.get("warning"),
                "scan": p.get("scan"),
            }
            for p in pools_data
        ],
        "alerts": [
            {
                "level": a.get("level"),
                "klass": a.get("klass"),
                "formatted": a.get("formatted"),
                "dismissed": a.get("dismissed"),
            }
            for a in alerts_data
        ],
    }

def update_status():
    current = system_info().get("version")

    config = None
    try:
        config = api("GET", "/update/")
    except Exception as e:
        config = {"error": str(e)}

    checks = []
    for endpoint in [
        "/update/check_available",
        "/update/check_available/",
        "/update/check_available?train=GENERAL",
        "/update/get_pending",
        "/update/get_pending/",
    ]:
        try:
            result = api("GET", endpoint)
            checks.append({
                "endpoint": endpoint,
                "ok": True,
                "result": result,
            })
        except Exception as e:
            checks.append({
                "endpoint": endpoint,
                "ok": False,
                "error": str(e),
            })

    available = None
    best_result = None

    for c in checks:
        if c.get("ok"):
            best_result = c.get("result")
            if best_result:
                available = True
            else:
                available = False
            break

    return {
        "current_version": current,
        "config": config,
        "available": available,
        "result": best_result,
        "checks": checks,
    }
