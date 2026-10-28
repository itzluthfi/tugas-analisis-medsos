import os
import json
import glob
import time
import io
import zipfile
from typing import Optional, List, Dict, Any
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

from scrapers.youtube_scraper import YouTubeScraper
from scrapers.instagram_scraper import InstagramScraper
from pipeline.service import SentimentResearchService

try:
    from scrapers.twitter_scraper import TwitterScraper
    tw_scraper = TwitterScraper(output_dir="data/twitter")
except Exception:
    tw_scraper = None

app = FastAPI(title="Media Social Analyzer & Scraper Hub")

# Inisialisasi Scrapers
yt_scraper = YouTubeScraper(output_dir="data/youtube")
ig_scraper = InstagramScraper(output_dir="data/instagram")

# Ensure Data Directories
os.makedirs("data/saved", exist_ok=True)
os.makedirs("data/youtube", exist_ok=True)
os.makedirs("data/twitter", exist_ok=True)
os.makedirs("data/instagram", exist_ok=True)

class UnifiedSearchRequest(BaseModel):
    query: str
    max_results: int = 6
    enable_youtube: bool = True
    enable_instagram: bool = True
    enable_twitter: bool = True

class ScrapeItemRequest(BaseModel):
    platform: str # 'youtube', 'instagram', or 'twitter'
    url: str
    max_comments: int = 300
    replies_per_comment: int = 10

class InstagramConfig(BaseModel):
    sessionid: str

class SaveItemRequest(BaseModel):
    id: str
    data: Dict[str, Any]

@app.post("/api/search")
def unified_search(req: UnifiedSearchRequest):
    """
    Mencari konten dari YouTube, Instagram, dan/atau X (Twitter) sesuai status toggle aktif pengguna.
    Mengembalikan daftar preview card agar user bisa memilih mana yang ingin di-scrape.
    """
    yt_results = []
    ig_results = []
    tw_results = []

    # 1. Search YouTube (jika toggle aktif)
    if req.enable_youtube:
        try:
            yt_raw = yt_scraper.search_videos(req.query, max_results=req.max_results)
            for item in yt_raw:
                yt_results.append({
                    "id": item["id"],
                    "platform": "youtube",
                    "title": item["title"],
                    "author": item["channel"],
                    "thumbnail": item["thumbnail"],
                    "url": item["url"],
                    "views": item.get("view_count"),
                    "duration": item.get("duration"),
                    "duration_text": item.get("duration_text"),
                    "view_text": item.get("view_text")
                })
        except Exception as e:
            print(f"[Search YT Error]: {e}")

    # 2. Search Instagram (jika toggle aktif)
    if req.enable_instagram:
        try:
            ig_results = ig_scraper.search_posts(req.query, max_results=req.max_results)
        except Exception as e:
            print(f"[Search Instagram Error]: {e}")

    # 3. Search Twitter / X (jika toggle aktif)
    if req.enable_twitter:
        try:
            tw_results = tw_scraper.search_tweets_public(req.query, max_results=req.max_results)
        except Exception as e:
            print(f"[Search X Error]: {e}")

    return {
        "query": req.query,
        "youtube": yt_results,
        "instagram": ig_results,
        "twitter": tw_results,
        "total": len(yt_results) + len(ig_results) + len(tw_results)
    }

@app.post("/api/scrape")
def scrape_selected_content(req: ScrapeItemRequest):
    """
    Scraping mendalam isi konten (Metadata + Transkrip Konteks + Komentar Netizen)
    ketika salah satu card konten diklik oleh user.
    """
    if req.platform == "youtube":
        try:
            # 1. Metadata
            meta = yt_scraper.get_metadata(req.url)
            video_id = meta["id"]
            
            # 2. Transkrip Isi Konteks
            transcript = yt_scraper.get_transcript(video_id)
            
            # 3. Komentar Netizen (dengan nested replies)
            comments = yt_scraper.get_comments(req.url, max_comments=req.max_comments, replies_per_comment=req.replies_per_comment)
            
            bundle = {
                "id": video_id,
                "platform": "youtube",
                "metadata": meta,
                "context_transcript": transcript,
                "comments_count_scraped": len(comments),
                "total_comments_available": meta.get("comment_count", len(comments)),
                "comments": comments,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            return bundle
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal scraping YouTube: {str(e)}")

    elif req.platform == "instagram":
        try:
            bundle = ig_scraper.get_post_detail(req.url, max_comments=req.max_comments, replies_per_comment=req.replies_per_comment)
            bundle["scraped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            return bundle
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal scraping Instagram: {str(e)}")

    elif req.platform == "twitter":
        try:
            bundle = tw_scraper.get_tweet_detail(req.url, replies_per_comment=req.replies_per_comment)
            bundle["scraped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            return bundle
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal scraping X: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Platform tidak dikenali")

@app.get("/api/config/instagram")
def get_instagram_config():
    """Cek status konfigurasi sessionid Instagram."""
    sessionid = ig_scraper.get_saved_sessionid()
    return {
        "has_sessionid": bool(sessionid),
        "sessionid_preview": f"{sessionid[:6]}...{sessionid[-4:]}" if sessionid and len(sessionid) > 10 else None
    }

@app.post("/api/config/instagram")
def save_instagram_config(cfg: InstagramConfig):
    """Simpan sessionid Instagram untuk scraping realtime tanpa batas."""
    ok = ig_scraper.save_sessionid(cfg.sessionid)
    if ok:
        return {"status": "success", "message": "Instagram sessionid berhasil disimpan!"}
    raise HTTPException(status_code=500, detail="Gagal menyimpan sessionid")

@app.post("/api/save")
def save_analyzed_content(req: SaveItemRequest):
    """
    Menyimpan konten yang sudah di-scrape ke penyimpanan permanen lokal
    (data/saved/{platform}_{id}.json) dan mencatat riwayatnya.
    """
    platform = req.data.get("platform", "youtube")
    filename = f"{platform}_{req.id}.json"
    filepath = os.path.join("data/saved", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(req.data, f, ensure_ascii=False, indent=2)

    return {"status": "success", "message": "Konten berhasil disimpan ke database lokal", "file": filepath}

@app.get("/api/saved")
def list_saved_items():
    """Mengambil semua daftar konten yang sudah disimpan."""
    files = glob.glob("data/saved/*.json")
    saved = []
    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
                meta = d.get("metadata", {})
                saved.append({
                    "id": d.get("id", meta.get("id")),
                    "platform": d.get("platform", "youtube"),
                    "title": meta.get("title", "Untitled"),
                    "author": meta.get("channel") or meta.get("author", "-"),
                    "comments_count": d.get("comments_count_scraped", len(d.get("comments", []))),
                    "has_transcript": d.get("context_transcript", {}).get("available", False),
                    "scraped_at": d.get("scraped_at", "-")
                })
        except Exception:
            continue
    return sorted(saved, key=lambda x: x.get("scraped_at", ""), reverse=True)

@app.get("/api/saved/{item_id}")
def get_saved_item(item_id: str):
    files = glob.glob(f"data/saved/*_{item_id}.json")
    if not files:
        raise HTTPException(status_code=404, detail="Data simpanan tidak ditemukan")
    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)

@app.delete("/api/saved/{item_id}")
def delete_saved_item(item_id: str):
    """Menghapus 1 item riwayat simpanan berdasarkan ID."""
    files = glob.glob(f"data/saved/*_{item_id}.json")
    if not files:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan di riwayat")
    deleted_count = 0
    for f in files:
        try:
            os.remove(f)
            deleted_count += 1
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal menghapus file: {e}")
    return {"status": "success", "message": f"Item {item_id} berhasil dihapus.", "deleted": deleted_count}

@app.delete("/api/saved")
def clear_all_saved_items():
    """Menghapus seluruh riwayat simpanan (Clear All History)."""
    files = glob.glob("data/saved/*.json")
    deleted_count = 0
    for f in files:
        try:
            os.remove(f)
            deleted_count += 1
        except Exception:
            pass
    return {"status": "success", "message": f"Seluruh riwayat ({deleted_count} item) berhasil dibersihkan.", "deleted": deleted_count}

class RenameSavedRequest(BaseModel):
    title: str

@app.patch("/api/saved/{item_id}")
def rename_saved_item(item_id: str, req: RenameSavedRequest):
    """Mengubah judul/catatan item riwayat tersimpan."""
    files = glob.glob(f"data/saved/*_{item_id}.json")
    if not files:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    filepath = files[0]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["title"] = req.title.strip()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "success", "message": "Judul item berhasil diperbarui.", "title": req.title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memperbarui item: {e}")

# ==============================================================
# FITUR EXPORT LENGKAP: EXCEL (MULTI-SHEET), CSV, JSON, & BATCH ZIP
# ==============================================================

def generate_excel_bytes_from_bundle(data: Dict[str, Any]) -> io.BytesIO:
    """Menghasilkan file Excel (.xlsx) dengan 3 Sheet: Metadata, Transcript, Komentar & Balasan."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Metadata
        meta = data.get("metadata", {})
        meta_rows = [
            {"Parameter": "ID Konten", "Value": data.get("id", "")},
            {"Parameter": "Platform", "Value": data.get("platform", "").upper()},
            {"Parameter": "Judul", "Value": meta.get("title", "")},
            {"Parameter": "Pembuat / Channel", "Value": meta.get("channel") or meta.get("author", "")},
            {"Parameter": "Views", "Value": meta.get("view_count", 0)},
            {"Parameter": "Likes", "Value": meta.get("like_count", 0)},
            {"Parameter": "Komentar Utama Terunduh", "Value": data.get("comments_count_scraped", 0)},
            {"Parameter": "Waktu Scraping", "Value": data.get("scraped_at", "")},
            {"Parameter": "URL Asli", "Value": meta.get("url", "")}
        ]
        pd.DataFrame(meta_rows).to_excel(writer, sheet_name="Metadata", index=False)

        # Sheet 2: Transkrip Linimasa
        transcript = data.get("context_transcript", {})
        segments = transcript.get("segments", [])
        if segments:
            t_rows = []
            for s in segments:
                start_sec = s.get("start", 0)
                m = int(start_sec // 60)
                sec = int(start_sec % 60)
                t_rows.append({
                    "Timestamp": f"{m:02d}:{sec:02d}",
                    "Detik_Mulai": round(start_sec, 2),
                    "Durasi": s.get("duration", 0),
                    "Teks_Ucapan": s.get("text", "")
                })
            pd.DataFrame(t_rows).to_excel(writer, sheet_name="Transkrip_Linimasa", index=False)
        else:
            pd.DataFrame([{"Transkrip_Full": transcript.get("full_text", "Tidak ada subtitle")}]).to_excel(writer, sheet_name="Transkrip_Linimasa", index=False)

        # Sheet 3: Komentar & Replies (Hierarchy)
        comments = data.get("comments", [])
        c_rows = []
        for idx, c in enumerate(comments, 1):
            c_rows.append({
                "Tipe": "Komentar Utama",
                "Induk_ID": "-",
                "Komentar_ID": c.get("cid", f"cid_{idx}"),
                "Author": c.get("author", "Netizen"),
                "Likes_Votes": c.get("votes", 0),
                "Waktu": c.get("time", ""),
                "Isi_Komentar": c.get("text", "")
            })
            for rep in c.get("replies", []):
                c_rows.append({
                    "Tipe": "Balasan (Reply)",
                    "Induk_ID": c.get("cid", f"cid_{idx}"),
                    "Komentar_ID": rep.get("cid", "-"),
                    "Author": rep.get("author", "Netizen"),
                    "Likes_Votes": rep.get("votes", 0),
                    "Waktu": rep.get("time", ""),
                    "Isi_Komentar": rep.get("text", "")
                })
        pd.DataFrame(c_rows).to_excel(writer, sheet_name="Komentar_Netizen", index=False)

    output.seek(0)
    return output

@app.get("/api/export/{item_id}")
def export_single_item(item_id: str, format: str = "xlsx"):
    """Export satu konten yang sedang dibuka ke Excel, CSV, atau JSON."""
    files = glob.glob(f"data/saved/*_{item_id}.json")
    if not files:
        # Coba periksa file temporary hasil scrape di data/youtube
        files = glob.glob(f"data/youtube/{item_id}_full_data.json")
    if not files:
        raise HTTPException(status_code=404, detail="Data konten tidak ditemukan untuk diekspor")

    with open(files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    title_slug = "".join([c if c.isalnum() else "_" for c in data.get("metadata", {}).get("title", item_id)])[:40]

    if format == "xlsx":
        excel_stream = generate_excel_bytes_from_bundle(data)
        headers = {"Content-Disposition": f'attachment; filename="Export_{data.get("platform","item")}_{title_slug}.xlsx"'}
        return StreamingResponse(excel_stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

    elif format == "csv":
        # Export komentar & balasan dalam bentuk CSV datar yang cocok untuk Data Science / Pandas
        comments = data.get("comments", [])
        c_rows = []
        for idx, c in enumerate(comments, 1):
            c_rows.append({
                "Tipe": "Komentar Utama",
                "Induk_ID": "-",
                "Komentar_ID": c.get("cid", f"cid_{idx}"),
                "Author": c.get("author", "Netizen"),
                "Likes_Votes": c.get("votes", 0),
                "Waktu": c.get("time", ""),
                "Isi_Komentar": c.get("text", "")
            })
            for rep in c.get("replies", []):
                c_rows.append({
                    "Tipe": "Balasan (Reply)",
                    "Induk_ID": c.get("cid", f"cid_{idx}"),
                    "Komentar_ID": rep.get("cid", "-"),
                    "Author": rep.get("author", "Netizen"),
                    "Likes_Votes": rep.get("votes", 0),
                    "Waktu": rep.get("time", ""),
                    "Isi_Komentar": rep.get("text", "")
                })
        df = pd.DataFrame(c_rows)
        csv_bytes = io.BytesIO()
        df.to_csv(csv_bytes, index=False, encoding="utf-8-sig")
        csv_bytes.seek(0)
        headers = {"Content-Disposition": f'attachment; filename="Comments_{title_slug}.csv"'}
        return StreamingResponse(csv_bytes, media_type="text/csv", headers=headers)

    elif format == "json":
        json_bytes = io.BytesIO(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
        headers = {"Content-Disposition": f'attachment; filename="FullData_{title_slug}.json"'}
        return StreamingResponse(json_bytes, media_type="application/json", headers=headers)
    else:
        raise HTTPException(status_code=400, detail="Format tidak didukung. Pilih xlsx, csv, atau json.")

@app.get("/api/export-all")
def export_all_saved_data():
    """Mengunduh seluruh database konten yang tersimpan dalam format ZIP berisi file Excel tiap project."""
    saved_files = glob.glob("data/saved/*.json")
    if not saved_files:
        raise HTTPException(status_code=404, detail="Belum ada konten yang tersimpan di database untuk diekspor")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for fpath in saved_files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    item_data = json.load(f)
                item_id = item_data.get("id", "item")
                platform = item_data.get("platform", "media")
                title_slug = "".join([c if c.isalnum() else "_" for c in item_data.get("metadata", {}).get("title", item_id)])[:30]

                # Masukkan file Excel untuk tiap konten ke dalam ZIP
                excel_io = generate_excel_bytes_from_bundle(item_data)
                zip_file.writestr(f"{platform.upper()}_{item_id}_{title_slug}.xlsx", excel_io.getvalue())
            except Exception as e:
                print(f"Error packing {fpath} to zip: {e}")

    zip_buffer.seek(0)
    current_date = time.strftime("%Y%m%d_%H%M")
    headers = {"Content-Disposition": f'attachment; filename="SocialIntelligence_FullBackup_{current_date}.zip"'}
    return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)

class SentimentPredictRequest(BaseModel):
    text: str

@app.get("/api/sentiment/summary")
def get_sentiment_summary():
    """Mengembalikan ringkasan dataset, distribusi sentimen, dan tabel metrik evaluasi 3 metode."""
    srv = SentimentResearchService.get_instance()
    summary = srv.get_summary()
    return summary

@app.get("/api/sentiment/dataset")
def get_sentiment_dataset(
    page: int = 1,
    page_size: int = 20,
    platform: str = "all",
    sentiment: str = "all",
    query: str = "",
    split: str = "all",
    status_filter: str = "all"
):
    """Mengambil data komentar terproses untuk visualisasi tabel di frontend dengan filter akurasi dan split."""
    srv = SentimentResearchService.get_instance()
    return srv.get_dataset_page(page=page, page_size=page_size, platform=platform, sentiment=sentiment, query=query, split=split, status_filter=status_filter)

@app.post("/api/sentiment/predict")
def predict_custom_sentiment(req: SentimentPredictRequest):
    """Menjalankan preprocessing 5 tahap dan inferensi komparasi 3 metode untuk teks input."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Teks tidak boleh kosong.")
    srv = SentimentResearchService.get_instance()
    return srv.predict_text(req.text)

@app.get("/api/sentiment/export/dataset")
def export_sentiment_dataset(format: str = "xlsx", platform: str = "all"):
    """Mengunduh dataset preprocessed lengkap dalam format Excel atau CSV (bisa difilter platform: all, youtube, instagram)."""
    p_lower = platform.lower()
    if p_lower == "youtube":
        suffix = "_youtube"
        name_tag = "YouTube"
    elif p_lower == "instagram":
        suffix = "_instagram"
        name_tag = "Instagram"
    else:
        suffix = ""
        name_tag = "Combined"

    ext = "xlsx" if format == "xlsx" else "csv"
    fpath = f"data/dataset_bbm_preprocessed{suffix}.{ext}"
    filename = f"Dataset_BBM_Preprocessed_{name_tag}.{ext}"
    
    if not os.path.exists(fpath):
        fpath = f"data/dataset_bbm_preprocessed.{ext}"
        filename = f"Dataset_BBM_Preprocessed.{ext}"
        
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="File dataset belum tersedia.")
        
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if ext == "xlsx" else "text/csv"
    return FileResponse(fpath, filename=filename, media_type=media_type)

@app.get("/api/sentiment/export/ground-truth")
def export_sentiment_ground_truth(format: str = "xlsx", platform: str = "all"):
    """Mengunduh file Ground Truth resmi LLM (bisa difilter platform: all, youtube, instagram)."""
    p_lower = platform.lower()
    if p_lower == "youtube":
        suffix = "_youtube"
        name_tag = "YouTube"
    elif p_lower == "instagram":
        suffix = "_instagram"
        name_tag = "Instagram"
    else:
        suffix = ""
        name_tag = "Combined"

    ext = "xlsx" if format == "xlsx" else "csv"
    fpath = f"data/dataset_bbm_ground_truth{suffix}.{ext}"
    filename = f"Ground_Truth_BBM_{name_tag}.{ext}"
    
    if not os.path.exists(fpath):
        fpath = f"data/dataset_bbm_ground_truth.{ext}"
        filename = f"Ground_Truth_BBM.{ext}"
        
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="File ground truth belum tersedia.")
        
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if ext == "xlsx" else "text/csv"
    return FileResponse(fpath, filename=filename, media_type=media_type)

@app.get("/api/sentiment/export/presentation")
def export_sentiment_presentation():
    """Mengunduh slide presentasi PowerPoint proyek dalam format .pptx."""
    fpath = "Presentasi_Riset_Sentimen_BBM.pptx"
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="File presentasi PowerPoint belum tersedia.")
    return FileResponse(
        fpath,
        filename="Presentasi_Riset_Sentimen_BBM.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

@app.get("/api/sentiment/export/evaluation")
def export_sentiment_evaluation():
    """Mengunduh laporan komparasi 3 metode dalam format Excel."""
    fpath = "data/evaluasi_komparasi_sentimen.xlsx"
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="File laporan evaluasi belum tersedia.")
    return FileResponse(
        fpath,
        filename="Laporan_Evaluasi_Komparasi_Sentimen.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Static Frontend Mount
os.makedirs("frontend/dist", exist_ok=True)
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    import socket

    def is_port_in_use(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    target_port = int(os.environ.get("PORT", 8000))
    if target_port == 8000 and is_port_in_use(8000):
        target_port = 8001
        print(f"[!] Port 8000 sedang digunakan oleh aplikasi lain. Server dialihkan ke port {target_port}")

    print(f"[+] Menjalankan server di http://127.0.0.1:{target_port}")
    uvicorn.run("server:app", host="127.0.0.1", port=target_port, reload=True)
