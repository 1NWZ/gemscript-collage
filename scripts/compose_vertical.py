#!/usr/bin/env python3
"""Stack a 3:2 GemScript effect above a focal crop of the real source photo."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from PIL import Image, ImageOps


def crop_3x2(image: Image.Image, focus_x: float, focus_y: float) -> Image.Image:
    width, height = image.size
    if width / height > 1.5:
        crop_h = height
        crop_w = round(height * 1.5)
    else:
        crop_w = width
        crop_h = round(width / 1.5)

    center_x = focus_x * width
    center_y = focus_y * height
    left = min(max(round(center_x - crop_w / 2), 0), width - crop_w)
    top = min(max(round(center_y - crop_h / 2), 0), height - crop_h)
    return image.crop((left, top, left + crop_w, top + crop_h))


def open_rgb(path: Path) -> Image.Image:
    image = ImageOps.exif_transpose(Image.open(path))
    if image.mode == "RGBA":
        background = Image.new("RGBA", image.size, "white")
        image = Image.alpha_composite(background, image)
    return image.convert("RGB")


def compose(effect: Path, original: Path, output: Path, width: int, focus_x: float, focus_y: float, force: bool) -> None:
    if output.suffix.lower() != ".png":
        raise ValueError("Output must use a .png extension")
    if output.exists() and not force:
        raise FileExistsError(f"Output already exists: {output}; use --force to replace it")
    if width < 300:
        raise ValueError("Width must be at least 300 pixels")
    if not 0 <= focus_x <= 1 or not 0 <= focus_y <= 1:
        raise ValueError("Focus coordinates must be between 0 and 1")

    half_height = round(width / 1.5)
    size = (width, half_height)
    effect_image = crop_3x2(open_rgb(effect), 0.5, 0.5).resize(size, Image.Resampling.LANCZOS)
    original_image = crop_3x2(open_rgb(original), focus_x, focus_y).resize(size, Image.Resampling.LANCZOS)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (width, half_height * 2), "white")
    canvas.paste(effect_image, (0, 0))
    canvas.paste(original_image, (0, half_height))
    canvas.save(output, "PNG", optimize=True)


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        effect = root / "effect.png"
        original = root / "original.png"
        output = root / "final.png"
        Image.new("RGB", (900, 600), "red").save(effect)
        Image.new("RGB", (600, 900), "blue").save(original)
        compose(effect, original, output, 600, 0.5, 0.5, False)
        result = Image.open(output)
        assert result.size == (600, 800)
        assert result.getpixel((300, 100)) == (255, 0, 0)
        assert result.getpixel((300, 700)) == (0, 0, 255)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--effect", type=Path)
    parser.add_argument("--original", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--width", type=int, default=1536)
    parser.add_argument("--focus-x", type=float, default=0.5)
    parser.add_argument("--focus-y", type=float, default=0.5)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("self-test passed")
        return
    if not args.effect or not args.original or not args.output:
        parser.error("--effect, --original, and --output are required")
    compose(args.effect, args.original, args.output, args.width, args.focus_x, args.focus_y, args.force)
    print(args.output)


if __name__ == "__main__":
    main()
