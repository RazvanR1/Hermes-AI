import requests
from core.config import config as hermes_config

def env(name):
    return hermes_config.require(name)

def headers():
    return {
        "Authorization": f"Bearer {env('HOMEASSISTANT_TOKEN')}",
        "Content-Type": "application/json",
    }

def api(method, path, data=None):
    url = f"{env('HOMEASSISTANT_URL').rstrip('/')}/api{path}"
    r = requests.request(method, url, headers=headers(), json=data, timeout=15)
    r.raise_for_status()
    if not r.text:
        return {}
    return r.json()

def status():
    return api("GET", "/")

def states():
    return api("GET", "/states")

def state(entity_id):
    return api("GET", f"/states/{entity_id}")

def services():
    return api("GET", "/services")

def events():
    return api("GET", "/events")

def config():
    return api("GET", "/config")

def call_service(domain, service, data=None):
    if data is None:
        data = {}
    return api("POST", f"/services/{domain}/{service}", data)

def climate_fan_mode(entity_id, fan_mode):
    return call_service("climate", "set_fan_mode", {"entity_id": entity_id, "fan_mode": fan_mode})

def climate_preset_mode(entity_id, preset_mode):
    return call_service("climate", "set_preset_mode", {"entity_id": entity_id, "preset_mode": preset_mode})

def climate_swing_mode(entity_id, swing_mode):
    return call_service("climate", "set_swing_mode", {"entity_id": entity_id, "swing_mode": swing_mode})

def script_run(entity_id):
    return call_service("script", "turn_on", {"entity_id": entity_id})

def scene_activate(entity_id):
    return call_service("scene", "turn_on", {"entity_id": entity_id})

def automation_enable(entity_id):
    return call_service("automation", "turn_on", {"entity_id": entity_id})

def automation_disable(entity_id):
    return call_service("automation", "turn_off", {"entity_id": entity_id})

def automation_trigger(entity_id):
    return call_service("automation", "trigger", {"entity_id": entity_id, "skip_condition": False})

def updates():
    states_data = states()
    return [
        {
            "entity_id": e.get("entity_id"),
            "state": e.get("state"),
            "friendly_name": e.get("attributes", {}).get("friendly_name"),
            "latest_version": e.get("attributes", {}).get("latest_version"),
            "installed_version": e.get("attributes", {}).get("installed_version"),
            "release_summary": e.get("attributes", {}).get("release_summary"),
        }
        for e in states_data
        if e.get("entity_id", "").startswith("update.")
    ]
