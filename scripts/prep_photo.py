#!/usr/bin/env python3
"""
scripts/prep_photo.py

Pipeline for photo-to-ASCII processing.
Converts high-contrast portrait photos into stylized, monochrome terminal ASCII art.

Guidelines:
- Stylized, monochrome, restrained, high-contrast, terminal-compatible
- NOT photorealistic, NOT a social media avatar
- Visual secondary element to engineering identity
- Outputs clean ASCII text suitable for embed into SVGs or README
"""

import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

ASCII_RAMP_DARK_TO_LIGHT = " .:-=+*#%@"
ASCII_RAMP_HIGH_CONTRAST = "  .:-=+#@"


def process_photo_to_ascii(
    image_path: Optional[Path] = None,
    target_width: int = 60,
    aspect_ratio_correction: float = 0.55
) -> str:
    """
    Converts an input image file into a restrained ASCII text string.
    If image_path is None or file does not exist, returns the default identity ASCII block.
    """
    if image_path is None or not image_path.exists():
        return (
            "  ██╗  ██╗███████╗███╗   ██╗██╗██╗     ██╗      ██████╗ ██╗     \n"
            "  ██║  ██║██╔════╝████╗  ██║██║██║     ██║     ██╔═══██╗██║     \n"
            "  ███████║█████╗  ██╔██╗ ██║██║██║     ██║     ██║   ██║██║     \n"
            "  ██╔══██║██╔══╝  ██║╚██╗██║██║██║     ██║     ██║   ██║██║     \n"
            "  ██║  ██║███████╗██║ ╚████║██║███████╗███████╗╚██████╔╝███████╗\n"
            "  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝\n"
        )

    try:
        from PIL import Image
    except ImportError:
        print("[!] Pillow library not installed. Using standard ASCII identity stub.", file=sys.stderr)
        return process_photo_to_ascii(None, target_width, aspect_ratio_correction)

    try:
        with Image.open(image_path) as img:
            img = img.convert("L")
            w, h = img.size
            target_height = int((h / w) * target_width * aspect_ratio_correction)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            pixels = img.getdata()
            ramp_len = len(ASCII_RAMP_HIGH_CONTRAST)
            
            ascii_lines = []
            for y in range(target_height):
                line = []
                for x in range(target_width):
                    pixel_val = pixels[y * target_width + x]
                    char_idx = int((pixel_val / 255.0) * (ramp_len - 1))
                    line.append(ASCII_RAMP_HIGH_CONTRAST[char_idx])
                ascii_lines.append("".join(line))
                
            return "\n".join(ascii_lines)

    except Exception as e:
        print(f"[-] Error processing image '{image_path}': {e}", file=sys.stderr)
        return process_photo_to_ascii(None, target_width, aspect_ratio_correction)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = process_photo_to_ascii()
    print("[+] Photo-to-ASCII Pipeline ready:")
    print(result)
