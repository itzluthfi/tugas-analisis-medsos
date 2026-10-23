import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeScraper:
    def __init__(self, output_dir: str = "data/youtube"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_video_id(self, url_or_id: str) -> str:
        """Ekstrak 11-karakter video ID dari URL YouTube."""
        if "v=" in url_or_id:
            return url_or_id.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url_or_id:
            return url_or_id.split("youtu.be/")[1].split("?")[0]
        return url_or_id.strip()

    def search_videos(self, query: str, max_results: int = 8) -> List[Dict[str, Any]]:
        """Mencari video di YouTube via ytInitialData."""
        results = []
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={encoded}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
            })
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
            
            idx = html.find('var ytInitialData = ')
            if idx != -1:
                end_idx = html.find(';</script>', idx)
                json_str = html[idx + 20:end_idx]
                data = json.loads(json_str)
                
                contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
                for sec in contents:
                    items = sec.get('itemSectionRenderer', {}).get('contents', [])
                    for it in items:
                        if 'videoRenderer' in it:
                            v = it['videoRenderer']
                            vid = v.get('videoId')
                            if not vid:
                                continue
                            
                            title = ""
                            if 'title' in v and 'runs' in v['title']:
                                title = v['title']['runs'][0].get('text', '')
                            
                            channel = ""
                            if 'ownerText' in v and 'runs' in v['ownerText']:
                                channel = v['ownerText']['runs'][0].get('text', '')
                                
                            duration = v.get('lengthText', {}).get('simpleText', '')
                            view_text = v.get('viewCountText', {}).get('simpleText', '')
                            
                            thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                            if 'thumbnail' in v and 'thumbnails' in v['thumbnail'] and v['thumbnail']['thumbnails']:
                                thumb = v['thumbnail']['thumbnails'][-1]['url']
                                
                            results.append({
                                "id": vid,
                                "title": title,
                                "channel": channel,
                                "duration_text": duration,
                                "view_text": view_text,
                                "url": f"https://www.youtube.com/watch?v={vid}",
                                "thumbnail": thumb
                            })
                            if len(results) >= max_results:
                                break
                    if len(results) >= max_results:
                        break
        except Exception as e:
            print(f"[YouTube Search Error]: {e}")
            
        return results

    def get_metadata(self, video_url: str) -> Dict[str, Any]:
        """Mengambil metadata video menggunakan yt-dlp."""
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': False,
            'ignoreerrors': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            if not info:
                vid = self.extract_video_id(video_url)
                return {
                    "id": vid,
                    "title": f"Video #{vid}",
                    "channel": "YouTube Channel",
                    "view_count": 0,
                    "like_count": 0,
                    "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                    "embed_url": f"https://www.youtube.com/embed/{vid}?autoplay=0",
                    "url": video_url
                }
            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "channel": info.get("uploader") or info.get("channel"),
                "duration_seconds": info.get("duration"),
                "view_count": info.get("view_count", 0),
                "like_count": info.get("like_count", 0),
                "comment_count": info.get("comment_count", 0),
                "description": info.get("description", ""),
                "thumbnail": info.get("thumbnail") or f"https://i.ytimg.com/vi/{info.get('id')}/hqdefault.jpg",
                "embed_url": f"https://www.youtube.com/embed/{info.get('id')}?autoplay=0",
                "url": video_url
            }

    def get_transcript(self, video_id: str, languages: List[str] = ['id', 'en']) -> Dict[str, Any]:
        """Mengambil transkrip isi video (mendukung subtitle manual dan auto-generated)."""
        clean_id = self.extract_video_id(video_id)
        result = {
            "available": False,
            "full_text": "",
            "segments": []
        }
        try:
            api = YouTubeTranscriptApi()
            fetched = None
            try:
                # 1. Coba fetch langsung
                fetched = api.fetch(clean_id)
            except Exception:
                # 2. Coba cari dari daftar transcript (manual / auto-generated)
                try:
                    tl = api.list(clean_id)
                    try:
                        t_obj = tl.find_transcript(languages)
                        fetched = t_obj.fetch()
                    except Exception:
                        try:
                            t_obj = tl.find_generated_transcript(languages)
                            fetched = t_obj.fetch()
                        except Exception:
                            # Ambil transcript pertama yang ada
                            for t in tl:
                                fetched = t.fetch()
                                break
                except Exception:
                    pass

            if fetched:
                segments = []
                words = []
                for item in fetched:
                    t = getattr(item, 'text', '') if not isinstance(item, dict) else item.get('text', '')
                    st = getattr(item, 'start', 0) if not isinstance(item, dict) else item.get('start', 0)
                    dur = getattr(item, 'duration', 0) if not isinstance(item, dict) else item.get('duration', 0)
                    segments.append({"text": t, "start": st, "duration": dur})
                    words.append(t)
                    
                result["available"] = True
                result["full_text"] = " ".join(words)
                result["segments"] = segments
            else:
                result["full_text"] = "Subtitle/transkrip tidak tersedia pada video ini."
        except Exception as e:
            result["full_text"] = "Subtitle/transkrip tidak tersedia pada video ini."
            
        return result

    def get_comments(self, video_url: str, max_comments: int = 300, replies_per_comment: int = 10) -> List[Dict[str, Any]]:
        """
        Mengambil komentar netizen dalam jumlah banyak beserta BALASAN (Replies) bersarang (nested).
        """
        top_comments = []
        replies_map = {}

        try:
            fetch_limit = max_comments * 3
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'getcomments': True,
                'extract_flat': False,
                'extractor_args': {
                    'youtube': {
                        'max_comments': [str(fetch_limit), 'all', 'all', 'all']
                    }
                }
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                raw_comments = info.get('comments', []) if info else []
                
                # Pisahkan komentar induk (parent) dan balasan (replies)
                for c in raw_comments:
                    parent_id = c.get('parent')
                    cid = c.get('id')
                    
                    comment_obj = {
                        "cid": cid,
                        "author": c.get("author") or "Netizen",
                        "author_thumbnail": c.get("author_thumbnail", ""),
                        "text": c.get("text", ""),
                        "time": c.get("_time_text") or (f"{c.get('timestamp')}s" if c.get('timestamp') else ""),
                        "votes": c.get("like_count", 0),
                        "replies": []
                    }
                    
                    if parent_id and parent_id != 'root':
                        if parent_id not in replies_map:
                            replies_map[parent_id] = []
                        if len(replies_map[parent_id]) < replies_per_comment:
                            replies_map[parent_id].append(comment_obj)
                    else:
                        if len(top_comments) < max_comments:
                            top_comments.append(comment_obj)
                            
            # Gabungkan replies ke parent comment
            for p in top_comments:
                p["replies"] = replies_map.get(p["cid"], [])
                
        except Exception as e:
            print(f"[Comments Scrape Error]: {e}")
            
        return top_comments
