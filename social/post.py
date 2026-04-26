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


def oauth_signature(method: str, url: str, params: dict, consumer_secret: str, token_secret: str) -> str:
    base = "&".join([
        method.upper(),
        urllib.parse.quote(url, safe=""),
        urllib.parse.quote("&".join(f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted(params.items())), safe=""),
    ])
    key = f"{urllib.parse.quote(consumer_secret, safe='')}&{urllib.parse.quote(token_secret, safe='')}"
    return base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()


def build_auth_header(method: str, url: str, body_params: dict | None = None) -> str:
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
    sig = oauth_signature(method, url, all_params, api_secret, access_secret)
    oauth_params["oauth_signature"] = sig

    header = "OAuth " + ", ".join(
        f'{k}="{urllib.parse.quote(str(v), safe="")}"'
        for k, v in sorted(oauth_params.items())
    )
    return header


def post_tweet(text: str) -> dict:
    body = json.dumps({"text": text}).encode()
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


def get_next_post() -> Path | None:
    files = sorted(QUEUE_DIR.glob("*.json"))
    return files[0] if files else None


def main():
    POSTED_DIR.mkdir(exist_ok=True)
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

    try:
        result = post_tweet(text)
        tweet_id = result.get("data", {}).get("id", "unknown")
        print(f"[social] Posted successfully. Tweet ID: {tweet_id}")

        data["posted_at"] = datetime.now(timezone.utc).isoformat()
        data["tweet_id"] = tweet_id

        posted_name = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{post_file.name}"
        with open(POSTED_DIR / posted_name, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        post_file.unlink()
        print(f"[social] Moved to posted/{posted_name}")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else "no body"
        print(f"[social] ERROR {e.code}: {error_body}")
        sys.exit(1)


if __name__ == "__main__":
    main()
