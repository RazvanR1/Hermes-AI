def format_rootcause(rc):
    if not rc:
        return "Nu există informații."

    lines = []

    lines.append("🧠 Root Cause Analysis")
    lines.append("")

    lines.append(f"Serviciu: {rc.get('entity','-')}")
    lines.append(f"Încredere: {rc.get('confidence',0)}%")
    lines.append("")

    lines.append("Cauză probabilă:")
    lines.append(f"  {rc.get('root_cause')}")
    lines.append("")

    evidence = rc.get("evidence", [])
    if evidence:
        lines.append("Observații:")
        for e in evidence:
            lines.append(f"  • {e}")
        lines.append("")

    chain = rc.get("chain", [])
    if chain:
        lines.append("Lanț dependențe:")

        for item in chain:
            if "component" in item:
                lines.append(f"  → {item['component']}")
            elif "node" in item:
                lines.append(f"  → {item['node'].get('name')}")
            elif "provider" in item:
                lines.append(f"  → {item['provider']}")
            elif "edge" in item:
                lines.append(
                    f"  → {item['edge'].get('relation')} ({item['edge'].get('target')})"
                )

        lines.append("")

    return "\n".join(lines)
