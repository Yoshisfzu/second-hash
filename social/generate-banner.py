"""
Second Hash — Category-Aware Banner Generator v2

Generates branded 1200x675 banners with category-specific layouts:
  - product:    Product image hero + specs text
  - meme:       Bold text-forward, punchy single line
  - philosophy: Minimalist typographic, abstract accents
  - community:  Dialogue-style, question motif
  - recap:      Dashboard/data visual aesthetic
  - launch:     Full-impact logo + tagline centered

Usage:
  python social/generate-banner.py                    # all queue/*.json
  python social/generate-banner.py queue/post.json    # single file
"""

import json
import math
import os
import sys
import textwrap
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- Paths ---
SOCIAL_DIR = Path(__file__).parent
QUEUE_DIR = SOCIAL_DIR / "queue"
IMAGES_DIR = SOCIAL_DIR.parent / "site" / "images"

# --- Brand Colors ---
BG_PRIMARY = (10, 12, 15)
BG_SECONDARY = (22, 25, 32)
BG_CARD = (28, 32, 40)
ACCENT = (212, 146, 74)
ACCENT_DIM = (158, 106, 48)
ACCENT_BRIGHT = (235, 170, 90)
TEXT_PRIMARY = (232, 233, 236)
TEXT_SECONDARY = (139, 143, 154)
TEXT_MUTED = (92, 96, 112)
BORDER = (37, 40, 48)

# --- Banner Size ---
WIDTH = 1200
HEIGHT = 675

# --- Fonts ---
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"

# --- Product image mapping ---
PRODUCT_MAP = {
    "R1": "SH-R1_Reclaim.png", "Reclaim": "SH-R1_Reclaim.png",
    "R2": "SH-R2_Reforge.png", "Reforge": "SH-R2_Reforge.png",
    "R3": "SH-R3_Refit.png", "Refit": "SH-R3_Refit.png",
    "R4": "SH-R4_Fuse.png", "Fuse": "SH-R4_Fuse.png",
    "B1": "SH-B1_Patch.png", "Patch": "SH-B1_Patch.png",
    "B2": "SH-B2_Splice.png", "Splice": "SH-B2_Splice.png",
    "B3": "SH-B3_Overclock.png", "Overclock": "SH-B3_Overclock.png",
    "B4": "SH-B4_Surge.png", "Surge": "SH-B4_Surge.png",
    "B5": "SH-B5_Regulate.png", "Regulate": "SH-B5_Regulate.png",
    "X1": "SH-X1_Overhaul.png", "Overhaul": "SH-X1_Overhaul.png",
    "X2": "SH-X2_Apex.png", "Apex": "SH-X2_Apex.png",
}


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def pick_product_image(text):
    for keyword, img_file in PRODUCT_MAP.items():
        if keyword in text:
            return img_file
    # Fallback
    fallbacks = ["SH-R4_Fuse.png", "SH-X1_Overhaul.png", "SH-R1_Reclaim.png"]
    return fallbacks[hash(text) % len(fallbacks)]


def draw_glow(img, cx, cy, radius, color, alpha=35):
    glow = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(radius, 0, -3):
        a = int(alpha * (i / radius) ** 2)
        gd.ellipse([radius - i, radius - i, radius + i, radius + i], fill=(*color, a))
    img.paste(glow, (cx - radius, cy - radius), glow)


def extract_key_line(text, max_len=60):
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("@")]
    keywords = ["second chance", "mispriced", "junk", "refab", "depreciation",
                "margin", "residual", "retail", "dead", "never pay", "rule",
                "strategy", "two lives", "thesis", "appraise", "inventory"]
    for line in lines:
        if len(line) < max_len and any(w in line.lower() for w in keywords):
            return line
    return lines[0][:max_len] if lines else "Second Hash"


def draw_logo(img, draw, x, y, size=50):
    logo_path = IMAGES_DIR / "SH_Logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((size, size), Image.LANCZOS)
        img.paste(logo, (x, y), logo)
    return img


def draw_bottom_bar(draw, font_tag):
    # Accent bottom border
    draw.rectangle([0, HEIGHT - 3, WIDTH, HEIGHT], fill=ACCENT)
    # Hashtags
    tags = "#ClubHashCash  #SecondHash"
    bbox = draw.textbbox((0, 0), tags, font=font_tag)
    draw.text((WIDTH - (bbox[2] - bbox[0]) - 30, HEIGHT - 28), tags, fill=TEXT_MUTED, font=font_tag)


# =============================================================
# CATEGORY RENDERERS
# =============================================================

def render_product(img, draw, text, fonts):
    """Product Spotlight: hero product image right, specs left."""
    # Left dark panel
    panel = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rectangle([0, 0, 650, HEIGHT], fill=(*BG_SECONDARY, 220))
    img = Image.alpha_composite(img, panel)
    draw = ImageDraw.Draw(img)

    # Accent left edge
    draw.rectangle([0, 0, 5, HEIGHT], fill=ACCENT)

    # Product image (right, large)
    product_file = pick_product_image(text)
    product_path = IMAGES_DIR / product_file
    if product_path.exists():
        draw_glow(img, 920, HEIGHT // 2, 380, ACCENT, alpha=25)
        product = Image.open(product_path).convert("RGBA")
        product = product.resize((520, 520), Image.LANCZOS)
        img.paste(product, (640, (HEIGHT - 520) // 2), product)
        draw = ImageDraw.Draw(img)

    # Category label
    draw.text((50, 55), "PRODUCT SPOTLIGHT", fill=ACCENT, font=fonts["sub"])
    lbl_bbox = draw.textbbox((50, 55), "PRODUCT SPOTLIGHT", font=fonts["sub"])
    draw.rectangle([50, lbl_bbox[3] + 3, lbl_bbox[2], lbl_bbox[3] + 5], fill=ACCENT)

    # Headline
    headline = extract_key_line(text, 50)
    wrapped = textwrap.fill(headline, width=24)
    y = 110
    for line in wrapped.split("\n")[:4]:
        draw.text((50, y), line, fill=TEXT_PRIMARY, font=fonts["headline"])
        y += 55

    # Secondary text: extract product code if present
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("@")]
    if len(lines) > 1:
        sub_text = lines[1][:65]
        y += 15
        draw.text((50, y), sub_text, fill=TEXT_SECONDARY, font=fonts["body"])

    # Logo
    draw_logo(img, draw, 50, HEIGHT - 95, 55)
    draw.text((115, HEIGHT - 85), "SECOND HASH", fill=TEXT_PRIMARY, font=fonts["logo"])
    draw.text((115, HEIGHT - 58), "Refabricated Mining Hardware", fill=TEXT_SECONDARY, font=fonts["sub"])

    draw_bottom_bar(draw, fonts["tag"])
    return img


def render_meme(img, draw, text, fonts):
    """Meme/Humor: Bold text center-stage, minimal imagery."""
    # Full dark bg with subtle texture lines
    for i in range(0, WIDTH, 80):
        draw.line([(i, 0), (i, HEIGHT)], fill=(*BORDER, 30), width=1)

    # Accent bars top and bottom
    draw.rectangle([0, 0, WIDTH, 6], fill=ACCENT)
    draw.rectangle([0, HEIGHT - 6, WIDTH, HEIGHT], fill=ACCENT)

    # Category label top-left
    draw.text((50, 30), "HASH HUMOR", fill=ACCENT_DIM, font=fonts["tag"])

    # Extract the punchiest line
    headline = extract_key_line(text, 55)
    # Large centered text
    font_big = load_font(FONT_BOLD, 48)
    wrapped = textwrap.fill(headline, width=26)
    lines = wrapped.split("\n")[:3]

    total_h = len(lines) * 62
    y_start = (HEIGHT - total_h) // 2 - 20

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_big)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_start), line, fill=TEXT_PRIMARY, font=font_big)
        y_start += 62

    # Accent underline below text
    draw.rectangle([(WIDTH // 2 - 80), y_start + 10, (WIDTH // 2 + 80), y_start + 13], fill=ACCENT)

    # Small product image bottom-right (subtle)
    product_file = pick_product_image(text)
    product_path = IMAGES_DIR / product_file
    if product_path.exists():
        product = Image.open(product_path).convert("RGBA")
        product = product.resize((160, 160), Image.LANCZOS)
        # Make semi-transparent
        alpha = product.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.4))
        product.putalpha(alpha)
        img.paste(product, (WIDTH - 190, HEIGHT - 200), product)
        draw = ImageDraw.Draw(img)

    # Logo bottom-left
    draw_logo(img, draw, 40, HEIGHT - 70, 40)
    draw.text((90, HEIGHT - 62), "SECOND HASH", fill=TEXT_MUTED, font=fonts["sub"])

    return img


def render_philosophy(img, draw, text, fonts):
    """Philosophy/Thesis: Minimalist typographic, abstract geometric accents."""
    # Subtle diagonal accent lines (abstract geometric)
    for i in range(-HEIGHT, WIDTH + HEIGHT, 120):
        draw.line([(i, HEIGHT), (i + HEIGHT, 0)], fill=(*ACCENT_DIM, 15), width=1)

    # Large quotation mark accent
    font_quote = load_font(FONT_BOLD, 200)
    draw.text((40, 30), "\u201C", fill=(*ACCENT_DIM, 60), font=font_quote)

    # Category label
    draw.text((60, 50), "THE REFAB THESIS", fill=ACCENT, font=fonts["sub"])
    lbl_bbox = draw.textbbox((60, 50), "THE REFAB THESIS", font=fonts["sub"])
    draw.rectangle([60, lbl_bbox[3] + 4, 60 + 30, lbl_bbox[3] + 6], fill=ACCENT)

    # Main text: larger, more breathing room
    headline = extract_key_line(text, 65)
    font_phil = load_font(FONT_BOLD, 42)
    wrapped = textwrap.fill(headline, width=30)
    lines = wrapped.split("\n")[:4]

    y = 140
    for line in lines:
        draw.text((60, y), line, fill=TEXT_PRIMARY, font=font_phil)
        y += 56

    # Secondary quote / supporting line
    all_lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("@")]
    if len(all_lines) > 2:
        sub = all_lines[-1][:70] if len(all_lines[-1]) < 70 else all_lines[1][:70]
        y += 20
        draw.text((60, y), sub, fill=TEXT_SECONDARY, font=fonts["body"])

    # Vertical accent bar right side
    draw.rectangle([WIDTH - 20, 60, WIDTH - 16, HEIGHT - 60], fill=ACCENT)

    # Small geometric circles (abstract)
    circle_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cd = ImageDraw.Draw(circle_overlay)
    cd.ellipse([WIDTH - 250, HEIGHT - 250, WIDTH - 50, HEIGHT - 50], outline=(*ACCENT_DIM, 50), width=2)
    cd.ellipse([WIDTH - 200, HEIGHT - 200, WIDTH - 80, HEIGHT - 80], outline=(*ACCENT_DIM, 30), width=1)
    img = Image.alpha_composite(img, circle_overlay)
    draw = ImageDraw.Draw(img)

    # Logo
    draw_logo(img, draw, 50, HEIGHT - 90, 50)
    draw.text((110, HEIGHT - 80), "SECOND HASH", fill=TEXT_PRIMARY, font=fonts["logo"])

    draw_bottom_bar(draw, fonts["tag"])
    return img


def render_community(img, draw, text, fonts):
    """Community: Dialogue-style, question motif, engagement-focused."""
    # Speech bubble / dialogue aesthetic
    # Background: slightly warmer tint
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_SECONDARY, 80))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Accent top bar
    draw.rectangle([0, 0, WIDTH, 4], fill=ACCENT)

    # Category
    draw.text((50, 40), "COMMUNITY", fill=ACCENT, font=fonts["sub"])

    # Large question mark or dialogue motif
    font_q = load_font(FONT_BOLD, 280)
    # Draw large "?" watermark
    q_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    qd = ImageDraw.Draw(q_overlay)
    qd.text((WIDTH - 300, 100), "?", fill=(*ACCENT, 25), font=font_q)
    img = Image.alpha_composite(img, q_overlay)
    draw = ImageDraw.Draw(img)

    # Speech bubble shape (rounded rect)
    bubble_x, bubble_y = 50, 100
    bubble_w, bubble_h = 750, 300
    bubble = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bubble)
    bd.rounded_rectangle(
        [bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
        radius=20, fill=(*BG_CARD, 200), outline=(*ACCENT_DIM, 100), width=2
    )
    # Triangle pointer
    tri_x = bubble_x + 100
    tri_y = bubble_y + bubble_h
    bd.polygon([(tri_x, tri_y), (tri_x + 40, tri_y), (tri_x + 10, tri_y + 35)],
               fill=(*BG_CARD, 200))
    img = Image.alpha_composite(img, bubble)
    draw = ImageDraw.Draw(img)

    # Text inside bubble
    headline = extract_key_line(text, 60)
    font_comm = load_font(FONT_BOLD, 36)
    wrapped = textwrap.fill(headline, width=32)
    lines = wrapped.split("\n")[:4]
    y = bubble_y + 40
    for line in lines:
        draw.text((bubble_x + 40, y), line, fill=TEXT_PRIMARY, font=font_comm)
        y += 48

    # "Join the conversation" CTA
    cta_y = bubble_y + bubble_h + 50
    draw.text((70, cta_y), "@ClubHashcash", fill=ACCENT, font=fonts["sub"])

    # Logo bottom-right
    draw_logo(img, draw, WIDTH - 200, HEIGHT - 85, 50)
    draw.text((WIDTH - 140, HEIGHT - 75), "SH", fill=TEXT_PRIMARY, font=fonts["logo"])

    draw_bottom_bar(draw, fonts["tag"])
    return img


def render_recap(img, draw, text, fonts):
    """Recap: Dashboard/data visual, stats-styled layout."""
    # Grid lines background
    for x in range(0, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=(*BORDER, 40), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([(0, y), (WIDTH, y)], fill=(*BORDER, 40), width=1)

    # Header bar
    draw.rectangle([0, 0, WIDTH, 60], fill=(*BG_SECONDARY, 255))
    draw.rectangle([0, 58, WIDTH, 62], fill=ACCENT)
    draw.text((30, 18), "WEEKLY RECAP  |  SECOND HASH", fill=ACCENT, font=fonts["sub"])
    font_status = load_font(FONT_MONO, 14)
    draw.text((WIDTH - 200, 22), "STATUS: OPERATIONAL", fill=(*ACCENT_BRIGHT, 200), font=font_status)

    # Stat cards
    cards = [
        ("REFABBED", "[X]", "units"),
        ("SOLD", "[X]", "units"),
        ("MARGIN", "HEALTHY", ""),
        ("UPTIME", "99.7%", ""),
    ]
    card_w = 250
    card_h = 120
    gap = 20
    start_x = (WIDTH - (card_w * 4 + gap * 3)) // 2
    card_y = 100

    for i, (label, value, unit) in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        # Card background
        card_overlay = Image.new("RGBA", (card_w, card_h), (*BG_CARD, 220))
        card_draw = ImageDraw.Draw(card_overlay)
        card_draw.rectangle([0, 0, card_w, 3], fill=ACCENT)
        img.paste(card_overlay, (cx, card_y), card_overlay)
        draw = ImageDraw.Draw(img)

        draw.text((cx + 20, card_y + 20), label, fill=TEXT_MUTED, font=font_status)
        font_val = load_font(FONT_BOLD, 36)
        draw.text((cx + 20, card_y + 45), value, fill=TEXT_PRIMARY, font=font_val)
        if unit:
            draw.text((cx + 20, card_y + 88), unit, fill=TEXT_SECONDARY, font=font_status)

    # Main text below cards
    headline = extract_key_line(text, 70)
    y = card_y + card_h + 50
    font_recap = load_font(FONT_REGULAR, 24)
    wrapped = textwrap.fill(headline, width=55)
    for line in wrapped.split("\n")[:3]:
        bbox = draw.textbbox((0, 0), line, font=font_recap)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y), line, fill=TEXT_SECONDARY, font=font_recap)
        y += 34

    # Decorative bar chart (abstract)
    bar_y = HEIGHT - 180
    bar_h_max = 100
    bar_w = 30
    bar_gap = 15
    n_bars = 14
    bar_start = (WIDTH - (bar_w + bar_gap) * n_bars) // 2
    rng = random.Random(hash(text))
    for i in range(n_bars):
        bh = int(rng.uniform(0.2, 1.0) * bar_h_max)
        bx = bar_start + i * (bar_w + bar_gap)
        color = ACCENT if i >= n_bars - 3 else (*TEXT_MUTED, 80)
        draw.rectangle([bx, bar_y + bar_h_max - bh, bx + bar_w, bar_y + bar_h_max], fill=color)

    # Logo
    draw_logo(img, draw, 40, HEIGHT - 60, 35)
    draw.text((82, HEIGHT - 52), "SECOND HASH", fill=TEXT_MUTED, font=fonts["tag"])

    draw.rectangle([0, HEIGHT - 3, WIDTH, HEIGHT], fill=ACCENT)
    return img


def render_launch(img, draw, text, fonts):
    """Launch: Full-impact, logo centered, tagline prominent."""
    # Radial glow center
    draw_glow(img, WIDTH // 2, HEIGHT // 2 - 30, 400, ACCENT, alpha=30)
    draw = ImageDraw.Draw(img)

    # Accent lines from center (starburst)
    burst = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    cx, cy = WIDTH // 2, HEIGHT // 2 - 30
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        ex = cx + int(600 * math.cos(rad))
        ey = cy + int(600 * math.sin(rad))
        bd.line([(cx, cy), (ex, ey)], fill=(*ACCENT_DIM, 10), width=1)
    img = Image.alpha_composite(img, burst)
    draw = ImageDraw.Draw(img)

    # Large logo
    draw_logo(img, draw, WIDTH // 2 - 70, 100, 140)
    draw = ImageDraw.Draw(img)

    # Brand name
    font_brand = load_font(FONT_BOLD, 52)
    brand = "SECOND HASH"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 270), brand, fill=TEXT_PRIMARY, font=font_brand)

    # Accent line
    draw.rectangle([(WIDTH // 2 - 60), 335, (WIDTH // 2 + 60), 338], fill=ACCENT)

    # Tagline
    font_tag_lg = load_font(FONT_REGULAR, 22)
    tagline = "Every hash deserves a second chance."
    bbox2 = draw.textbbox((0, 0), tagline, font=font_tag_lg)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - tw2) // 2, 355), tagline, fill=TEXT_SECONDARY, font=font_tag_lg)

    # Sub info
    font_info = load_font(FONT_MONO, 14)
    info = "Refabricated Mining Hardware  |  Built on Avalanche  |  @ClubHashcash"
    bbox3 = draw.textbbox((0, 0), info, font=font_info)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((WIDTH - tw3) // 2, 400), info, fill=TEXT_MUTED, font=font_info)

    # "NOW OPEN" badge
    badge_w, badge_h = 180, 40
    badge_x = (WIDTH - badge_w) // 2
    badge_y = 460
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
                            radius=6, fill=ACCENT)
    font_badge = load_font(FONT_BOLD, 18)
    btxt = "NOW OPEN"
    bb = draw.textbbox((0, 0), btxt, font=font_badge)
    btw = bb[2] - bb[0]
    bth = bb[3] - bb[1]
    draw.text((badge_x + (badge_w - btw) // 2, badge_y + (badge_h - bth) // 2 - 2),
              btxt, fill=BG_PRIMARY, font=font_badge)

    # Product images small at bottom
    product_files = ["SH-R1_Reclaim.png", "SH-B3_Overclock.png", "SH-X1_Overhaul.png",
                     "SH-R4_Fuse.png", "SH-X2_Apex.png"]
    prod_size = 90
    total_w = len(product_files) * prod_size + (len(product_files) - 1) * 15
    px_start = (WIDTH - total_w) // 2
    for i, pf in enumerate(product_files):
        pp = IMAGES_DIR / pf
        if pp.exists():
            pi = Image.open(pp).convert("RGBA")
            pi = pi.resize((prod_size, prod_size), Image.LANCZOS)
            img.paste(pi, (px_start + i * (prod_size + 15), HEIGHT - 130), pi)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, HEIGHT - 4, WIDTH, HEIGHT], fill=ACCENT)
    return img


def render_teaser(img, draw, text, fonts):
    """Teaser: Minimal, mysterious, pre-launch hype. Centered headline with scan-line effect."""
    # Subtle scan-line effect (horizontal)
    for y in range(0, HEIGHT, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(*BG_SECONDARY, 40), width=1)

    # Glitch-style accent bars (random positions)
    rng = random.Random(hash(text))
    for _ in range(5):
        gy = rng.randint(50, HEIGHT - 50)
        gw = rng.randint(40, 200)
        gx = rng.randint(0, WIDTH - gw)
        gh = rng.randint(2, 4)
        draw.rectangle([gx, gy, gx + gw, gy + gh], fill=(*ACCENT, rng.randint(15, 40)))

    # Central glow (subtle, mysterious)
    draw_glow(img, WIDTH // 2, HEIGHT // 2, 300, ACCENT, alpha=15)
    draw = ImageDraw.Draw(img)

    # Read headline/subline from post data or extract from text
    all_lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("@")]
    headline = all_lines[0] if all_lines else "..."
    subline = all_lines[-1] if len(all_lines) > 1 else ""

    # Large centered headline
    font_big = load_font(FONT_BOLD, 52)
    wrapped = textwrap.fill(headline, width=24)
    lines = wrapped.split("\n")[:3]
    total_h = len(lines) * 68
    y_start = (HEIGHT - total_h) // 2 - 30

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_big)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_start), line, fill=TEXT_PRIMARY, font=font_big)
        y_start += 68

    # Accent line below headline
    draw.rectangle([(WIDTH // 2 - 50), y_start + 10, (WIDTH // 2 + 50), y_start + 13], fill=ACCENT)

    # Subline below accent
    if subline and subline != headline:
        font_sub = load_font(FONT_REGULAR, 20)
        bbox2 = draw.textbbox((0, 0), subline, font=font_sub)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((WIDTH - tw2) // 2, y_start + 30), subline, fill=TEXT_SECONDARY, font=font_sub)

    # Corner accent marks (mysterious framing)
    corner_len = 40
    ct = 2
    # Top-left
    draw.line([(30, 30), (30 + corner_len, 30)], fill=ACCENT, width=ct)
    draw.line([(30, 30), (30, 30 + corner_len)], fill=ACCENT, width=ct)
    # Top-right
    draw.line([(WIDTH - 30, 30), (WIDTH - 30 - corner_len, 30)], fill=ACCENT, width=ct)
    draw.line([(WIDTH - 30, 30), (WIDTH - 30, 30 + corner_len)], fill=ACCENT, width=ct)
    # Bottom-left
    draw.line([(30, HEIGHT - 30), (30 + corner_len, HEIGHT - 30)], fill=ACCENT, width=ct)
    draw.line([(30, HEIGHT - 30), (30, HEIGHT - 30 - corner_len)], fill=ACCENT, width=ct)
    # Bottom-right
    draw.line([(WIDTH - 30, HEIGHT - 30), (WIDTH - 30 - corner_len, HEIGHT - 30)], fill=ACCENT, width=ct)
    draw.line([(WIDTH - 30, HEIGHT - 30), (WIDTH - 30, HEIGHT - 30 - corner_len)], fill=ACCENT, width=ct)

    # #ClubHashCash tag bottom-center
    font_tag = load_font(FONT_MONO, 13)
    tag = "#ClubHashCash"
    bbox3 = draw.textbbox((0, 0), tag, font=font_tag)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((WIDTH - tw3) // 2, HEIGHT - 50), tag, fill=TEXT_MUTED, font=font_tag)

    return img


# =============================================================
# MAIN GENERATOR
# =============================================================

RENDERERS = {
    "product": render_product,
    "meme": render_meme,
    "philosophy": render_philosophy,
    "community": render_community,
    "recap": render_recap,
    "launch": render_launch,
    "teaser": render_teaser,
}


def generate_banner(post_data: dict, output_path: Path) -> bool:
    text = post_data.get("text", "")
    category = post_data.get("category", "product")

    # Create RGBA canvas
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Load fonts
    fonts = {
        "headline": load_font(FONT_BOLD, 42),
        "sub": load_font(FONT_REGULAR, 16),
        "body": load_font(FONT_REGULAR, 18),
        "tag": load_font(FONT_MONO, 13),
        "logo": load_font(FONT_BOLD, 24),
    }

    # Dispatch to category renderer
    renderer = RENDERERS.get(category, render_product)
    img = renderer(img, draw, text, fonts)

    # Save
    final = img.convert("RGB")
    final.save(output_path, "PNG", quality=95)
    return True


def process_queue(target_file: str = None):
    if target_file:
        files = [Path(target_file)]
    else:
        files = sorted(QUEUE_DIR.glob("*.json"))

    generated = 0
    for json_path in files:
        png_path = json_path.with_suffix(".png")

        # Always regenerate (v2 upgrade)
        with open(json_path) as f:
            post_data = json.load(f)

        if generate_banner(post_data, png_path):
            post_data["image"] = png_path.name
            with open(json_path, "w") as f:
                json.dump(post_data, f, indent=2, ensure_ascii=False)
            print(f"[banner] Generated {png_path.name} ({post_data.get('category', '?')})")
            generated += 1

    print(f"[banner] Done. {generated} banner(s) generated.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    process_queue(target)
