#!/usr/bin/env python3
"""
scripts/make_ascii_svg.py

Generates the terminal ASCII SVG asset (assets/henil-ascii.svg) for HenilLol profile README.
Editorial Terminal x Minimalism x Engineering.

Fixes Implemented:
- FIX 1: Content defaults to opacity: 1 so SVG remains 100% visible if animations are disabled
- FIX 4: Removed internal development / phase text from public meta label
- CDATA block wrapping for strict XML parser validity
- Media query for prefers-reduced-motion support
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from theme import THEME

OUTPUT_FILE = PROJECT_ROOT / "assets" / "henil-ascii.svg"

# Clean high-contrast ASCII block art for HenilLol identity
ASCII_ART_LINES = [
    r"  ██╗  ██╗███████╗███╗   ██╗██╗██╗     ██╗      ██████╗ ██╗     ",
    r"  ██║  ██║██╔════╝████╗  ██║██║██║     ██║     ██╔═══██╗██║     ",
    r"  ███████║█████╗  ██╔██╗ ██║██║██║     ██║     ██║   ██║██║     ",
    r"  ██╔══██║██╔══╝  ██║╚██╗██║██║██║     ██║     ██║   ██║██║     ",
    r"  ██║  ██║███████╗██║ ╚████║██║███████╗███████╗╚██████╔╝███████╗",
    r"  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝",
]


def generate_ascii_svg(output_path: Path = OUTPUT_FILE) -> None:
    """Generates the terminal ASCII SVG asset."""
    svg_width = 820
    svg_height = 230

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <defs>',
        '    <style><![CDATA[',
        f'      .bg {{ fill: {THEME["bg"]}; stroke: {THEME["border"]}; stroke-width: 1; rx: 6px; ry: 6px; }}',
        f'      .card-surface {{ fill: {THEME["surface"]}; stroke: {THEME["border_subtle"]}; stroke-width: 1; rx: 4px; ry: 4px; }}',
        f'      .header-title {{ font-family: {THEME["font_mono"]}; font-size: 12px; fill: {THEME["text_secondary"]}; font-weight: 500; }}',
        f'      .header-prompt {{ font-family: {THEME["font_mono"]}; font-size: 12px; fill: {THEME["accent"]}; font-weight: 600; }}',
        f'      .ascii-text {{ font-family: {THEME["font_mono"]}; font-size: 11px; fill: {THEME["accent"]}; font-weight: 700; white-space: pre; }}',
        f'      .meta-text {{ font-family: {THEME["font_mono"]}; font-size: 11px; fill: {THEME["text_secondary"]}; }}',
        f'      .dim {{ font-family: {THEME["font_mono"]}; font-size: 11px; fill: {THEME["text_dim"]}; }}',
        '      /* FIX 1: Content defaults to opacity: 1 for animation-disabled fallback */',
        '      .reveal-line {',
        '        opacity: 1;',
        '        animation: lineFade 0.3s ease-out forwards;',
        '      }',
        '      @keyframes lineFade {',
        '        from { opacity: 0; transform: translateY(2px); }',
        '        to { opacity: 1; transform: translateY(0); }',
        '      }',
        '      @media (prefers-reduced-motion: reduce) {',
        '        .reveal-line { animation: none !important; opacity: 1 !important; }',
        '      }',
        '    ]]></style>',
        '  </defs>',
        '',
        '  <!-- Background Canvas -->',
        f'  <rect x="0.5" y="0.5" width="{svg_width - 1}" height="{svg_height - 1}" class="bg"/>',
        '',
        '  <!-- Header Bar -->',
        '  <g transform="translate(16, 24)">',
        '    <circle cx="0" cy="0" r="4.5" fill="#FF5F56" opacity="0.8"/>',
        '    <circle cx="14" cy="0" r="4.5" fill="#FFBD2E" opacity="0.8"/>',
        '    <circle cx="28" cy="0" r="4.5" fill="#27C93F" opacity="0.8"/>',
        '    <text x="44" y="4" class="header-prompt">henil@github:~$</text>',
        '    <text x="160" y="4" class="header-title">cat ascii_identity.txt</text>',
        '  </g>',
        '',
        f'  <line x1="16" y1="36" x2="{svg_width - 16}" y2="36" stroke="{THEME["border_subtle"]}" stroke-width="1"/>',
        '',
        '  <!-- Card Surface -->',
        '  <g transform="translate(24, 50)">',
        f'    <rect x="0" y="0" width="{svg_width - 48}" height="{svg_height - 74}" class="card-surface"/>',
        '  </g>',
        '',
        '  <!-- ASCII Content Container -->',
        '  <g transform="translate(44, 75)">',
    ]

    line_height = 16
    for idx, line in enumerate(ASCII_ART_LINES):
        delay = round(0.08 + (idx * 0.05), 2)
        y_pos = idx * line_height
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        svg_lines.extend([
            f'    <g class="reveal-line" style="animation-delay: {delay}s;">',
            f'      <text x="0" y="{y_pos}" class="ascii-text" xml:space="preserve">{safe_line}</text>',
            '    </g>'
        ])

    meta_y = (len(ASCII_ART_LINES) * line_height) + 16
    meta_delay = round(0.08 + (len(ASCII_ART_LINES) * 0.05) + 0.1, 2)
    
    svg_lines.extend([
        f'    <g class="reveal-line" style="animation-delay: {meta_delay}s;">',
        f'      <text x="0" y="{meta_y}" class="meta-text">id :: Henil Patel [HenilLol] | Computer Engineering Student | Software · AI</text>',
        '    </g>',
        '  </g>',
        '</svg>'
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines) + "\n")

    print(f"[+] Successfully generated ASCII SVG asset -> {output_path}")


if __name__ == "__main__":
    generate_ascii_svg()
