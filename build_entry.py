"""Builds entry.png: one image summing up the world news of Saturday 21 November 2026.

Four editorial illustrations (made with an image model, one per story) are laid out in a
2x2 grid under a date banner, each with a short caption bar drawn here so the words are
crisp and exact:

  - Shenzhen: the US, Chinese and Russian leaders meet and issue a joint declaration
  - a Russian missile comes down in Poland during the strikes on Ukraine
  - the World Court (ICJ) finds Myanmar committed genocide against the Rohingya
  - COP31 climate talks run on with no agreement in sight

Output: entry.png (JPEG bytes, as the rules allow: the format is told by its first
bytes), 1024 x 1024, well under the 1 MiB cap.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
NAVY = (13, 24, 48)
CREAM = (244, 236, 216)
RED = (216, 64, 62)
TEAL = (38, 148, 164)

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

HEADER_H = 148
GUTTER = 12
CAPTION_H = 78

STORIES = [
    ("panels/summit.jpg", ["SHENZHEN SUMMIT", "US · CHINA · RUSSIA LEADERS MEET"]),
    ("panels/missile.jpg", ["RUSSIAN MISSILE", "LANDS IN POLAND"]),
    ("panels/court.jpg", ["WORLD COURT RULES", "MYANMAR GENOCIDE OF ROHINGYA"]),
    ("panels/climate.jpg", ["COP31 CLIMATE TALKS", "DEADLOCKED, NO DEAL IN SIGHT"]),
]


def cover_crop(img, target_w, target_h):
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    x = (resized.width - target_w) // 2
    y = (resized.height - target_h) // 2
    return resized.crop((x, y, x + target_w, y + target_h))


def centred(draw, cx, y, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((cx - (box[2] - box[0]) / 2, y), text, font=font, fill=fill)


def main():
    canvas = Image.new("RGB", (W, W), NAVY)
    draw = ImageDraw.Draw(canvas)

    # Header: kicker, the date, and a red rule.
    kicker_font = ImageFont.truetype(FONT, 27)
    date_font = ImageFont.truetype(FONT, 55)
    centred(draw, W / 2, 16, "T H E   W O R L D   I N   O N E   D A Y", kicker_font, RED)
    centred(draw, W / 2, 52, "SATURDAY 21 NOVEMBER 2026", date_font, CREAM)
    draw.rectangle([GUTTER, HEADER_H - 12, W - GUTTER, HEADER_H - 7], fill=RED)

    cell_w = (W - GUTTER * 3) // 2
    grid_h = W - HEADER_H - GUTTER
    cell_h = (grid_h - GUTTER) // 2
    img_h = cell_h - CAPTION_H

    caption_font = ImageFont.truetype(FONT, 25)
    for i, (path, lines) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = GUTTER + col * (cell_w + GUTTER)
        y = HEADER_H + row * (cell_h + GUTTER)
        panel = Image.open(path).convert("RGB")
        canvas.paste(cover_crop(panel, cell_w, img_h), (x, y))
        bar_y = y + img_h
        draw.rectangle([x, bar_y, x + cell_w, bar_y + CAPTION_H], fill=NAVY)
        draw.rectangle([x, bar_y, x + cell_w, bar_y + 3], fill=TEAL)
        line_y = bar_y + 10
        for line in lines:
            centred(draw, x + cell_w / 2, line_y, line, caption_font, CREAM)
            line_y += 30

    canvas.save("entry.png", "JPEG", quality=88)
    print("wrote entry.png", canvas.size)


if __name__ == "__main__":
    main()
