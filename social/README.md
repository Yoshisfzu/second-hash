# Second Hash — Social Automation

Automated X (Twitter) posting system for @SecondHashHQ.

## How it works

```
22:00 UTC  generate-plan.py → creates tomorrow's posts in queue/ → opens PR
 ↓
Morning    Yoshimasa reviews PR → Merge = approve, Close = skip
 ↓
09:00 UTC  post.py → posts morning tweet from queue/
15:00 UTC  post.py → posts afternoon tweet from queue/
```

## Directory structure

```
social/
├── brand-voice.md       # Brand guidelines & vocabulary
├── content-calendar.md  # Weekly schedule & content mix
├── generate-plan.py     # Creates daily post queue (runs via GH Actions)
├── post.py              # Posts to X API v2 (runs via GH Actions)
├── queue/               # Pending posts (JSON files)
├── posted/              # Archive of posted tweets
├── templates/           # Custom templates (optional)
└── README.md
```

## Post format (JSON)

```json
{
  "text": "Tweet content here (max 280 chars)",
  "category": "product|meme|philosophy|community|recap",
  "scheduled_for": "2026-04-27T09:00:00Z",
  "slot": "morning|afternoon"
}
```

## Manual posting

Add a JSON file to `social/queue/` and push. The next scheduled run will post it.

## GitHub Secrets required

- `X_API_KEY` — Consumer key
- `X_API_SECRET` — Consumer secret
- `X_ACCESS_TOKEN` — Access token (Read+Write)
- `X_ACCESS_TOKEN_SECRET` — Access token secret
