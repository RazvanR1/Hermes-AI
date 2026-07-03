from providers.homelab import client as homelab

def run():
    try:
        return {
            "ok": True,
            "result": homelab.auto_fix(),
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }
