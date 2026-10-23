import os
import sys
import io
import json
import time
import pandas as pd
from typing import List, Dict, Any

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapers.youtube_scraper import YouTubeScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.instagram_scraper import InstagramScraper

def collect_youtube_comments(video_ids: List[Dict[str, str]], max_per_video: int = 150) -> List[Dict[str, Any]]:
    scraper = YouTubeScraper()
    all_comments = []
    
    for v in video_ids:
        vid = v["id"]
        vtitle = v["title"]
        channel = v.get("channel", "YouTube")
        url = f"https://www.youtube.com/watch?v={vid}"
        print(f"[YouTube] Scraping comments from: {channel} - '{vtitle[:40]}...' ({vid})")
        
        try:
            comments = scraper.get_comments(url, max_comments=max_per_video, replies_per_comment=5)
            print(f"  -> Got {len(comments)} parent comments")
            
            for c in comments:
                text = (c.get("text") or "").strip()
                if text and len(text) > 5:
                    all_comments.append({
                        "id": f"yt_{c.get('cid', len(all_comments))}",
                        "platform": "YouTube",
                        "source_title": vtitle,
                        "author": c.get("author", "Netizen"),
                        "text": text,
                        "likes": c.get("votes", 0),
                        "timestamp": c.get("time", ""),
                        "url": url
                    })
                
                # Balasan (replies)
                for rep in c.get("replies", []):
                    rep_text = (rep.get("text") or "").strip()
                    if rep_text and len(rep_text) > 5:
                        all_comments.append({
                            "id": f"yt_{rep.get('cid', len(all_comments))}",
                            "platform": "YouTube",
                            "source_title": f"Reply on {vtitle[:30]}",
                            "author": rep.get("author", "Netizen"),
                            "text": rep_text,
                            "likes": rep.get("votes", 0),
                            "timestamp": rep.get("time", ""),
                            "url": url
                        })
        except Exception as e:
            print(f"  [Error]: {e}")
            
    return all_comments

def collect_multiplatform_labor_data():
    os.makedirs("data", exist_ok=True)
    
    youtube_videos = [
        {"id": "34lJ9BdHDSM", "title": "Sarjana Indonesia Susah Cari Kerja, RI Banjir Pengangguran", "channel": "CNBC Indonesia"},
        {"id": "ArRoXdYaGNw", "title": "Perjuangan Cari Kerja Gen Z Indonesia: Setelah Kirim 2.245 Lamaran", "channel": "CNA Insider"},
        {"id": "cIGuGNQzXTA", "title": "Ancaman PHK Massal! Pemerintah Siapkan Langkah Situasi Kritis", "channel": "KOMPASTV"},
        {"id": "6nrJ4owSCGM", "title": "Menaker Yassierli Bicara Lapangan Pekerjaan, Harapan & Kenyataan", "channel": "KOMPASTV ROSI"},
        {"id": "hChPhCg00po", "title": "Badai PHK Meluas, DPR Minta Lindungi Pekerja", "channel": "METRO TV"},
        {"id": "Plx4cvxzAMM", "title": "Inilah Biang Kerok PHK Massal Industri Tekstil", "channel": "KONTAN TV"},
        {"id": "mhYkSKKThCA", "title": "Gelombang PHK Massal Industri Tekstil Hingga Bangkrut", "channel": "Bernarasi"}
    ]
    
    print("=== TAHAP I: PENGUMPULAN DATA MULTIPLATFORM MEDIA SOSIAL ===")
    yt_data = collect_youtube_comments(youtube_videos, max_per_video=120)
    print(f"\n[Total YouTube Comments Collected]: {len(yt_data)}")
    
    # Platform 2: X / Twitter Public Search Data
    print("\n[X/Twitter] Scraping public discourse on labor crisis...")
    tw_scraper = TwitterScraper()
    tw_queries = [
        "krisis ketenagakerjaan indonesia phk",
        "susah cari kerja syarat batas umur",
        "sarjana nganggur loker sepi",
        "phk massal pabrik tutup pesangon"
    ]
    tw_data = []
    for tq in tw_queries:
        try:
            tweets = tw_scraper.search_tweets_public(tq, max_results=25)
            for tw in tweets:
                tw_text = (tw.get("text") or "").strip()
                if tw_text and len(tw_text) > 10:
                    tw_data.append({
                        "id": f"tw_{tw.get('id', len(tw_data))}",
                        "platform": "Twitter/X",
                        "source_title": f"Query: {tq}",
                        "author": tw.get("author", "Twitter User"),
                        "text": tw_text,
                        "likes": tw.get("likes", 0),
                        "timestamp": tw.get("time", ""),
                        "url": tw.get("url", "https://twitter.com")
                    })
        except Exception as e:
            print(f"  [Twitter Search Error]: {e}")
            
    print(f"[Total Twitter/X Posts Collected]: {len(tw_data)}")
    
    # Gabungkan semua data
    combined = yt_data + tw_data
    
    # Hapus duplikasi teks
    seen = set()
    unique_data = []
    for item in combined:
        norm_key = " ".join(item["text"].split())[:80].lower()
        if norm_key not in seen:
            seen.add(norm_key)
            unique_data.append(item)
            
    print(f"\n[Total Unique Comments Collected]: {len(unique_data)} (Target: >= 500)")
    
    # Simpan dataset mentah
    df = pd.DataFrame(unique_data)
    csv_path = "data/dataset_ketenagakerjaan_raw.csv"
    xlsx_path = "data/dataset_ketenagakerjaan_raw.xlsx"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)
    print(f"Dataset tersimpan di {csv_path} dan {xlsx_path}")
    return df

if __name__ == "__main__":
    collect_multiplatform_labor_data()
