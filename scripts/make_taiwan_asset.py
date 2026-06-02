#!/usr/bin/env python
"""Generate a small bitmap asset for the public directory header."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/msjhbd.ttc" if bold else "C:/Windows/Fonts/msjh.ttc",
        "C:/Windows/Fonts/NotoSansTC-Regular.otf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def main() -> int:
    out = Path("public/assets/taiwan-welfare-map.png")
    out.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (960, 720), "#eef5f1")
    draw = ImageDraw.Draw(img)

    # Abstract Taiwan silhouette, intentionally simple and locally generated.
    island = [
        (548, 72), (607, 117), (637, 188), (625, 269), (661, 341),
        (628, 435), (581, 507), (557, 611), (493, 661), (433, 624),
        (412, 544), (362, 489), (379, 407), (338, 324), (375, 250),
        (394, 169), (458, 112)
    ]
    draw.polygon(island, fill="#ffffff", outline="#006c67")
    draw.line(island + [island[0]], fill="#006c67", width=5)

    pins = [
        (472, 155, "#b87912", "北"),
        (456, 302, "#006c67", "中"),
        (502, 471, "#9c3157", "南"),
        (575, 357, "#2e5f8a", "東"),
    ]
    for x, y, color, label in pins:
        draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=color)
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill="#ffffff")
        draw.text((x + 34, y - 20), label, fill=color, font=font(32, bold=True))

    draw.rounded_rectangle((48, 64, 360, 288), radius=18, fill="#ffffff", outline="#d9dfd8", width=2)
    draw.text((78, 94), "社福資源", fill="#18211f", font=font(42, bold=True))
    draw.text((78, 154), "找得到", fill="#006c67", font=font(34, bold=True))
    draw.text((78, 202), "查得到", fill="#b87912", font=font(34, bold=True))
    draw.text((78, 250), "追得到更新", fill="#9c3157", font=font(30, bold=True))

    draw.rounded_rectangle((620, 560, 902, 654), radius=14, fill="#fff3d8", outline="#e5c477", width=2)
    draw.text((646, 584), "Dec-Jan", fill="#6f4607", font=font(28, bold=True))
    draw.text((646, 620), "跨年度密集檢查", fill="#6f4607", font=font(24, bold=True))

    img.save(out, "PNG", optimize=True)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
