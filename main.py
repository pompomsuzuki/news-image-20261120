#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026.

Draws a newspaper front page that sums up the day's world news in one
1024x1024 PNG and writes it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
Pure standard library, no network, deterministic output.
"""

import os
import struct
import zlib

W = H = 1024

PAPER = (247, 242, 231)
INK = (26, 26, 40)
FAINT = (96, 96, 104)
RED = (178, 34, 52)
BLUE = (28, 52, 110)
SKY = (38, 84, 150)
GOLD = (198, 150, 44)
GREEN = (34, 110, 64)
ORANGE = (224, 122, 26)
WHITE = (250, 250, 248)

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", ".#.#.", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"],
    "3": [".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".....", ".##..", ".#..."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "'": [".##..", ".##..", ".#...", ".....", ".....", ".....", "....."],
    ":": [".....", ".##..", ".##..", ".....", ".....", ".##..", ".##.."],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def frame(self, x, y, w, h, color, t=3):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=2):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d2 <= r * r:
                    self.set(xx, yy, color)
                if not fill and r * r - 2 * r <= d2 <= r * r:
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def text_c(self, cx, y, s, scale, color):
        return self.text(cx - self.text_w(s, scale) // 2, y, s, scale, color)


def star(cv, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    for yy in range(int(cy - r), int(cy + r) + 1):
        for xx in range(int(cx - r), int(cx + r) + 1):
            inside = False
            j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > yy) != (yj > yy) and \
                        xx < (xj - xi) * (yy - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                cv.set(xx, yy, color)


def union_jack(cv, x, y, w, h):
    cv.rect(x, y, w, h, BLUE)
    # white diagonals
    cv.line(x, y, x + w, y + h, WHITE, 10)
    cv.line(x + w, y, x, y + h, WHITE, 10)
    # red diagonals (offset, simplified centred)
    cv.line(x, y, x + w, y + h, RED, 4)
    cv.line(x + w, y, x, y + h, RED, 4)
    # white cross
    cv.rect(x + w // 2 - 13, y, 26, h, WHITE)
    cv.rect(x, y + h // 2 - 13, w, 26, WHITE)
    # red cross
    cv.rect(x + w // 2 - 8, y, 16, h, RED)
    cv.rect(x, y + h // 2 - 8, w, 16, RED)
    cv.frame(x, y, w, h, INK, 2)


def eu_flag(cv, x, y, w, h):
    import math
    cv.rect(x, y, w, h, SKY)
    cx, cy = x + w // 2, y + h // 2
    r = int(h * 0.32)
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        star(cv, int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang)),
             9, GOLD)
    cv.frame(x, y, w, h, INK, 2)


def bridge_icon(cv, x, y):
    # deck and towers
    cv.rect(x, y + 58, 150, 8, INK)
    cv.rect(x + 18, y + 18, 9, 48, INK)
    cv.rect(x + 122, y + 18, 9, 48, INK)
    # suspension cables
    for t in range(0, 21):
        px = x + 22 + t * 5
        py = y + 22 + int(20 * (1 - (t / 10 - 1) ** 2)) if t <= 10 else \
            y + 22 + int(20 * (1 - ((20 - t) / 10 - 1) ** 2))
        cv.set(px, py, INK)
        cv.set(px, py + 1, INK)
    cv.line(x + 22, y + 22, x + 75, y + 56, INK, 2)
    cv.line(x + 75, y + 56, x + 126, y + 22, INK, 2)
    # explosion star above
    star(cv, x + 118, y + 2, 17, ORANGE)
    star(cv, x + 118, y + 2, 9, RED)


def chart_icon(cv, x, y):
    cv.line(x + 6, y + 6, x + 6, y + 74, INK, 3)
    cv.line(x + 6, y + 74, x + 140, y + 74, INK, 3)
    pts = [(x + 14, y + 18), (x + 48, y + 30), (x + 74, y + 24),
           (x + 104, y + 48), (x + 132, y + 62)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 5)
    # arrowhead at the end, pointing down-right
    cv.line(x + 132, y + 62, x + 116, y + 60, RED, 5)
    cv.line(x + 132, y + 62, x + 128, y + 46, RED, 5)


def globe_icon(cv, x, y):
    cx, cy, r = x + 48, y + 42, 40
    cv.circle(cx, cy, r, SKY, fill=False)
    cv.circle(cx, cy, r - 2, SKY, fill=False)
    for yy in range(cy - r, cy + r + 1):
        xx = int((r * r - (yy - cy) ** 2) ** 0.5)
        cv.set(cx - xx, yy, SKY)
        cv.set(cx + xx, yy, SKY)
    cv.line(cx - r, cy, cx + r, cy, SKY, 2)
    cv.line(cx - r, cy - 20, cx + r, cy - 20, SKY, 2)
    cv.line(cx - r, cy + 20, cx + r, cy + 20, SKY, 2)
    cv.line(cx, cy - r, cx, cy + r, SKY, 2)
    # leaf
    cv.circle(x + 112, y + 58, 11, GREEN)
    cv.line(x + 98, y + 70, x + 124, y + 44, GREEN, 3)


def medic_icon(cv, x, y):
    cv.rect(x + 8, y + 8, 76, 76, WHITE)
    cv.frame(x + 8, y + 8, 76, 76, INK, 3)
    cv.rect(x + 38, y + 24, 16, 44, RED)
    cv.rect(x + 24, y + 38, 44, 16, RED)
    # green check
    cv.line(x + 100, y + 56, x + 112, y + 68, GREEN, 6)
    cv.line(x + 112, y + 68, x + 136, y + 36, GREEN, 6)


def panel(cv, x, y, w, h, icon_fn, head, subs, head_color=INK):
    cv.frame(x, y, w, h, INK, 3)
    icon_fn(cv, x + 18, y + 16)
    hx = x + 172
    cy = y + 26
    for ln in head:
        cv.text(hx, cy, ln, 3, head_color)
        cy += 27
    sy = y + 118
    for ln in subs:
        cv.text(x + 20, sy, ln, 2, INK)
        sy += 23


def main():
    cv = Canvas(W, H, PAPER)

    # masthead
    cv.text_c(512, 34, "THE WORLD IN ONE DAY", 7, INK)
    cv.rect(36, 102, 952, 5, INK)
    cv.rect(36, 113, 952, 2, INK)
    cv.text_c(512, 126, "FRIDAY 20 NOVEMBER 2026", 3, INK)

    # lead story: UK-EU reset deal
    lx, ly, lw, lh = 36, 168, 952, 252
    cv.frame(lx, ly, lw, lh, INK, 4)
    cv.rect(lx, ly, lw, 40, BLUE)
    cv.text(lx + 18, ly + 8, "LEAD STORY - BRUSSELS", 3, WHITE)
    union_jack(cv, lx + 24, ly + 66, 128, 86)
    eu_flag(cv, lx + 168, ly + 66, 128, 86)
    cv.text(lx + 24, ly + 168, "LONDON", 2, FAINT)
    cv.text(lx + 168, ly + 168, "BRUSSELS", 2, FAINT)
    tx = lx + 330
    cv.text(tx, ly + 62, "UK AND EU SEAL", 6, INK)
    cv.text(tx, ly + 110, "RESET DEAL", 6, RED)
    subs = [
        "FOOD TRADE EASED AND CARBON",
        "MARKETS LINKED FROM 2028",
        "100,000 YOUNG PEOPLE A YEAR",
        "TO LIVE AND WORK BOTH WAYS",
    ]
    sy = ly + 164
    for ln in subs:
        cv.text(tx, sy, ln, 2, INK)
        sy += 22

    # four panels, 2 x 2
    pw, ph = 468, 218
    gx, gy = 36, 444
    gap = 16
    panel(cv, gx, gy, pw, ph, bridge_icon,
          ["RUSSIA POUNDS", "KYIV BRIDGES"],
          ["OVERNIGHT MISSILE STRIKES KILL 8",
           "AND INJURE 28 ACROSS UKRAINE",
           "TWO MISSILES AND A DRONE CROSS",
           "INTO POLISH AIRSPACE"], RED)
    panel(cv, gx + pw + gap, gy, pw, ph, chart_icon,
          ["AI FEARS HIT", "WORLD MARKETS"],
          ["TOKYO'S NIKKEI FALLS 4.8%",
           "ANTHROPIC SLIDES ON DAY TWO",
           "AFTER ITS RECORD IPO DEBUT",
           "WALL STREET DOWN A SIXTH DAY"], RED)
    panel(cv, gx, gy + ph + gap, pw, ph, globe_icon,
          ["FOSSIL FUELS", "CUT FROM DRAFT"],
          ["COP31 IN ANTALYA DROPS THE",
           "PHASE-OUT FROM THE NEW TEXT",
           "A 35% ELECTRIFICATION GOAL",
           "IS KEPT IN THE DRAFT DEAL"])
    panel(cv, gx + pw + gap, gy + ph + gap, pw, ph, medic_icon,
          ["KENYA NEARS END", "OF EBOLA FIGHT"],
          ["LAST EBOLA PATIENT DISCHARGED",
           "42-DAY COUNTDOWN TO EBOLA-FREE",
           "DECLARATION NOW BEGINS",
           "37 DAYS AFTER THE FIRST CASE"], GREEN)

    # footer ticker
    fy = gy + 2 * ph + gap + 22
    cv.rect(36, fy, 952, 3, INK)
    cv.text_c(512, fy + 14, "ALSO TODAY: VAN GOGH SELLS FOR RECORD $190.4M", 2, INK)
    cv.text_c(512, fy + 40, "SAUDI-LED COALITION STRIKES YEMEN PORT OF HODEIDAH", 2, INK)
    cv.text_c(512, fy + 72, "FIVE STORIES - ONE DAY - ONE PAGE", 2, FAINT)

    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw += cv.px[yy * W * 3:(yy + 1) * W * 3]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()
