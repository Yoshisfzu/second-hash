"""
Second Hash — Daily Social Plan Generator

Generates tomorrow's post queue based on the content calendar.
Runs daily via GitHub Actions, creates a PR for review.

Usage:
  python social/generate-plan.py
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

QUEUE_DIR = Path(__file__).parent / "queue"
BRAND_VOICE = Path(__file__).parent / "brand-voice.md"

# Content templates by day of week (0=Mon, 6=Sun)
TEMPLATES = {
    0: {  # Monday — Product Spotlight
        "category": "product",
        "templates": [
            "R1 Reclaim: entry-level refab rig. Dead miner in, 42 MH/s out.\n\nRetail wants $800 for those numbers. We want your junk.\n\n#ClubHashCash #Hashathon @ClubHashcash",
            "R2 Reforge: mid-tier refab. Two dead boards, one working rig.\n\nDepreciation is just opportunity with a longer name.\n\n#ClubHashCash #SecondHash @ClubHashcash",
            "B3 Overclock: boost module that squeezes 15% more hash from any R-series rig.\n\nOther vendors sell new. We sell better.\n\n#ClubHashCash #Hashathon @ClubHashcash",
            "X1 Overhaul: experimental-grade refab. Three dead rigs fused into one beast.\n\nThe math doesn't work until it does.\n\n#ClubHashCash #SecondHash @ClubHashcash",
            "R4 Fuse: our flagship refab rig. Four salvaged boards, one unified hash machine.\n\nJunk is mispriced loot.\n\n#ClubHashCash #Hashathon @ClubHashcash",
        ],
    },
    1: {  # Tuesday — Meme
        "category": "meme",
        "templates": [
            "POV: you just paid retail for a mining rig that Second Hash sells refabbed at 40% off.\n\n#ClubHashCash",
            "Other vendors: \"Brand new, factory sealed!\"\nSecond Hash: \"Battle-tested, margin-approved.\"\n\nWe are not the same.\n\n#SecondHash @ClubHashcash",
            "Buying new hardware in a bear market is just donating to a depreciation curve.\n\nWe accept your donations. And refab them.\n\n#ClubHashCash #Hashathon",
            "The first rule of refab: never pay retail.\nThe second rule of refab: NEVER pay retail.\n\n#SecondHash #ClubHashCash @ClubHashcash",
            "\"Why is your gear so cheap?\"\n\nBecause someone else already paid the depreciation. We just fixed the solder.\n\n#ClubHashCash #Hashathon",
        ],
    },
    2: {  # Wednesday — Philosophy
        "category": "philosophy",
        "templates": [
            "Every piece of hardware has two lives.\n\nThe first owner pays retail. The second owner pays residual value.\n\nSecond Hash exists for the second owner.\n\nEvery hash deserves a second chance.\n\n#SecondHash @ClubHashcash",
            "The refab thesis:\n\n1. All hardware depreciates\n2. Depreciation != death\n3. Residual value is real value\n4. Junk is mispriced loot\n\nWe built a company on line 4.\n\n#ClubHashCash #Hashathon",
            "New hardware loses 30% the moment you unbox it.\n\nRefabbed hardware already absorbed that loss. You start at the bottom of the curve.\n\nThat's not a disadvantage. That's a strategy.\n\n#SecondHash @ClubHashcash",
            "In every market crash, two things happen:\n\n1. Retail buyers panic sell\n2. Refab buyers load inventory\n\nGuess which one we are.\n\n#ClubHashCash #Hashathon @ClubHashcash",
        ],
    },
    3: {  # Thursday — Product Spotlight
        "category": "product",
        "templates": [
            "B1 Patch: the simplest boost module. Plug in, +5% hash rate.\n\nNo firmware update. No configuration. Just margin.\n\n#ClubHashCash @ClubHashcash",
            "B4 Surge: temporary overclock module. 30% boost for 24 hours.\n\nSome call it a gamble. We call it calculated depreciation.\n\n#ClubHashCash #Hashathon @ClubHashcash",
            "X2 Apex: the rarest refab in the Second Hash catalog.\n\nFive dead rigs. One experimental build. Zero retail markup.\n\n#SecondHash #ClubHashCash @ClubHashcash",
            "R3 Refit: specialized refab. Takes damaged components other vendors reject.\n\nOne person's write-off is another's working rig.\n\n#ClubHashCash #Hashathon @ClubHashcash",
            "B5 Regulate: stability module for R-series rigs. Reduces variance, extends lifespan.\n\nThe boring module that prints consistent hashes.\n\n#SecondHash @ClubHashcash",
        ],
    },
    4: {  # Friday — Meme
        "category": "meme",
        "templates": [
            "Weekend plans:\n- Appraise junk\n- Refab junk\n- Sell not-junk\n- Repeat\n\n#SecondHash #ClubHashCash",
            "Me: *sees a pile of dead mining rigs*\nAlso me: \"That's at least three R2 Reforges and a Boost Module.\"\n\nThe refab brain never sleeps.\n\n#ClubHashCash @ClubHashcash",
            "Retail price is just the first buyer's mistake.\n\nHappy Friday.\n\n#SecondHash #Hashathon",
            "If your mining rig is collecting dust, it's not retired.\n\nIt's pre-refab inventory.\n\nDM us.\n\n#ClubHashCash @ClubHashcash",
        ],
    },
    5: {  # Saturday — Community
        "category": "community",
        "templates": [
            "What's the worst deal you've ever seen in the @ClubHashcash lobby?\n\nWe'll appraise it.\n\n#ClubHashCash #Hashathon",
            "Shoutout to everyone grinding the @ClubHashcash mines this weekend.\n\nRemember: if it drops, we'll buy it. Salvage grade or better.\n\n#ClubHashCash #SecondHash",
            "Saturday market report:\n\nR-series demand: steady\nB-series demand: rising\nRetail prices: still overpriced\n\nAs always.\n\n@ClubHashcash #ClubHashCash",
        ],
    },
    6: {  # Sunday — Recap
        "category": "recap",
        "templates": [
            "Weekly shelf inspection complete.\n\nRefabbed: [X] units\nSold: [X] units\nMargin: healthy\n\nAnother week in the refab business.\n\n#SecondHash #ClubHashCash @ClubHashcash",
            "Sunday inventory check.\n\nDead rigs received: plenty\nWorking rigs shipped: more than last week\nRetail buyers convinced to go refab: a few\n\nProgress.\n\n#ClubHashCash #Hashathon",
        ],
    },
}


def generate_daily_posts(target_date: datetime) -> list[dict]:
    dow = target_date.weekday()
    day_config = TEMPLATES[dow]
    category = day_config["category"]
    templates = day_config["templates"]

    # Pick template based on week number for rotation
    week_num = target_date.isocalendar()[1]
    idx = week_num % len(templates)

    morning_post = {
        "text": templates[idx],
        "category": category,
        "scheduled_for": f"{target_date.strftime('%Y-%m-%d')}T09:00:00Z",
        "slot": "morning",
    }

    # Afternoon post: pick next template
    afternoon_idx = (idx + 1) % len(templates)
    afternoon_post = {
        "text": templates[afternoon_idx],
        "category": category,
        "scheduled_for": f"{target_date.strftime('%Y-%m-%d')}T15:00:00Z",
        "slot": "afternoon",
    }

    return [morning_post, afternoon_post]


def main():
    QUEUE_DIR.mkdir(exist_ok=True)
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    posts = generate_daily_posts(tomorrow)

    date_str = tomorrow.strftime("%Y%m%d")
    for post in posts:
        filename = f"{date_str}_{post['slot']}.json"
        filepath = QUEUE_DIR / filename

        if filepath.exists():
            print(f"[plan] {filename} already exists. Skipping.")
            continue

        with open(filepath, "w") as f:
            json.dump(post, f, indent=2, ensure_ascii=False)
        print(f"[plan] Created {filename}: {post['text'][:60]}...")

    print(f"[plan] Generated {len(posts)} posts for {tomorrow.strftime('%Y-%m-%d')} ({tomorrow.strftime('%A')})")


if __name__ == "__main__":
    main()
