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

def parse_metric(item):
    if "total_value" in item:
        return item["total_value"].get("value", 0)
    elif "values" in item and item["values"]:
        return item["values"][0].get("value", 0)
    return 0

def fetch_insights(logs):
    updated = False
    for entry in logs:
        post_id = entry.get("post_id")
        if not post_id or entry.get("status") != "ok":
            continue

        # insights endpoint — views, reposts, quotes
        r = requests.get(
            f"https://graph.threads.net/v1.0/{post_id}/insights",
            params={"metric": "views,reposts,quotes", "access_token": ACCESS_TOKEN}
        )
        for item in r.json().get("data", []):
            name = item.get("name")
            if name:
                entry[name] = parse_metric(item)

        # media fields — likes dan replies ada direct field
        r2 = requests.get(
            f"https://graph.threads.net/v1.0/{post_id}",
            params={"fields": "like_count,replies_count", "access_token": ACCESS_TOKEN}
        )
        media = r2.json()
        if "like_count" in media:
            entry["likes"] = media["like_count"]
        if "replies_count" in media:
            entry["replies"] = media["replies_count"]

        updated = True
        print(f"{post_id}: views={entry.get('views',0)} likes={entry.get('likes',0)} replies={entry.get('replies',0)} reposts={entry.get('reposts',0)}")

    return updated

logs = load_logs()
changed = backfill_post_ids(logs)
changed |= fetch_insights(logs)

if changed:
    save_logs(logs)
    print("log.json dikemaskini.")
else:
    print("Tiada perubahan.")
