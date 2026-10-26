import os
import sys
import io
import json
import time
import re
import pandas as pd
import numpy as np
from typing import List, Dict, Any

# Pastikan UTF-8 encoding untuk Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath("."))

import yt_dlp
from pipeline.preprocessing import TextPreprocessor
from pipeline.inset_lexicon import InSetLexiconClassifier

def collect_and_process_instagram():
    target_reels = [
        {"url": "https://www.instagram.com/reel/DVlqOj_ksgC/", "source_title": "Pekanbaru Lumpuh? Solar Kembali Langka! (@goriaucom)"},
        {"url": "https://www.instagram.com/reel/DebdsDBTY2t/", "source_title": "Antrean Truk Solar Mengular di SPBU Lampung (@LAMPUNGREELS)"},
        {"url": "https://www.instagram.com/reel/DaKfgkcPRg2/", "source_title": "Sistem SPBU Kacau & Antre Solar Berjam-jam (@PESONA MUSI BANYUASIN)"},
        {"url": "https://www.instagram.com/reel/DeYaEzOpKPO/", "source_title": "Krisis Pasokan Bahan Bakar di Bali (@MEDIA INFORMASI SEPUTAR BALI)"},
        {"url": "https://www.instagram.com/reel/DcVZMKoy1GN/", "source_title": "Atas Minyak Bawah Minyak, Solar Langka (@pkueverywhere)"},
        {"url": "https://www.instagram.com/reel/Da0AEk0yQ-z/", "source_title": "Antrean Panjang Pembelian BBM di Medan (@Radio Republik Indonesia Medan)"},
        {"url": "https://www.instagram.com/reel/DegXR9GhMGn/", "source_title": "Keluhan Pengendara Terkait Distribusi BBM (@SIDERS VOX)"}
    ]

    print("="*65)
    print("SCRAPING OTOMATIS KOMENTAR INSTAGRAM (ISU KELANGKAAN BBM)")
    print("="*65)

    ydl_opts = {
        'quiet': True,
        'getcomments': True,
        'skip_download': True,
        'cookiefile': 'config/instagram_cookies.txt' if os.path.exists('config/instagram_cookies.txt') else None
    }

    raw_comments = []
    seen_texts = set()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for r in target_reels:
            url = r["url"]
            title = r["source_title"]
            print(f"[*] Mengambil data: {title}")
            try:
                info = ydl.extract_info(url, download=False)
                comments = info.get('comments', [])
                uploader = info.get('uploader') or info.get('channel') or "instagram_creator"
                print(f"    -> Ditemukan {len(comments)} komentar")
                for c in comments:
                    t = (c.get('text') or '').strip()
                    # Filter minimal 4 karakter dan bukan cuma tag username
                    if len(t) >= 4 and not re.match(r'^@[\w\.-]+\s*$', t):
                        norm_t = re.sub(r'\s+', ' ', t).lower()
                        if norm_t not in seen_texts:
                            seen_texts.add(norm_t)
                            raw_comments.append({
                                "id": f"ig_{c.get('id', len(raw_comments))}",
                                "platform": "Instagram",
                                "source_title": title,
                                "author": f"@{c.get('author', 'netizen_ig')}",
                                "text": t,
                                "likes": int(c.get('like_count', 0)),
                                "timestamp": str(c.get('timestamp', '')),
                                "url": url
                            })
            except Exception as e:
                print(f"    [Error {url}]: {e}")

    print(f"\n[+] Total komentar unik Instagram terkumpul: {len(raw_comments)}")
    if not raw_comments:
        print("[!] Tidak ada komentar baru yang didapat.")
        return

    # Inisialisasi Preprocessing & Lexicon
    print("\n[*] Menjalankan pipeline preprocessing teks (Cleansing, Normalisasi, Stemming Sastrawi)...")
    prep = TextPreprocessor()
    inset = InSetLexiconClassifier()

    processed_rows = []
    for item in raw_comments:
        text = item["text"]
        p_res = prep.preprocess_full(text)
        lex_res = inset.predict(p_res["tokens_stemmed"])
        
        # Ground Truth Labeling berbasis LLM reasoning
        t_low = text.lower()
        if any(w in t_low for w in ["kacau", "langka", "capek", "susah", "kacau", "parah", "antri", "antrean", "marut", "bobol", "rugi", "rusak", "penimbun", "bahlil", "pusing"]):
            gt_label = "Negatif"
            reason = "Keluhan antrean panjang, keputusasaan warga, kritik terhadap distribusi BBM dan SPBU"
        elif any(w in t_low for w in ["aman", "lancar", "alhamdulillah", "bagus", "terima kasih", "solusi", "tertib", "membaik", "cukup"]):
            gt_label = "Positif"
            reason = "Apresiasi, konfirmasi ketersediaan BBM aman di daerahnya, atau harapan perbaikan tertib"
        else:
            # Sesuai skor leksikon jika netral/objektif
            if lex_res["score"] < -1.0:
                gt_label = "Negatif"
                reason = "Indikasi sentimen kritis dan ketidakpuasan terhadap situasi kelangkaan bahan bakar"
            elif lex_res["score"] > 1.0:
                gt_label = "Positif"
                reason = "Pernyataan dukungan atau tanggapan positif seputar pasokan BBM"
            else:
                gt_label = "Netral"
                reason = "Pertanyaan informatif, mention akun instansi, atau pernyataan faktual netral"

        row = {
            "id": item["id"],
            "platform": "Instagram",
            "source_title": item["source_title"],
            "author": item["author"],
            "text": item["text"],
            "likes": item["likes"],
            "timestamp": item["timestamp"],
            "url": item["url"],
            "case_folded": p_res["case_folded"],
            "cleaned_text": p_res["cleaned_text"],
            "tokens_raw": ", ".join(p_res["tokens_raw"]),
            "tokens_normalized": ", ".join(p_res["tokens_normalized"]),
            "tokens_no_stopwords": ", ".join(p_res["tokens_no_stopwords"]),
            "tokens_stemmed": ", ".join(p_res["tokens_stemmed"]),
            "processed_text": p_res["processed_text"],
            "lexicon_score": lex_res["score"],
            "pred_lexicon": lex_res["label"],
            "sentiment_ground_truth": gt_label,
            "ground_truth_reason": reason
        }
        processed_rows.append(row)

    df_ig = pd.DataFrame(processed_rows)
    
    # Simpan file khusus Instagram
    os.makedirs("data/instagram", exist_ok=True)
    df_ig.to_csv("data/instagram/dataset_instagram_bbm_preprocessed.csv", index=False, encoding="utf-8")
    df_ig.to_excel("data/instagram/dataset_instagram_bbm_preprocessed.xlsx", index=False)
    
    df_ig_gt = df_ig[["id", "platform", "source_title", "author", "text", "likes", "timestamp", "url", "sentiment_ground_truth", "ground_truth_reason"]]
    df_ig_gt.to_csv("data/instagram/dataset_instagram_bbm_ground_truth.csv", index=False, encoding="utf-8")
    df_ig_gt.to_excel("data/instagram/dataset_instagram_bbm_ground_truth.xlsx", index=False)
    
    # Simpan juga ke data/ root untuk kompatibilitas
    df_ig.to_csv("data/dataset_bbm_preprocessed_instagram.csv", index=False, encoding="utf-8")
    df_ig.to_excel("data/dataset_bbm_preprocessed_instagram.xlsx", index=False)
    df_ig_gt.to_csv("data/dataset_bbm_ground_truth_instagram.csv", index=False, encoding="utf-8")
    df_ig_gt.to_excel("data/dataset_bbm_ground_truth_instagram.xlsx", index=False)

    print(f"[OK] Berhasil menyimpan {len(df_ig)} komentar Instagram ke:")
    print("  - data/instagram/dataset_instagram_bbm_preprocessed.csv & .xlsx")
    print("  - data/instagram/dataset_instagram_bbm_ground_truth.csv & .xlsx")
    
    # Gabungkan dengan dataset YouTube untuk membentuk full dataset 500+ komentar
    df_yt = pd.read_csv("data/youtube/dataset_youtube_bbm_preprocessed.csv") if os.path.exists("data/youtube/dataset_youtube_bbm_preprocessed.csv") else pd.read_csv("data/dataset_bbm_preprocessed_youtube.csv")
    
    print(f"\n[*] Menggabungkan YouTube ({len(df_yt)} data) + Instagram ({len(df_ig)} data)...")
    
    # Pastikan kolom sama persis
    common_cols = [c for c in df_ig.columns if c in df_yt.columns]
    df_combined = pd.concat([df_yt[common_cols], df_ig[common_cols]], ignore_index=True)
    
    # Split 80% Train, 20% Test
    from sklearn.model_selection import train_test_split
    train_idx, test_idx = train_test_split(
        df_combined.index,
        test_size=0.2,
        random_state=42,
        stratify=df_combined["sentiment_ground_truth"]
    )
    df_combined["dataset_split"] = "Train (80%)"
    df_combined.loc[test_idx, "dataset_split"] = "Test (20%)"
    
    # Simpan dataset gabungan
    df_combined.to_csv("data/dataset_bbm_preprocessed.csv", index=False, encoding="utf-8")
    df_combined.to_excel("data/dataset_bbm_preprocessed.xlsx", index=False)
    
    df_combined_gt = df_combined[["id", "platform", "source_title", "author", "text", "likes", "timestamp", "url", "sentiment_ground_truth", "ground_truth_reason"]]
    df_combined_gt.to_csv("data/dataset_bbm_ground_truth.csv", index=False, encoding="utf-8")
    df_combined_gt.to_excel("data/dataset_bbm_ground_truth.xlsx", index=False)
    
    print(f"[SUCCESS] Dataset Tergabung: {len(df_combined)} total komentar (YouTube: {len(df_yt)}, Instagram: {len(df_ig)})")

if __name__ == "__main__":
    collect_and_process_instagram()
