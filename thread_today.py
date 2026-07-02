import requests
import time
import sys
import os
from datetime import datetime

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = "36445274191783117"

THREADS = {
    "Monday": {
        "hook": "cara aku dapat client pertama: buat kerja free untuk kawan, upah roti dan air. ni cerita penuh dia.",
        "replies": [
            "masa tu aku takde portfolio langsung. kawan aku perlukan tolong, dia takde bajet. aku buat je. bukan sebab strategik pun, sebab aku memang nak buat kerja tu. siap, aku simpan hasil dia elok-elok.",
            "hasil kerja tu jadi satu-satunya contoh yang aku ada. bila orang lain tanya boleh tengok kerja kau tak, aku ada benda nak tunjuk. dari situ kawan refer ke kawan dia, kawan dia refer ke company. bola bergolek.",
            "lesson dia bukan kerja free tu bagus. lesson dia: kau perlukan satu contoh kerja yang boleh tunjuk. macam mana kau dapat contoh tu, terpulang. tapi tanpa dia, semua pintu tertutup.\n\nkorang dapat contoh kerja pertama korang macam mana?",
        ]
    },
    "Tuesday": {
        "hook": "client tanya harga, aku tak bagi. aku ajak meeting dulu. sebab tu aku boleh charge lebih tinggi.",
        "replies": [
            "aku takde rate card khusus. sebab setiap client masalah dia lain. bila kau bagi harga sebelum faham masalah diorang, kau letak nilai kerja sendiri secara buta. jadi aku ajak online meeting 15 sampai 30 minit. aku panggil dia discovery call.",
            "dalam call tu aku buat dua benda serentak. present hasil kerja aku betul-betul, dan study business diorang. tanya apa yang aku nak tanya. dari situ trust terbina sebelum harga pun disebut lagi.",
            "habis meeting, aku terus buat custom quotation ikut apa yang aku belajar masa call tu. bukan template. client rasa quotation tu memang untuk diorang, sebab memang pun. peluang dapat project dengan cara ni sangat tinggi.\n\nkorang bagi harga terus, atau ajak meeting dulu?",
        ]
    },
    "Wednesday": {
        "hook": "bertahun aku buat animation, design, web, game. lepas tu aku jumpa satu benda yang ikat semua tu sekali.",
        "replies": [
            "masa buat semua benda tu, setiap client kenal aku beza. ada yang ingat aku orang design. ada yang ingat aku orang web. aku sendiri tak tahu nak describe diri sebagai apa. portfolio pun bersepah.",
            "aku tak terus jumpa jawapan. aku perhatikan pattern: apa yang aku paling enjoy buat, dan apa yang orang paling kerap minta dari aku. dari dua benda tu baru nampak satu servis yang boleh gabung semua minat aku.",
            "ambil masa nak fokus. rasa rugi nak tinggalkan yang lain. tapi sekarang, asal orang sebut servis tu, terus ingat nama aku. bukan sebab aku seorang je boleh buat. sebab aku konsisten dengan satu benda tu.\n\nkorang dah jumpa benda korang, atau masih explore?",
        ]
    },
    "Thursday": {
        "hook": "dulu client reject kerja aku tanpa sebab, aku terus refund. sekarang tak lagi. ni apa yang aku belajar.",
        "replies": [
            "masa awal dulu aku jenis malas nak pening kepala. client tak puas hati, refund je, move on ke next project. rasa macam professional. tapi sebenarnya aku tengah ajar client macam tu yang perangai camtu boleh dapat kerja free.",
            "lepas tu aku mula document semua benda. setiap progress, setiap request client, setiap approval. dalam whatsapp, dalam email. untuk project besar aku siap buat website khas untuk client tengok progress dan semua details.",
            "sekarang kalau client bantah, aku tak perlu argue pun. aku tunjuk record je. ni yang kita agree, ni yang kau approve, ni yang berubah. dokumentasi bukan untuk menang gaduh. dia buat kau tak payah gaduh langsung.\n\nkorang pernah kena client macam ni? macam mana handle?",
        ]
    },
    "Friday": {
        "hook": "setiap project aku buat lebih dari yang client minta. bukan untuk client tu. untuk aku sendiri.",
        "replies": [
            "sebab hasil kerja tu bukan sekadar deliverable untuk client. dia jadi portfolio aku, bahan cerita aku, dan sebab orang refer aku ke orang lain. kalau siap sekadar siap, kau dapat bayaran je. habis situ.",
            "tapi kalau siap sampai tahap showcase, kau dapat tiga benda: bayaran, portfolio yang kuat, dan client yang teruja nak cerita pasal kau kat orang lain. sebab tu hampir semua client aku sekarang datang dari referral.",
            "cara fikir dia mudah: client bayar untuk kerja tu sekali je. tapi portfolio yang terhasil, kau guna berkali-kali untuk tahun-tahun akan datang. effort lebih tu bukan free work. tu investment.\n\nkorang siapkan kerja sekadar siap, atau sampai jadi showcase?",
        ]
    },
    "Saturday": {
        "hook": "aku masih buat project yang takde siapa bayar. sampai sekarang. dan ni sebab dia.",
        "replies": [
            "bukan sebab takde kerja. ada je. tapi personal project adalah cara aku kekal sharp. bila buat untuk diri sendiri, takde constraint. boleh explore sesuka hati. sempena raya buat design sendiri. jumpa tools baru terus cuba.",
            "dari personal project la aku selalu jumpa teknik baru, tools baru, cara baru selesaikan masalah. lepas tu bila apply kat kerja client, quality naik. client tak tahu pun benda tu datang dari project suka-suka aku.",
            "kalau tunggu client dulu baru nak belajar benda baru, kau akan selalu satu langkah di belakang. buat dulu untuk diri sendiri. client datang kemudian.\n\nkorang last buat personal project bila? tunjuk sini kalau ada.",
        ]
    },
    "Sunday": {
        "hook": "aku share pasal freelance bukan sebab aku dah berjaya. aku share sebab aku masih dalam proses.",
        "replies": [
            "mula dengan kerja free upah roti dan air. interview bawa hardisk. bertahun buat macam-macam sampai tak tahu describe diri sendiri. portfolio bersepah. client datang dari referral je, tak boleh control bila.",
            "perlahan-lahan jumpa fokus. belajar buat discovery call. belajar document semua benda. belajar buat setiap project jadi showcase. tapi consistency masih jadi cabaran sampai sekarang.",
            "aku rasa ramai yang sama situasi dengan aku. skill ada, minat ada, tapi tak tahu arah mana atau macam mana nak consistent. kita figure out sama-sama.\n\napa benda paling besar korang struggle sekarang? reply, aku baca semua.",
        ]
    },
}

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
