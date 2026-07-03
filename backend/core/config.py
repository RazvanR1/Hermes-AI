import os
from pathlib import Path

ENV_FILES = [
    "/etc/default/hermes",
    "/home/hermes/.hermes/.env",
    "/home/hermes/.opnsense.env",
]

class Config:
    def __init__(self):
        self._loaded = False
        self._values = {}

    def load(self):
        if self._loaded:
            return self

        for path in ENV_FILES:
            self._load_file(path)

        for key, value in os.environ.items():
            self._values[key] = value

        self._loaded = True
        return self

    def _load_file(self, path):
        p = Path(path)
        if not p.exists():
            return

        for raw in p.read_text(errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in self._values:
                self._values[key] = value
                os.environ.setdefault(key, value)

    def get(self, key, default=None):
        self.load()
        return self._values.get(key, default)

    def require(self, key):
        value = self.get(key)
        if not value:
            raise RuntimeError(f"Lipsește variabila {key}")
        return value

    def validate(self):
        groups = {
            "proxmox": ["PROXMOX_HOST", "PROXMOX_USER", "PROXMOX_TOKEN_NAME", "PROXMOX_TOKEN_VALUE"],
            "homeassistant": ["HOMEASSISTANT_URL", "HOMEASSISTANT_TOKEN"],
            "truenas": ["TRUENAS_URL", "TRUENAS_API_KEY"],
            "opnsense": ["OPNSENSE_URL", "OPNSENSE_KEY", "OPNSENSE_SECRET"],
            "docker": ["DOCKER_SSH_TARGET"],
        }
        out = {}
        for group, keys in groups.items():
            missing = [k for k in keys if not self.get(k)]
            out[group] = {
                "ok": not missing,
                "missing": missing,
                "configured": [k for k in keys if self.get(k)],
            }
        return out

config = Config()
