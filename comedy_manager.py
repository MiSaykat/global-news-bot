"""
Comedy Show Video Automation for Indian Prime Time & Peak Hours
Fetches unposted videos in chronological order (from the very beginning/oldest to newest)
from @RDCComedyShow and publishes 5 times daily at peak traffic hours to Dailymotion & YouTube.

Optimized with the user's most viral Dailymotion settings:
- Title format: {clean_title} _ The Kapil Sharma Show 2026 _ New Hindi Comedy Episode
- Viral Hashtag Description matching user's top-performing video
- High-Traffic Viral Tags based on user's proven viral video formula
"""
import os
import sys
import json
import subprocess
import datetime
import re
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMP_DIR = os.path.join(BASE_DIR, "temp_comedy")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(DATA_DIR, "comedy_history.json")
CHANNEL_URL = "https://www.youtube.com/@RDCComedyShow/videos"

# Proven viral description from user's screenshot
VIRAL_DESCRIPTION = (
    "#reels #viral #explore #explorepage #instagram #trending #instadaily #viralvideos #reelsinstagram "
    "#model #likes #beautiful #me #trendingreels #beauty #bollywood #goodvibes #art #instalike "
    "#foryoupage #beauty #onlineshopping #liketime #snapchat #bbtaj #photoshoot #smile #cute #post "
    "#comment #nature #instafashion #mumbai #fashionblogger #lifestyle #travel #funny #exploremore "
    "#cold #fashionstyle #instanature #new #comedy #kapilsharma #kapilsharmashow"
)

# Proven viral tags from user's screenshot + targeted comedy keywords
VIRAL_TAGS = [
    "boxoffice", "movieclips", "movie", "clips", "box office", "movie clips", "movie scenes",
    "boxoffice movie scenes", "animation", "movies", "best scenes", "action scenes", "movie trailers",
    "full movie", "full movies", "free movie", "action movie", "movies 2024 full movie", "new movie",
    "2024 movie", "full movie 2024", "comedy", "the kapil sharma show", "kapil sharma show",
    "krushna abhishek", "funny deol", "garam ji", "laughter challenge", "viral", "trending", "comedy clips"
]

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

def format_viral_title(title: str) -> str:
    """Formats title following the high-CTR viral pattern."""
    clean = re.sub(r'[\uFEFF\u200B-\u200D]', '', title)
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    # Matching user's viral style: TITLE _ The Kapil Sharma Show 2026 _ New Hindi Comedy Episode
    if "kapil sharma" not in clean.lower():
        formatted = f"{clean} _ The Kapil Sharma Show 2026 _ New Hindi Comedy Episode"
    else:
        formatted = clean

    return formatted[:255]

def upload_to_dailymotion(file_path: str, title: str, description: str, tags: list):
    """
    Uploads video to Dailymotion applying the user's proven viral title, description, and tags.
    """
    api_key = os.getenv("DM_API_KEY")
    api_secret = os.getenv("DM_API_SECRET")
    username = os.getenv("DM_USERNAME")
    password = os.getenv("DM_PASSWORD")

    if not all([api_key, api_secret, username, password]):
        print("[!] Dailymotion credentials missing. Set DM_API_KEY, DM_API_SECRET, DM_USERNAME, DM_PASSWORD.")
        return False

    print(f"[*] Authenticating with Dailymotion API for: {title}...")
    try:
        # Step 1: OAuth2 Token
        token_res = requests.post("https://api.dailymotion.com/oauth/token", data={
            "grant_type": "password",
            "client_id": api_key,
            "client_secret": api_secret,
            "username": username,
            "password": password,
            "scope": "manage_videos"
        }, timeout=30).json()

        access_token = token_res.get("access_token")
        if not access_token:
            print(f"[!] Dailymotion Auth Failed: {token_res}")
            return False

        headers = {"Authorization": f"Bearer {access_token}"}

        # Step 2: Get Upload URL
        upload_init = requests.get("https://api.dailymotion.com/file/upload", headers=headers, timeout=30).json()
        upload_url = upload_init.get("upload_url")
        if not upload_url:
            print(f"[!] Failed to get upload URL: {upload_init}")
            return False

        # Step 3: Stream Video File
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"[*] Uploading video binary to Dailymotion ({file_size_mb:.1f} MB)...")
        with open(file_path, "rb") as f:
            file_res = requests.post(upload_url, files={"file": f}, timeout=600).json()
            hosted_url = file_res.get("url")

        if not hosted_url:
            print(f"[!] Dailymotion File Upload Failed: {file_res}")
            return False

        # Step 4: Publish with Viral Metadata
        payload = {
            "url": hosted_url,
            "title": title,
            "description": description,
            "tags": ",".join(tags),
            "channel": "fun",
            "published": "true"
        }

        publish_res = requests.post("https://api.dailymotion.com/me/videos", headers=headers, data=payload, timeout=30).json()

        if "id" in publish_res:
            dm_id = publish_res["id"]
            print(f"[SUCCESS] Dailymotion Video Published: https://www.dailymotion.com/video/{dm_id}")
            return True
        else:
            print(f"[!] Dailymotion Publish Failed: {publish_res}")
            return False

    except Exception as e:
        print(f"[!] Dailymotion Exception: {e}")
        return False

def process_next_comedy_video():
    """Main runner: finds next unposted video in chronological order and publishes with Viral Settings."""
    print("=" * 60)
    print("🔥 COMEDY SHOW AUTOMATION - VIRAL BOOST MODE")
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

    title = format_viral_title(target["title"])
    print(f"[*] Viral Title: {title}")
    print(f"[*] Applied Viral Hashtags & High-Volume Tags")

    print("\n[*] Publishing to Dailymotion...")
    dm_ok = upload_to_dailymotion(video_path, title, VIRAL_DESCRIPTION, VIRAL_TAGS)

    # Optional YouTube
    yt_client_id = os.getenv("YOUTUBE_CLIENT_ID")
    if yt_client_id:
        try:
            from auto_publisher import upload_to_youtube
            upload_to_youtube(video_path, title, VIRAL_DESCRIPTION, VIRAL_TAGS, is_short=False)
        except Exception as e:
            print(f"[*] YouTube optional upload skipped or failed: {e}")

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
