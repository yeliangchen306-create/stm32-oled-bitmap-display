"""Convert black line art on a white background to SSD1306 page data."""

import argparse
from pathlib import Path

from PIL import Image, ImageOps


WIDTH = 128
HEIGHT = 64


def convert(source: Path, threshold: int, invert: bool):
    image = Image.open(source).convert("L")
    image.thumbnail((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    canvas = Image.new("L", (WIDTH, HEIGHT), 255)
    x = (WIDTH - image.width) // 2
    y = (HEIGHT - image.height) // 2
    canvas.paste(image, (x, y))

    if invert:
        canvas = ImageOps.invert(canvas)

    # Default: dark lines become lit OLED pixels.
    lit = canvas.point(lambda value: 255 if value < threshold else 0, mode="1")

    data = []
    pixels = lit.load()
    for page in range(HEIGHT // 8):
        for column in range(WIDTH):
            value = 0
            for bit in range(8):
                if pixels[column, page * 8 + bit]:
                    value |= 1 << bit
            data.append(value)

    return data, lit


def write_array(output: Path, data):
    lines = [
        "static const uint8_t CartoonBitmap[1024] =",
        "{",
    ]
    for page in range(8):
        lines.append(f"    /* Page {page} */")
        for start in range(0, 128, 16):
            row = data[page * 128 + start : page * 128 + start + 16]
            lines.append("    " + ", ".join(f"0x{value:02X}" for value in row) + ",")
    lines.append("};")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Convert an image to a 128x64 OLED C array")
    parser.add_argument("input", type=Path, help="input image")
    parser.add_argument("output", type=Path, help="output text file")
    parser.add_argument("--threshold", type=int, default=190, help="black/white threshold (0-255)")
    parser.add_argument("--invert", action="store_true", help="invert source before conversion")
    args = parser.parse_args()

    if not 0 <= args.threshold <= 255:
        parser.error("--threshold must be between 0 and 255")

    data, preview = convert(args.input, args.threshold, args.invert)
    write_array(args.output, data)

    preview_path = args.output.with_name(args.output.stem + "_preview.png")
    preview.resize((WIDTH * 6, HEIGHT * 6), Image.Resampling.NEAREST).save(preview_path)
    print(f"Wrote {len(data)} bytes to {args.output}")
    print(f"Preview: {preview_path}")


if __name__ == "__main__":
    main()

