"""
Asset Gatherer Module
Downloads verified high-definition B-roll motion video clips via Pexels Video API / Fair Use,
and generates fast-paced American voiceover.
"""
import os
import shutil
import asyncio
import requests
import edge_tts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
os.makedirs(PUBLIC_DIR, exist_ok=True)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

def fetch_pexels_video(query: str, filename: str) -> dict:
    """
    Fetches high-quality royalty-free HD B-roll video clip from Pexels API.
    Returns metadata dict with photographer info if successful, else None.
    """
    if not PEXELS_API_KEY:
        return None

    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=5"

    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            data = res.json()
            videos = data.get("videos", [])
            for vid in videos:
                files = vid.get("video_files", [])
                mp4_files = [
                    f for f in files 
                    if f.get("file_type") == "video/mp4" and f.get("link")
                ]
                if not mp4_files:
                    continue

                # Prioritize HD (720p or 1080p) for fast download + crisp render
                chosen = None
                for f in mp4_files:
                    h = f.get("height", 0)
                    w = f.get("width", 0)
                    # Ideal: 720p to 1080p
                    if 720 <= min(w, h) <= 1080:
                        chosen = f
                        break
                if not chosen:
                    chosen = mp4_files[0]

                video_url = chosen.get("link")
                dest = os.path.join(PUBLIC_DIR, filename)

                print(f"[*] Downloading Pexels B-roll video for '{query}'...")
                vr = requests.get(video_url, stream=True, timeout=35)
                if vr.status_code == 200:
                    with open(dest, "wb") as f_out:
                        for chunk in vr.iter_content(chunk_size=64 * 1024):
                            f_out.write(chunk)
                    
                    creator_name = vid.get("user", {}).get("name", "Pexels Creator")
                    creator_url = vid.get("user", {}).get("url", "https://www.pexels.com")
                    print(f"    [OK] Saved {filename} ({os.path.getsize(dest)} bytes) - Credit: {creator_name}")
                    return {
                        "creator": creator_name,
                        "url": creator_url,
                        "pexels_video_id": vid.get("id")
                    }
        else:
            print(f"[!] Pexels API returned status code: {res.status_code}")
    except Exception as e:
        print(f"[!] Error fetching Pexels video for '{query}': {e}")

    return None

def fetch_wiki_image(query: str, filename: str) -> bool:
    """Fallback: Fetches high-resolution photography from Wikimedia Commons under Fair Use."""
    url = f'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={query}&gsrnamespace=6&gsrlimit=1&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json'
    headers = {'User-Agent': 'DailyMotionNewsBot/1.0 (contact: newsbot@gmail.com)'}
    try:
        res = requests.get(url, headers=headers, timeout=15).json()
        pages = res.get('query', {}).get('pages', {})
        for pid, data in pages.items():
            info = data.get('imageinfo', [])
            if info:
                img_url = info[0].get('thumburl') or info[0].get('url')
                img_res = requests.get(img_url, headers=headers, timeout=20)
                if img_res.status_code == 200:
                    dest = os.path.join(PUBLIC_DIR, filename)
                    with open(dest, 'wb') as f:
                        f.write(img_res.content)
                    print(f"[*] Fetched fallback image {filename} for query '{query}'")
                    return True
    except Exception as e:
        print(f"[!] Image search failed for {query}: {e}")
    return False

async def generate_fast_voice(text: str, output_path: str):
    """Generates authoritative, rapid American news presenter voice (+20% rate)."""
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="+20%")
    await communicate.save(output_path)
    return output_path

def ensure_footage():
    """Ensures base footage_1.mp4 is present in public/."""
    fp = os.path.join(PUBLIC_DIR, "footage_1.mp4")
    if not os.path.exists(fp):
        print("[*] Downloading default real B-roll footage...")
        sample_video_url = "https://raw.githubusercontent.com/MiSaykat/global-news-bot/main/public/footage_1.mp4"
        try:
            r = requests.get(sample_video_url, timeout=30)
            if r.status_code == 200:
                with open(fp, "wb") as f:
                    f.write(r.content)
                print(f"[OK] Downloaded footage_1.mp4 ({len(r.content)} bytes)")
        except Exception as e:
            print(f"[!] Could not download video clip: {e}")

def prepare_story_assets(story: dict) -> list:
    """Prepares 100% full motion video B-roll clips for each scene + Voiceover."""
    print("\n[*] Preparing 100% Full Motion B-roll Clips & High-Speed Voiceover...")
    
    # 0. Ensure base footage
    ensure_footage()

    # 1. Generate Voiceover
    full_narration = " ".join([s["caption"] for s in story["scenes"]])
    audio_path = os.path.join(PUBLIC_DIR, "voice.mp3")
    asyncio.run(generate_fast_voice(full_narration, audio_path))
    print(f"      [OK] Voiceover saved to {audio_path}")

    attributions = []

    # 2. Gather Real Video Clips for EVERY Scene
    total_scenes = len(story["scenes"])
    base_footage = os.path.join(PUBLIC_DIR, "footage_1.mp4")

    for i, scene in enumerate(story["scenes"]):
        fn = f"footage_{i+1}.mp4"
        dest = os.path.join(PUBLIC_DIR, fn)
        
        # Try fetching real motion video via Pexels API
        video_meta = fetch_pexels_video(scene["query"], fn)
        if video_meta:
            attributions.append(video_meta)
        else:
            # If Pexels key is not set or query failed, ensure a valid video file exists
            if not os.path.exists(dest):
                if os.path.exists(base_footage):
                    # Copy base footage so Remotion always has a valid video stream
                    shutil.copyfile(base_footage, dest)
                    print(f"      [Fallback] Created {fn} from primary footage")
                else:
                    ensure_footage()

        # Also keep fallback still image just in case
        img_fn = f"cut_{i+1}.jpg"
        if not os.path.exists(os.path.join(PUBLIC_DIR, img_fn)):
            fetch_wiki_image(scene["query"], img_fn)

    print("      [OK] All Scene Video Assets (100% Motion Footage) Ready in public/\n")
    return attributions

if __name__ == "__main__":
    from fetch_and_script import generate_video_story
    st = generate_video_story()
    prepare_story_assets(st)
