#!/usr/bin/env python3
"""The NIMBLE GLOBE - front page for Thursday 19 November 2026.

Deterministic 1024x1024 PNG (Pillow only). No network, no time, no randomness.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 232)
INK = (28, 26, 24)
RED = (178, 34, 24)
GREY = (120, 115, 108)
CREAM = (240, 233, 220)
BLUE = (24, 60, 110)
BAND = (222, 217, 206)
WOOD = (146, 104, 62)
WOOD_LT = (196, 156, 114)
GOLD = (246, 214, 74)
HAIR = (120, 115, 108)
DIM = (180, 175, 165)
GULF = (150, 20, 20)

W = H = 1024
M = 28

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_font_cache = {}


def _first_existing(names):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.isfile(p):
            return p
    return None


def F(sz, bold=False, serif=False):
    """Font helper with deterministic fallback chain."""
    key = (sz, bold, serif)
    if key in _font_cache:
        return _font_cache[key]
    if serif:
        names = ["DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"]
        lib = ["LiberationSerif-Bold.ttf" if bold else "LiberationSerif-Regular.ttf"]
    else:
        names = ["DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"]
        lib = ["LiberationMono-Bold.ttf" if bold else "LiberationMono-Regular.ttf"]
    path = _first_existing(names) or _first_existing(lib)
    font = None
    if path:
        try:
            font = ImageFont.truetype(path, sz)
        except Exception:
            font = None
    if font is None:
        cand = None
        for root, dirs, files in sorted(os.walk("/usr/share/fonts")):
            dirs.sort()
            for fn in sorted(files):
                if fn.lower().endswith(".ttf"):
                    cand = os.path.join(root, fn)
                    break
            if cand:
                break
        if cand:
            try:
                font = ImageFont.truetype(cand, sz)
            except Exception:
                font = None
    if font is None:
        font = ImageFont.load_default()
    _font_cache[key] = font
    return font


# ---------------------------------------------------------------- helpers
def tw(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(d, cx, y, text, font, fill):
    d.text((cx - tw(d, text, font) / 2.0, y), text, font=font, fill=fill)


def right(d, rx, y, text, font, fill):
    d.text((rx - tw(d, text, font), y), text, font=font, fill=fill)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- sections
def masthead(d):
    d.rectangle([M, 14, W - M, 92], fill=RED)
    center(d, W / 2, 28, "THE NIMBLE GLOBE", F(40, bold=True, serif=True), CREAM)
    center(d, W / 2, 76, "ONE DAY'S WORLD NEWS, IN ONE PICTURE", F(12, bold=True), CREAM)
    d.rectangle([M, 100, W - M, 103], fill=INK)
    d.rectangle([M, 106, W - M, 107], fill=INK)


def edition(d):
    d.text((M, 122), "EDITION No 2026-325", font=F(11, bold=True), fill=INK)
    d.text((M, 138), "WORLD EDITION - 5 CONTINENTS - 1 PAGE", font=F(11), fill=INK)
    d.text((M, 154), "PRICE: FREE. CURRENCY: TRUTH.", font=F(10), fill=GREY)
    dx0, dy0 = W - M - 240, 114
    d.rectangle([dx0, dy0, W - M, 164], fill=INK)
    d.text((dx0 + 12, dy0 + 12), "DATE CHECK", font=F(10, bold=True), fill=CREAM)
    d.text((dx0 + 12, dy0 + 26), "THURSDAY 19 NOV 2026", font=F(13, bold=True), fill=CREAM)


def top_story(d):
    tx, ty, tww, th = M, 176, 620, 330
    d.rectangle([tx, ty, tx + tww, ty + th], fill=PAPER, outline=INK, width=3)
    # tag bar
    d.rectangle([tx + 10, ty + 10, tx + 230, ty + 28], fill=RED)
    d.text((tx + 16, ty + 14), "FRONT PAGE - TOP STORY", font=F(11, bold=True), fill=CREAM)
    # headline
    d.text((tx + 14, ty + 40), "TRUMP, XI AND PUTIN SIT DOWN", font=F(26, bold=True, serif=True), fill=INK)
    d.text((tx + 14, ty + 68), "FOR THE FIRST TIME IN HISTORY", font=F(26, bold=True, serif=True), fill=RED)
    d.rectangle([tx + 14, ty + 104, tx + tww - 14, ty + 105], fill=INK)
    # illustration band
    bx, by, bw, bh = tx + 14, ty + 112, tww - 28, 100
    d.rectangle([bx, by, bx + bw, by + bh], fill=BAND, outline=INK, width=1)
    cxm = bx + bw // 2 - 20
    # table
    d.ellipse([cxm - 160, by + 34, cxm + 160, by + 86], fill=WOOD, outline=INK, width=2)
    d.ellipse([cxm - 52, by + 46, cxm + 52, by + 74], outline=INK, width=1)
    d.arc([cxm - 120, by + 38, cxm + 80, by + 72], start=200, end=340, fill=WOOD_LT, width=3)
    # flags
    fy = by + 14
    flags = [("US", cxm - 120), ("CHINA", cxm - 20), ("RUSSIA", cxm + 80)]
    for name, fx in flags:
        d.rectangle([fx, fy, fx + 40, fy + 26], outline=INK, width=1)
        if name == "US":
            for i in range(7):
                col = RED if i % 2 == 0 else CREAM
                d.rectangle([fx + 1, fy + 1 + i * 26 // 7, fx + 39, fy + 1 + (i + 1) * 26 // 7 - 1], fill=col)
            d.rectangle([fx + 1, fy + 1, fx + 17, fy + 12], fill=BLUE)
            d.ellipse([fx + 7, fy + 4, fx + 11, fy + 8], fill=CREAM)
        elif name == "CHINA":
            d.rectangle([fx + 1, fy + 1, fx + 39, fy + 25], fill=RED)
            star(d, fx + 10, fy + 10, 5, GOLD)
            for ang in (-55, -20, 15, 50):
                star(d, fx + 10 + 11 * math.cos(math.radians(ang)), fy + 10 + 11 * math.sin(math.radians(ang)), 2, GOLD)
        else:  # RUSSIA
            d.rectangle([fx + 1, fy + 1, fx + 39, fy + 1 + 24 // 3], fill=CREAM)
            d.rectangle([fx + 1, fy + 1 + 24 // 3, fx + 39, fy + 1 + 2 * 24 // 3], fill=BLUE)
            d.rectangle([fx + 1, fy + 1 + 2 * 24 // 3, fx + 39, fy + 25], fill=RED)
        center(d, fx + 20, fy + 28, name, F(9, bold=True), INK)
    # location pin
    px = bx + bw - 70
    d.ellipse([px - 9, by + 21, px + 9, by + 39], fill=RED, outline=INK, width=1)
    d.rectangle([px - 1, by + 37, px + 1, by + 49], fill=INK)
    center(d, px, by + 52, "SHENZHEN", F(9, bold=True), RED)
    center(d, px, by + 63, "APEC 2026", F(8), INK)
    center(d, bx + bw / 2, by + bh - 12, "FIRST TRILATERAL EVER: THREE NUCLEAR POWERS, ONE TABLE", F(9), INK)
    # kicker + body + byline
    d.text((tx + 14, ty + 224), "APEC SUMMIT, DAY 2", font=F(11, bold=True), fill=RED)
    body = ("The US, China and Russia held their first-ever trilateral summit in "
            "Shenzhen on Thursday - the three nuclear superpowers at one table for "
            "the first time in history. Trump and Xi signed 11 deals, including US "
            "tariff relief on Chinese goods; Putin met both men separately; Ukraine "
            "was 'on the table', the Kremlin said.")
    lines = wrap(d, body, F(11), tww - 42)
    for i, ln in enumerate(lines):
        d.text((tx + 21, ty + 242 + i * 15), ln, font=F(11), fill=INK)
    d.rectangle([tx + 14, ty + th - 18, tx + tww - 14, ty + th - 17], fill=HAIR)
    d.text((tx + 14, ty + th - 14), "REUTERS | AP | AGENCY", font=F(9), fill=GREY)


def watch_rail(d):
    rx, ry = 662, 176
    rw, rh = W - M - rx, 330
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=INK)
    d.text((rx + 12, ry + 12), "THE WATCH", font=F(14, bold=True), fill=CREAM)
    y = ry + 12
    d.rectangle([rx + 12, y + 22, rx + rw - 12, y + 23], fill=HAIR)
    y += 32
    d.text((rx + 12, y), "NSA COMMS OUTAGE FALL-OUT", font=F(10, bold=True), fill=CREAM)
    y += 16
    for ln in ("The US national security agency's",
               "classified communications network",
               "went dark Wednesday - its first",
               "confirmed major outage since 1999.",
               "A 'partial' loss at a Georgia",
               "facility cut 1000s of US users.",
               "No cause released yet."):
        d.text((rx + 12, y), ln, font=F(10), fill=CREAM)
        y += 14
    y += 4
    d.rectangle([rx + 12, y, rx + rw - 12, y + 1], fill=HAIR)
    y += 6
    d.text((rx + 12, y), "MARKET TAPS - 19 NOV", font=F(10, bold=True), fill=GOLD)
    y += 16
    for label, val, note in (("S&P 500", "+1.0%", "6,770.06"),
                             ("NVDA", "+5.0%", "AFTER HRS"),
                             ("GOLD", "-0.9%", "13-MO LOW"),
                             ("BRENT OIL", "+2.0%", "$64.22")):
        d.text((rx + 12, y), label, font=F(10, bold=True), fill=CREAM)
        d.text((rx + 96, y), val, font=F(10, bold=True), fill=GOLD)
        right(d, rx + rw - 20, y, note, F(10), CREAM)
        y += 16
    y += 2
    d.rectangle([rx + 12, y, rx + rw - 12, y + 1], fill=HAIR)
    y += 6
    d.text((rx + 12, y), "PREVIEW", font=F(10, bold=True), fill=GOLD)
    y += 16
    for ln in ("FRIDAY: APEC CLOSING SUMMIT;", "US-CHINA JOINT STATEMENT DUE."):
        d.text((rx + 12, y), ln, font=F(10), fill=CREAM)
        y += 14
    d.text((rx + 12, ry + rh - 16), "AGENCY - 18/19 NOV", font=F(9), fill=DIM)


def cards(d):
    cw, ch, cy = 233, 218, 520
    gap = 12
    specs = [
        ("GAZA", RED, "GROUND RAID ON GAZA CITY",
         "Israel's army entered Gaza City Thursday, the first ground raid since the "
         "ceasefire began in October - a step towards the reconstruction phase, the "
         "IDF said. 3,519 killed under the truce since 10 Oct; 24 aid convoys a day, "
         "days short of the 60 goal.", "JPOST - 19 NOV"),
        ("MARKETS", BLUE, "US RECORDS, GOLD SLIDE",
         "S&P 500 closed +1% at 6,770, its second straight record; NVDA beat on "
         "data-centre revenue +73% and shares jumped 5% after the bell. Gold hit a "
         "13-month low as risk assets rallied; Brent +2% at $64.22 on the Gulf "
         "flare-up.", "BLOOMBERG - 19 NOV"),
        ("GULF", GULF, "IRAN HITS KUWAIT, DAY 6",
         "Tehran struck Kuwaiti territory for a sixth straight day after the US and "
         "Israel hit Iran's nuclear programme on 16 Nov. 108 were injured; Kuwait "
         "vowed to respond; the US warned Tehran further strikes would be answered; "
         "oil markets rattled.", "REUTERS - 19 NOV"),
        ("WORLD", BLUE, "BRIEFS FROM AROUND",
         "APEC: US-China sign 11 deals - tariff relief, strategic stability. UK: PM "
         "Starmer resigns after a leadership revolt. UN: Trump says the AI race is "
         "the superpower fight. EGYPT: Camp David accords mark 50 years. US: back "
         "inside the WHO.", "WORLD DESK - 19 NOV"),
    ]
    for i, (tag, tcol, title, body, stamp) in enumerate(specs):
        x = M + i * (cw + gap)
        d.rectangle([x, cy, x + cw, cy + ch], fill=PAPER, outline=INK, width=2)
        d.rectangle([x + 8, cy + 8, x + 8 + 8 + len(tag) * 7 + 14, cy + 8 + 16], fill=tcol)
        d.text((x + 12, cy + 10), tag, font=F(10, bold=True), fill=CREAM)
        d.text((x + 8, cy + 32), title, font=F(12, bold=True), fill=INK)
        lines = wrap(d, body, F(9), cw - 16)
        for j, ln in enumerate(lines[:11]):
            d.text((x + 8, cy + 56 + j * 12), ln, font=F(9), fill=INK)
        d.rectangle([x + 8, cy + 198, x + cw - 8, cy + 199], fill=HAIR)
        d.text((x + 8, cy + 202), stamp, font=F(8), fill=GREY)


def bottom_band(d):
    d.rectangle([M, 752, W - M, 860], fill=CREAM, outline=INK, width=2)
    d.text((M + 12, 762), "ALSO TODAY", font=F(13, bold=True), fill=RED)
    d.rectangle([M + 12, 782, W - M - 12, 783], fill=INK)
    items = [
        ("APEC", "Closes in Shenzhen; 11", "US-China deals signed."),
        ("WHO", "US re-enters the World", "Health Organization."),
        ("UK", "PM Starmer resigns after", "leadership revolt."),
        ("UN", "Trump: the AI race is the", "'superpower' fight."),
        ("EGYPT", "Camp David accords mark", "their 50th anniversary."),
    ]
    span, gap = 948, 12
    bw = (span - 4 * gap) // 5
    for i, (label, l1, l2) in enumerate(items):
        x = M + 10 + i * (bw + gap)
        d.rectangle([x, 788, x + bw, 852], fill=PAPER, outline=INK, width=1)
        d.text((x + 8, 794), label, font=F(10, bold=True), fill=RED)
        d.text((x + 8, 810), l1, font=F(8), fill=INK)
        d.text((x + 8, 822), l2, font=F(8), fill=INK)


def footer(d):
    d.rectangle([M, H - 34, W - M, H - 14], fill=INK)
    d.text((M + 12, H - 27), "THE NIMBLE GLOBE - PRINTED ONCE, ON THE DAY", font=F(9, bold=True), fill=CREAM)
    center(d, W / 2, H - 27, "make.fun", F(9), DIM)
    right(d, W - M - 12, H - 27, "THURSDAY 19 NOVEMBER 2026", F(9, bold=True), CREAM)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    edition(d)
    top_story(d)
    watch_rail(d)
    cards(d)
    bottom_band(d)
    footer(d)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        try:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "entry.png")
            img.save(path)
            print("wrote", path)
            return
        except OSError:
            pass
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "entry.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
