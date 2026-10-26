import os
import sys
import io
import json
import time
import urllib.request
import urllib.parse
import pandas as pd
from typing import List, Dict, Any

# Pastikan UTF-8 encoding untuk Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_env(path: str = ".env"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env()
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

# ====================================================================
# 1. PENCARIAN & SCRAPING OTOMATIS YOUTUBE (DATA API V3)
# ====================================================================

def search_youtube_videos_by_topic(queries: List[str], max_videos: int = 15) -> List[Dict[str, str]]:
    """Mencari video berita terpopuler secara otomatis berdasarkan kata kunci topik."""
    found_videos = []
    seen_ids = set()

    for q in queries:
        encoded_q = urllib.parse.quote(q)
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={encoded_q}&type=video&maxResults=8&order=relevance&key={YOUTUBE_API_KEY}"
        try:
            req = urllib.request.urlopen(url, timeout=12)
            data = json.loads(req.read().decode("utf-8"))
            for item in data.get("items", []):
                vid = item["id"]["videoId"]
                if vid not in seen_ids:
                    seen_ids.add(vid)
                    found_videos.append({
                        "id": vid,
                        "title": item["snippet"]["title"],
                        "channel": item["snippet"]["channelTitle"],
                        "published_at": item["snippet"]["publishedAt"]
                    })
        except Exception as e:
            print(f"  [YouTube Search Notice query='{q}']: {e}")

        if len(found_videos) >= max_videos:
            break

    return found_videos[:max_videos]


def fetch_youtube_comments(video_id: str, video_title: str, max_comments: int = 100) -> List[Dict[str, Any]]:
    """Mengambil komentar utama dan balasan dari suatu video."""
    collected = []
    page_token = ""
    url_base = "https://www.googleapis.com/youtube/v3/commentThreads"

    while len(collected) < max_comments:
        params = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": min(100, max_comments - len(collected)),
            "key": YOUTUBE_API_KEY,
            "textFormat": "plainText"
        }
        if page_token:
            params["pageToken"] = page_token

        try:
            req_url = f"{url_base}?{urllib.parse.urlencode(params)}"
            req = urllib.request.urlopen(req_url, timeout=12)
            data = json.loads(req.read().decode("utf-8"))
        except Exception as e:
            break

        items = data.get("items", [])
        if not items:
            break

        for item in items:
            top = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
            c_text = (top.get("textDisplay") or top.get("textOriginal") or "").strip()
            cid = item.get("id", f"yt_{len(collected)}")
            author = top.get("authorDisplayName", "@Netizen")
            likes = int(top.get("likeCount", 0))
            time_pub = top.get("publishedAt", "")

            if len(c_text) >= 5:
                collected.append({
                    "id": f"yt_{cid}",
                    "platform": "YouTube",
                    "source_title": video_title,
                    "author": author,
                    "text": c_text,
                    "likes": likes,
                    "timestamp": time_pub,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                })

            # Balasan (replies)
            for rep in item.get("replies", {}).get("comments", []):
                r_snip = rep.get("snippet", {})
                r_text = (r_snip.get("textDisplay") or r_snip.get("textOriginal") or "").strip()
                if len(r_text) >= 5:
                    collected.append({
                        "id": f"yt_{rep.get('id', len(collected))}",
                        "platform": "YouTube",
                        "source_title": f"Balasan: {video_title[:30]}",
                        "author": r_snip.get("authorDisplayName", "@Netizen"),
                        "text": r_text,
                        "likes": int(r_snip.get("likeCount", 0)),
                        "timestamp": r_snip.get("publishedAt", ""),
                        "url": f"https://www.youtube.com/watch?v={video_id}"
                    })

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return collected


# ====================================================================
# 2. PENGUMPUL DATA KOMENTAR INSTAGRAM (YT-DLP & DIRECT EXTRACTOR)
# ====================================================================

def collect_instagram_bbm_comments() -> List[Dict[str, Any]]:
    """Mengambil komentar dari postingan/Reels berita BBM di Instagram menggunakan yt-dlp."""
    import yt_dlp

    known_bbm_reels = [
        {"url": "https://www.instagram.com/reel/DVlqOj_ksgC/", "title": "Pekanbaru Lumpuh? Solar Kembali Langka! (@goriaucom)"},
        {"url": "https://www.instagram.com/reel/DegVK_dksZq/", "title": "Antrean Mengular Solar di SPBU (@sahat656)"},
        {"url": "https://www.instagram.com/reel/Def6fVIC2ty/", "title": "Krisis Pasokan BBM di Bali (@rudiahmadbalidraivertour)"}
    ]

    ig_comments = []
    print("\n" + "="*60)
    print("TAHAP 2: SCRAPING KOMENTAR INSTAGRAM (BERITA KELANGKAAN BBM)")
    print("="*60)

    ydl_opts = {
        'quiet': True,
        'getcomments': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for r_info in known_bbm_reels:
            url = r_info["url"]
            source_title = r_info["title"]
            print(f"[*] Mengambil data Instagram: {source_title} ({url})")
            try:
                info = ydl.extract_info(url, download=False)
                comments = info.get('comments', [])
                uploader = info.get('uploader') or info.get('channel') or "@instagram_media"
                post_likes = info.get('like_count', 0)
                print(f"    -> Likes Postingan: {post_likes} | Komentar Ditemukan: {len(comments)}")

                for c in comments:
                    t = (c.get('text') or '').strip()
                    if len(t) >= 5:
                        ig_comments.append({
                            "id": f"ig_{c.get('id', len(ig_comments))}",
                            "platform": "Instagram",
                            "source_title": source_title,
                            "author": f"@{c.get('author', 'netizen_ig')}",
                            "text": t,
                            "likes": int(c.get('like_count', 0)),
                            "timestamp": str(c.get('timestamp', '')),
                            "url": url
                        })
            except Exception as e:
                print(f"    [Notice IG]: {e}")

    # Tambahan: Cek apakah ada file ekspor CSV Instagram di folder data/
    import glob
    for f in glob.glob("data/*instagram*.csv") + glob.glob("data/*ig*.csv"):
        if "ketenagakerjaan" in f or "preprocessed" in f:
            continue
        try:
            df_extra = pd.read_csv(f)
            text_col = next((c for c in ["text", "comment", "Comment", "Isi_Komentar"] if c in df_extra.columns), None)
            if text_col:
                for _, row in df_extra.iterrows():
                    val = str(row[text_col]).strip()
                    if len(val) >= 5:
                        ig_comments.append({
                            "id": f"ig_csv_{len(ig_comments)}",
                            "platform": "Instagram",
                            "source_title": str(row.get("source_title", "Berita BBM Instagram")),
                            "author": str(row.get("author", "@netizen_ig")),
                            "text": val,
                            "likes": int(row.get("likes", 0)) if pd.notnull(row.get("likes", 0)) else 0,
                            "timestamp": str(row.get("timestamp", "")),
                            "url": str(row.get("url", "https://instagram.com"))
                        })
        except Exception:
            pass

    print(f"[Total Komentar Instagram Terkumpul]: {len(ig_comments)} komentar")
    return ig_comments


# ====================================================================
# 3. RUNNER UTAMA: OTOMATIS BERBASIS TOPIK
# ====================================================================

def run_auto_bbm_scraping(target_quota: int = 500):
    print("=" * 65)
    print("SCRAPING OTOMATIS MULTIPLATFORM: KELANGKAAN BBM DI INDONESIA")
    print(f"Target Kuota Minimal: {target_quota} komentar unik")
    print("Platform: YouTube (Official API) & Instagram (Authenticated Session)")
    print("=" * 65)

    # 1. Topik Pencarian Otomatis Berita Nasional BBM
    search_queries = [
        "kelangkaan bbm solar pertalite spbu indonesia",
        "antrean panjang bbm solar spbu medan bali manado",
        "stok pertalite kosong spbu dirut pertamina",
        "krisis solar subsidi antre truk berjam jam spbu",
        "penyebab bbm langka spbu pertamina penimbun",
        "antre bbm spbu pertalite habis pengendara menjerit"
    ]

    print("\n[Langkah 1] Menemukan video-video berita terpopuler secara otomatis...")
    videos = search_youtube_videos_by_topic(search_queries, max_videos=20)
    print(f"-> Ditemukan {len(videos)} video berita relevan:")
    for i, v in enumerate(videos, 1):
        print(f"   {i}. [{v['id']}] {v['channel']}: {v['title'][:65]}")

    # 2. Unduh Komentar YouTube Multi-Konten Berantai hingga Kuota Tercapai
    all_yt_comments = []
    print(f"\n[Langkah 2] Mengunduh komentar netizen secara berantai (Target: >={target_quota})...")
    for i, v in enumerate(videos, 1):
        cmts = fetch_youtube_comments(v["id"], v["title"], max_comments=100)
        all_yt_comments.extend(cmts)
        print(f"   [{i}/{len(videos)}] {v['channel']} ({v['id']}) -> Dapat {len(cmts)} komentar (Akumulasi: {len(all_yt_comments)})")
        time.sleep(0.3)
        if len(all_yt_comments) >= target_quota:
            print(f"   [Quota Reached] Kuota {target_quota} komentar terpenuhi pada konten ke-{i}!")
            break

    print(f"\n[Total YouTube Comments]: {len(all_yt_comments)} komentar")

    # 3. Ambil Komentar Instagram
    all_ig_comments = collect_instagram_bbm_comments()

    # 4. Gabungkan dan Deduplikasi
    combined = all_yt_comments + all_ig_comments

    seen = set()
    unique_records = []
    for item in combined:
        clean_key = " ".join(item["text"].split()).lower()[:80]
        if clean_key not in seen:
            seen.add(clean_key)
            unique_records.append(item)

    df = pd.DataFrame(unique_records)
    os.makedirs("data", exist_ok=True)
    csv_path = "data/dataset_bbm_raw.csv"
    xlsx_path = "data/dataset_bbm_raw.xlsx"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)

    print("\n" + "=" * 65)
    print("RINGKASAN DATASET KELANGKAAN BBM BERHASIL DIBUAT")
    print("=" * 65)
    print(f"- Total Data Terkumpul   : {len(combined)}")
    print(f"- Total Data Unik Bersih : {len(unique_records)} komentar")
    print(f"- Distribusi Platform    :")
    print(df["platform"].value_counts().to_string())
    print(f"\nFile tersimpan di:")
    print(f"1. CSV   : {csv_path}")
    print(f"2. Excel : {xlsx_path}")
    return df


if __name__ == "__main__":
    run_auto_bbm_scraping()
