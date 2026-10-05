#!/usr/bin/env python3
"""
scripts/make_info_card.py

Generates an editorial info card SVG (assets/info-card.svg) for HenilLol profile README.
Minimal, high typography, no progress bars, no fake percentages, no decorative badges.
Terminal window visual layout.

Fixes Implemented:
- FIX 1: Content defaults to opacity: 1 so SVG remains 100% visible if animations are disabled
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

OUTPUT_FILE = PROJECT_ROOT / "assets" / "info-card.svg"


def generate_info_card_svg(output_path: Path = OUTPUT_FILE) -> None:
    """Generates the minimal editorial info card SVG."""
    svg_width = 820
    svg_height = 310

    name = "HENIL PATEL"
    role = "Computer Engineering Student"
    
    sections = [
        ("Focus", "Software · AI · GenAI · Agentic Systems"),
        ("Building", "HENEOXY (AI-powered Personal Computing Environment)"),
        ("Learning", "C · C++ · Web Development · Python"),
        ("Selected work", "COALINTEL · FluxDock · RecycLens · Portfolio")
    ]

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <defs>',
        '    <style><![CDATA[',
        f'      .bg {{ fill: {THEME["bg"]}; stroke: {THEME["border"]}; stroke-width: 1; rx: 6px; ry: 6px; }}',
        f'      .card-surface {{ fill: {THEME["surface"]}; stroke: {THEME["border_subtle"]}; stroke-width: 1; rx: 4px; ry: 4px; }}',
        f'      .header-title {{ font-family: {THEME["font_mono"]}; font-size: 12px; fill: {THEME["text_secondary"]}; font-weight: 500; }}',
        f'      .header-prompt {{ font-family: {THEME["font_mono"]}; font-size: 12px; fill: {THEME["accent"]}; font-weight: 600; }}',
        f'      .name {{ font-family: {THEME["font_mono"]}; font-size: 18px; fill: {THEME["text_primary"]}; font-weight: 700; letter-spacing: 1px; }}',
        f'      .role {{ font-family: {THEME["font_mono"]}; font-size: 13px; fill: {THEME["accent"]}; font-weight: 500; }}',
        f'      .sec-label {{ font-family: {THEME["font_mono"]}; font-size: 11px; fill: {THEME["text_secondary"]}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}',
        f'      .sec-val {{ font-family: {THEME["font_mono"]}; font-size: 13px; fill: {THEME["text_primary"]}; font-weight: 400; }}',
        f'      .dim {{ font-family: {THEME["font_mono"]}; font-size: 11px; fill: {THEME["text_dim"]}; }}',
        '      /* FIX 1: Content defaults to opacity: 1 for animation-disabled fallback */',
        '      .reveal-line {',
        '        opacity: 1;',
        '        animation: lineFade 0.4s ease-out forwards;',
        '      }',
        '      @keyframes lineFade {',
        '        from { opacity: 0; transform: translateY(3px); }',
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
        '    <text x="160" y="4" class="header-title">whoami --card</text>',
        '  </g>',
        '',
        f'  <line x1="16" y1="36" x2="{svg_width - 16}" y2="36" stroke="{THEME["border_subtle"]}" stroke-width="1"/>',
        '',
        '  <!-- Terminal Card Body -->',
        '  <g transform="translate(24, 52)">',
        f'    <rect x="0" y="0" width="{svg_width - 48}" height="{svg_height - 76}" class="card-surface"/>',
        '  </g>',
        '',
        '  <!-- Content Group -->',
        '  <g transform="translate(44, 82)">',
        '    <!-- Name & Role -->',
        '    <g class="reveal-line" style="animation-delay: 0.05s;">',
        f'      <text x="0" y="0" class="name">{name}</text>',
        f'      <text x="0" y="22" class="role">{role}</text>',
        '    </g>',
        '',
        f'    <line x1="0" y1="36" x2="{svg_width - 88}" y2="36" stroke="{THEME["border_subtle"]}" stroke-width="1" class="reveal-line" style="animation-delay: 0.1s;"/>',
    ]

    start_y = 60
    row_gap = 42

    for idx, (label, val) in enumerate(sections):
        delay = round(0.15 + (idx * 0.08), 2)
        y_pos = start_y + (idx * row_gap)
        
        svg_lines.extend([
            f'    <g class="reveal-line" style="animation-delay: {delay}s;">',
            f'      <text x="0" y="{y_pos}" class="sec-label">{label}</text>',
            f'      <text x="0" y="{y_pos + 18}" class="sec-val">{val}</text>',
            '    </g>'
        ])

    svg_lines.extend([
        '  </g>',
        '</svg>'
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines) + "\n")

    print(f"[+] Successfully generated info card SVG -> {output_path}")


if __name__ == "__main__":
    generate_info_card_svg()
