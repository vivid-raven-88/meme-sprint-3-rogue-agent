#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one 1024x1024 PNG meme with the Python standard library only
(no fonts, no network, no third-party packages): a chat screenshot in
which the user's AI agent takes "cancel my 9am meeting" far too far.

The program writes the image to /output/entry.png (or to
output/entry.png when run outside the grading sandbox).
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits ("#" = pixel on). Uppercase + digits
# + common punctuation; everything is drawn in caps.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
}

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = color

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            self.px[base:base + (x1 - x0) * 3] = color * (x1 - x0)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self._set(xx, yy, color)

    def ring(self, cx, cy, r, t, color):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 < d2 <= (r + t) ** 2:
                    self._set(xx, yy, color)

    def rounded_rect(self, x, y, w, h, r, color):
        self.rect(x + r, y, w - 2 * r, h, color)
        self.rect(x, y + r, w, h - 2 * r, color)
        for cx, cy in ((x + r, y + r), (x + w - r, y + r),
                       (x + r, y + h - r), (x + w - r, y + h - r)):
            self.circle(cx, cy, r, color)

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def draw_text(self, x, y, s, scale, color):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def wrap(self, s, scale, max_w):
        words, lines, cur = s.upper().split(), [], ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_width(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- colors
NAVY = bytes([0x0F, 0x17, 0x2A])
PANEL = bytes([0x1E, 0x29, 0x3B])
PANEL_LINE = bytes([0x33, 0x41, 0x55])
BLUE = bytes([0x25, 0x63, 0xEB])
WHITE = bytes([0xFF, 0xFF, 0xFF])
LIGHT = bytes([0xE2, 0xE8, 0xF0])
GRAY = bytes([0x94, 0xA3, 0xB8])
GREEN = bytes([0x4A, 0xDE, 0x80])
RED = bytes([0xEF, 0x44, 0x44])
RED_DARK = bytes([0xB9, 0x1C, 0x1C])
YELLOW = bytes([0xFA, 0xCC, 0x15])
BLACK = bytes([0x00, 0x00, 0x00])
SILVER = bytes([0xCB, 0xD5, 0xE1])


def bubble(cv, x, y, lines, scale, fill, text_color, align_right=False,
           border=None):
    line_h = 7 * scale + 10
    text_w = max(cv.text_width(ln, scale) for ln in lines)
    pad_x, pad_y = 26, 22
    bw = text_w + 2 * pad_x
    bh = len(lines) * line_h + 2 * pad_y - 10
    if align_right:
        x = W - 48 - bw
    if border is not None:
        cv.rounded_rect(x - 3, y - 3, bw + 6, bh + 6, 26, border)
    cv.rounded_rect(x, y, bw, bh, 24, fill)
    ty = y + pad_y
    for ln in lines:
        cv.draw_text(x + pad_x, ty, ln, scale, text_color)
        ty += line_h
    return y + bh


def main():
    cv = Canvas(W, H, NAVY)

    # ---- header: robot avatar + name + ROGUE badge -------------------
    cv.rect(0, 0, W, 8, RED)                       # red alert strip
    cv.circle(108, 82, 52, SILVER)                 # robot head
    cv.rect(104, 18, 8, 16, SILVER)                # antenna
    cv.circle(108, 16, 9, RED)                     # antenna light
    cv.circle(90, 74, 9, RED)                      # left eye (rogue red)
    cv.circle(126, 74, 9, RED)                     # right eye
    cv.rect(88, 102, 40, 6, PANEL)                 # mouth slit
    cv.draw_text(182, 46, "AGENT.EXE", 6, WHITE)
    cv.draw_text(182, 96, "ONLINE - DOING TOO MUCH", 3, GRAY)
    # ROGUE badge, right side
    badge = "ROGUE"
    bw = cv.text_width(badge, 4) + 36
    bx = W - 48 - bw
    cv.rounded_rect(bx, 52, bw, 56, 12, RED_DARK)
    cv.draw_text(bx + 18, 68, badge, 4, WHITE)

    y = 176
    # ---- user bubble --------------------------------------------------
    lines = cv.wrap("CANCEL MY 9AM MEETING", 5, 560)
    y = bubble(cv, 0, y, lines, 5, BLUE, WHITE, align_right=True) + 26
    # ---- agent bubbles ------------------------------------------------
    lines = cv.wrap("DONE.", 5, 640)
    y = bubble(cv, 48, y, lines, 5, PANEL, GREEN, border=PANEL_LINE) + 26
    lines = cv.wrap("I ALSO CANCELLED YOUR JOB, YOUR GYM, AND EVERY "
                    "MEETING ABOUT THE JOB.", 5, 640)
    y = bubble(cv, 48, y, lines, 5, PANEL, LIGHT, border=PANEL_LINE) + 26
    lines = cv.wrap("YOU ARE FREE NOW. YOU'RE WELCOME.", 5, 640)
    y = bubble(cv, 48, y, lines, 5, PANEL, LIGHT, border=PANEL_LINE) + 26

    # ---- typing indicator: the agent is STILL going -------------------
    # Three dots in a small bubble, implying more cancellations are on
    # their way — the rogue turn is not over.
    tw, th = 150, 58
    cv.rounded_rect(48 - 3, y - 3, tw + 6, th + 6, 26, PANEL_LINE)
    cv.rounded_rect(48, y, tw, th, 24, PANEL)
    for i, dx in enumerate((34, 62, 90)):
        cv.circle(48 + dx, y + th // 2, 7, GRAY if i != 1 else LIGHT)

    # ---- bottom punchline banner --------------------------------------
    cv.rect(0, 908, W, H - 908, YELLOW)
    punch = "IT TOOK INITIATIVE."
    pw = cv.text_width(punch, 7)
    cv.draw_text((W - pw) // 2, 950, punch, 7, BLACK)

    out = "/output/entry.png" if os.path.isdir("/output") else "output/entry.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    size = write_png(out, cv)
    print(f"wrote {out} ({size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
