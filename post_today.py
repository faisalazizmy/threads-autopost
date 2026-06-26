import requests
import time
import sys
import os
from datetime import datetime

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = os.environ.get("THREADS_USER_ID", "36445274191783117")

POSTS = {
    "Monday": {
        # angle: zero dari awal — soalan trigger
        "pagi": "korang pernah tak terfikir nak buat duit sendiri dari rumah tapi tak tahu nak buat apa. bukan takde idea, tapi terlalu banyak idea sampai tak buat apa-apa pun.",

        # angle: ada skill tapi tak tahu jual — myth bust
        "tengahari": "kau dah tahu buat benda ni. dah buat untuk diri sendiri, untuk kawan, untuk suka-suka. tapi bila ada orang tanya berapa harga, kau blank. bukan sebab tak tahu buat. sebab tak tahu macam mana nak letak nilai kat benda yang kau buat.",

        # angle: dua-dua — actionable
        "malam": "tak kisah kau ada skill ke tak lagi, langkah pertama sama je. kena tahu dulu kau nak bantu siapa dan masalah apa yang kau boleh selesaikan. tanpa tu, semua benda lain jadi hentam keromo.",
    },

    "Tuesday": {
        # angle: zero dari awal — soalan survival
        "pagi": "kalau kau kena cari RM500 dalam masa seminggu guna laptop je, tanpa keluar rumah, tanpa modal, kau akan buat apa?",

        # angle: ada skill tapi tak tahu jual — relatable
        "tengahari": "ramai yang dah ada skill digital tapi masih apply kerja gaji RM1,500. bukan sebab skill tu tak bernilai. sebab tak tahu macam mana nak charge RM1,500 untuk satu projek je.",

        # angle: dua-dua — contrast
        "malam": "orang yang dapat client bukan selalu yang paling pandai. selalu yang paling berani offer diri dulu. skill boleh improve sambil jalan. keberanian nak start tu yang susah nak datang kalau kau tunggu.",
    },

    "Wednesday": {
        # angle: dua-dua — soalan buat orang nak reply
        "pagi": "apa yang paling buat korang rasa takut nak mula buat duit sendiri secara digital? takut tak laku, tak tahu nak start, atau benda lain?",

        # angle: zero dari awal — myth bust
        "tengahari": "tak ada skill pun boleh mula sekarang. pilih satu benda yang kau nak belajar, luangkan 2 jam sehari, dalam 3 bulan kau dah boleh charge orang. yang penting pilih satu je dulu. jangan cuba belajar semua sekali.",

        # angle: ada skill tapi tak tahu jual — tip konkrit
        "malam": "kalau tak tahu nak charge berapa, cara paling mudah adalah tengok orang lain dalam niche yang sama charge apa. ambik tengah-tengah tu sebagai starting point. jangan letak paling murah sebab nak menarik client. client yang datang sebab murah paling susah nak handle.",
    },

    "Thursday": {
        # angle: ada skill tapi tak tahu jual — soalan insecurity
        "pagi": "pernah tak rasa skill kau tu biasa je, sampai rasa tak layak charge mahal. lepas tu tengok orang lain dengan skill sama charge 3x ganda dan client pun ada.",

        # angle: zero dari awal — straight truth
        "tengahari": "belajar skill digital sekarang lagi senang dari 10 tahun dulu. semua ada kat YouTube, percuma. yang susahnya bukan belajar. yang susahnya nak duduk diam 2 jam sehari buat benda yang belum nampak hasilnya lagi.",

        # angle: dua-dua — story dua karakter
        "malam": "dua orang start freelance sama masa. sorang buat research 3 bulan dulu, tunggu semua perfect. sorang lagi terus hantar offer, kena reject, hantar lagi, dapat client minggu ketiga. yang dapat client tu bukan lagi pandai. dia just tak tunggu ready.",
    },

    "Friday": {
        # angle: dua-dua — soalan visualize
        "pagi": "kalau kau boleh buat RM3,000 sebulan dari rumah guna laptop, skill apa yang kau rasa paling berpotensi untuk kau belajar atau jual sekarang?",

        # angle: ada skill tapi tak tahu jual — myth bust
        "tengahari": "tak perlu website cantik, logo professional, atau business card untuk start ambik client. client nak tahu satu benda je. boleh ke kau selesaikan masalah diorang. yang lain-lain tu hiasan je, boleh datang kemudian.",

        # angle: dua-dua — tip tiga benda
        "malam": "tiga benda yang buat client pilih kau walaupun kau baru start. kau faham masalah diorang sebelum diorang habis explain. kau balas mesej dengan cepat dan jelas. kau buat apa yang kau janji. skill boleh improve. tiga benda ni boleh buat dari hari pertama.",
    },

    "Saturday": {
        # angle: dua-dua — soalan hot buat orang nak share opinion
        "pagi": "setuju tak, ramai Malaysian ada skill tapi takut nak promote diri sendiri. apa yang buat korang rasa macam tu?",

        # angle: zero dari awal — validate perasaan lepas tu flip
        "tengahari": "rasa macam semua orang dah jauh depan tu normal. diorang dah ada client, dah ada income. padahal 6 bulan lepas diorang pun duduk tempat yang sama dengan kau sekarang. bezanya diorang tak berhenti kat rasa tu.",

        # angle: ada skill tapi tak tahu jual — contrast
        "malam": "ada dua jenis orang dengan skill yang sama. yang pertama tunggu orang perasan dia pandai. yang kedua pergi bagitau orang dia boleh buat apa. result diorang jauh berbeza bukan sebab skill berbeza. sebab satu visible, satu invisible.",
    },

    "Sunday": {
        # angle: dua-dua — soalan ringan positif
        "pagi": "kalau dapat RM1,000 pertama dari skill digital korang, benda pertama apa yang korang nak buat dengan duit tu?",

        # angle: dua-dua — relatable closing
        "tengahari": "tak ada skill pun okay. ada skill tapi tak tahu jual pun okay. dua-dua boleh selesai. yang tak okay adalah bila kau dah tahu kau nak buat sesuatu tapi kau biarkan hari berlalu macam tu je.",

        # angle: dua-dua — closing minggu penuh value
        "malam": "seminggu kita cakap banyak benda. tapi kalau nak simplify jadi satu, pilih satu skill, bagitau satu orang kau boleh bantu diorang dengan skill tu, dan tengok apa jadi. bukan plan panjang yang kau perlukan sekarang. kau perlukan satu langkah kecil yang betul.",
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

def post(text, slot, day):
    r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", data={
        "media_type": "TEXT",
        "text": text,
        "access_token": ACCESS_TOKEN
    })
    cid = r.json().get("id")
    if not cid:
        print(f"Gagal create: {r.json()}")
        save_log(text, slot, day, "fail")
        return
    time.sleep(5)
    r2 = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish", data={
        "creation_id": cid,
        "access_token": ACCESS_TOKEN
    })
    post_id = r2.json().get("id")
    if post_id:
        print(f"[{datetime.now()}] Berjaya post — {day} {slot}")
        save_log(text, slot, day, "ok", post_id)
    else:
        print(f"Gagal publish: {r2.json()}")
        save_log(text, slot, day, "fail")

def already_posted(slot, day):
    import json
    log_file = "log.json"
    if not os.path.exists(log_file):
        return False
    with open(log_file) as f:
        try:
            logs = json.load(f)
        except:
            return False
    return any(l.get("slot") == slot and l.get("day") == day and l.get("status") == "ok" for l in logs)

today = datetime.now().strftime("%A")
slot = sys.argv[1] if len(sys.argv) > 1 else None

if not slot:
    print("Sila masukkan slot: pagi / tengahari / malam")
elif today not in POSTS:
    print(f"Tiada post untuk hari {today}")
elif slot not in POSTS[today]:
    print(f"Slot '{slot}' tidak wujud.")
elif already_posted(slot, today):
    print(f"Slot '{slot}' untuk {today} dah dipost hari ni — skip.")
else:
    post(POSTS[today][slot], slot, today)
