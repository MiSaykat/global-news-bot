"""
WooW Entertainment Video Automation for Indian Prime Time
Fetches unposted videos (trailers, teasers, and episodes) from @woowchannels,
and publishes them at Indian Peak Hours (1:30 PM IST & 8:30 PM IST) to Dailymotion & YouTube.
"""
import os
import sys
import json
import subprocess
import datetime
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from auto_publisher import upload_to_dailymotion, upload_to_youtube

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMP_DIR = os.path.join(BASE_DIR, "temp_woow")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(DATA_DIR, "woow_history.json")
CHANNEL_URL = "https://www.youtube.com/@woowchannels/videos"

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
        json.dump({"posted_ids": list(posted_ids), "last_updated": str(datetime.datetime.now())}, f, indent=2)

def fetch_channel_videos() -> list:
    """Uses yt-dlp to extract latest video list without downloading."""
    python_exe = sys.executable
    cmd = [
        python_exe, "-m", "yt_dlp",
        "--flat-playlist",
        "--dump-json",
        CHANNEL_URL,
        "--playlist-end", "40"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=60)
        videos = []
        for line in res.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                v = json.loads(line)
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
            except Exception:
                continue
        return videos
    except Exception as e:
        print(f"[!] Error querying channel videos: {e}")
        return []

def download_video(video_info: dict) -> str:
    """Downloads video in optimized 720p/1080p MP4 using mobile clients to bypass rate-limits."""
    vid = video_info["id"]
    output_template = os.path.join(TEMP_DIR, f"{vid}.mp4")

    # If already downloaded
    if os.path.exists(output_template) and os.path.getsize(output_template) > 1024:
        return output_template

    python_exe = sys.executable
    cmd = [
        python_exe, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=android,mweb,web",
        "-f", "18/bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        video_info["url"]
    ]
    print(f"[*] Downloading: {video_info['title']} ({video_info.get('duration')}s)...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if os.path.exists(output_template) and os.path.getsize(output_template) > 1024:
        size_mb = os.path.getsize(output_template) / (1024 * 1024)
        print(f"    [OK] Downloaded successfully: {size_mb:.1f} MB")
        return output_template
    else:
        print(f"[!] Download failed: {res.stderr[:300]}")
        return None

def process_next_woow_video():
    """Main runner: finds next unposted video and publishes to Dailymotion & YouTube."""
    print("=" * 60)
    print("🎬 WOOW ENTERTAINMENT INDIAN PEAK-HOUR AUTOMATION")
    print(f"[*] Time (UTC): {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    history = load_history()
    print(f"[*] Total previously posted videos: {len(history)}")

    videos = fetch_channel_videos()
    if not videos:
        print("[!] No videos fetched from channel.")
        return False

    # Find unposted videos
    unposted = [v for v in videos if v["id"] not in history]
    if not unposted:
        print("[!] All fetched videos have already been posted!")
        return False

    # Prioritize viral trailers, teasers, and promo clips (30s to 15m) for maximum engagement
    short_unposted = [v for v in unposted if 30 <= (v.get("duration") or 0) <= 900]
    target = short_unposted[0] if short_unposted else unposted[0]

    print(f"[*] Selected Next Video: [{target['id']}] {target['title']}")
    
    # Download
    video_path = download_video(target)
    if not video_path:
        print("[!] Could not download video.")
        return False

    # Publish
    title = target["title"]
    description = (
        f"{title}\n\n"
        f"Watch trending Hindi Web Series, Trailers and Drama episodes.\n"
        f"Subscribe for more exciting Indian web series updates and episodes.\n\n"
        f"#HindiWebSeries #WooW #WebSeries #Drama #IndianSeries"
    )
    tags = ["HindiWebSeries", "WooW", "Drama", "IndianDrama", "Episode", "Trailer"]

    print("\n[*] Publishing to Dailymotion & YouTube...")
    dm_ok = upload_to_dailymotion(video_path, title, description, tags)
    yt_ok = upload_to_youtube(video_path, title, description, tags, is_short=False)

    # Save to history so it's not repeated
    history.add(target["id"])
    save_history(history)
    print(f"[OK] History updated. Video ID '{target['id']}' marked as posted.")

    # Clean up temp file to save disk space
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
            print("[*] Cleaned up temporary video file.")
    except Exception:
        pass

    return True

if __name__ == "__main__":
    process_next_woow_video()
