from providers.operations import history

def _set(items):
    return set(str(x) for x in (items or []))

def compare_latest():
    current = history.latest_payload()
    previous = history.previous_payload()

    if not current:
        return {
            "available": False,
            "reason": "Nu există încă snapshot-uri în istoric.",
        }

    if not previous:
        return {
            "available": False,
            "reason": "Există un singur snapshot. Mai rulează sysadmin încă o dată pentru comparație.",
            "current": {
                "status": current.get("status"),
                "score": current.get("score"),
            },
        }

    cur_critical = _set(current.get("critical"))
    prev_critical = _set(previous.get("critical"))

    cur_warnings = _set(current.get("warnings"))
    prev_warnings = _set(previous.get("warnings"))

    return {
        "available": True,
        "score": {
            "previous": previous.get("score"),
            "current": current.get("score"),
            "delta": (current.get("score") or 0) - (previous.get("score") or 0),
        },
        "status": {
            "previous": previous.get("status"),
            "current": current.get("status"),
            "changed": previous.get("status") != current.get("status"),
        },
        "critical": {
            "new": sorted(cur_critical - prev_critical),
            "resolved": sorted(prev_critical - cur_critical),
            "unchanged": sorted(cur_critical & prev_critical),
        },
        "warnings": {
            "new": sorted(cur_warnings - prev_warnings),
            "resolved": sorted(prev_warnings - cur_warnings),
            "unchanged": sorted(cur_warnings & prev_warnings),
        },
    }
