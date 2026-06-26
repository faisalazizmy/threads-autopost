import requests
import json
import os

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
LOG_FILE = "log.json"

def fetch_insights():
    if not os.path.exists(LOG_FILE):
        print("log.json tidak jumpa")
        return

    with open(LOG_FILE) as f:
        logs = json.load(f)

    updated = False
    for entry in logs:
        post_id = entry.get("post_id")
        if not post_id or entry.get("status") != "ok":
            continue

        r = requests.get(
            f"https://graph.threads.net/v1.0/{post_id}/insights",
            params={
                "metric": "views,likes,replies,reposts,quotes",
                "access_token": ACCESS_TOKEN
            }
        )
        data = r.json().get("data", [])
        if not data:
            print(f"Tiada insights untuk {post_id}: {r.json()}")
            continue

        for item in data:
            name = item.get("name")
            value = item.get("total_value", {}).get("value", 0)
            if name:
                entry[name] = value
        updated = True
        print(f"Updated {post_id}: " + ", ".join(f"{i['name']}={i.get('total_value',{}).get('value',0)}" for i in data))

    if updated:
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        print("log.json dikemaskini dengan insights.")
    else:
        print("Tiada post untuk dikemaskini.")

fetch_insights()
