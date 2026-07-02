import requests
import time
import sys
import os
from datetime import datetime

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
USER_ID = os.environ.get("THREADS_USER_ID", "36445274191783117")

POSTS = {
    "Monday": {
        # cerita: first job roti dan air
        "pagi": "upah pertama aku: roti dan air.\n\nclient pertama tu kawan aku sendiri. dia takde duit. aku pun tak kisah, sebab aku just nak buat kerja tu.\n\ntapi dari kerja tu aku ada portfolio pertama aku. satu contoh je. cukup untuk dapat client seterusnya.\n\nkorang punya first job dulu macam mana?",

        # cerita: mula suka-suka
        "malam": "aku tak start freelance dengan target nak jadi fulltime pun.\n\njust nak duit lebih. buat bila ada masa lapang. takde tekanan.\n\ntapi sebab buat dengan enjoy, kerja jadi lagi baik. client happy, dapat refer ke orang lain.\n\nkorang start freelance sebab apa? duit, minat, atau terpaksa?",
    },

    "Tuesday": {
        # cerita: interview bawa hardisk
        "pagi": "interview kerja pertama aku, aku bawa hardisk.\n\ntakde resume cantik. takde sijil nak tunjuk. aku terus tunjuk kerja dari situ.\n\ndiorang tengok, diam sekejap, terus tanya bila boleh start.\n\nkorang pernah dapat kerja sebab portfolio, bukan sebab resume?",

        # cerita: sijil decoration
        "malam": "aku tak pernah dapat kerja sebab sijil.\n\nselalu sebab orang tengok kerja aku terus. sijil aku ada. tapi tak pernah jadi faktor pun.\n\nkalau kau ada kerja yang boleh tunjuk, sijil jadi decoration je.\n\nsetuju ke tak? aku nak dengar pendapat korang.",
    },

    "Wednesday": {
        # cerita: minat banyak benda
        "pagi": "masalah aku dulu: aku minat buat banyak benda.\n\nanimation, game, design, web. semua aku cuba. semua aku ambil kalau ada orang tanya.\n\nrasa macam bagus sebab serba boleh. tapi bila orang tanya aku buat apa, aku jawab freelancer je. generic. tak ada siapa ingat.\n\nkorang jenis fokus satu benda ke minat banyak benda macam aku?",

        # cerita: portfolio bersepah
        "malam": "portfolio aku dulu bersepah.\n\nbuat macam-macam, letak semua sekali, nampak takde arah. macam kedai yang jual segalanya tapi takde specialty.\n\nclient yang datang pun random. nak market diri sendiri pun tak tahu nak highlight apa.\n\nkorang pernah tengok balik portfolio sendiri dan rasa macam ni?",
    },

    "Thursday": {
        # cerita: kerja murah tapi buat 100%
        "pagi": "aku pernah ambil kerja murah sebab minat sangat nak buat.\n\nbayaran tak seberapa. tapi aku buat lebih 100%. explore tools baru, polish sampai puas hati sendiri.\n\nkerja tu jadi showcase terbaik dalam portfolio aku. dan dari situ dapat tawaran lagi tinggi.\n\npernah tak korang buat kerja yang usaha lebih dari bayaran? berbaloi ke?",

        # cerita: referral tak consistent
        "malam": "hampir semua client aku datang dari referral.\n\nkawan refer. company lama refer. orang yang pernah tengok kerja aku refer. aku tak pergi cari pun.\n\ntapi masalahnya referral tak consistent. ada bulan banyak, ada bulan senyap. dan aku tak boleh control bila diorang datang.\n\nkorang punya client selalu datang dari mana?",
    },

    "Friday": {
        # cerita: minat jadi kelebihan
        "pagi": "sebab aku minat, aku tak rasa penat walaupun kerja lama.\n\norang lain kena paksa buat overtime. aku buat overtime sendiri sebab nak polish lagi.\n\nbukan semua orang ada benda tu. dan bila client nampak perbezaan tu, diorang ingat kau.\n\nkorang pernah tak sedar dah kerja berjam-jam sebab seronok?",

        # cerita: known for one thing
        "malam": "perasaan bila orang mula associate nama kau dengan satu benda, lain macam sikit.\n\ndulu orang tanya aku buat apa, aku explain panjang. diorang confused.\n\nlepas aku fokus satu benda, aku jawab satu ayat je. diorang faham terus.\n\nkalau korang kena describe diri korang dalam satu ayat, apa ayat dia?",
    },

    "Saturday": {
        # cerita: hot take pasal minat
        "pagi": "orang selalu kata jangan buat kerja yang kau suka, nanti hilang minat.\n\naku tak setuju.\n\naku buat kerja yang aku minat dari dulu sampai sekarang. sebab tu aku boleh buat lagi baik dari orang yang buat sebab duit je.\n\nminat tak hilang bila kau buat kerja. minat hilang bila kau buat kerja yang salah.\n\nkorang team mana: kerja ikut minat, atau minat jangan jadikan kerja?",

        # cerita: struggle consistency
        "malam": "benda paling aku struggle sampai sekarang bukan skill.\n\nbukan cari client. bukan bayaran. tapi consistency.\n\nada masa aku productive gila, siap kerja berlambak. ada masa aku procrastinate sampai deadline dah dekat baru gerak.\n\nkorang struggle dengan apa paling banyak? jom confess sini.",
    },

    "Sunday": {
        # cerita: nasihat untuk diri sendiri dulu
        "pagi": "kalau boleh balik masa, aku nak cakap satu benda je dengan diri sendiri yang dulu.\n\nfokus lagi awal.\n\nbukan maksud tak boleh explore. explore kena. tapi kena ada satu anchor yang ikat semua tu. tanpa anchor, kau spend bertahun buat banyak benda tapi tak pergi mana.\n\nkorang nak cakap apa dengan diri sendiri 5 tahun lepas?",

        # cerita: spark — closing minggu
        "malam": "spark aku datang dari dua benda yang berlaku serentak.\n\nmak aku cikgu. ada laptop. aku explore teknologi, tengok apa yang boleh aku hasilkan dengan benda tu.\n\nmakcik aku belajar multimedia. aku tengok dia buat kerja, tengok benda yang dia belajar.\n\nvideo pertama aku buat untuk sepupu sendiri. guna je tools yang ada dalam laptop tu. tak tunggu semua cukup dulu.\n\ncara orang dapat spark memang beza. tapi cara guna dia sama: mula dengan apa yang ada depan mata.\n\nkorang punya spark datang dari mana? aku nak baca semua.",
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
    print("Sila masukkan slot: pagi / malam")
elif today not in POSTS:
    print(f"Tiada post untuk hari {today}")
elif slot not in POSTS[today]:
    print(f"Slot '{slot}' tidak wujud.")
elif already_posted(slot, today):
    print(f"Slot '{slot}' untuk {today} dah dipost hari ni — skip.")
else:
    post(POSTS[today][slot], slot, today)
