#!/usr/bin/env python3
"""THE WORLD — Saturday 21 November 2026.

A one-day newspaper front page: 51 stories, 7 regions, 17 fields, every
story verified as having happened or first been reported on 21 November
2026 (UTC), with a printed date audit (LEFT OUT / NOT YET) for the big
stories that belong to another day.

The program is a deterministic compositor. It holds no network access and
no clocks: it decodes the PNG panels and pre-rendered text strips kept in
assets/ (photos generated for this entry; text rendered with DejaVu fonts
at build time), lays them out with the fixed operations in OPS, and writes
a single 1024x1024 PNG. Running it twice produces the same bytes.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Python 3.13, standard library only.
"""

import os
import struct
import sys
import zlib

W, H = 1024, 1024
PAPER = (247, 242, 231)

# Asset files held in this repository. Photos are the six illustrations
# generated for this entry (world map, three lead photos, trading floor,
# laboratory); text strips are transparent PNGs rendered with DejaVu
# Serif / DejaVu Sans at build time.
FILES = {
    "lead1": "assets/lead1.png",
    "lead2": "assets/lead2.png",
    "lead3": "assets/lead3.png",
    "map": "assets/map.png",
    "mini04": "assets/mini04.png",
    "mini05": "assets/mini05.png",
    "mini06": "assets/mini06.png",
    "mini07": "assets/mini07.png",
    "mini08": "assets/mini08.png",
    "mini09": "assets/mini09.png",
    "mini10": "assets/mini10.png",
    "mini11": "assets/mini11.png",
    "mini12": "assets/mini12.png",
    "mini13": "assets/mini13.png",
    "mini14": "assets/mini14.png",
    "mini15": "assets/mini15.png",
    "masthead": "assets/text/masthead.png",
    "timeline": "assets/text/timeline.png",
    "lead1_kicker": "assets/text/lead1_kicker.png",
    "lead1_head": "assets/text/lead1_head.png",
    "lead1_deck": "assets/text/lead1_deck.png",
    "lead1_tag": "assets/text/lead1_tag.png",
    "lead2_kicker": "assets/text/lead2_kicker.png",
    "lead2_head": "assets/text/lead2_head.png",
    "lead2_deck": "assets/text/lead2_deck.png",
    "lead2_tag": "assets/text/lead2_tag.png",
    "lead3_kicker": "assets/text/lead3_kicker.png",
    "lead3_head": "assets/text/lead3_head.png",
    "lead3_deck": "assets/text/lead3_deck.png",
    "lead3_tag": "assets/text/lead3_tag.png",
    "map_title": "assets/text/map_title.png",
    "map_legend": "assets/text/map_legend.png",
    "dc_title": "assets/text/dc_title.png",
    "dc_left_title": "assets/text/dc_left_title.png",
    "dc_left": "assets/text/dc_left.png",
    "dc_right_title": "assets/text/dc_right_title.png",
    "dc_right": "assets/text/dc_right.png",
    "mini04_head": "assets/text/mini04_head.png",
    "mini04_tag": "assets/text/mini04_tag.png",
    "mini05_head": "assets/text/mini05_head.png",
    "mini05_tag": "assets/text/mini05_tag.png",
    "mini06_head": "assets/text/mini06_head.png",
    "mini06_tag": "assets/text/mini06_tag.png",
    "mini07_head": "assets/text/mini07_head.png",
    "mini07_tag": "assets/text/mini07_tag.png",
    "mini08_head": "assets/text/mini08_head.png",
    "mini08_tag": "assets/text/mini08_tag.png",
    "mini09_head": "assets/text/mini09_head.png",
    "mini09_tag": "assets/text/mini09_tag.png",
    "mini10_head": "assets/text/mini10_head.png",
    "mini10_tag": "assets/text/mini10_tag.png",
    "mini11_head": "assets/text/mini11_head.png",
    "mini11_tag": "assets/text/mini11_tag.png",
    "mini12_head": "assets/text/mini12_head.png",
    "mini12_tag": "assets/text/mini12_tag.png",
    "mini13_head": "assets/text/mini13_head.png",
    "mini13_tag": "assets/text/mini13_tag.png",
    "mini14_head": "assets/text/mini14_head.png",
    "mini14_tag": "assets/text/mini14_tag.png",
    "mini15_head": "assets/text/mini15_head.png",
    "mini15_tag": "assets/text/mini15_tag.png",
    "index_head": "assets/text/index_head.png",
    "index_col0": "assets/text/index_col0.png",
    "index_col1": "assets/text/index_col1.png",
    "index_col2": "assets/text/index_col2.png",
    "markets": "assets/text/markets.png",
    "footer": "assets/text/footer.png",
    "dot01": "assets/text/dot01.png",
    "dot02": "assets/text/dot02.png",
    "dot03": "assets/text/dot03.png",
    "dot07": "assets/text/dot07.png",
    "dot09": "assets/text/dot09.png",
    "dot10": "assets/text/dot10.png",
    "dot12": "assets/text/dot12.png",
    "dot13": "assets/text/dot13.png",
    "dot14": "assets/text/dot14.png",
    "dot15": "assets/text/dot15.png",
    "dot31": "assets/text/dot31.png",
    "dot32": "assets/text/dot32.png",
    "dot33": "assets/text/dot33.png",
}

# Fixed layout. Ops: ["bg", rgb] | ["paste", key, x, y] |
# ["line", x0, y0, x1, y1, rgb, width] |
# ["fill", x, y, w, h, rgb] | ["outline", x, y, w, h, rgb]
# Coordinates are in the 1024x1024 page; the masthead is at the top,
# the three leads below the UTC timeline, the world map and the DATE
# CHECK box in the middle, twelve illustrated minis, the 36-line index,
# and the markets strip and source footer at the bottom.
OPS = [
    ["bg", (247, 242, 231)],
    ["paste", "masthead", 24, 6],
    ["line", 24, 98, 1000, 98, (26, 26, 26), 2],
    ["line", 24, 101, 1000, 101, (26, 26, 26), 1],
    ["paste", "timeline", 24, 106],
    ["line", 24, 134, 1000, 134, (26, 26, 26), 1],
    ["paste", "lead1", 24, 140],
    ["outline", 23, 139, 319, 142, (26, 26, 26)],
    ["paste", "lead1_kicker", 24, 284],
    ["paste", "lead1_head", 24, 298],
    ["paste", "lead1_deck", 24, 366],
    ["paste", "lead1_tag", 24, 424],
    ["paste", "lead2", 353, 140],
    ["outline", 352, 139, 319, 142, (26, 26, 26)],
    ["paste", "lead2_kicker", 353, 284],
    ["paste", "lead2_head", 353, 298],
    ["paste", "lead2_deck", 353, 366],
    ["paste", "lead2_tag", 353, 424],
    ["paste", "lead3", 682, 140],
    ["outline", 681, 139, 319, 142, (26, 26, 26)],
    ["paste", "lead3_kicker", 682, 284],
    ["paste", "lead3_head", 682, 298],
    ["paste", "lead3_deck", 682, 366],
    ["paste", "lead3_tag", 682, 424],
    ["line", 24, 442, 1000, 442, (26, 26, 26), 1],
    ["fill", 24, 448, 620, 16, (20, 33, 61)],
    ["paste", "map_title", 24, 448],
    ["paste", "map", 24, 466],
    ["paste", "map_legend", 24, 656],
    ["paste", "dot01", 369, 499],
    ["paste", "dot02", 176, 577],
    ["paste", "dot03", 355, 515],
    ["paste", "dot07", 349, 472],
    ["paste", "dot09", 316, 469],
    ["paste", "dot10", 181, 491],
    ["paste", "dot12", 593, 642],
    ["paste", "dot13", 377, 515],
    ["paste", "dot14", 500, 567],
    ["paste", "dot15", 129, 507],
    ["paste", "dot31", 345, 588],
    ["paste", "dot32", 535, 499],
    ["paste", "dot33", 527, 543],
    ["outline", 656, 448, 344, 222, (163, 22, 33)],
    ["fill", 656, 448, 344, 16, (163, 22, 33)],
    ["paste", "dc_title", 664, 448],
    ["paste", "dc_left_title", 664, 472],
    ["paste", "dc_left", 664, 486],
    ["paste", "dc_right_title", 664, 566],
    ["paste", "dc_right", 664, 580],
    ["paste", "mini04", 24, 676],
    ["paste", "mini04_tag", 24, 722],
    ["paste", "mini04_head", 24, 733],
    ["paste", "mini05", 187, 676],
    ["paste", "mini05_tag", 187, 722],
    ["paste", "mini05_head", 187, 733],
    ["paste", "mini06", 350, 676],
    ["paste", "mini06_tag", 350, 722],
    ["paste", "mini06_head", 350, 733],
    ["paste", "mini07", 513, 676],
    ["paste", "mini07_tag", 513, 722],
    ["paste", "mini07_head", 513, 733],
    ["paste", "mini08", 676, 676],
    ["paste", "mini08_tag", 676, 722],
    ["paste", "mini08_head", 676, 733],
    ["paste", "mini09", 839, 676],
    ["paste", "mini09_tag", 839, 722],
    ["paste", "mini09_head", 839, 733],
    ["paste", "mini10", 24, 766],
    ["paste", "mini10_tag", 24, 812],
    ["paste", "mini10_head", 24, 823],
    ["paste", "mini11", 187, 766],
    ["paste", "mini11_tag", 187, 812],
    ["paste", "mini11_head", 187, 823],
    ["paste", "mini12", 350, 766],
    ["paste", "mini12_tag", 350, 812],
    ["paste", "mini12_head", 350, 823],
    ["paste", "mini13", 513, 766],
    ["paste", "mini13_tag", 513, 812],
    ["paste", "mini13_head", 513, 823],
    ["paste", "mini14", 676, 766],
    ["paste", "mini14_tag", 676, 812],
    ["paste", "mini14_head", 676, 823],
    ["paste", "mini15", 839, 766],
    ["paste", "mini15_tag", 839, 812],
    ["paste", "mini15_head", 839, 823],
    ["paste", "index_head", 24, 862],
    ["paste", "index_col0", 24, 876],
    ["paste", "index_col1", 353, 876],
    ["paste", "index_col2", 682, 876],
    ["line", 347, 876, 347, 991, (200, 192, 172), 1],
    ["line", 676, 876, 676, 991, (200, 192, 172), 1],
    ["line", 24, 996, 1000, 996, (26, 26, 26), 1],
    ["paste", "markets", 24, 998],
    ["paste", "footer", 24, 1013],
]


def _chunk(data, off):
    length = struct.unpack(">I", data[off:off + 4])[0]
    ctype = data[off + 4:off + 8]
    return ctype, data[off + 8:off + 8 + length], off + 12 + length


def read_png(path):
    """Decode an 8-bit non-interlaced PNG (colour types 2 and 6).

    Returns (width, height, rgba_bytes)."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG: %s" % path)
    off = 8
    width = height = bit_depth = color_type = None
    idat = bytearray()
    while off < len(data):
        ctype, chunk, off = _chunk(data, off)
        if ctype == b"IHDR":
            (width, height, bit_depth, color_type,
             _comp, _filt, interlace) = struct.unpack(">IIBBBBB", chunk)
            if bit_depth != 8:
                raise ValueError("only 8-bit PNGs: %s" % path)
            if color_type not in (2, 6):
                raise ValueError("only RGB/RGBA PNGs: %s" % path)
            if interlace != 0:
                raise ValueError("only non-interlaced PNGs: %s" % path)
        elif ctype == b"IDAT":
            idat += chunk
        elif ctype == b"IEND":
            break
    if width is None:
        raise ValueError("no IHDR: %s" % path)
    bpp = 3 if color_type == 2 else 4
    raw = zlib.decompress(bytes(idat))
    stride = width * bpp
    if len(raw) != (stride + 1) * height:
        raise ValueError("bad IDAT length: %s" % path)
    out = bytearray(width * height * 4)
    prev = bytearray(stride)
    pos = 0
    for y in range(height):
        ftype = raw[pos]
        pos += 1
        row = bytearray(raw[pos:pos + stride])
        pos += stride
        if ftype == 0:
            pass
        elif ftype == 1:
            for i in range(bpp, stride):
                row[i] = (row[i] + row[i - bpp]) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                row[i] = (row[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                left = row[i - bpp] if i >= bpp else 0
                row[i] = (row[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                a = row[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
                row[i] = (row[i] + pr) & 0xFF
        else:
            raise ValueError("unknown PNG filter %d: %s" % (ftype, path))
        prev = row
        base = y * width * 4
        if bpp == 4:
            out[base:base + width * 4] = row
        else:
            for x in range(width):
                o = base + x * 4
                s = x * 3
                out[o] = row[s]
                out[o + 1] = row[s + 1]
                out[o + 2] = row[s + 2]
                out[o + 3] = 255
    return width, height, bytes(out)


def write_png(path, width, height, rgb):
    """Write an RGB PNG with fixed settings (filter 0, zlib level 6)."""
    def chunk(ctype, payload):
        out = struct.pack(">I", len(payload)) + ctype + payload
        return out + struct.pack(">I", zlib.crc32(ctype + payload) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    blob = b"\x89PNG\r\n\x1a\n"
    blob += chunk(b"IHDR", ihdr)
    blob += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    blob += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(blob)


class Canvas:
    def __init__(self, width, height, rgb):
        self.w = width
        self.h = height
        self.px = bytearray(rgb * width * height)

    def set(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.px[o:o + 3] = bytes(rgb)

    def fill(self, x, y, w, h, rgb):
        for yy in range(y, y + h):
            if 0 <= yy < self.h:
                for xx in range(x, x + w):
                    if 0 <= xx < self.w:
                        self.set(xx, yy, rgb)

    def outline(self, x, y, w, h, rgb):
        self.fill(x, y, w, 1, rgb)
        self.fill(x, y + h - 1, w, 1, rgb)
        self.fill(x, y, 1, h, rgb)
        self.fill(x + w - 1, y, 1, h, rgb)

    def line(self, x0, y0, x1, y1, rgb, width):
        if y0 == y1:
            for dy in range(width):
                self.fill(min(x0, x1), y0 + dy, abs(x1 - x0) + 1, 1, rgb)
        elif x0 == x1:
            for dx in range(width):
                self.fill(x0 + dx, min(y0, y1), 1, abs(y1 - y0) + 1, rgb)
        else:
            raise ValueError("only axis-aligned lines are used")

    def paste(self, img_w, img_h, rgba, dx, dy):
        for y in range(img_h):
            py = dy + y
            if py < 0 or py >= self.h:
                continue
            for x in range(img_w):
                px = dx + x
                if px < 0 or px >= self.w:
                    continue
                s = (y * img_w + x) * 4
                a = rgba[s + 3]
                if a == 0:
                    continue
                o = (py * self.w + px) * 3
                if a == 255:
                    self.px[o] = rgba[s]
                    self.px[o + 1] = rgba[s + 1]
                    self.px[o + 2] = rgba[s + 2]
                else:
                    inv = 255 - a
                    self.px[o] = (rgba[s] * a + self.px[o] * inv) // 255
                    self.px[o + 1] = (rgba[s + 1] * a + self.px[o + 1] * inv) // 255
                    self.px[o + 2] = (rgba[s + 2] * a + self.px[o + 2] * inv) // 255


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    canvas = Canvas(W, H, PAPER)
    cache = {}
    for op in OPS:
        kind = op[0]
        if kind == "bg":
            canvas.fill(0, 0, W, H, tuple(op[1]))
        elif kind == "paste":
            key, x, y = op[1], op[2], op[3]
            if key not in cache:
                cache[key] = read_png(os.path.join(here, FILES[key]))
            w, h, rgba = cache[key]
            canvas.paste(w, h, rgba, x, y)
        elif kind == "line":
            canvas.line(op[1], op[2], op[3], op[4], tuple(op[5]), op[6])
        elif kind == "fill":
            canvas.fill(op[1], op[2], op[3], op[4], tuple(op[5]))
        elif kind == "outline":
            canvas.outline(op[1], op[2], op[3], op[4], tuple(op[5]))
        else:
            raise ValueError("unknown op %r" % (op,))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    write_png(out_path, W, H, bytes(canvas.px))
    print("wrote %s (%dx%d)" % (out_path, W, H))


if __name__ == "__main__":
    sys.exit(main())
