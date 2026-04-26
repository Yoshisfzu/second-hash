"""
Second Hash — Category-Aware Video Generator

Generates 6-8 second branded MP4 videos for X posts.
Each category has a unique motion design:

  product:    Product zoom-in + specs text fade-in
  meme:       Typewriter text reveal + accent flash
  philosophy: Quote fade-in with geometric animation
  community:  Speech bubble pop-in + text appear
  recap:      Bar chart grow animation + stats count-up
  launch:     Logo reveal + product lineup slide-in

Usage:
  python social/generate-video.py                     # all queue/*.json
  python social/generate-video.py queue/post.json     # single file

Requires: Pillow, ffmpeg (system)
"""

import json
import math
import os
import shutil
import subprocess
import sys
import textwrap
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- Paths ---
SOCIAL_DIR = Path(__file__).parent
QUEUE_DIR = SOCIAL_DIR / "queue"
IMAGES_DIR = SOCIAL_DIR.parent / "site" / "images"
TEMP_DIR = SOCIAL_DIR / ".video_tmp"

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

# --- Video Settings ---
WIDTH = 1200
HEIGHT = 676
FPS = 24
DURATION = 7  # seconds
TOTAL_FRAMES = FPS * DURATION

# --- Fonts ---
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"

# --- Product mapping ---
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
    for kw, img in PRODUCT_MAP.items():
        if kw in text:
            return img
    return ["SH-R4_Fuse.png", "SH-X1_Overhaul.png", "SH-R1_Reclaim.png"][hash(text) % 3]


def extract_key_line(text, max_len=55):
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("@")]
    keywords = ["second chance", "mispriced", "junk", "refab", "depreciation",
                "margin", "residual", "retail", "dead", "never pay", "rule",
                "strategy", "two lives", "thesis", "appraise", "inventory"]
    for line in lines:
        if len(line) < max_len and any(w in line.lower() for w in keywords):
            return line
    return lines[0][:max_len] if lines else "Second Hash"


def extract_sub_lines(text, max_lines=3):
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("@")]
    return lines[1:max_lines + 1] if len(lines) > 1 else []


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    return 3 * t * t - 2 * t * t * t


def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def draw_glow(img, cx, cy, radius, color, alpha=35):
    if radius <= 0:
        return
    glow = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(radius, 0, -4):
        a = int(alpha * (i / radius) ** 2)
        gd.ellipse([radius - i, radius - i, radius + i, radius + i], fill=(*color, a))
    img.paste(glow, (cx - radius, cy - radius), glow)


def draw_logo(img, x, y, size=50):
    logo_path = IMAGES_DIR / "SH_Logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((size, size), Image.LANCZOS)
        img.paste(logo, (x, y), logo)
    return img


# =============================================================
# CATEGORY ANIMATION RENDERERS
# =============================================================

def render_product_frame(frame_num, text, fonts, product_img):
    """Product: zoom-in product + text fade-in from left."""
    t = frame_num / TOTAL_FRAMES  # 0.0 to 1.0
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Phase timing
    product_t = min(1, t / 0.5)  # 0-50%: product animates
    text_t = max(0, min(1, (t - 0.25) / 0.4))  # 25-65%: text slides in
    sub_t = max(0, min(1, (t - 0.5) / 0.3))  # 50-80%: sub text fades
    logo_t = max(0, min(1, (t - 0.65) / 0.25))  # 65-90%: logo appears

    # Left dark panel (slides in)
    panel_x = int(-700 + 700 * ease_out_cubic(min(1, t / 0.3)))
    panel = Image.new("RGBA", (700, HEIGHT), (*BG_SECONDARY, 220))
    img.paste(panel, (panel_x, 0), panel)
    draw = ImageDraw.Draw(img)

    # Accent left edge
    if t > 0.2:
        accent_h = int(HEIGHT * ease_out_cubic(min(1, (t - 0.2) / 0.3)))
        draw.rectangle([panel_x + 695, (HEIGHT - accent_h) // 2, panel_x + 700, (HEIGHT + accent_h) // 2], fill=ACCENT)

    # Product image: zoom from 0.7x to 1.0x
    if product_img:
        scale = 0.7 + 0.3 * ease_out_cubic(product_t)
        prod_size = int(520 * scale)
        resized = product_img.resize((prod_size, prod_size), Image.LANCZOS)
        # Glow
        glow_alpha = int(25 * ease_out_cubic(product_t))
        draw_glow(img, 920, HEIGHT // 2, int(380 * scale), ACCENT, alpha=glow_alpha)
        px = 640 + (520 - prod_size) // 2
        py = (HEIGHT - prod_size) // 2
        img.paste(resized, (px, py), resized)
        draw = ImageDraw.Draw(img)

    # Category label
    if t > 0.15:
        label_alpha = int(255 * ease_out_cubic(min(1, (t - 0.15) / 0.2)))
        draw.text((50 + panel_x, 55), "PRODUCT SPOTLIGHT", fill=(*ACCENT, label_alpha), font=fonts["sub"])
        lbl_bbox = draw.textbbox((50 + panel_x, 55), "PRODUCT SPOTLIGHT", font=fonts["sub"])
        line_w = int((lbl_bbox[2] - lbl_bbox[0]) * ease_out_cubic(min(1, (t - 0.2) / 0.25)))
        if line_w > 0:
            draw.rectangle([50 + panel_x, lbl_bbox[3] + 3, 50 + panel_x + line_w, lbl_bbox[3] + 5], fill=ACCENT)

    # Headline: slide in from left
    if text_t > 0:
        headline = extract_key_line(text, 50)
        wrapped = textwrap.fill(headline, width=24)
        offset_x = int(-400 * (1 - ease_out_cubic(text_t)))
        y = 110
        for line in wrapped.split("\n")[:4]:
            alpha = int(255 * ease_out_cubic(text_t))
            draw.text((50 + offset_x, y), line, fill=(*TEXT_PRIMARY, alpha), font=fonts["headline"])
            y += 55

    # Sub text fade
    if sub_t > 0:
        sub_lines = extract_sub_lines(text, 2)
        y_sub = 110 + 55 * min(4, len(textwrap.fill(extract_key_line(text, 50), width=24).split("\n"))) + 20
        for sl in sub_lines[:2]:
            alpha = int(255 * ease_out_cubic(sub_t))
            draw.text((50, y_sub), sl[:60], fill=(*TEXT_SECONDARY, alpha), font=fonts["body"])
            y_sub += 28

    # Logo
    if logo_t > 0:
        logo_alpha = int(255 * ease_out_cubic(logo_t))
        draw_logo(img, 50, HEIGHT - 95, 55)
        draw = ImageDraw.Draw(img)
        draw.text((115, HEIGHT - 85), "SECOND HASH", fill=(*TEXT_PRIMARY, logo_alpha), font=fonts["logo"])
        draw.text((115, HEIGHT - 58), "Refabricated Mining Hardware", fill=(*TEXT_SECONDARY, logo_alpha), font=fonts["sub"])

    # Bottom accent bar
    bar_w = int(WIDTH * ease_out_cubic(min(1, t / 0.4)))
    if bar_w > 0:
        draw.rectangle([0, HEIGHT - 3, bar_w, HEIGHT], fill=ACCENT)

    # Hashtags
    if t > 0.7:
        tag_alpha = int(255 * ease_out_cubic(min(1, (t - 0.7) / 0.2)))
        tags = "#ClubHashCash  #SecondHash"
        bbox = draw.textbbox((0, 0), tags, font=fonts["tag"])
        draw.text((WIDTH - (bbox[2] - bbox[0]) - 30, HEIGHT - 28), tags, fill=(*TEXT_MUTED, tag_alpha), font=fonts["tag"])

    return img


def render_meme_frame(frame_num, text, fonts, product_img):
    """Meme: typewriter text reveal with accent flash."""
    t = frame_num / TOTAL_FRAMES
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Vertical lines (static)
    for i in range(0, WIDTH, 80):
        draw.line([(i, 0), (i, HEIGHT)], fill=(*BORDER, 30), width=1)

    # Top/bottom accent bars (grow from center)
    bar_w = int((WIDTH / 2) * ease_out_cubic(min(1, t / 0.2)))
    if bar_w > 0:
        draw.rectangle([WIDTH // 2 - bar_w, 0, WIDTH // 2 + bar_w, 6], fill=ACCENT)
        draw.rectangle([WIDTH // 2 - bar_w, HEIGHT - 6, WIDTH // 2 + bar_w, HEIGHT], fill=ACCENT)

    # Category label
    if t > 0.1:
        a = int(255 * min(1, (t - 0.1) / 0.15))
        draw.text((50, 30), "HASH HUMOR", fill=(*ACCENT_DIM, a), font=fonts["tag"])

    # Typewriter text
    headline = extract_key_line(text, 55)
    font_big = load_font(FONT_BOLD, 48)

    # Calculate total characters
    type_start = 0.15
    type_end = 0.65
    type_t = max(0, min(1, (t - type_start) / (type_end - type_start)))
    chars_to_show = int(len(headline) * ease_out_cubic(type_t))
    visible_text = headline[:chars_to_show]

    wrapped = textwrap.fill(visible_text, width=26)
    lines = wrapped.split("\n")[:3]

    total_h = len(textwrap.fill(headline, width=26).split("\n")) * 62
    y_start = (HEIGHT - total_h) // 2 - 20

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_big)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_start), line, fill=TEXT_PRIMARY, font=font_big)
        y_start += 62

    # Cursor blink
    if type_t < 1 and int(t * 8) % 2 == 0:
        if lines:
            last_line = lines[-1]
            bbox = draw.textbbox((0, 0), last_line, font=font_big)
            cursor_x = (WIDTH - (bbox[2] - bbox[0])) // 2 + (bbox[2] - bbox[0])
            cursor_y = y_start - 62
            draw.rectangle([cursor_x + 4, cursor_y + 5, cursor_x + 8, cursor_y + 50], fill=ACCENT)

    # Underline (appears after text complete)
    if t > 0.7:
        ul_t = ease_out_cubic(min(1, (t - 0.7) / 0.15))
        ul_w = int(160 * ul_t)
        if ul_w > 0:
            draw.rectangle([(WIDTH // 2 - ul_w // 2), y_start + 10, (WIDTH // 2 + ul_w // 2), y_start + 13], fill=ACCENT)

    # Product image (fades in bottom-right)
    if t > 0.5 and product_img:
        fade = ease_out_cubic(min(1, (t - 0.5) / 0.3))
        pimg = product_img.resize((160, 160), Image.LANCZOS)
        alpha = pimg.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.4 * fade))
        pimg.putalpha(alpha)
        img.paste(pimg, (WIDTH - 190, HEIGHT - 200), pimg)
        draw = ImageDraw.Draw(img)

    # Logo
    if t > 0.6:
        la = int(255 * ease_out_cubic(min(1, (t - 0.6) / 0.2)))
        draw_logo(img, 40, HEIGHT - 70, 40)
        draw = ImageDraw.Draw(img)
        draw.text((90, HEIGHT - 62), "SECOND HASH", fill=(*TEXT_MUTED, la), font=fonts["sub"])

    return img


def render_philosophy_frame(frame_num, text, fonts, product_img):
    """Philosophy: quote fade-in with rotating geometric elements."""
    t = frame_num / TOTAL_FRAMES
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Animated diagonal lines (slowly shifting)
    offset = int(t * 60)
    for i in range(-HEIGHT + offset, WIDTH + HEIGHT, 120):
        draw.line([(i, HEIGHT), (i + HEIGHT, 0)], fill=(*ACCENT_DIM, 12), width=1)

    # Quotation mark (scales up)
    if t > 0.05:
        q_scale = ease_out_back(min(1, (t - 0.05) / 0.3))
        q_size = int(200 * q_scale)
        font_q = load_font(FONT_BOLD, q_size)
        q_alpha = int(60 * min(1, q_scale))
        draw.text((40, 30), "“", fill=(*ACCENT_DIM, q_alpha), font=font_q)

    # Category label
    if t > 0.1:
        a = int(255 * min(1, (t - 0.1) / 0.2))
        draw.text((60, 50), "THE REFAB THESIS", fill=(*ACCENT, a), font=fonts["sub"])
        lbl_bbox = draw.textbbox((60, 50), "THE REFAB THESIS", font=fonts["sub"])
        line_w = int(30 * ease_out_cubic(min(1, (t - 0.15) / 0.2)))
        if line_w > 0:
            draw.rectangle([60, lbl_bbox[3] + 4, 60 + line_w, lbl_bbox[3] + 6], fill=ACCENT)

    # Main quote text (word by word fade-in)
    headline = extract_key_line(text, 65)
    font_phil = load_font(FONT_BOLD, 42)
    wrapped = textwrap.fill(headline, width=30)
    lines = wrapped.split("\n")[:4]

    reveal_start = 0.2
    reveal_end = 0.65
    reveal_t = max(0, min(1, (t - reveal_start) / (reveal_end - reveal_start)))
    total_chars = sum(len(l) for l in lines)
    chars_visible = int(total_chars * ease_out_cubic(reveal_t))

    y = 140
    chars_shown = 0
    for line in lines:
        if chars_shown >= chars_visible:
            break
        visible = line[:max(0, chars_visible - chars_shown)]
        chars_shown += len(line)
        draw.text((60, y), visible, fill=TEXT_PRIMARY, font=font_phil)
        y += 56

    # Sub line
    if t > 0.6:
        sub_a = int(255 * ease_out_cubic(min(1, (t - 0.6) / 0.2)))
        sub_lines = extract_sub_lines(text, 1)
        if sub_lines:
            draw.text((60, y + 15), sub_lines[0][:70], fill=(*TEXT_SECONDARY, sub_a), font=fonts["body"])

    # Vertical accent bar (grows)
    if t > 0.3:
        bar_h = int((HEIGHT - 120) * ease_out_cubic(min(1, (t - 0.3) / 0.4)))
        draw.rectangle([WIDTH - 20, 60, WIDTH - 16, 60 + bar_h], fill=ACCENT)

    # Animated circles
    if t > 0.4:
        c_t = ease_out_cubic(min(1, (t - 0.4) / 0.4))
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        cd = ImageDraw.Draw(overlay)
        r1 = int(100 * c_t)
        r2 = int(60 * c_t)
        cd.ellipse([WIDTH - 150 - r1, HEIGHT - 150 - r1, WIDTH - 150 + r1, HEIGHT - 150 + r1],
                   outline=(*ACCENT_DIM, int(50 * c_t)), width=2)
        cd.ellipse([WIDTH - 140 - r2, HEIGHT - 140 - r2, WIDTH - 140 + r2, HEIGHT - 140 + r2],
                   outline=(*ACCENT_DIM, int(30 * c_t)), width=1)
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

    # Logo
    if t > 0.7:
        la = int(255 * ease_out_cubic(min(1, (t - 0.7) / 0.2)))
        draw_logo(img, 50, HEIGHT - 90, 50)
        draw = ImageDraw.Draw(img)
        draw.text((110, HEIGHT - 80), "SECOND HASH", fill=(*TEXT_PRIMARY, la), font=fonts["logo"])

    # Bottom bar
    bar_w = int(WIDTH * ease_out_cubic(min(1, t / 0.35)))
    if bar_w > 0:
        draw.rectangle([0, HEIGHT - 3, bar_w, HEIGHT], fill=ACCENT)

    return img


def render_community_frame(frame_num, text, fonts, product_img):
    """Community: bubble pop-in + text appear."""
    t = frame_num / TOTAL_FRAMES
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Background warmth
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_SECONDARY, 60))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Top bar
    bar_w = int(WIDTH * ease_out_cubic(min(1, t / 0.25)))
    if bar_w > 0:
        draw.rectangle([(WIDTH - bar_w) // 2, 0, (WIDTH + bar_w) // 2, 4], fill=ACCENT)

    # Category
    if t > 0.08:
        a = int(255 * min(1, (t - 0.08) / 0.15))
        draw.text((50, 40), "COMMUNITY", fill=(*ACCENT, a), font=fonts["sub"])

    # Large "?" watermark
    if t > 0.1:
        q_t = ease_out_cubic(min(1, (t - 0.1) / 0.3))
        q_size = int(280 * q_t)
        font_q = load_font(FONT_BOLD, max(10, q_size))
        q_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        qd = ImageDraw.Draw(q_overlay)
        qd.text((WIDTH - 300, 100), "?", fill=(*ACCENT, int(25 * q_t)), font=font_q)
        img = Image.alpha_composite(img, q_overlay)
        draw = ImageDraw.Draw(img)

    # Bubble (pop-in with overshoot)
    bubble_start = 0.15
    if t > bubble_start:
        b_t = ease_out_back(min(1, (t - bubble_start) / 0.35))
        bx, by = 50, 100
        bw = int(750 * b_t)
        bh = int(300 * b_t)
        if bw > 20 and bh > 20:
            bubble = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            bd = ImageDraw.Draw(bubble)
            bd.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20,
                                 fill=(*BG_CARD, int(200 * b_t)), outline=(*ACCENT_DIM, int(100 * b_t)), width=2)
            if b_t > 0.8:
                tri_x = bx + 100
                tri_y = by + bh
                bd.polygon([(tri_x, tri_y), (tri_x + 40, tri_y), (tri_x + 10, tri_y + 35)],
                           fill=(*BG_CARD, int(200 * b_t)))
            img = Image.alpha_composite(img, bubble)
            draw = ImageDraw.Draw(img)

    # Text inside bubble (typewriter)
    text_start = 0.4
    if t > text_start:
        headline = extract_key_line(text, 60)
        font_comm = load_font(FONT_BOLD, 36)
        txt_t = min(1, (t - text_start) / 0.35)
        chars = int(len(headline) * ease_out_cubic(txt_t))
        visible = headline[:chars]
        wrapped = textwrap.fill(visible, width=32)
        y = 140
        for line in wrapped.split("\n")[:4]:
            draw.text((90, y), line, fill=TEXT_PRIMARY, font=font_comm)
            y += 48

    # @ClubHashcash
    if t > 0.7:
        cta_a = int(255 * ease_out_cubic(min(1, (t - 0.7) / 0.15)))
        draw.text((70, 450), "@ClubHashcash", fill=(*ACCENT, cta_a), font=fonts["sub"])

    # Logo
    if t > 0.75:
        la = int(255 * ease_out_cubic(min(1, (t - 0.75) / 0.15)))
        draw_logo(img, WIDTH - 200, HEIGHT - 85, 50)
        draw = ImageDraw.Draw(img)
        draw.text((WIDTH - 140, HEIGHT - 75), "SH", fill=(*TEXT_PRIMARY, la), font=fonts["logo"])

    # Bottom bar
    bw = int(WIDTH * min(1, t / 0.3))
    if bw > 0:
        draw.rectangle([0, HEIGHT - 3, bw, HEIGHT], fill=ACCENT)
    return img


def render_recap_frame(frame_num, text, fonts, product_img):
    """Recap: dashboard with growing bars and counting stats."""
    t = frame_num / TOTAL_FRAMES
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Grid lines
    grid_a = int(40 * min(1, t / 0.2))
    for x in range(0, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=(*BORDER, grid_a), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([(0, y), (WIDTH, y)], fill=(*BORDER, grid_a), width=1)

    # Header bar (slides down)
    header_t = ease_out_cubic(min(1, t / 0.2))
    header_y = int(-60 + 60 * header_t)
    draw.rectangle([0, header_y, WIDTH, header_y + 60], fill=(*BG_SECONDARY, 255))
    draw.rectangle([0, header_y + 58, WIDTH, header_y + 62], fill=ACCENT)
    draw.text((30, header_y + 18), "WEEKLY RECAP  |  SECOND HASH", fill=ACCENT, font=fonts["sub"])
    font_status = load_font(FONT_MONO, 14)
    draw.text((WIDTH - 200, header_y + 22), "STATUS: OPERATIONAL", fill=ACCENT_BRIGHT, font=font_status)

    # Stat cards (stagger in)
    cards = [("REFABBED", "[X]", "units"), ("SOLD", "[X]", "units"),
             ("MARGIN", "HEALTHY", ""), ("UPTIME", "99.7%", "")]
    card_w, card_h = 250, 120
    gap = 20
    start_x = (WIDTH - (card_w * 4 + gap * 3)) // 2
    card_y_target = 100

    for i, (label, value, unit) in enumerate(cards):
        card_start = 0.15 + i * 0.08
        if t < card_start:
            continue
        c_t = ease_out_cubic(min(1, (t - card_start) / 0.25))
        cx = start_x + i * (card_w + gap)
        cy_offset = int(50 * (1 - c_t))
        cy = card_y_target + cy_offset
        c_alpha = int(220 * c_t)

        card_ov = Image.new("RGBA", (card_w, card_h), (*BG_CARD, c_alpha))
        cd = ImageDraw.Draw(card_ov)
        cd.rectangle([0, 0, card_w, 3], fill=(*ACCENT, int(255 * c_t)))
        img.paste(card_ov, (cx, cy), card_ov)
        draw = ImageDraw.Draw(img)

        val_a = int(255 * c_t)
        draw.text((cx + 20, cy + 20), label, fill=(*TEXT_MUTED, val_a), font=font_status)
        font_val = load_font(FONT_BOLD, 36)
        draw.text((cx + 20, cy + 45), value, fill=(*TEXT_PRIMARY, val_a), font=font_val)
        if unit:
            draw.text((cx + 20, cy + 88), unit, fill=(*TEXT_SECONDARY, val_a), font=font_status)

    # Bar chart (bars grow up one by one)
    bar_y = HEIGHT - 160
    bar_h_max = 100
    bar_w = 30
    bar_gap = 15
    n_bars = 14
    bar_start_x = (WIDTH - (bar_w + bar_gap) * n_bars) // 2
    rng = random.Random(hash(text))
    bar_heights = [rng.uniform(0.2, 1.0) for _ in range(n_bars)]

    for i in range(n_bars):
        b_start = 0.35 + i * 0.025
        if t < b_start:
            continue
        b_t = ease_out_cubic(min(1, (t - b_start) / 0.2))
        bh = int(bar_heights[i] * bar_h_max * b_t)
        bx = bar_start_x + i * (bar_w + bar_gap)
        color = ACCENT if i >= n_bars - 3 else TEXT_MUTED
        if bh > 0:
            draw.rectangle([bx, bar_y + bar_h_max - bh, bx + bar_w, bar_y + bar_h_max], fill=color)

    # Logo
    if t > 0.8:
        la = int(255 * ease_out_cubic(min(1, (t - 0.8) / 0.15)))
        draw_logo(img, 40, HEIGHT - 55, 35)
        draw = ImageDraw.Draw(img)
        draw.text((82, HEIGHT - 47), "SECOND HASH", fill=(*TEXT_MUTED, la), font=fonts["tag"])

    draw.rectangle([0, HEIGHT - 3, WIDTH, HEIGHT], fill=ACCENT)
    return img


def render_launch_frame(frame_num, text, fonts, product_img):
    """Launch: logo reveal + product lineup slide-in."""
    t = frame_num / TOTAL_FRAMES
    img = Image.new("RGBA", (WIDTH, HEIGHT), (*BG_PRIMARY, 255))
    draw = ImageDraw.Draw(img)

    # Starburst (rotates slowly)
    burst = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    cx, cy = WIDTH // 2, HEIGHT // 2 - 30
    angle_offset = t * 15
    burst_a = int(10 * min(1, t / 0.3))
    for angle in range(0, 360, 15):
        rad = math.radians(angle + angle_offset)
        ex = cx + int(600 * math.cos(rad))
        ey = cy + int(600 * math.sin(rad))
        bd.line([(cx, cy), (ex, ey)], fill=(*ACCENT_DIM, burst_a), width=1)
    img = Image.alpha_composite(img, burst)
    draw = ImageDraw.Draw(img)

    # Glow
    glow_t = ease_out_cubic(min(1, t / 0.4))
    draw_glow(img, WIDTH // 2, HEIGHT // 2 - 30, int(400 * glow_t), ACCENT, alpha=int(30 * glow_t))
    draw = ImageDraw.Draw(img)

    # Logo (scales up with bounce)
    if t > 0.05:
        logo_t = ease_out_back(min(1, (t - 0.05) / 0.35))
        logo_size = int(140 * logo_t)
        if logo_size > 5:
            draw_logo(img, WIDTH // 2 - logo_size // 2, int(100 + (1 - logo_t) * 30), logo_size)
            draw = ImageDraw.Draw(img)

    # Brand name
    if t > 0.25:
        name_t = ease_out_cubic(min(1, (t - 0.25) / 0.25))
        font_brand = load_font(FONT_BOLD, 52)
        brand = "SECOND HASH"
        bbox = draw.textbbox((0, 0), brand, font=font_brand)
        tw = bbox[2] - bbox[0]
        name_a = int(255 * name_t)
        draw.text(((WIDTH - tw) // 2, 270), brand, fill=(*TEXT_PRIMARY, name_a), font=font_brand)

    # Accent line (grows from center)
    if t > 0.35:
        line_t = ease_out_cubic(min(1, (t - 0.35) / 0.15))
        lw = int(120 * line_t)
        if lw > 0:
            draw.rectangle([(WIDTH // 2 - lw // 2), 335, (WIDTH // 2 + lw // 2), 338], fill=ACCENT)

    # Tagline
    if t > 0.4:
        tag_t = ease_out_cubic(min(1, (t - 0.4) / 0.2))
        tag_a = int(255 * tag_t)
        font_tag_lg = load_font(FONT_REGULAR, 22)
        tagline = "Every hash deserves a second chance."
        bbox2 = draw.textbbox((0, 0), tagline, font=font_tag_lg)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((WIDTH - tw2) // 2, 355), tagline, fill=(*TEXT_SECONDARY, tag_a), font=font_tag_lg)

    # "NOW OPEN" badge
    if t > 0.55:
        badge_t = ease_out_back(min(1, (t - 0.55) / 0.2))
        badge_w, badge_h = 180, 40
        badge_x = (WIDTH - badge_w) // 2
        badge_y = 430 + int(30 * (1 - badge_t))
        badge_a = int(255 * min(1, badge_t))
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
                                radius=6, fill=(*ACCENT, badge_a))
        font_badge = load_font(FONT_BOLD, 18)
        btxt = "NOW OPEN"
        bb = draw.textbbox((0, 0), btxt, font=font_badge)
        btw = bb[2] - bb[0]
        bth = bb[3] - bb[1]
        draw.text((badge_x + (badge_w - btw) // 2, badge_y + (badge_h - bth) // 2 - 2),
                  btxt, fill=(*BG_PRIMARY, badge_a), font=font_badge)

    # Product lineup (slides in from right)
    if t > 0.6:
        lineup_t = ease_out_cubic(min(1, (t - 0.6) / 0.3))
        product_files = ["SH-R1_Reclaim.png", "SH-B3_Overclock.png", "SH-X1_Overhaul.png",
                         "SH-R4_Fuse.png", "SH-X2_Apex.png"]
        prod_size = 90
        total_w = len(product_files) * prod_size + (len(product_files) - 1) * 15
        px_start = (WIDTH - total_w) // 2
        slide_offset = int(WIDTH * (1 - lineup_t))

        for i, pf in enumerate(product_files):
            pp = IMAGES_DIR / pf
            if pp.exists():
                delay = i * 0.04
                item_t = ease_out_cubic(min(1, max(0, lineup_t - delay) / (1 - delay))) if delay < 1 else lineup_t
                pi = Image.open(pp).convert("RGBA")
                pi = pi.resize((prod_size, prod_size), Image.LANCZOS)
                item_offset = int(200 * (1 - item_t))
                img.paste(pi, (px_start + i * (prod_size + 15) + item_offset, HEIGHT - 130), pi)
        draw = ImageDraw.Draw(img)

    bw_bottom = int(WIDTH * min(1, t / 0.3))
    if bw_bottom > 0:
        draw.rectangle([0, HEIGHT - 4, bw_bottom, HEIGHT], fill=ACCENT)
    return img


# =============================================================
# VIDEO BUILDER
# =============================================================

RENDERERS = {
    "product": render_product_frame,
    "meme": render_meme_frame,
    "philosophy": render_philosophy_frame,
    "community": render_community_frame,
    "recap": render_recap_frame,
    "launch": render_launch_frame,
}


def generate_video(post_data: dict, output_path: Path) -> bool:
    text = post_data.get("text", "")
    category = post_data.get("category", "product")
    renderer = RENDERERS.get(category, render_product_frame)

    # Load fonts
    fonts = {
        "headline": load_font(FONT_BOLD, 42),
        "sub": load_font(FONT_REGULAR, 16),
        "body": load_font(FONT_REGULAR, 18),
        "tag": load_font(FONT_MONO, 13),
        "logo": load_font(FONT_BOLD, 24),
    }

    # Load product image if needed
    product_img = None
    product_file = pick_product_image(text)
    product_path = IMAGES_DIR / product_file
    if product_path.exists():
        product_img = Image.open(product_path).convert("RGBA")

    # Create temp directory for frames
    TEMP_DIR.mkdir(exist_ok=True)
    frame_dir = TEMP_DIR / output_path.stem
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir()

    # Generate frames
    for i in range(TOTAL_FRAMES):
        frame = renderer(i, text, fonts, product_img)
        frame_rgb = frame.convert("RGB")
        frame_rgb.save(frame_dir / f"frame_{i:04d}.png")

        if i % FPS == 0:
            print(f"  [{output_path.stem}] Frame {i}/{TOTAL_FRAMES}", end="\r")

    print(f"  [{output_path.stem}] Frames complete. Encoding MP4...")

    # Encode with FFmpeg
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frame_dir / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "23",
        "-movflags", "+faststart",
        str(output_path),
    ]
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FFmpeg error: {result.stderr[-500:]}")
        return False

    # Cleanup frames
    shutil.rmtree(frame_dir)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  [{output_path.stem}] Done: {size_mb:.1f}MB")
    return True


def process_queue(target_file: str = None):
    if target_file:
        files = [Path(target_file)]
    else:
        files = sorted(QUEUE_DIR.glob("*.json"))

    generated = 0
    for json_path in files:
        mp4_path = json_path.with_suffix(".mp4")

        with open(json_path) as f:
            post_data = json.load(f)

        print(f"[video] Generating {mp4_path.name} ({post_data.get('category', '?')})...")
        if generate_video(post_data, mp4_path):
            # Update JSON to reference video
            post_data["video"] = mp4_path.name
            with open(json_path, "w") as f:
                json.dump(post_data, f, indent=2, ensure_ascii=False)
            print(f"[video] {mp4_path.name} complete.")
            generated += 1

    print(f"[video] Done. {generated} video(s) generated.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    process_queue(target)
