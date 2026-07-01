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
        "pagi": "upah pertama aku buat kerja freelance?\n\nroti dan air.\n\nclient pertama tu kawan aku sendiri. dia tak ada duit. aku pun tak kisah sebab aku just nak buat kerja tu.\n\ntapi dari kerja tu je aku ada portfolio pertama aku. satu contoh je. tapi cukup untuk dapat client seterusnya.\n\nkadang first job bukan pasal duit. pasal kau ada sesuatu untuk tunjuk.",

        # cerita: buat personal project walaupun takde client
        "tengahari": "aku selalu buat project walaupun takde siapa bayar.\n\nsempena raya buat design sendiri. jumpa tools baru terus explore suka-suka. buat benda yang takde orang minta.\n\norang kata buang masa. tapi bila tiba masa nak tunjuk portfolio, aku ada benda nak tunjuk.\n\nkalau tunggu ada client dulu baru nak practice, kau akan tunggu lama.",

        # cerita: mula suka-suka, bukan target fulltime pun
        "malam": "aku tak start freelance dengan target nak buat fulltime pun dulu.\n\njust nak buat duit lebih. buat bila ada masa lapang. tak ada tekanan.\n\ntapi bila buat dengan enjoy, kerja jadi lagi baik. client happy, dapat refer ke orang lain.\n\nternyata yang start tanpa target besar pun boleh pergi jauh.",
    },

    "Tuesday": {
        # cerita: apply kerja bawa hardisk
        "pagi": "cara aku dapat kerja pertama aku dulu?\n\npergi interview. bawa hardisk.\n\ntunjuk kerja terus dari situ. takde sijil cantik, takde resume panjang, tak sebut pun pointer berapa.\n\ndiorang tengok kerja dalam hardisk tu, terus offer.\n\nramai sangat fokus nak polish resume. tapi orang yang hire kau nak tengok kau boleh buat apa, bukan kau pernah belajar apa.",

        # cerita: portfolio beats cert
        "tengahari": "aku tak pernah dapat kerja atau project sebab sijil.\n\nselalu sebab orang tengok kerja aku terus.\n\nbukan aku tak ada sijil. ada. tapi tak pernah jadi faktor pun.\n\nkalau kau ada kerja yang kau boleh tunjuk, sijil jadi decoration je.",

        # cerita: ambil kerja murah tapi buat lebih
        "malam": "aku pernah ambil kerja murah sebab minat sangat nak buat.\n\nbayaran tak seberapa. tapi aku buat lebih dari apa yang diorang minta. explore tools baru, polish sampai puas hati sendiri.\n\nkerja tu jadi showcase terbaik dalam portfolio aku. dan dari situ dapat tawaran yang lagi tinggi.\n\nusaha kau buat tu selalu lebih dari bayaran yang kau terima.",
    },

    "Wednesday": {
        # cerita: minat banyak benda
        "pagi": "masalah aku dulu, aku minat buat banyak benda.\n\nanimation, game, design, web. semua aku cuba. semua aku ambil kalau ada orang tanya.\n\nrasa macam bagus sebab serba boleh. tapi sebenarnya aku tak tahu nak describe diri aku sebagai apa.\n\norang tanya kau buat apa, kau jawab freelancer. generic. tak ada siapa yang ingat.",

        # cerita: setiap client kenal kau beza-beza
        "tengahari": "kelakar bila aku fikir balik.\n\nada client kenal aku sebagai orang buat design. ada yang kenal sebab web. ada yang kenal sebab animation.\n\nbukan seorang pun yang kenal aku sebagai semua tu sekali.\n\nsetiap orang ada versi berbeza pasal siapa aku. dan aku sendiri pun confused.",

        # cerita: portfolio bersepah
        "malam": "portfolio aku dulu bersepah.\n\nbuat macam-macam, tapi bila letak semua sekali nampak tak ada arah. macam kedai yang jual segalanya tapi takde specialty.\n\nclient yang datang pun random. dan bila nak market diri sendiri, tak tahu nak highlight apa dulu.\n\nbukannya skill tak ada. tapi tak tersusun.",
    },

    "Thursday": {
        # cerita: buat kerja lebih dari bayaran
        "pagi": "aku pernah explore tools baru dalam project client yang bayar murah.\n\nbukannya aku kena buat pun. tapi aku nak cuba. sebab minat.\n\nclient dapat result lagi bagus dari yang diorang expect. aku dapat experience dari tools baru tu.\n\ndua-dua untung. walaupun bayaran time tu tak reflect usaha aku langsung.",

        # cerita: dari referral je
        "tengahari": "hampir semua client aku datang dari referral.\n\nkawan refer. company lama refer. orang yang pernah tengok kerja aku refer.\n\nbukan aku pergi cari pun. diorang datang sendiri.\n\ntapi masalahnya, referral tak consistent. ada bulan banyak, ada bulan senyap. dan aku tak ada cara nak control bila diorang datang.",

        # cerita: struggle consistency
        "malam": "benda yang aku paling struggle sampai sekarang bukan skill.\n\nbukan cari client. bukan bayaran.\n\ntapi consistency.\n\nada masa aku productive gila, siap kerja berlambak. ada masa aku procrastinate sampai deadline dah dekat baru gerak.\n\ntu masalah yang aku masih keje nak selesaikan.",
    },

    "Friday": {
        # cerita: minat jadi kelebihan
        "pagi": "sebab aku minat, aku tak rasa penat walaupun kerja lama.\n\nclient lain mungkin kena paksa pekerja diorang buat overtime. aku buat overtime sendiri sebab nak polish lagi.\n\nbukan semua orang ada tu. dan bila client rasa perbezaan tu, diorang ingat kau.",

        # cerita: jumpa satu servis yang gabung semua minat
        "tengahari": "bertahun aku buat macam-macam. animation, design, web, game.\n\nlepas tu aku jumpa satu servis yang boleh gabungkan semua tu sekali.\n\nambil masa nak fokus. tapi bila dah fokus kat satu benda tu, barulah mudah promote diri.\n\nasal sebut servis tu, orang terus ingat nama aku. bukan nama orang lain.",

        # cerita: dari scattered jadi known for one thing
        "malam": "perasaan bila orang mula associate nama kau dengan satu benda tu lain sikit.\n\nsebelum ni orang tanya aku buat apa, aku explain panjang. diorang pun confused.\n\nlepas aku fokus kat satu benda, orang tanya kau buat apa, aku jawab satu ayat. diorang faham terus.\n\nitu je bezanya. tapi effect dia jauh sangat.",
    },

    "Saturday": {
        # cerita: first job free jadi pintu
        "pagi": "kerja free pertama aku bukan rugi.\n\nwalaupun upah roti dan air, aku buat dengan sepenuh hati. sebab aku genuinely enjoy buat kerja tu.\n\nlepas tu kawan tu refer aku ke orang lain. lepas tu orang lain tu refer ke company. dan dari situlah bola mula bergolek.\n\nkadang pintu pertama tu kecil je. tapi dia yang buka semua pintu lain.",

        # cerita: buat personal project jadi habit
        "tengahari": "sampai sekarang aku masih buat personal project walaupun takde siapa bayar.\n\nbukan sebab takde kerja. tapi sebab itu cara aku stay sharp.\n\ncuba tools baru, explore idea yang aku sendiri nak tengok hasilnya, buat benda yang tak ada dalam portfolio lagi.\n\nkalau tunggu client je baru nak belajar benda baru, kau akan selalu ketinggalan.",

        # cerita: hot take pasal minat
        "malam": "orang selalu kata jangan buat kerja yang kau suka sebab nanti hilang minat.\n\naku tak setuju.\n\naku buat kerja yang aku minat dari dulu sampai sekarang. dan sebab tu aku boleh buat lagi baik dari orang yang buat sebab duit je.\n\nminat tak hilang bila kau buat kerja. minat hilang bila kau buat kerja yang salah.",
    },

    "Sunday": {
        # cerita: reflect perjalanan
        "pagi": "kalau aku tengok balik dari mula sampai sekarang.\n\nmula dengan kerja free upah roti dan air. portfolio satu contoh je. interview bawa hardisk.\n\nbertahun buat macam-macam sampai tak tahu nak describe diri sendiri.\n\nlepas tu perlahan-lahan jumpa satu fokus. dan dari situ baru nampak arah.\n\nperjalanan dia tak straight. tapi setiap bengkang-bengkok tu ada sebabnya.",

        # cerita: nasihat untuk diri sendiri dulu
        "tengahari": "kalau boleh balik masa dan cakap satu benda je dengan diri sendiri yang dulu.\n\naku cakap, fokus lagi awal.\n\nbukan maksud tak boleh explore. explore kena. tapi kena ada satu anchor yang ikat semua tu.\n\ntanpa anchor, kau akan spend tahun buat banyak benda tapi tak pergi mana-mana.",

        # cerita: spark — closing minggu
        "malam": "spark aku datang dari dua benda yang berlaku serentak.\n\nmak aku cikgu. ada laptop. aku explore teknologi, tengok apa yang boleh aku hasilkan dengan benda tu.\n\nmakcik aku belajar multimedia. aku tengok dia buat kerja, tengok benda yang dia belajar.\n\ndari situ timbul sesuatu. rasa nak tahu lagi. rasa seronok bila sedar teknologi ni boleh hasilkan benda yang kita sendiri reka.\n\nvideo pertama aku buat untuk sepupu sendiri. guna je tools yang dah ada dalam laptop tu. tak tunggu ada software lagi canggih, tak tunggu semua cukup dulu.\n\nguna apa yang ada. hasilkan sesuatu. belajar dari situ.\n\ncara orang dapat spark memang beza-beza. tapi cara guna spark tu sama je. mula dengan apa yang ada depan mata kau sekarang.",
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
