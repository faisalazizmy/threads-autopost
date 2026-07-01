import requests
import time
import sys
import os
from datetime import datetime

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = "36445274191783117"

THREADS = {
    "Monday": {
        "hook": "upah pertama aku buat kerja? roti dan air. dan aku buat dengan sepenuh hati.",
        "replies": [
            "kawan aku yang minta tolong. dia tak ada bajet, aku pun tak kisah. masa tu portfolio aku kosong. satu contoh pun takde. kerja free tu jadi satu-satunya contoh yang aku ada.",
            "dari kerja tu je aku dapat kerja lain. kawan tu refer aku ke kawan dia. kawan dia refer ke tempat lain. bola mula bergolek dari satu kerja yang upahnya roti dan air.",
            "benda yang aku belajar: first job bukan pasal bayaran. pasal kau ada sesuatu untuk tunjuk bila orang tanya ada contoh kerja tak. kalau takde, susah nak maju. kalau ada satu pun, tu dah cukup untuk start.",
        ]
    },
    "Tuesday": {
        "hook": "aku pergi interview kerja pertama aku dengan bawa hardisk. takde resume cantik. takde sijil nak tunjuk.",
        "replies": [
            "aku prepare benda lain je masa tu. kumpul semua kerja yang pernah aku buat, masukkan dalam hardisk. bukan banyak pun. tapi ada.",
            "masa interview, aku tak banyak cakap pasal background. aku terus tunjuk kerja dalam hardisk. diorang tengok, diam sekejap, pastu tanya bila boleh start.",
            "tu la kali pertama aku sedar. orang yang nak hire kau tak kisah sangat kau belajar kat mana atau result exam berapa. diorang nak tengok kau boleh buat apa. portfolio tu bahasa yang semua orang faham.",
        ]
    },
    "Wednesday": {
        "hook": "dulu aku tak tahu nak describe diri aku sebagai apa. design ke, web ke, animation ke, game ke. semua aku buat.",
        "replies": [
            "bila orang tanya kau buat apa, aku cakap je freelancer. sebab aku sendiri pun tak tahu nak explain lebih. ada masa buat design, ada masa buat web, ada masa buat animation. ambil je apa yang datang.",
            "masalahnya setiap client kenal aku beza. ada yang ingat aku orang design. ada yang ingat aku orang web. takde seorang pun yang ada gambaran penuh pasal apa yang aku sebenarnya buat.",
            "dan bila nak promote diri sendiri pun susah. nak letak apa dalam bio? nak highlight kerja mana dulu? portfolio nampak bersepah sebab memang bersepah. ni masalah yang ramai freelancer dengan minat banyak benda hadapi tapi jarang cakap pasal.",
        ]
    },
    "Thursday": {
        "hook": "aku pernah buat kerja yang bayarannya tak seberapa tapi aku habiskan masa lagi banyak dari yang sepatutnya.",
        "replies": [
            "client tu bayar murah. aku terima sebab aku genuinely minat nak buat projek tu. lepas terima, aku cuba tools yang dah lama nak explore. polish sampai rasa puas hati sendiri, bukan sekadar cukup-cukup je.",
            "client dapat hasil lagi bagus dari expectation diorang. aku dapat experience dari tools baru yang aku explore. dan kerja tu jadi salah satu yang paling kuat dalam portfolio aku.",
            "ramai kata jangan jual murah. aku faham logic tu. tapi ada situasi di mana kerja bagi kau lebih dari sekadar duit. kau kena tahu bezakan mana yang jual diri, mana yang invest dalam diri sendiri.",
        ]
    },
    "Friday": {
        "hook": "lepas bertahun buat macam-macam, akhirnya aku jumpa satu benda yang boleh ikat semua minat aku sekali.",
        "replies": [
            "bukan senang nak jumpa. aku explore dulu, buat banyak benda, nampak pattern apa yang aku enjoy paling banyak dan apa yang orang minta paling kerap. dari situ baru nampak satu servis yang make sense.",
            "ambil masa nak fokus kat satu benda tu je. rasa macam rugi sebab kena tinggalkan yang lain. tapi bila dah fokus, marketing jadi senang. orang senang nak ingat kau untuk apa.",
            "sekarang bila orang sebut servis tu, diorang ingat nama aku. bukan sebab aku seorang je yang buat. tapi sebab aku konsisten dan orang dah associate nama aku dengan benda tu. tu power fokus.",
        ]
    },
    "Saturday": {
        "hook": "aku masih buat project yang takde siapa bayar. sampai sekarang.",
        "replies": [
            "bukan sebab takde kerja. ada je. tapi personal project adalah cara aku kekal sharp dan kekal excited dengan kerja aku. bila buat untuk diri sendiri, takde constraint. boleh explore sesuka hati.",
            "dari personal project inilah aku selalu jumpa teknik baru, tools baru, cara baru nak selesaikan masalah. lepas tu bila apply kat kerja client, quality naik.",
            "kalau kau tunggu client dulu baru nak belajar benda baru, kau akan selalu satu langkah di belakang. buat dulu untuk diri sendiri. client datang kemudian.",
        ]
    },
    "Sunday": {
        "hook": "aku bukan share pasal freelance sebab aku dah figure out semua benda. aku share sebab aku masih dalam proses.",
        "replies": [
            "mula dengan kerja free upah roti dan air. interview dengan hardisk. bertahun buat macam-macam sampai tak tahu describe diri sendiri apa. portfolio bersepah. referral je datang, tak ada cara nak control.",
            "perlahan-lahan jumpa fokus. jumpa satu servis yang make sense. tapi consistency masih jadi cabaran. masih ada bulan yang senyap. masih ada masa nak procrastinate.",
            "aku rasa ramai yang sama situasi dengan aku. skill ada, minat ada, tapi tak tahu nak arah ke mana atau macam mana nak jadi consistent. kita sama je sebenarnya. kita figure out sama-sama.",
        ]
    },
}

def post_thread():
    today = datetime.now().strftime("%A")
    if today not in THREADS:
        print(f"Tiada thread untuk {today}")
        return

    thread = THREADS[today]
    hook = thread["hook"]
    replies = thread["replies"]

    r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", data={
        "media_type": "TEXT",
        "text": hook,
        "access_token": ACCESS_TOKEN
    })
    cid = r.json().get("id")
    if not cid:
        print(f"Gagal hook: {r.json()}")
        save_log(hook, "thread", today, "fail")
        return
    time.sleep(8)
    r2 = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish", data={
        "creation_id": cid,
        "access_token": ACCESS_TOKEN
    })
    main_id = r2.json().get("id")
    if not main_id:
        print(f"Gagal publish hook: {r2.json()}")
        save_log(hook, "thread", today, "fail")
        return
    print(f"[{datetime.now()}] Hook posted: {main_id}")
    save_log(hook, "thread", today, "ok", main_id)

    for i, reply_text in enumerate(replies):
        time.sleep(15)
        r3 = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", data={
            "media_type": "TEXT",
            "text": reply_text,
            "reply_to_id": main_id,
            "access_token": ACCESS_TOKEN
        })
        rcid = r3.json().get("id")
        if not rcid:
            print(f"Gagal reply {i+1}: {r3.json()}")
            continue
        time.sleep(15)
        r4 = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish", data={
            "creation_id": rcid,
            "access_token": ACCESS_TOKEN
        })
        print(f"Reply {i+1} posted: {r4.json().get('id')}")
        time.sleep(10)

def save_log(text, slot, day, status, post_id=None):
    import json
    log_file = "log.json"
    logs = []
    if os.path.exists(log_file):
        with open(log_file) as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    entry = {
        "time": datetime.utcnow().isoformat(),
        "day": day,
        "slot": slot,
        "text": text,
        "status": status
    }
    if post_id:
        entry["post_id"] = post_id
    logs.append(entry)
    with open(log_file, "w") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def already_posted_thread(day):
    import json
    log_file = "log.json"
    if not os.path.exists(log_file):
        return False
    with open(log_file) as f:
        try:
            logs = json.load(f)
        except:
            return False
    return any(l.get("slot") == "thread" and l.get("day") == day and l.get("status") == "ok" for l in logs)

today_check = datetime.now().strftime("%A")
if already_posted_thread(today_check):
    print(f"Thread untuk {today_check} dah dipost hari ni — skip.")
else:
    post_thread()
