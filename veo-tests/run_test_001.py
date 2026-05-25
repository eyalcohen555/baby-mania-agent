"""
VEO 3 Test #001 — minimal, credit-efficient
Model: veo-3.0-fast-generate-001 | Duration: 5s | Resolution: 720p
"""
import os
import sys
import time
import datetime

from dotenv import dotenv_values
from google import genai
from google.genai import types

# ── config ──────────────────────────────────────────────────────────────────
ENV_PATH   = r"C:\Projects\baby-mania-agent\.env"
OUTPUT_MP4 = r"C:\Projects\baby-mania-agent\veo-tests\test_001.mp4"
LOG_PATH   = r"C:\Projects\baby-mania-agent\veo-tests\test_001.log"
MODEL      = "veo-3.0-fast-generate-001"
PROMPT     = "A reborn baby doll lying on a soft white blanket, natural lighting, gentle close-up, photorealistic"
DURATION   = 5
POLL_INTERVAL = 15  # seconds between polls

# ── helpers ──────────────────────────────────────────────────────────────────
def log(msg: str, also_print: bool = True):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    if also_print:
        print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def fail(msg: str):
    log(f"RESULT: FAIL — {msg}")
    sys.exit(1)

# ── main ─────────────────────────────────────────────────────────────────────
def main():
    run_start = datetime.datetime.now()
    log(f"=== VEO TEST 001 START === {run_start.isoformat()}")

    # 1. load credentials
    env = dotenv_values(ENV_PATH)
    api_key = env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY")
    if not api_key:
        fail("No GEMINI_API_KEY or GOOGLE_API_KEY found in .env")
    log(f"API key loaded: ...{api_key[-6:]} (len={len(api_key)})")

    # 2. build client
    client = genai.Client(api_key=api_key)
    log(f"Client ready. Model: {MODEL}")

    # 3. submit generation request
    log("Submitting video generation request...")
    t_submit = time.time()

    try:
        operation = client.models.generate_videos(
            model=MODEL,
            prompt=PROMPT,
            config=types.GenerateVideosConfig(
                aspectRatio="16:9",
                numberOfVideos=1,
            ),
        )
    except Exception as e:
        err = str(e)
        # billing / quota errors
        if any(kw in err.lower() for kw in ["billing", "quota", "429", "403", "paymentrequired", "resourceexhausted"]):
            fail(f"BILLING/QUOTA ERROR — {err}")
        fail(f"Submit failed — {err}")

    log(f"Operation submitted: {operation.name}")

    # 4. poll until done
    poll_count = 0
    while not operation.done:
        poll_count += 1
        elapsed = round(time.time() - t_submit, 1)
        log(f"  polling #{poll_count} — elapsed {elapsed}s — status: not done yet")
        time.sleep(POLL_INTERVAL)
        try:
            operation = client.operations.get(operation)
        except Exception as e:
            fail(f"Poll failed — {e}")

    t_done = time.time()
    gen_seconds = round(t_done - t_submit, 1)
    log(f"Generation complete in {gen_seconds}s ({poll_count} polls)")

    # 5. check for errors in result
    if operation.error and operation.error.code != 0:
        fail(f"Operation error code={operation.error.code} — {operation.error.message}")

    # 6. extract video URI
    result = operation.result
    if not result or not result.generated_videos:
        fail("No generated_videos in result")

    video_obj = result.generated_videos[0]
    log(f"Video object received: {video_obj}")

    # 7. download
    log(f"Downloading to {OUTPUT_MP4} ...")
    try:
        video_bytes = client.files.download(file=video_obj.video)
        with open(OUTPUT_MP4, "wb") as f:
            f.write(video_bytes)
    except Exception as e:
        fail(f"Download failed — {e}")

    # 8. verify file
    if not os.path.exists(OUTPUT_MP4):
        fail("File not written to disk")

    file_size_mb = round(os.path.getsize(OUTPUT_MP4) / 1024 / 1024, 2)
    total_elapsed = round(time.time() - t_submit, 1)

    log(f"RESULT: SUCCESS")
    log(f"  file:     {OUTPUT_MP4}")
    log(f"  size:     {file_size_mb} MB")
    log(f"  gen time: {gen_seconds}s")
    log(f"  total:    {total_elapsed}s")
    log(f"=== VEO TEST 001 DONE ===")

    print()
    print("=" * 50)
    print(f"✅ SUCCESS")
    print(f"   File:    {OUTPUT_MP4}")
    print(f"   Size:    {file_size_mb} MB")
    print(f"   Time:    {gen_seconds}s generation / {total_elapsed}s total")
    print("=" * 50)


if __name__ == "__main__":
    main()
