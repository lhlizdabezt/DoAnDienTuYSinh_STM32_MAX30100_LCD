from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
GIF_PATH = ASSETS / "pulse-wave.gif"
PREVIEW_PATH = ASSETS / "pulse-wave-preview.png"

W, H = 960, 360
FRAME_COUNT = 42


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONT_TITLE = font(34, True)
FONT_SUB = font(20)
FONT_LABEL = font(18, True)
FONT_SMALL = font(15)
FONT_LCD = font(30, True)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient_background() -> Image.Image:
    img = Image.new("RGB", (W, H), "#0f172a")
    px = img.load()
    for y in range(H):
        for x in range(W):
            tx = x / (W - 1)
            ty = y / (H - 1)
            mix = min(1.0, 0.68 * tx + 0.46 * ty)
            r = lerp(12, 15, mix)
            g = lerp(24, 118, mix)
            b = lerp(45, 110, mix)
            px[x, y] = (r, g, b)
    return img


def round_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    for x in range(0, W, 48):
        draw.line((x, 0, x, H), fill=(125, 211, 252, 28), width=1)
    for y in range(0, H, 40):
        draw.line((0, y, W, y), fill=(125, 211, 252, 24), width=1)


def pulse_points(phase: float) -> list[tuple[int, int]]:
    base_y = 226
    pts: list[tuple[int, int]] = []
    for i in range(0, 560, 8):
        x = 286 + i
        t = (i / 560 + phase) % 1
        y = base_y + 8 * math.sin(2 * math.pi * (t * 3.2))
        for center, amp, width in [(0.16, -78, 0.014), (0.20, 54, 0.018), (0.35, -38, 0.020), (0.58, -88, 0.012), (0.63, 62, 0.018), (0.80, -34, 0.018)]:
            y += amp * math.exp(-((t - center) ** 2) / (2 * width**2))
        pts.append((x, int(y)))
    return pts


def frame(idx: int) -> Image.Image:
    phase = idx / FRAME_COUNT
    img = gradient_background().convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_grid(draw)

    draw.text((40, 38), "Đồ án Điện tử Y sinh STM32", font=FONT_TITLE, fill="#ffffff")
    draw.text((42, 84), "MAX30100/MAX30102 đo BPM, SpO2 và hiển thị LCD1602", font=FONT_SUB, fill="#cffafe")

    round_rect(draw, (42, 132, 240, 294), 22, "#0b1220", "#38bdf8", 3)
    round_rect(draw, (66, 158, 216, 222), 10, "#d8f3dc", None)
    bpm = 76 + int(3 * math.sin(2 * math.pi * phase))
    spo2 = 97 + int(1.5 * math.sin(2 * math.pi * (phase + 0.25)))
    draw.text((82, 172), f"BPM {bpm:03d}", font=FONT_LCD, fill="#0f172a")
    draw.text((82, 205), f"SpO2 {spo2}%", font=FONT_SMALL, fill="#0f766e")
    beat_r = 8 + int(6 * (0.5 + 0.5 * math.sin(2 * math.pi * phase)))
    draw.ellipse((146 - beat_r, 252 - beat_r, 146 + beat_r, 252 + beat_r), fill="#22c55e")
    draw.text((72, 270), "LCD1602 4-bit", font=FONT_SMALL, fill="#bae6fd")

    pts = pulse_points(phase)
    for width, color in [(10, (20, 184, 166, 80)), (5, (248, 250, 252, 255))]:
        draw.line(pts, fill=color, width=width, joint="curve")
    for x, y in pts[::10]:
        if (x // 10 + idx) % 11 == 0:
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill="#f97316")

    chips = [
        ("STM32F103C8T6", 292, 112, 172, "#2563eb"),
        ("I2C", 486, 112, 66, "#0f766e"),
        ("MAX30100 / MAX30102", 574, 112, 228, "#d95319"),
        ("Serial1 log", 824, 112, 124, "#334155"),
    ]
    for text, x, y, w, color in chips:
        round_rect(draw, (x, y, x + w, y + 42), 18, color, None)
        tw = draw.textlength(text, font=FONT_LABEL)
        draw.text((x + (w - tw) / 2, y + 12), text, font=FONT_LABEL, fill="#ffffff")

    draw.text((294, 300), "Kiểm chứng: cảm biến -> I2C -> firmware -> LCD", font=FONT_LABEL, fill="#ffffff")
    draw.text((294, 324), "Bằng chứng: video demo, Proteus, release assets.", font=FONT_SMALL, fill="#cffafe")
    draw.text((646, 324), "Không thay thế thiết bị y tế được kiểm định.", font=FONT_SMALL, fill="#cffafe")

    return Image.alpha_composite(img, overlay).convert("P", palette=Image.Palette.ADAPTIVE, colors=128)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    frames = [frame(i) for i in range(FRAME_COUNT)]
    frames[0].save(PREVIEW_PATH)
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"wrote {GIF_PATH}")
    print(f"wrote {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
