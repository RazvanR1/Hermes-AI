from __future__ import annotations

import json
import sys

from brain import brain


def main() -> int:
    message = " ".join(sys.argv[1:]).strip()

    if not message:
        print("Usage: python3 brain_demo.py <mesaj>")
        return 1

    context = brain.analyze(message)

    print(json.dumps(context.to_dict(), indent=2, ensure_ascii=False))
    print()
    print(brain.explain(message))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
