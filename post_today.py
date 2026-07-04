import requests
import time
import sys
import os
import json
from datetime import datetime, timedelta

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = os.environ.get("THREADS_USER_ID", "36445274191783117")
LOG_FILE = "log.json"
PAGES_BASE = "https://faisalazizmy.github.io/threads-autopost/"

with open("queue.json") as f:
    POSTS_QUEUE = json.load(f)

# map: idx (str) -> cover image path, kalau content tu ada gambar
COVERS = {}
if os.path.exists("covers.json"):
    with open("covers.json") as f:
        try:
            COVERS = json.load(f)
        except:
            COVERS = {}

def my_now():
    return datetime.utcnow() + timedelta(hours=8)

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE) as f:
        try:
            return json.load(f)
        except:
            return []

def save_log(text, slot, status, idx, post_id=None):
    logs = load_logs()
    now = my_now()
    entry = {
        "time": datetime.utcnow().isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A"),
        "slot": slot,
        "idx": idx,
        "text": text,
        "status": status
    }
    if post_id:
        entry["post_id"] = post_id
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def already_posted_today(slot, logs):
    today = my_now().strftime("%Y-%m-%d")
    return any(l.get("date") == today and l.get("slot") == slot and l.get("status") == "ok" for l in logs)

def next_idx(logs):
    posted = {l.get("idx") for l in logs if l.get("status") == "ok" and l.get("idx") is not None}
    for i in range(len(POSTS_QUEUE)):
        if i not in posted:
            return i
    return None

def post(text, slot, idx):
    cover = COVERS.get(str(idx))
    if cover:
        # post gambar (cover) + caption
        image_url = PAGES_BASE + cover
        data = {
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": text,
            "access_token": ACCESS_TOKEN
        }
        print(f"Post dengan gambar: {image_url}")
    else:
        data = {
            "media_type": "TEXT",
            "text": text,
            "access_token": ACCESS_TOKEN
        }
    r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", data=data)
    cid = r.json().get("id")
    if not cid:
        print(f"Gagal create: {r.json()}")
        save_log(text, slot, "fail", idx)
        return
    time.sleep(5)
    r2 = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish", data={
        "creation_id": cid,
        "access_token": ACCESS_TOKEN
    })
    post_id = r2.json().get("id")
    if post_id:
        print(f"[{datetime.now()}] Berjaya post — queue #{idx+1} ({slot})")
        save_log(text, slot, "ok", idx, post_id)
    else:
        print(f"Gagal publish: {r2.json()}")
        save_log(text, slot, "fail", idx)

slot = sys.argv[1] if len(sys.argv) > 1 else None
force_idx = sys.argv[2].strip() if len(sys.argv) > 2 and sys.argv[2].strip() != "" else None

def already_posted_idx(idx, logs):
    return any(l.get("idx") == idx and l.get("status") == "ok" for l in logs)

if slot not in ("pagi", "malam"):
    print("Sila masukkan slot: pagi / malam")
else:
    logs = load_logs()
    if force_idx is not None:
        # Post content spesifik ikut nombor queue (manual pick dari dashboard)
        try:
            idx = int(force_idx)
        except ValueError:
            print(f"force_idx tak sah: {force_idx}")
            sys.exit(0)
        if idx < 0 or idx >= len(POSTS_QUEUE):
            print(f"force_idx di luar julat queue: {idx}")
        elif already_posted_idx(idx, logs):
            print(f"Content #{idx+1} dah dipost sebelum ni — skip.")
        else:
            post(POSTS_QUEUE[idx], slot, idx)
    elif already_posted_today(slot, logs):
        print(f"Slot '{slot}' hari ni dah dipost — skip.")
    else:
        idx = next_idx(logs)
        if idx is None:
            print("Queue habis — tiada content baru untuk dipost.")
        else:
            post(POSTS_QUEUE[idx], slot, idx)
