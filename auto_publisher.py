"""
Auto-Publisher Module
Handles simultaneous posting to Dailymotion (16:9) and YouTube (Shorts 9:16 + Regular 16:9).
Includes US Eastern Time (EST) sleep window logic.
"""
import os
import sys
import datetime
import requests

try:
    import pytz
except ImportError:
    pytz = None

def is_us_sleep_hours() -> bool:
    """
    Checks if current time is within US Eastern Time (EST) midnight window (00:00 - 06:00 EST).
    During these hours, posting is paused to avoid dead-traffic algorithm penalties.
    """
    if pytz:
        est = pytz.timezone('US/Eastern')
        now_est = datetime.datetime.now(est)
    else:
        # Fallback approximation: UTC-5
        now_utc = datetime.datetime.utcnow()
        now_est = now_utc - datetime.timedelta(hours=5)

    hour = now_est.hour
    print(f"[*] Current US Eastern Time (EST): {now_est.strftime('%Y-%m-%d %H:%M:%S')} (Hour: {hour})")
    
    if 0 <= hour < 6:
        print("[!] US MIDNIGHT SLEEP MODE: Audience is asleep (00:00-06:00 EST). Skipping publish to protect reach.")
        return True
    return False

def upload_to_dailymotion(file_path: str, title: str, description: str, tags: list):
    """
    Uploads 16:9 Landscape video to Dailymotion via REST API.
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
        # Step 1: OAuth2 token
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

        # Step 2: Get upload URL
        upload_init = requests.get("https://api.dailymotion.com/file/upload", headers=headers, timeout=30).json()
        upload_url = upload_init.get("upload_url")
        if not upload_url:
            print(f"[!] Failed to get upload URL: {upload_init}")
            return False

        # Step 3: Stream file
        print(f"[*] Uploading 16:9 video to Dailymotion ({os.path.getsize(file_path) / (1024*1024):.1f} MB)...")
        with open(file_path, "rb") as f:
            file_res = requests.post(upload_url, files={"file": f}, timeout=300).json()
            hosted_url = file_res.get("url")

        # Step 4: Publish
        publish_res = requests.post("https://api.dailymotion.com/me/videos", headers=headers, data={
            "url": hosted_url,
            "title": title[:255],
            "description": description,
            "published": "true",
            "tags": ",".join(tags) if tags else "news,breaking,usa"
        }, timeout=30).json()

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

def upload_to_youtube(file_path: str, title: str, description: str, tags: list, is_short: bool = False):
    """
    Uploads video to YouTube using YouTube Data API v3.
    """
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")

    if not all([refresh_token, client_id, client_secret]):
        print(f"[!] YouTube credentials missing. Set YOUTUBE_REFRESH_TOKEN, YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET.")
        return False

    final_title = f"{title} #Shorts" if is_short else title
    print(f"[*] Uploading to YouTube ({'Shorts 9:16' if is_short else 'Landscape 16:9'}): {final_title}...")
    
    # Refresh OAuth2 token
    try:
        r = requests.post("https://oauth2.googleapis.com/token", data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }, timeout=30).json()
        
        access_token = r.get("access_token")
        if not access_token:
            print(f"[!] YouTube Token Refresh Failed: {r}")
            return False

        # Resumable upload metadata init
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(os.path.getsize(file_path))
        }

        body = {
            "snippet": {
                "title": final_title[:100],
                "description": description,
                "tags": tags,
                "categoryId": "25" # News & Politics
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        init_req = requests.post(
            "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
            headers=headers,
            json=body,
            timeout=30
        )

        upload_location = init_req.headers.get("Location")
        if not upload_location:
            print(f"[!] YouTube Upload Location Init Failed: {init_req.text}")
            return False

        # Upload the video binary
        with open(file_path, "rb") as f:
            upload_res = requests.put(
                upload_location,
                headers={"Content-Type": "video/mp4"},
                data=f,
                timeout=300
            ).json()

        yt_id = upload_res.get("id")
        if yt_id:
            print(f"[SUCCESS] YouTube Video Published: https://youtu.be/{yt_id}")
            return True
        else:
            print(f"[!] YouTube Upload Failed: {upload_res}")
            return False
    except Exception as e:
        print(f"[!] YouTube Exception: {e}")
        return False

def publish_all(landscape_file: str, shorts_file: str, story: dict, ignore_sleep: bool = False):
    """
    Executes simultaneous multi-platform publishing.
    """
    if not ignore_sleep and is_us_sleep_hours():
        return

    title = story.get("title", "Breaking News Alert")
    desc = f"{story.get('title')}\n\nQuestion of the Day: {story.get('question')}\n\nFootage licensed under Fair Use for educational news reporting."
    tags = story.get("tags", ["News", "Breaking", "USA"])

    print("\n" + "="*50)
    print("🚀 PUBLISHING SIMULTANEOUSLY ACROSS PLATFORMS")
    print("="*50)

    # 1. Dailymotion: 16:9 Landscape Video
    if os.path.exists(landscape_file):
        upload_to_dailymotion(landscape_file, title, desc, tags)

    # 2. YouTube: 9:16 Shorts
    if os.path.exists(shorts_file):
        upload_to_youtube(shorts_file, title, desc, tags, is_short=True)

    # 3. YouTube: 16:9 Landscape
    if os.path.exists(landscape_file):
        upload_to_youtube(landscape_file, title, desc, tags, is_short=False)

    print("="*50 + "\n")

if __name__ == "__main__":
    test_story = {
        "title": "Why Big Tech is Buying Nuclear Power Plants",
        "question": "Will AI cause nationwide power blackouts in America?",
        "tags": ["AI", "TechNews", "EnergyCrisis", "USA"]
    }
    land = os.path.join(os.path.dirname(__file__), "out", "remotion_news_landscape_16x9.mp4")
    sh = os.path.join(os.path.dirname(__file__), "out", "remotion_news_shorts_9x16.mp4")
    publish_all(land, sh, test_story, ignore_sleep=True)
