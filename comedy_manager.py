"""
Comedy Show Video Automation for Indian Prime Time & Peak Hours
Fetches unposted videos in chronological order (from the very beginning/oldest to newest)
from @RDCComedyShow and publishes 5 times daily at peak traffic hours to Dailymotion & YouTube.
"""
import os
import sys
import json
import subprocess
import datetime
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from auto_publisher import upload_to_dailymotion, upload_to_youtube

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMP_DIR = os.path.join(BASE_DIR, "temp_comedy")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(DATA_DIR, "comedy_history.json")
CHANNEL_URL = "https://www.youtube.com/@RDCComedyShow/videos"

def load_history() -> set:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("posted_ids", []))
        except Exception:
            return set()
    return set()

def save_history(posted_ids: set):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "posted_ids": list(posted_ids),
            "last_updated": str(datetime.datetime.now()),
            "total_posted": len(posted_ids)
        }, f, indent=2)

def fetch_channel_videos_oldest_first() -> list:
    """Uses yt-dlp to extract full video list and reverses it to get oldest-to-newest order."""
    python_exe = sys.executable
    cmd = [
        python_exe, "-m", "yt_dlp",
        "--flat-playlist",
        "--dump-single-json",
        CHANNEL_URL
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=120)
        data = json.loads(res.stdout)
        entries = data.get("entries", [])
        print(f"[*] Total videos found on channel: {len(entries)}")
        
        # YouTube returns newest first, so reverse to process from the very beginning
        entries.reverse()
        
        videos = []
        for v in entries:
            vid = v.get("id")
            title = v.get("title", "")
            duration = v.get("duration") or 0
            if vid:
                videos.append({
                    "id": vid,
                    "title": title,
                    "duration": duration,
                    "url": f"https://www.youtube.com/watch?v={vid}"
                })
        return videos
    except Exception as e:
        print(f"[!] Error querying channel videos: {e}")
        return []

def download_video(video_info: dict) -> str:
    """Downloads video in optimized 720p MP4 using mobile clients to bypass rate-limits."""
    vid = video_info["id"]
    output_template = os.path.join(TEMP_DIR, f"{vid}.mp4")

    if os.path.exists(output_template) and os.path.getsize(output_template) > 1024:
        return output_template

    python_exe = sys.executable
    cmd = [
        python_exe, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=android,mweb,web",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        video_info["url"]
    ]
    print(f"[*] Downloading: {video_info['title']} ({video_info.get('duration')}s)...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if os.path.exists(output_template) and os.path.getsize(output_template) > 1024:
        size_mb = os.path.getsize(output_template) / (1024 * 1024)
        print(f"    [OK] Downloaded successfully: {size_mb:.1f} MB")
        return output_template
    else:
        print(f"[!] Download failed: {res.stderr[:300]}")
        return None

def optimize_metadata(title: str):
    """Generates high-ranking SEO titles, descriptions, and trending comedy tags."""
    clean_title = re.sub(r'[\uFEFF\u200B-\u200D]', '', title)
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()
    
    # Ensure brand identity
    if "kapil sharma" not in clean_title.lower():
        optimized_title = f"{clean_title} | Kapil Sharma Comedy Show"
    else:
        optimized_title = clean_title

    description = (
        f"{optimized_title}\n\n"
        f"Get ready for non-stop laughter and rib-tickling comedy moments from The Kapil Sharma Show!\n"
        f"Featuring Krushna Abhishek, Kiku Sharda, Kapil Sharma, Bharti Singh, Chandu, and celebrity guests.\n\n"
        f"Follow & Subscribe for daily high-energy comedy episodes!\n\n"
        f"#TheKapilSharmaShow #KapilSharmaShow #KrushnaAbhishek #HindiComedy #FunnyDeol #TrendingComedy #ComedyTadka"
    )

    tags = [
        "KapilSharmaShow",
        "TheKapilSharmaShow",
        "KrushnaAbhishek",
        "HindiComedy",
        "FunnyDeol",
        "GaramJi",
        "KikuSharda",
        "ComedyShow",
        "LaughterChallenge",
        "TrendingComedy"
    ]

    return optimized_title[:255], description, tags

def process_next_comedy_video():
    """Main runner: finds next unposted video in chronological order and publishes."""
    print("=" * 60)
    print("😂 COMEDY SHOW (KAPIL SHARMA) INDIAN PEAK-HOUR AUTOMATION")
    print(f"[*] Time (UTC): {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    history = load_history()
    print(f"[*] Total previously posted comedy videos: {len(history)}")

    videos = fetch_channel_videos_oldest_first()
    if not videos:
        print("[!] No videos fetched from channel.")
        return False

    # Find next unposted video from the start (chronological order)
    unposted = [v for v in videos if v["id"] not in history]
    if not unposted:
        print("[!] All videos from this channel have been posted!")
        return False

    target = unposted[0]
    print(f"[*] Next Chronological Video: [{target['id']}] {target['title']}")

    video_path = download_video(target)
    if not video_path:
        print("[!] Could not download video.")
        return False

    title, description, tags = optimize_metadata(target["title"])

    print("\n[*] Publishing to Dailymotion & YouTube...")
    dm_ok = upload_to_dailymotion(video_path, title, description, tags)
    yt_ok = upload_to_youtube(video_path, title, description, tags, is_short=False)

    # Save to history
    history.add(target["id"])
    save_history(history)
    print(f"[OK] History updated. Video ID '{target['id']}' marked as posted.")

    # Cleanup temp file
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
            print("[*] Cleaned up temporary video file.")
    except Exception:
        pass

    return True

if __name__ == "__main__":
    process_next_comedy_video()
