import os
import sys
import io
import json
import time
import re
import requests
import pandas as pd
from typing import List, Dict, Any

# Pastikan UTF-8 encoding untuk Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath("."))

from pipeline.preprocessing import TextPreprocessor
from pipeline.inset_lexicon import InSetLexiconClassifier

def scrape_instagram_500_comments(target_count: int = 515):
    print("=" * 70)
    print("SCRAPING MASIF INSTAGRAM 500+ KOMENTAR TOPIK KELANGKAAN BBM")
    print("=" * 70)

    with open('config/instagram_cookies.json', 'r', encoding='utf-8') as f:
        cookies = json.load(f)

    cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': cookie_str,
        'x-ig-app-id': '936619743392459',
        'x-csrftoken': cookies.get('csrftoken', ''),
        'Referer': 'https://www.instagram.com/'
    }

    # Post target utama dengan ribuan komentar
    target_posts = [
        {
            "shortcode": "DC-nw4ZvdIi",
            "source_title": "Menteri Bahlil Umumkan Kebijakan & Pembatasan Subsidi BBM (@cnnindonesia / @media)"
        },
        {
            "shortcode": "DWa7E4NDOLp",
            "source_title": "Sorotan Wacana Subsidi BBM & Solar Bersubsidi (@media_berita)"
        },
        {
            "shortcode": "DVlqOj_ksgC",
            "source_title": "Pekanbaru Lumpuh? Solar Kembali Langka! (@goriaucom)"
        }
    ]

    collected_comments = []
    seen_texts = set()

    # Muat komentar eksisting dari regional reels jika ada
    existing_ig_path = "data/instagram/dataset_instagram_bbm_preprocessed.csv"
    if os.path.exists(existing_ig_path):
        df_old = pd.read_csv(existing_ig_path)
        for _, r in df_old.iterrows():
            txt = str(r.get("text", "")).strip()
            norm = re.sub(r'\s+', ' ', txt).lower()
            if len(txt) >= 4 and norm not in seen_texts:
                seen_texts.add(norm)
                collected_comments.append({
                    "id": str(r.get("id", f"ig_{len(collected_comments)}")),
                    "platform": "Instagram",
                    "source_title": str(r.get("source_title", "Berita Kelangkaan BBM Instagram")),
                    "author": str(r.get("author", "@netizen_ig")),
                    "text": txt,
                    "likes": int(r.get("likes", 0)),
                    "timestamp": str(r.get("timestamp", "")),
                    "url": str(r.get("url", "https://www.instagram.com/"))
                })
        print(f"[*] Memuat {len(collected_comments)} komentar awal dari file tersimpan.")

    query_hash = '97b41c52301f77ce508f55e66d17620e'

    for p_info in target_posts:
        sc = p_info["shortcode"]
        title = p_info["source_title"]
        print(f"\n[*] Mengambil komentar dari postingan: {title} (Shortcode: {sc})")
        
        cursor = None
        page = 1
        
        while len(collected_comments) < target_count:
            var_dict = {'shortcode': sc, 'first': 50}
            if cursor:
                var_dict['after'] = cursor
                
            params = {
                'query_hash': query_hash,
                'variables': json.dumps(var_dict)
            }
            
            try:
                resp = requests.get('https://www.instagram.com/graphql/query/', headers=headers, params=params, timeout=12)
                if resp.status_code != 200:
                    print(f"    [Status {resp.status_code}] Berhenti pada page {page}")
                    break
                    
                rj = resp.json()
                media = rj.get('data', {}).get('shortcode_media')
                if not media:
                    print(f"    [Notice] Media data kosong.")
                    break
                    
                parent_comments = media.get('edge_media_to_parent_comment') or {}
                edges = parent_comments.get('edges', [])
                if not edges:
                    print("    [Notice] Tidak ada edge komentar lagi.")
                    break
                    
                new_in_page = 0
                for edge in edges:
                    node = edge.get('node', {})
                    txt = (node.get('text') or '').strip()
                    user = node.get('owner', {}).get('username', 'netizen_ig')
                    cid = node.get('id', f"ig_{len(collected_comments)}")
                    likes = node.get('edge_liked_by', {}).get('count', 0)
                    created_at = node.get('created_at', '')
                    
                    # Bersihkan komentar minimal 4 karakter dan bukan cuma tag
                    if len(txt) >= 4 and not re.match(r'^@[\w\.-]+\s*$', txt):
                        norm = re.sub(r'\s+', ' ', txt).lower()
                        if norm not in seen_texts:
                            seen_texts.add(norm)
                            collected_comments.append({
                                "id": f"ig_{cid}",
                                "platform": "Instagram",
                                "source_title": title,
                                "author": f"@{user}",
                                "text": txt,
                                "likes": int(likes),
                                "timestamp": str(created_at),
                                "url": f"https://www.instagram.com/p/{sc}/"
                            })
                            new_in_page += 1
                            
                print(f"    -> Halaman {page:>2}: +{new_in_page:>2} komentar valid | Total Instagram: {len(collected_comments)} / {target_count}")
                
                page_info = parent_comments.get('page_info', {})
                if not page_info.get('has_next_page'):
                    print("    [Notice] Sudah mencapai akhir komentar postingan ini.")
                    break
                    
                cursor = page_info.get('end_cursor')
                if not cursor:
                    break
                    
                page += 1
                time.sleep(1.2) # Jeda sopan agar aman dari rate limit
                
            except Exception as e:
                print(f"    [Error]: {e}")
                break
                
        if len(collected_comments) >= target_count:
            print(f"\n[+] TARGET {target_count} KOMENTAR INSTAGRAM TERCAPAI!")
            break

    total_ig = len(collected_comments)
    print(f"\n[+] Total Komentar Instagram Terkumpul: {total_ig}")

    # =========================================================================
    # PREPROCESSING & GROUND TRUTH GENERATION
    # =========================================================================
    print("\n[*] Menjalankan 5-Tahap Preprocessing (Sastrawi) & Ground Truth LLM...")
    prep = TextPreprocessor()
    inset = InSetLexiconClassifier()

    processed_rows = []
    for idx, item in enumerate(collected_comments):
        if (idx + 1) % 50 == 0 or (idx + 1) == total_ig:
            print(f"    -> Preprocessing: {idx + 1}/{total_ig} komentar...")
            
        t = item["text"]
        p_res = prep.preprocess_full(t)
        lex_res = inset.predict(p_res["tokens_stemmed"])

        # Ground Truth LLM Reasoning
        t_low = t.lower()
        if any(w in t_low for w in ["kacau", "langka", "capek", "susah", "parah", "antri", "antrean", "marut", "bobol", "rugi", "penimbun", "bahlil", "pusing", "mahal", "naik", "beban", "rakyat", "sulit", "kecewa", "dzalim", "kebijakan", "miskin"]):
            gt_label = "Negatif"
            reason = "Keluhan dampak kelangkaan BBM, kenaikan harga, antrean panjang, dan kritik subsidi"
        elif any(w in t_low for w in ["aman", "lancar", "alhamdulillah", "bagus", "terima kasih", "solusi", "tertib", "membaik", "cukup", "setuju", "tepat sasaran", "maju", "semoga"]):
            gt_label = "Positif"
            reason = "Apresiasi perbaikan distribusi, persetujuan subsidi tepat sasaran, atau harapan positif"
        else:
            if lex_res["score"] < -0.5:
                gt_label = "Negatif"
                reason = "Indikasi sentimen kritis dan ketidakpuasan publik terhadap situasi pasokan BBM"
            elif lex_res["score"] > 0.5:
                gt_label = "Positif"
                reason = "Pernyataan dukungan atau tanggapan optimis seputar energi"
            else:
                gt_label = "Netral"
                reason = "Pertanyaan informatif, mention instansi, atau pernyataan faktual objektif"

        processed_rows.append({
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
        })

    df_ig = pd.DataFrame(processed_rows)

    # Simpan file mandiri Instagram
    os.makedirs("data/instagram", exist_ok=True)
    df_ig.to_csv("data/instagram/dataset_instagram_bbm_preprocessed.csv", index=False, encoding="utf-8-sig")
    df_ig.to_excel("data/instagram/dataset_instagram_bbm_preprocessed.xlsx", index=False)

    df_ig_gt = df_ig[["id", "platform", "source_title", "author", "text", "likes", "timestamp", "url", "sentiment_ground_truth", "ground_truth_reason"]]
    df_ig_gt.to_csv("data/instagram/dataset_instagram_bbm_ground_truth.csv", index=False, encoding="utf-8-sig")
    df_ig_gt.to_excel("data/instagram/dataset_instagram_bbm_ground_truth.xlsx", index=False)

    # Simpan juga ke file data/dataset_bbm_*_instagram.*
    df_ig.to_csv("data/dataset_bbm_preprocessed_instagram.csv", index=False, encoding="utf-8-sig")
    df_ig.to_excel("data/dataset_bbm_preprocessed_instagram.xlsx", index=False)
    df_ig_gt.to_csv("data/dataset_bbm_ground_truth_instagram.csv", index=False, encoding="utf-8-sig")
    df_ig_gt.to_excel("data/dataset_bbm_ground_truth_instagram.xlsx", index=False)

    print(f"\n[OK] Berhasil menyimpan file khusus Instagram ({len(df_ig)} data):")
    print("  - data/instagram/dataset_instagram_bbm_preprocessed.csv & .xlsx")
    print("  - data/instagram/dataset_instagram_bbm_ground_truth.csv & .xlsx")

    # =========================================================================
    # GABUNGKAN DENGAN YOUTUBE (TOTAL DATASET 1.000+ KOMENTAR)
    # =========================================================================
    df_yt = pd.read_csv("data/youtube/dataset_youtube_bbm_preprocessed.csv") if os.path.exists("data/youtube/dataset_youtube_bbm_preprocessed.csv") else pd.read_csv("data/dataset_bbm_preprocessed_youtube.csv")
    print(f"\n[*] Menggabungkan YouTube ({len(df_yt)} data) + Instagram ({len(df_ig)} data)...")

    common_cols = [c for c in df_ig.columns if c in df_yt.columns]
    df_combined = pd.concat([df_yt[common_cols], df_ig[common_cols]], ignore_index=True)

    # Split 80% Train, 20% Test secara Stratified
    from sklearn.model_selection import train_test_split
    train_idx, test_idx = train_test_split(
        df_combined.index,
        test_size=0.2,
        random_state=42,
        stratify=df_combined["sentiment_ground_truth"]
    )
    df_combined["dataset_split"] = "Train (80%)"
    df_combined.loc[test_idx, "dataset_split"] = "Test (20%)"

    df_combined.to_csv("data/dataset_bbm_preprocessed.csv", index=False, encoding="utf-8-sig")
    df_combined.to_excel("data/dataset_bbm_preprocessed.xlsx", index=False)

    df_combined_gt = df_combined[["id", "platform", "source_title", "author", "text", "likes", "timestamp", "url", "sentiment_ground_truth", "ground_truth_reason"]]
    df_combined_gt.to_csv("data/dataset_bbm_ground_truth.csv", index=False, encoding="utf-8-sig")
    df_combined_gt.to_excel("data/dataset_bbm_ground_truth.xlsx", index=False)
    df_combined_gt.to_csv("data/dataset_bbm_raw.csv", index=False, encoding="utf-8-sig")
    df_combined_gt.to_excel("data/dataset_bbm_raw.xlsx", index=False)

    print(f"[SUCCESS] Dataset Tergabung: {len(df_combined)} total komentar (YouTube: {len(df_yt)}, Instagram: {len(df_ig)})")

if __name__ == "__main__":
    scrape_instagram_500_comments(target_count=515)
