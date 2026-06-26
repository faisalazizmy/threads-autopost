import requests
import json
import os

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = os.environ.get("THREADS_USER_ID", "36445274191783117")
LOG_FILE = "log.json"

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE) as f:
        try:
            return json.load(f)
        except:
            return []

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def backfill_post_ids(logs):
    missing = [l for l in logs if l.get("status") == "ok" and not l.get("post_id")]
    if not missing:
        print("Tiada log yang perlu backfill.")
        return False

    print(f"Backfill {len(missing)} entries...")
    r = requests.get(
        f"https://graph.threads.net/v1.0/{USER_ID}/threads",
        params={
            "fields": "id,text,timestamp",
            "limit": 50,
            "access_token": ACCESS_TOKEN
        }
    )
    threads = r.json().get("data", [])
    if not threads:
        print(f"Gagal fetch threads: {r.json()}")
        return False

    updated = False
    for entry in missing:
        log_text = entry.get("text", "").strip()
        for t in threads:
            thread_text = (t.get("text") or "").strip()
            if log_text and (log_text in thread_text or thread_text in log_text or log_text[:60] == thread_text[:60]):
                entry["post_id"] = t["id"]
                print(f"Matched: {t['id']} → {log_text[:50]}...")
                updated = True
                break

    return updated

def fetch_insights(logs):
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
            # Threads API returns either total_value or values[] format
            if "total_value" in item:
                value = item["total_value"].get("value", 0)
            elif "values" in item and item["values"]:
                value = item["values"][0].get("value", 0)
            else:
                value = 0
            if name:
                entry[name] = value
        updated = True
        stats = ", ".join(f"{i['name']}={i.get('total_value', {}).get('value') or (i.get('values') or [{}])[0].get('value', 0)}" for i in data)
        print(f"Insights {post_id}: {stats}")

    return updated

logs = load_logs()
changed = backfill_post_ids(logs)
changed |= fetch_insights(logs)

if changed:
    save_logs(logs)
    print("log.json dikemaskini.")
else:
    print("Tiada perubahan.")
