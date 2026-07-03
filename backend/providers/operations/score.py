def calculate(alerts):
    # Calibrated for homelab reality:
    # - SMART / degraded storage is serious, but one disk warning should not make the whole stack look dead.
    # - pending updates are maintenance, not outages.
    score = 100
    score -= len(alerts.get("critical", [])) * 18
    score -= len(alerts.get("warnings", [])) * 3
    score -= len(alerts.get("info", [])) * 1
    return max(0, min(100, score))
