import sys
import argparse
from scrapers.youtube_scraper import YouTubeScraper

def main():
    parser = argparse.ArgumentParser(description="Media Sosial Scraper Hub")
    subparsers = parser.add_subparsers(dest="platform", help="Platform yang ingin di-scrape")

    # Parser YouTube
    yt_parser = subparsers.add_parser("youtube", help="Scraping YouTube (Metadata, Transkrip Isi Video, Komentar)")
    yt_parser.add_argument("url", type=str, help="URL video YouTube")
    yt_parser.add_argument("--max-comments", type=int, default=100, help="Jumlah maksimal komentar (default: 100)")

    args = parser.parse_args()

    if args.platform == "youtube":
        scraper = YouTubeScraper()
        print(f"\n[+] Memulai scraping YouTube untuk: {args.url}")
        res = scraper.scrape_all(args.url, max_comments=args.max_comments)
        
        print("\n" + "="*50)
        print("RINGKASAN HASIL:")
        print(f"Judul Video : {res['metadata']['title']}")
        print(f"Channel     : {res['metadata']['channel']}")
        print(f"Views       : {res['metadata']['view_count']:,}")
        print(f"Transkrip   : {'Tersedia (' + str(len(res['context_transcript']['full_text'])) + ' karakter)' if res['context_transcript']['available'] else 'Tidak tersedia / Subtitle disabled'}")
        print(f"Komentar    : {res['comments_count_scraped']} komentar berhasil diunduh")
        print("="*50 + "\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
