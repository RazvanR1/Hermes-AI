import json
import os
import time

import requests


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API = os.getenv("HERMES_API_URL", "http://127.0.0.1:8088")

if not TOKEN:
    raise SystemExit("Missing TELEGRAM_BOT_TOKEN")

offset = None

print("telegram poller started", flush=True)

while True:
    try:
        params = {
            "timeout": 20,
            "allowed_updates": json.dumps([
                "message",
                "callback_query",
            ]),
        }

        if offset is not None:
            params["offset"] = offset

        response = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        payload = response.json()

        if not payload.get("ok"):
            print(f"Telegram error: {payload}", flush=True)
            time.sleep(5)
            continue

        updates = payload.get("result", [])

        if updates:
            print(f"got {len(updates)} update(s)", flush=True)

        for update in updates:
            offset = update["update_id"] + 1

            if "callback_query" in update:
                callback_data = update["callback_query"].get("data")
                print(f"callback: {callback_data}", flush=True)
            elif "message" in update:
                text = update["message"].get("text")
                print(f"message: {text}", flush=True)
            else:
                print(f"update keys: {list(update.keys())}", flush=True)

            webhook_response = requests.post(
                f"{API}/telegram/v8/webhook",
                json=update,
                timeout=120,
            )

            print(
                f"webhook status: {webhook_response.status_code} "
                f"{webhook_response.text[:1000]}",
                flush=True,
            )

    except Exception as exc:
        print(f"telegram poller error: {exc}", flush=True)
        time.sleep(5)
