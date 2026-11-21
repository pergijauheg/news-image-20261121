#!/usr/bin/env python3
"""Draw the Saturday Globe front page for 21 November 2026.

A one-page newspaper drawn from scratch with Pillow: masthead, headlines,
short decks and small pictograms for each story. No network, no randomness,
no timestamps, so the output is fully deterministic.

Run: python3 draw.py  ->  writes entry.png next to this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (31, 58, 95)
DARK = (22, 35, 58)
GREY = (90, 86, 78)
LIGHT = (190, 185, 170)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

M = 28                 # side margin
X1 = W - M             # right edge of the text block
COLW = X1 - M          # full text width


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, size=16):
    fnt = font(F_SANS_B, size)
    draw.text((x, y), label, font=fnt, fill=RED)
    return y + size + 7


def headline(draw, x, y, text, size, max_w):
    fnt = font(F_SERIF_B, size)
    lines = wrap(draw, text, fnt, max_w)
    return text_block(draw, x, y, lines, fnt, leading=int(size * 1.08))


def deck(draw, x, y, text, size, max_w):
    fnt = font(F_SANS, size)
    lines = wrap(draw, text, fnt, max_w)
    return text_block(draw, x, y, lines, fnt, leading=int(size * 1.32))


def hrule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def vrule(draw, x, y0, y1, width=1, fill=LIGHT):
    draw.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---- small pictograms -----------------------------------------------------

def radar_panel(draw, x, y, w, h):
    """Dark panel with radar rings and red contact dots."""
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    cx, cy = x + 70, y + h // 2
    for r in (56, 38, 20):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=(120, 150, 190), width=2)
    draw.line([(cx, cy - 56), (cx, cy + 56)], fill=(120, 150, 190), width=1)
    draw.line([(cx - 56, cy), (cx + 56, cy)], fill=(120, 150, 190), width=1)
    for dx, dy in ((32, -26), (44, 16), (-16, 36)):
        draw.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                     fill=RED)
    tx = x + 148
    f1 = font(F_SANS_B, 19)
    f2 = font(F_SANS, 15)
    f3 = font(F_SANS_B, 17)
    draw.text((tx, y + 24), "NOWA D\u0118BA", font=f1, fill=(255, 255, 255))
    draw.text((tx, y + 52), "Allied drills", font=f2, fill=(210, 215, 225))
    draw.text((tx, y + 80), "2 missiles \u2022 1 drone", font=f3,
              fill=(255, 210, 210))
    draw.text((tx, y + 110), "No casualties", font=f2, fill=(210, 215, 225))


def market_chart(draw, x, y, w, h):
    """A falling red line chart."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=GREY, width=1)
    ox, oy = x + 30, y + h - 20
    draw.line([(ox, y + 8), (ox, oy)], fill=GREY, width=1)
    draw.line([(ox, oy), (x + w - 8, oy)], fill=GREY, width=1)
    pts = [(0, 0.25), (0.18, 0.32), (0.36, 0.28), (0.52, 0.52),
           (0.68, 0.62), (0.84, 0.85), (1.0, 0.95)]
    px = [ox + int(t * (w - 44)) for t, _ in pts]
    py = [y + 10 + int(v * (h - 36)) for _, v in pts]
    draw.line(list(zip(px, py)), fill=RED, width=3)
    for cx, cy in zip(px, py):
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    f = font(F_SANS_B, 14)
    draw.text((x + w - 52, y + 4), "\u22123.7%", font=f, fill=RED)


def skyline(draw, x, y, w, h):
    """A dark city skyline silhouette."""
    base = y + h
    heights = [0.55, 0.8, 0.45, 0.95, 0.65, 0.85, 0.5, 0.75, 0.6]
    bw = w // len(heights)
    for i, frac in enumerate(heights):
        bh = int(h * frac)
        draw.rectangle([x + i * bw + 2, base - bh, x + (i + 1) * bw - 2, base],
                       fill=DARK)
        for wy in range(base - bh + 7, base - 5, 13):
            draw.rectangle([x + i * bw + 7, wy, x + i * bw + 11, wy + 4],
                           fill=(255, 220, 130))


def chalkboard(draw, x, y, w, h):
    """A dark strip with the zeta function and the primes."""
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    f1 = font(F_SANS, 16)
    draw.text((x + 10, y + h // 2 - 10),
              "\u03b6(s) = 0   \u00b7   2 3 5 7 11 13 17 19", font=f1,
              fill=(255, 220, 130))


def flags(draw, x, y, w, h):
    """Two small flags: the Union Jack (simplified) and the EU circle."""
    fw, fh = (w - 12) // 2, h
    draw.rectangle([x, y, x + fw, y + fh], fill=(30, 60, 130))
    draw.line([(x, y + fh // 2), (x + fw, y + fh // 2)], fill=(255, 255, 255),
              width=8)
    draw.line([(x + fw // 2, y), (x + fw // 2, y + fh)], fill=(255, 255, 255),
              width=8)
    draw.line([(x, y + fh // 2), (x + fw, y + fh // 2)], fill=(200, 20, 40),
              width=4)
    draw.line([(x + fw // 2, y), (x + fw // 2, y + fh)], fill=(200, 20, 40),
              width=4)
    ex = x + fw + 12
    draw.rectangle([ex, y, ex + fw, y + fh], fill=(20, 40, 110))
    cx, cy = ex + fw // 2, y + fh // 2
    for k in range(12):
        ang = 2 * math.pi * k / 12 - math.pi / 2
        dx = int(cx + 0.30 * fh * math.cos(ang))
        dy = int(cy + 0.30 * fh * math.sin(ang))
        draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 210, 60))


def server_rack(draw, x, y, w, h):
    """Three server units with status lights."""
    for i in range(3):
        uh = h // 3 - 2
        uy = y + i * (h // 3)
        draw.rectangle([x, uy, x + w, uy + uh], fill=DARK)
        for dxi in range(3):
            col = (120, 200, 120) if dxi != 1 else (255, 210, 60)
            draw.ellipse([x + 8 + dxi * 12, uy + uh // 2 - 2,
                          x + 12 + dxi * 12, uy + uh // 2 + 2], fill=col)
        draw.line([(x + 52, uy + 3), (x + w - 8, uy + 3)],
                  fill=(120, 150, 190), width=1)
        draw.line([(x + 52, uy + uh - 4), (x + w - 8, uy + uh - 4)],
                  fill=(120, 150, 190), width=1)


# ---- the front page ---------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    f_mast = font(F_SERIF_B, 60)
    d.text((W // 2, 16), "THE SATURDAY GLOBE", font=f_mast, fill=INK,
           anchor="ma")
    hrule(d, M, X1, 92, width=2)
    hrule(d, M, X1, 96, width=1)
    f_date = font(F_SANS_B, 21)
    d.text((M, 106), "SATURDAY 21 NOVEMBER 2026", font=f_date, fill=INK)
    d.text((X1, 106), "WORLD IN ONE PAGE", font=f_date, fill=RED, anchor="ra")
    hrule(d, M, X1, 136, width=3)
    hrule(d, M, X1, 140, width=1)

    # ---- Lead story: Poland ----------------------------------------------
    y = 154
    y = kicker(d, M, y, "WAR IN EUROPE")
    y = headline(d, M, y, "MISSILES LAND IN POLAND", 46, 600)
    y = deck(d, M, y + 4,
             "NATO calls it a \u201cgrave violation\u201d as two Russian "
             "missiles and a jet-powered drone come down in the "
             "south-east during allied drills. PM Tusk calls it an "
             "\u201cintentional provocation\u201d.",
             19, 592)
    radar_panel(d, 648, 154, X1 - 648, 172)
    hrule(d, M, X1, 348, width=1)

    # ---- Row 2: markets + GTA --------------------------------------------
    y = 362
    col2 = (COLW - 24) // 2
    y2 = kicker(d, M, y, "MARKETS")
    y2 = headline(d, M, y2, "AI ROUT DRAGS S&P INTO CORRECTION", 28, col2)
    y2 = deck(d, M, y2 + 3,
              "S&P 500 falls 3.7% and Nasdaq 5.3% as chip stocks plunge; "
              "Nvidia down 14%.",
              16, col2)
    market_chart(d, M, y2 + 6, col2, 58)

    x2 = M + col2 + 24
    y2 = kicker(d, x2, y, "ENTERTAINMENT")
    y2 = headline(d, x2, y2, "GTA VI BANKS $2.36bn IN A DAY", 28, col2)
    y2 = deck(d, x2, y2 + 3,
              "24.6m copies in 24 hours \u2014 the biggest entertainment "
              "launch ever.",
              16, col2)
    skyline(d, x2, y2 + 6, col2, 58)
    vrule(d, M + col2 + 12, 362, 548)
    hrule(d, M, X1, 556, width=1)

    # ---- Row 3: three columns ---------------------------------------------
    y = 570
    col3 = (COLW - 40) // 3
    xs = [M, M + col3 + 20, M + 2 * (col3 + 20)]
    y3 = kicker(d, xs[0], y, "SCIENCE")
    y3 = headline(d, xs[0], y3, "A PROOF, AT LAST?", 24, col3)
    y3 = deck(d, xs[0], y3 + 3,
              "AI-built Riemann proof \u201calmost certainly true\u201d, "
              "say checkers.",
              15, col3)
    chalkboard(d, xs[0], y3 + 5, col3, 36)

    y3 = kicker(d, xs[1], y, "BRITAIN & EUROPE")
    y3 = headline(d, xs[1], y3, "UK AND EU SIGN RESET DEAL", 24, col3)
    y3 = deck(d, xs[1], y3 + 3,
              "Food, carbon, youth pacts signed in Brussels; Burnham "
              "hails \u201cnew chapter\u201d.",
              15, col3)
    flags(d, xs[1], y3 + 5, col3, 36)

    y3 = kicker(d, xs[2], y, "TECH")
    y3 = headline(d, xs[2], y3, "TRUMP: NO CENTRES ABROAD", 24, col3)
    y3 = deck(d, xs[2], y3 + 3,
              "President threatens a \u201ctremendous tax\u201d on US firms "
              "building AI centres abroad.",
              15, col3)
    server_rack(d, xs[2], y3 + 5, col3, 36)
    for vx in (M + col3 + 10, M + 2 * col3 + 30):
        vrule(d, vx, 570, 724)
    hrule(d, M, X1, 734, width=1)

    # ---- Row 4: three columns ---------------------------------------------
    y = 748
    y4 = kicker(d, xs[0], y, "FRANCE", size=15)
    y4 = headline(d, xs[0], y4, "ZECLER OFFICERS JAILED", 22, col3)
    deck(d, xs[0], y4 + 3,
         "Three police convicted over the 2020 Zecler beating; racism "
         "an aggravating factor.",
         14, col3)

    y4 = kicker(d, xs[1], y, "CRICKET", size=15)
    y4 = headline(d, xs[1], y4, "RAHUL MAKES HISTORY", 22, col3)
    deck(d, xs[1], y4 + 3,
         "First Indian opener with Test hundreds in all SENA nations "
         "\u2014 100 off 207 balls.",
         14, col3)

    y4 = kicker(d, xs[2], y, "DEFENCE", size=15)
    y4 = headline(d, xs[2], y4, "PENTAGON RELEASES UFO FILMS", 22, col3)
    deck(d, xs[2], y4 + 3,
         "Three new UAP videos from the Middle East declassified.",
         14, col3)
    for vx in (M + col3 + 10, M + 2 * col3 + 30):
        vrule(d, vx, 748, 866)
    hrule(d, M, X1, 876, width=1)

    # ---- In brief -----------------------------------------------------------
    y = 888
    f_lab = font(F_SANS_B, 16)
    d.text((M, y), "IN BRIEF", font=f_lab, fill=RED)
    y += 26
    briefs = [
        ("CALIFORNIA SUBPOENAS NVIDIA",
         " over Huang\u2019s China ties."),
        ("879,000 AI CHIPS",
         " cleared for China, House panel reveals."),
        ("BINANCE HACKER",
         " moves $594m in ETH via THORChain."),
        ("FOOTBALL:",
         " Espanyol 1\u20130 Athletic; Bayern 1\u20131 K\u00f6ln; "
         "Troyes 3\u20131 Le Havre."),
    ]
    f_b = font(F_SANS, 15)
    f_b1 = font(F_SANS_B, 15)
    for lead, rest in briefs:
        d.text((M, y), "\u2022  " + lead, font=f_b1, fill=INK)
        tw = d.textlength("\u2022  " + lead, font=f_b1)
        d.text((M + tw, y), rest, font=f_b, fill=INK)
        y += 19

    # ---- Footer -------------------------------------------------------------
    hrule(d, M, X1, 994, width=1)
    f_ft = font(F_SANS, 14)
    d.text((W // 2, 1002),
           "The Saturday Globe  \u2022  Saturday 21 November 2026  \u2022  "
           "All stories as reported today",
           font=f_ft, fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
