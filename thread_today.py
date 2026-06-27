import requests
import time
import sys
import os
from datetime import datetime

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = "36445274191783117"

THREADS = {
    "Monday": {
        "hook": "cara dapat client pertama tanpa pengalaman, tanpa portfolio, tanpa keluar rumah.",
        "replies": [
            "1. tak perlu portfolio sempurna. buat satu kerja free untuk orang yang kau kenal dulu. screenshot hasilnya. tu dah jadi bukti kau boleh buat kerja. client nak tengok proof, bukan sijil.",
            "2. jangan terus pergi platform macam Fiverr atau Upwork. pergi dulu kat group facebook dalam niche kau. tengok masalah orang, offer bantuan. orang hire orang yang diorang dah kenal, bukan stranger.",
            "3. bila dah ready nak offer servis, jangan mesej \"ada kerja tak untuk saya?\" cuba \"saya nampak awak ada masalah ni, saya boleh bantu.\" beza cara tanya tu je yang tentukan dapat client atau tak.",
        ]
    },
    "Tuesday": {
        "hook": "skill ada, masa ada, laptop ada. tapi income dari freelance masih sifar. masalahnya bukan skill. masalahnya tak tahu nak buat apa dulu.",
        "replies": [
            "1. langkah pertama bukan cari client. tentukan dulu kau nak bantu siapa. graphic designer untuk siapa? content writer untuk industri apa? lagi specific lagi senang orang ingat kau.",
            "2. lepas tahu target, buat satu contoh kerja untuk niche tu walaupun takda client lagi. kalau kau nak buat social media untuk F&B, buat mock post untuk kedai makan yang kau suka. tu dah jadi portfolio.",
            "3. lepas ada contoh kerja, pergi kat tempat target kau ada. group facebook, forum, community. tunjuk kerja kau kat sana. bukan jual dulu, tunjuk dulu.",
        ]
    },
    "Wednesday": {
        "hook": "tak ada skill pun boleh start freelance. tapi kena tahu dulu nak belajar apa.",
        "replies": [
            "1. pilih skill berdasarkan dua benda. kau ada minat ke, dan ada orang yang nak bayar ke. kalau ada dua-dua, go ahead. kalau ada satu je, fikir balik.",
            "2. skill digital yang paling mudah dapat client pertama untuk pemula adalah content writing, data entry, dan social media management. tak perlu software mahal, tak perlu kursus bertahun.",
            "3. luangkan 2 jam sehari untuk belajar. dalam masa 6 minggu kau dah boleh buat kerja basic. dalam masa 3 bulan kau dah boleh charge orang. kuncinya konsisten, bukan belajar laju.",
        ]
    },
    "Thursday": {
        "hook": "ramai freelancer baru buat kesilapan yang sama bila set harga. dan kesilapan tu yang buat diorang penat tapi tak kaya.",
        "replies": [
            "1. jangan charge ikut masa. charge ikut value. kalau kau boleh selesaikan masalah client dalam 2 jam yang diorang dah struggle 2 minggu, 2 jam tu bernilai lebih dari RM50.",
            "2. tengok harga orang lain dalam niche sama sebagai reference, bukan standard. kau boleh charge lagi tinggi kalau kau communicate value kau dengan betul.",
            "3. bila client kata mahal, jangan terus turun harga. tanya dulu \"bajet awak berapa?\" kadang diorang ada bajet lebih, tapi nak test je kau akan turun ke tak.",
            "4. letak harga dengan confident. kalau kau sendiri rasa tak yakin masa sebut harga, client akan rasa tu. yakin dulu, baru orang lain yakin.",
        ]
    },
    "Friday": {
        "hook": "cara present diri sebagai freelancer supaya client percaya kau, walaupun kau baru start.",
        "replies": [
            "1. profile kau kena cakap satu benda dengan jelas. siapa kau bantu dan apa masalah kau selesaikan. bukan \"saya freelancer\" tapi \"saya bantu bisnes kecil dapat lebih customer guna social media.\"",
            "2. bila approach client, tunjukkan kau dah buat homework. sebut nama bisnes diorang, sebut apa yang kau nampak boleh improve. orang suka orang yang perhatikan diorang.",
            "3. follow up sekali kalau takde reply dalam 3 hari. ramai client bukan ignore, tapi busy. satu follow up yang sopan dah cukup. lebih dari tu dah jadi pushy.",
        ]
    },
    "Saturday": {
        "hook": "tiga sebab kenapa orang ada skill tapi masih tak dapat client.",
        "replies": [
            "1. diorang invisible. takde sesiapa yang tahu diorang wujud dan boleh buat kerja tu. solution dia mudah je. kena visible dulu sebelum boleh dapat kerja.",
            "2. diorang tunggu. tunggu ada orang tanya, tunggu ada orang refer, tunggu masa yang sesuai. tapi dalam freelance, orang yang pergi dulu yang dapat, bukan yang tunggu.",
            "3. diorang tak specific. cuba buat semua benda untuk semua orang. client susah nak percaya generalist. tapi specialist dalam satu benda nampak lagi credible walaupun pengalaman sama.",
        ]
    },
    "Sunday": {
        "hook": "minggu ni kita belajar banyak pasal freelance. tapi aku nak tanya satu soalan je.",
        "replies": [
            "1. apa yang betul-betul tahan kau dari start lagi? bukan jawapan standard. jawapan sebenar.",
            "2. sebab ramai yang tahu apa nak buat, tapi masih tak buat. bukan sebab malas. sebab takut. takut tak cukup bagus, takut orang reject, takut buang masa.",
            "3. tapi rejection pertama tu bukan tanda kau tak layak. dia tanda kau dah start. orang yang takde rejection langsung adalah orang yang tak pernah cuba pun.",
        ]
    },
}

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

post_thread()
