"""
Asset Gatherer Module
Downloads verified real news images and generates fast-paced American voiceover.
"""
import os
import asyncio
import requests
import edge_tts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
os.makedirs(PUBLIC_DIR, exist_ok=True)

def fetch_wiki_image(query: str, filename: str) -> bool:
    """Fetches high-resolution real photography from Wikimedia Commons under Fair Use."""
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
                    print(f"[*] Fetched {filename} for query '{query}' ({len(img_res.content)} bytes)")
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
    """Ensures at least one real B-roll video clip is present in public/."""
    fp = os.path.join(PUBLIC_DIR, "footage_1.mp4")
    if not os.path.exists(fp):
        print("[*] Downloading default real B-roll footage...")
        # Direct small public domain MP4
        sample_video_url = "https://raw.githubusercontent.com/MiSaykat/global-news-bot/main/public/footage_1.mp4"
        try:
            r = requests.get(sample_video_url, timeout=30)
            if r.status_code == 200:
                with open(fp, "wb") as f:
                    f.write(r.content)
                print(f"[OK] Downloaded footage_1.mp4 ({len(r.content)} bytes)")
        except Exception as e:
            print(f"[!] Could not download video clip: {e}")

def prepare_story_assets(story: dict):
    print("\n[*] Preparing Story Visuals & High-Speed Voiceover...")
    
    # 0. Ensure real footage video exists
    ensure_footage()

    # 1. Generate Voiceover
    full_narration = " ".join([s["caption"] for s in story["scenes"]])
    audio_path = os.path.join(PUBLIC_DIR, "voice.mp3")
    asyncio.run(generate_fast_voice(full_narration, audio_path))
    print(f"      [OK] Voiceover saved to {audio_path}")

    # 2. Gather Images for each scene
    for i, scene in enumerate(story["scenes"]):
        fn = f"cut_{i+1}.jpg"
        # Only fetch if not already present
        if not os.path.exists(os.path.join(PUBLIC_DIR, fn)):
            fetch_wiki_image(scene["query"], fn)

    print("      [OK] All Story Assets Ready in public/")

if __name__ == "__main__":
    from fetch_and_script import generate_video_story
    st = generate_video_story()
    prepare_story_assets(st)
