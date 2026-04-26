"""
Second Hash — X Auto-Poster

Reads the next queued post from social/queue/, posts it via X API v2,
then moves the file to social/posted/ with a timestamp.

Usage:
  python social/post.py

Requires env vars:
  X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
"""

import os
import sys
import json
import hmac
import hashlib
import time
import base64
import urllib.parse
import urllib.request
import ssl
from pathlib import Path
from datetime import datetime, timezone

QUEUE_DIR = Path(__file__).parent / "queue"
POSTED_DIR = Path(__file__).parent / "posted"
POST_URL = "https://api.x.com/2/tweets"
MEDIA_UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"


def oauth_signature(method: str, url: str, params: dict, consumer_secret: str, token_secret: str) -> str:
    base = "&".join([
        method.upper(),
        urllib.parse.quote(url, safe=""),
        urllib.parse.quote("&".join(f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted(params.items())), safe=""),
    ])
    key = f"{urllib.parse.quote(consumer_secret, safe='')}&{urllib.parse.quote(token_secret, safe='')}"
    return base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()


def build_auth_header(method: str, url: str, extra_params: dict | None = None) -> str:
    api_key = os.environ["X_API_KEY"]
    api_secret = os.environ["X_API_SECRET"]
    access_token = os.environ["X_ACCESS_TOKEN"]
    access_secret = os.environ["X_ACCESS_TOKEN_SECRET"]

    oauth_params = {
        "oauth_consumer_key": api_key,
        "oauth_nonce": base64.b64encode(os.urandom(32)).decode().strip("=+/"),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token,
        "oauth_version": "1.0",
    }

    all_params = {**oauth_params}
    if extra_params:
        all_params.update(extra_params)
    sig = oauth_signature(method, url, all_params, api_secret, access_secret)
    oauth_params["oauth_signature"] = sig

    header = "OAuth " + ", ".join(
        f'{k}="{urllib.parse.quote(str(v), safe="")}"'
        for k, v in sorted(oauth_params.items())
    )
    return header


def upload_media(image_path: str) -> str | None:
    """Upload an image to X via v1.1 media/upload and return media_id_string."""
    if not os.path.exists(image_path):
        print(f"[social] Image not found: {image_path}")
        return None

    with open(image_path, "rb") as f:
        image_data = f.read()

    # Build multipart form data
    boundary = "----SecondHashBoundary" + str(int(time.time()))
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media_data"\r\n\r\n'
        f"{base64.b64encode(image_data).decode()}\r\n"
        f"--{boundary}--\r\n"
    ).encode()

    auth = build_auth_header("POST", MEDIA_UPLOAD_URL)
    req = urllib.request.Request(
        MEDIA_UPLOAD_URL,
        data=body,
        headers={
            "Authorization": auth,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            result = json.loads(resp.read().decode())
            media_id = result.get("media_id_string")
            print(f"[social] Uploaded image. Media ID: {media_id}")
            return media_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else "no body"
        print(f"[social] Media upload error {e.code}: {error_body}")
        return None


def upload_video(video_path: str) -> str | None:
    """Upload a video to X via v1.1 chunked media/upload (INIT→APPEND→FINALIZE→STATUS)."""
    if not os.path.exists(video_path):
        print(f"[social] Video not found: {video_path}")
        return None

    file_size = os.path.getsize(video_path)
    print(f"[social] Uploading video ({file_size / 1024:.0f}KB)...")

    # --- INIT ---
    init_params = {
        "command": "INIT",
        "total_bytes": str(file_size),
        "media_type": "video/mp4",
        "media_category": "tweet_video",
    }
    init_body = urllib.parse.urlencode(init_params).encode()
    auth = build_auth_header("POST", MEDIA_UPLOAD_URL)
    req = urllib.request.Request(
        MEDIA_UPLOAD_URL, data=init_body,
        headers={"Authorization": auth, "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            init_result = json.loads(resp.read().decode())
        media_id = init_result["media_id_string"]
        print(f"[social] INIT ok. Media ID: {media_id}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else "no body"
        print(f"[social] Video INIT error {e.code}: {error_body}")
        return None

    # --- APPEND (chunked, 5MB segments) ---
    CHUNK_SIZE = 5 * 1024 * 1024
    with open(video_path, "rb") as f:
        segment = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            boundary = "----SHVideoBoundary" + str(int(time.time())) + str(segment)
            body_parts = []
            body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"command\"\r\n\r\nAPPEND\r\n".encode())
            body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"media_id\"\r\n\r\n{media_id}\r\n".encode())
            body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"segment_index\"\r\n\r\n{segment}\r\n".encode())
            body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"media_data\"\r\n\r\n".encode())
            body_parts.append(base64.b64encode(chunk))
            body_parts.append(f"\r\n--{boundary}--\r\n".encode())
            body = b"".join(body_parts)

            auth = build_auth_header("POST", MEDIA_UPLOAD_URL)
            req = urllib.request.Request(
                MEDIA_UPLOAD_URL, data=body,
                headers={"Authorization": auth, "Content-Type": f"multipart/form-data; boundary={boundary}"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, context=ctx) as resp:
                    resp.read()
                print(f"[social] APPEND segment {segment} ok")
            except urllib.error.HTTPError as e:
                error_body = e.read().decode() if e.fp else "no body"
                print(f"[social] Video APPEND error {e.code}: {error_body}")
                return None
            segment += 1

    # --- FINALIZE ---
    final_params = {"command": "FINALIZE", "media_id": media_id}
    final_body = urllib.parse.urlencode(final_params).encode()
    auth = build_auth_header("POST", MEDIA_UPLOAD_URL)
    req = urllib.request.Request(
        MEDIA_UPLOAD_URL, data=final_body,
        headers={"Authorization": auth, "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            final_result = json.loads(resp.read().decode())
        print(f"[social] FINALIZE ok")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else "no body"
        print(f"[social] Video FINALIZE error {e.code}: {error_body}")
        return None

    # --- STATUS (poll until processing complete) ---
    processing = final_result.get("processing_info")
    while processing and processing.get("state") in ("pending", "in_progress"):
        wait = processing.get("check_after_secs", 5)
        print(f"[social] Video processing... waiting {wait}s")
        time.sleep(wait)
        status_url = f"{MEDIA_UPLOAD_URL}?command=STATUS&media_id={media_id}"
        auth = build_auth_header("GET", MEDIA_UPLOAD_URL, {"command": "STATUS", "media_id": media_id})
        req = urllib.request.Request(status_url, headers={"Authorization": auth}, method="GET")
        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                status_result = json.loads(resp.read().decode())
            processing = status_result.get("processing_info")
        except urllib.error.HTTPError as e:
            print(f"[social] Video STATUS error {e.code}")
            break

    if processing and processing.get("state") == "failed":
        print(f"[social] Video processing failed: {processing.get('error', {})}")
        return None

    print(f"[social] Video ready. Media ID: {media_id}")
    return media_id


def post_tweet(text: str, media_id: str | None = None) -> dict:
    payload = {"text": text}
    if media_id:
        payload["media"] = {"media_ids": [media_id]}

    body = json.dumps(payload).encode()
    auth = build_auth_header("POST", POST_URL)
    req = urllib.request.Request(
        POST_URL,
        data=body,
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read().decode())


def pin_tweet(tweet_id: str, user_id: str) -> bool:
    """Pin a tweet to the user's profile using X API v2."""
    pin_url = f"https://api.x.com/2/users/{user_id}/pinned_lists"
    # Note: X API v2 doesn't have a direct pin endpoint for tweets.
    # We use the bookmarks-like approach via PUT /2/users/:id/pinned_tweets
    # But the actual endpoint for pinning is not publicly available via v2.
    # Pinning must be done manually via X web UI.
    print(f"[social] To pin this tweet, visit: https://x.com/SecondHashHQ/status/{tweet_id}")
    print(f"[social] Click the ··· menu → 'Pin to your profile'")
    return True


def get_next_post() -> Path | None:
    files = sorted(QUEUE_DIR.glob("*.json"))
    return files[0] if files else None


def main():
    POSTED_DIR.mkdir(exist_ok=True)

    # Allow specifying a file: python social/post.py social/queue/pinned_launch.json
    if len(sys.argv) > 1:
        post_file = Path(sys.argv[1])
        if not post_file.exists():
            print(f"[social] File not found: {post_file}")
            sys.exit(1)
    else:
        post_file = get_next_post()

    if not post_file:
        print("[social] No posts in queue. Exiting.")
        sys.exit(0)

    with open(post_file) as f:
        data = json.load(f)

    text = data.get("text", "").strip()
    if not text:
        print(f"[social] Empty text in {post_file.name}. Skipping.")
        post_file.unlink()
        sys.exit(0)

    if len(text) > 280:
        print(f"[social] WARNING: Text is {len(text)} chars (max 280). Truncating.")
        text = text[:277] + "..."

    print(f"[social] Posting: {text[:80]}...")

    # Upload media (prefer video over image)
    media_id = None
    video_file = data.get("video")
    image_file = data.get("image")

    if video_file:
        video_path = post_file.parent / video_file
        if video_path.exists():
            print(f"[social] Uploading video: {video_file}")
            media_id = upload_video(str(video_path))
        else:
            print(f"[social] Video file not found: {video_path}. Trying image fallback.")

    if not media_id and image_file:
        image_path = post_file.parent / image_file
        if image_path.exists():
            print(f"[social] Uploading image: {image_file}")
            media_id = upload_media(str(image_path))
        else:
            print(f"[social] Image file not found: {image_path}. Posting without media.")

    try:
        result = post_tweet(text, media_id=media_id)
        tweet_id = result.get("data", {}).get("id", "unknown")
        print(f"[social] Posted successfully. Tweet ID: {tweet_id}")

        # Show pin instructions if this is a pinned post
        if data.get("pinned"):
            print(f"\n{'='*50}")
            print(f"[social] PIN THIS TWEET:")
            print(f"  https://x.com/SecondHashHQ/status/{tweet_id}")
            print(f"  → Click ··· menu → 'Pin to your profile'")
            print(f"{'='*50}\n")

        data["posted_at"] = datetime.now(timezone.utc).isoformat()
        data["tweet_id"] = tweet_id

        posted_name = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{post_file.name}"
        with open(POSTED_DIR / posted_name, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Clean up: move JSON and delete media files
        post_file.unlink()
        for media_file in [image_file, video_file]:
            if media_file:
                mp = post_file.parent / media_file
                if mp.exists():
                    mp.unlink()
        print(f"[social] Moved to posted/{posted_name}")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else "no body"
        print(f"[social] ERROR {e.code}: {error_body}")
        sys.exit(1)


if __name__ == "__main__":
    main()
