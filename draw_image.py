#!/usr/bin/env python3
"""Draw entry.png: a one-image summary of world news on Thursday 19 November 2026.

Run locally (needs Pillow); the grader only runs main.py, which copies the
committed entry.png. Layout: masthead with the date, one lead story, eight
story cards with hand-drawn icons, footer. 1024x1024, deterministic.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (14, 22, 38)
PAPER = (246, 241, 231)
RED = (198, 40, 49)
GOLD = (232, 176, 32)
TEAL = (23, 133, 140)
GREEN = (46, 140, 84)
PURPLE = (108, 74, 160)
ORANGE = (222, 116, 28)
SKY = (58, 124, 196)
SLATE = (52, 64, 84)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def flag_us(d, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        c = (179, 34, 52) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    d.rectangle([x, y, x + w * 0.42, y + stripe * 4], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            cx = x + 6 + c * (w * 0.42 - 10) / 3
            cy = y + 5 + r * (stripe * 4 - 8) / 2
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=WHITE)
    d.rectangle([x, y, x + w, y + h], outline=BLACK, width=2)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=BLACK, width=2)
    cx, cy, r = x + w * 0.22, y + h * 0.3, h * 0.16
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))
    d.rectangle([x, y, x + w, y + h], outline=BLACK, width=2)


def icon_barrel(d, cx, cy, s, c):
    w, h = s * 0.62, s * 0.85
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=8, fill=c, outline=BLACK, width=3)
    for f in (0.28, 0.5, 0.72):
        d.line([cx - w / 2, cy - h / 2 + h * f, cx + w / 2, cy - h / 2 + h * f], fill=BLACK, width=3)
    d.ellipse([cx - w * 0.32, cy - h / 2 - 6, cx + w * 0.32, cy - h / 2 + 8], fill=c, outline=BLACK, width=3)


def icon_bridge(d, cx, cy, s, c):
    x0, x1 = cx - s * 0.48, cx + s * 0.48
    deck = cy - s * 0.05
    d.line([x0, deck, x1, deck], fill=c, width=7)
    for fx in (0.18, 0.5, 0.82):
        px = x0 + (x1 - x0) * fx
        d.line([px, deck - s * 0.34, px, deck + s * 0.3], fill=c, width=6)
    d.arc([x0, deck - s * 0.36, cx, deck + s * 0.1], 180, 360, fill=c, width=4)
    d.arc([cx, deck - s * 0.36, x1, deck + s * 0.1], 180, 360, fill=c, width=4)
    for i in range(3):
        wy = cy + s * (0.22 + i * 0.11)
        d.arc([cx - s * 0.4, wy - 8, cx - s * 0.05, wy + 8], 0, 180, fill=SKY, width=3)
        d.arc([cx + s * 0.05, wy - 8, cx + s * 0.4, wy + 8], 0, 180, fill=SKY, width=3)


def icon_tent(d, cx, cy, s, c):
    # a relief tent under a broken-ceasefire sun
    d.polygon([(cx - s * 0.46, cy + s * 0.34), (cx, cy - s * 0.3), (cx + s * 0.46, cy + s * 0.34)],
              fill=c, outline=BLACK)
    d.polygon([(cx - s * 0.13, cy + s * 0.34), (cx, cy - s * 0.02), (cx + s * 0.13, cy + s * 0.34)],
              fill=BLACK)
    d.line([cx - s * 0.52, cy + s * 0.38, cx + s * 0.52, cy + s * 0.38], fill=BLACK, width=4)
    sx, sy = cx + s * 0.34, cy - s * 0.34
    d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=GOLD, outline=BLACK, width=2)
    for a in range(0, 360, 45):
        x2 = sx + 16 * math.cos(math.radians(a))
        y2 = sy + 16 * math.sin(math.radians(a))
        d.line([sx, sy, x2, y2], fill=GOLD, width=3)


def icon_chart(d, cx, cy, s, c):
    x0, y0 = cx - s * 0.42, cy + s * 0.36
    d.line([x0, cy - s * 0.4, x0, y0], fill=BLACK, width=4)
    d.line([x0, y0, cx + s * 0.46, y0], fill=BLACK, width=4)
    bw = s * 0.16
    for i, hh in enumerate((0.22, 0.38, 0.56, 0.78)):
        bx = x0 + 8 + i * (bw + 6)
        d.rectangle([bx, y0 - s * hh, bx + bw, y0], fill=c, outline=BLACK, width=2)
    d.line([x0 + 4, y0 - s * 0.3, cx + s * 0.44, y0 - s * 0.86], fill=RED, width=5)
    d.polygon([(cx + s * 0.44, y0 - s * 0.86), (cx + s * 0.3, y0 - s * 0.84), (cx + s * 0.42, y0 - s * 0.72)], fill=RED)


def icon_scales(d, cx, cy, s, c):
    top = cy - s * 0.42
    d.line([cx, top, cx, cy + s * 0.3], fill=c, width=6)
    d.line([cx - s * 0.38, top + s * 0.1, cx + s * 0.38, top + s * 0.1], fill=c, width=6)
    d.ellipse([cx - 6, top - 6, cx + 6, top + 6], fill=c, outline=BLACK, width=2)
    for sx in (cx - s * 0.38, cx + s * 0.38):
        d.line([sx, top + s * 0.1, sx - s * 0.13, cy + s * 0.08], fill=c, width=3)
        d.line([sx, top + s * 0.1, sx + s * 0.13, cy + s * 0.08], fill=c, width=3)
        d.arc([sx - s * 0.15, cy - s * 0.02, sx + s * 0.15, cy + s * 0.2], 0, 180, fill=c, width=5)
    d.line([cx - s * 0.2, cy + s * 0.36, cx + s * 0.2, cy + s * 0.36], fill=c, width=7)


def icon_atom(d, cx, cy, s, c):
    for ang in (0, 60, 120):
        pts = []
        for i in range(61):
            t = i / 60 * 2 * math.pi
            ex, ey = s * 0.46 * math.cos(t), s * 0.18 * math.sin(t)
            rx = ex * math.cos(math.radians(ang)) - ey * math.sin(math.radians(ang))
            ry = ex * math.sin(math.radians(ang)) + ey * math.cos(math.radians(ang))
            pts.append((cx + rx, cy + ry))
        d.line(pts, fill=c, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=c, outline=BLACK, width=2)


def icon_leaf(d, cx, cy, s, c):
    x0, y0 = cx - s * 0.42, cy + s * 0.36
    x1, y1 = cx + s * 0.42, cy - s * 0.36
    upper, lower = [], []
    for i in range(41):
        t = i / 40
        bx = x0 + (x1 - x0) * t
        by = y0 + (y1 - y0) * t
        off = s * 0.3 * math.sin(t * math.pi)
        upper.append((bx - off * 0.7, by - off * 0.7))
        lower.append((bx + off * 0.7, by + off * 0.7))
    d.polygon(upper + lower[::-1], fill=c, outline=BLACK)
    d.line([x0, y0, x1, y1], fill=BLACK, width=4)
    d.line([cx - s * 0.12, cy + s * 0.1, cx - s * 0.2, cy - s * 0.08], fill=BLACK, width=3)
    d.line([cx + s * 0.1, cy - s * 0.08, cx + s * 0.02, cy - s * 0.26], fill=BLACK, width=3)


def icon_capitol(d, cx, cy, s, c):
    base = cy + s * 0.36
    d.arc([cx - s * 0.3, cy - s * 0.42, cx + s * 0.3, cy + s * 0.18], 180, 360, fill=c, width=8)
    d.line([cx, cy - s * 0.42, cx, cy - s * 0.52], fill=c, width=5)
    d.line([cx - s * 0.34, cy - s * 0.08, cx + s * 0.34, cy - s * 0.08], fill=c, width=6)
    for i in range(5):
        px = cx - s * 0.28 + i * s * 0.14
        d.line([px, cy - s * 0.02, px, base - s * 0.08], fill=c, width=5)
    d.line([cx - s * 0.4, base, cx + s * 0.4, base], fill=c, width=8)


CARDS = [
    ("MIDDLE EAST", RED, icon_barrel, "Iran widens attacks on Kuwait and Bahrain"),
    ("EUROPE", SKY, icon_bridge, "Third strike halts Kerch Bridge rail traffic"),
    ("GAZA", ORANGE, icon_tent, "Israel operates in central Gaza despite ceasefire"),
    ("BUSINESS", GREEN, icon_chart, "Anthropic's record $81B IPO at $1.5T value"),
    ("JUSTICE", PURPLE, icon_scales, "ICJ: Myanmar committed state genocide"),
    ("KOREA", SLATE, icon_atom, "IAEA: N. Korea expands uranium enrichment"),
    ("CLIMATE", TEAL, icon_leaf, "COP31 endgame: phaseout wording unresolved"),
    ("UNITED STATES", GOLD, icon_capitol, "Democrats secure 56-seat Senate majority"),
]


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    for gy in range(0, H, 46):
        for gx in range(0, W, 46):
            d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(30, 44, 66))

    d.text((48, 30), "THE WORLD IN ONE DAY", font=font(BOLD, 28), fill=GOLD)
    d.text((48, 66), "Thursday 19 November 2026", font=font(SERIFB, 50), fill=WHITE)
    d.rectangle([48, 134, W - 48, 142], fill=RED)

    ly0, ly1 = 160, 424
    d.rounded_rectangle([48, ly0, W - 48, ly1], radius=16, fill=PAPER)
    d.rectangle([48, ly0, 62, ly1], fill=RED)
    d.text((84, ly0 + 18), "LEAD STORY · DIPLOMACY", font=font(BOLD, 22), fill=RED)
    lead = "Trump, Xi and Putin open first trilateral summit in Shenzhen"
    y = ly0 + 52
    for line in wrap(d, lead, font(BOLD, 40), 560):
        d.text((84, y), line, font=font(BOLD, 40), fill=BLACK)
        y += 48
    sub = "\"Peace declaration\" after 90 minutes; Hormuz oil flow and nuclear risks on the table"
    y += 2
    for line in wrap(d, sub, font(REG, 22), 560):
        d.text((84, y), line, font=font(REG, 22), fill=SLATE)
        y += 28
    fx, fy = 700, ly0 + 34
    flag_us(d, fx, fy, 108, 72)
    flag_cn(d, fx + 122, fy, 108, 72)
    flag_ru(d, fx + 61, fy + 86, 108, 72)
    d.text((fx + 40, fy + 168), "Shenzhen · APEC", font=font(BOLD, 20), fill=SLATE)

    mx, gap = 48, 14
    cw = (W - 2 * mx - 3 * gap) // 4
    ch = 248
    y0 = 440
    for i, (tag, color, icon, head) in enumerate(CARDS):
        r, c = divmod(i, 4)
        x = mx + c * (cw + gap)
        yy = y0 + r * (ch + gap)
        d.rounded_rectangle([x, yy, x + cw, yy + ch], radius=14, fill=PAPER)
        d.rounded_rectangle([x, yy, x + cw, yy + 38], radius=14, fill=color)
        d.rectangle([x, yy + 24, x + cw, yy + 38], fill=color)
        d.text((x + 14, yy + 8), tag, font=font(BOLD, 19), fill=WHITE)
        icon(d, x + cw // 2, yy + 88, 80, color)
        ty = yy + 134
        for line in wrap(d, head, font(BOLD, 20), cw - 24):
            d.text((x + 12, ty), line, font=font(BOLD, 20), fill=BLACK)
            ty += 25

    fy = y0 + 2 * ch + gap + 16
    d.rectangle([48, fy, W - 48, fy + 6], fill=GOLD)
    d.text((48, fy + 14), "World news summary · Thursday 19 November 2026 · one day, every region",
           font=font(REG, 21), fill=(190, 200, 215))

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
