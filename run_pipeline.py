"""
Master Hourly Orchestrator
Executes: Live News Script -> Assets/Voice -> Remotion Render (9:16 & 16:9) -> Simultaneous Upload.
"""
import os
import sys
import subprocess
import argparse

# Force utf-8 for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from fetch_and_script import generate_video_story
from gather_assets import prepare_story_assets
from auto_publisher import publish_all, is_us_sleep_hours

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "out")
os.makedirs(OUT_DIR, exist_ok=True)

def run_pipeline(force_publish: bool = False, skip_render: bool = False):
    print("\n" + "="*60)
    print("🌍 STARTING 24/7 GLOBAL AUTOMATED NEWS PIPELINE")
    print("="*60)

    # Step 0: Check Sleep Window (00:00 - 06:00 EST)
    if not force_publish and is_us_sleep_hours():
        print("[!] Stopping pipeline during US sleeping window.")
        return

    # Step 1: Story Scripting
    print("\n[1/4] 📰 Generating Live Breaking News Story...")
    story = generate_video_story()
    print(f"      📌 Title: {story['title']}")
    print(f"      🏷️  Category: {story['category']}")
    print(f"      💬 Question: {story['question']}")

    # Step 2: Asset & Voice Generation
    print("\n[2/4] 🎙️  Synthesizing American Voiceover & Downloading Fair-Use Visuals...")
    prepare_story_assets(story)

    shorts_mp4 = os.path.join(OUT_DIR, "remotion_news_shorts_9x16.mp4")
    landscape_mp4 = os.path.join(OUT_DIR, "remotion_news_landscape_16x9.mp4")

    # Step 3: Remotion Rendering
    if not skip_render:
        print("\n[3/4] 🎬 Rendering Remotion Studio Videos (9:16 Shorts & 16:9 Broadcast)...")
        # Ensure node in path
        npx_cmd = "npx"
        if os.name == 'nt' and os.path.exists(r"C:\Program Files\nodejs\npx.cmd"):
            npx_cmd = r"C:\Program Files\nodejs\npx.cmd"

        print("      - Rendering 16:9 Landscape Broadcast Video...")
        subprocess.run([
            npx_cmd, "remotion", "render", "src/index.ts", "NewsLandscape",
            landscape_mp4, "--codec", "h264", "--crf", "18"
        ], cwd=BASE_DIR, check=True)

        print("      - Rendering 9:16 Shorts / Reels Video...")
        subprocess.run([
            npx_cmd, "remotion", "render", "src/index.ts", "NewsShorts",
            shorts_mp4, "--codec", "h264", "--crf", "18"
        ], cwd=BASE_DIR, check=True)

        print(f"      [OK] Both MP4 Files Successfully Generated in {OUT_DIR}")
    else:
        print("\n[3/4] ℹ️  Render skipped (--skip-render flag passed).")

    # Step 4: Simultaneous Publishing
    print("\n[4/4] 🌐 Publishing to Dailymotion and YouTube...")
    publish_all(landscape_mp4, shorts_mp4, story, ignore_sleep=force_publish)

    print("\n" + "="*60)
    print("✨ HOURLY BROADCAST COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="24/7 Global News Automation")
    parser.add_argument("--force", action="store_true", help="Ignore US midnight sleep window")
    parser.add_argument("--skip-render", action="store_true", help="Skip video render and only publish existing files")
    args = parser.parse_args()

    run_pipeline(force_publish=args.force, skip_render=args.skip_render)
