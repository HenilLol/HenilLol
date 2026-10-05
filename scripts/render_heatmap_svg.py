#!/usr/bin/env python3
"""
scripts/render_heatmap_svg.py

Renders an editorial contribution heatmap SVG for HenilLol profile README.
Reads data from data/contributions.json and generates assets/contrib-heatmap.svg.

Fixes Implemented:
- FIX 1: Content defaults to opacity: 1 so SVG remains 100% visible if animations are disabled
- FIX 2: Includes transform-box: fill-box and transform-origin: center for cross-browser stability
- Media query for prefers-reduced-motion support
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from theme import THEME

DATA_FILE = PROJECT_ROOT / "data" / "contributions.json"
OUTPUT_FILE = PROJECT_ROOT / "assets" / "contrib-heatmap.svg"


def load_contribution_data(data_path: Path = DATA_FILE) -> Dict[str, Any]:
    """Loads contribution data from JSON file."""
    if not data_path.exists():
        from fetch_contributions import fetch_contributions
        return fetch_contributions(output_path=data_path)
        
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_heatmap_svg(data: Dict[str, Any], output_path: Path = OUTPUT_FILE) -> None:
    """Generates the SVG contribution heatmap."""
    weeks = data.get("weeks", [])
    total_contributions = data.get("total_contributions", 0)

    # Grid configuration
    cell_size = 10
    cell_gap = 3.5
    grid_start_x = 45
    grid_start_y = 52
    
    # SVG Dimensions
    svg_width = 820
    svg_height = 175

    # Month labels calculation
    months_labels: List[tuple[str, int]] = []
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = -1

    for w_idx, week in enumerate(weeks):
        first_day_str = week.get("first_day")
        if first_day_str:
            dt = datetime.fromisoformat(first_day_str)
            if dt.month != last_month:
                months_labels.append((month_names[dt.month - 1], w_idx))
                last_month = dt.month

    levels = THEME["heatmap_levels"]
    
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <defs>',
        '    <style><![CDATA[',
        f'      .bg {{ fill: {THEME["bg"]}; stroke: {THEME["border"]}; stroke-width: 1; rx: 6px; ry: 6px; }}',
        f'      .header-title {{ font-family: {THEME["font_mono"]}; font-size: 12px; fill: {THEME["text_secondary"]}; font-weight: 500; }}',
        f'      .header-prompt {{ font-family: {THEME["font_mono"]}; font-size: 12px; fill: {THEME["accent"]}; font-weight: 600; }}',
        f'      .label {{ font-family: {THEME["font_mono"]}; font-size: 10px; fill: {THEME["text_secondary"]}; }}',
        f'      .sub-label {{ font-family: {THEME["font_mono"]}; font-size: 10px; fill: {THEME["text_dim"]}; }}',
        '      /* FIX 1 and FIX 2: Default opacity: 1 and transform-box: fill-box for Safari/Firefox */',
        '      .cell {',
        '        opacity: 1;',
        '        transform-box: fill-box;',
        '        transform-origin: center;',
        '        animation: cellFadeIn 0.35s ease-out forwards;',
        '      }',
        '      @keyframes cellFadeIn {',
        '        from { opacity: 0; transform: scale(0.85); }',
        '        to { opacity: 1; transform: scale(1); }',
        '      }',
        '      @media (prefers-reduced-motion: reduce) {',
        '        .cell { animation: none !important; opacity: 1 !important; }',
        '      }',
        '    ]]></style>',
        '  </defs>',
        '',
        '  <!-- Terminal Window Background -->',
        f'  <rect x="0.5" y="0.5" width="{svg_width - 1}" height="{svg_height - 1}" class="bg"/>',
        '',
        '  <!-- Terminal Header Bar -->',
        '  <g transform="translate(16, 24)">',
        '    <circle cx="0" cy="0" r="4.5" fill="#FF5F56" opacity="0.8"/>',
        '    <circle cx="14" cy="0" r="4.5" fill="#FFBD2E" opacity="0.8"/>',
        '    <circle cx="28" cy="0" r="4.5" fill="#27C93F" opacity="0.8"/>',
        '    <text x="44" y="4" class="header-prompt">henil@github:~$</text>',
        '    <text x="160" y="4" class="header-title">./contributions.sh --editorial-grid</text>',
        '  </g>',
        '',
        '  <!-- Divider line -->',
        f'  <line x1="16" y1="36" x2="{svg_width - 16}" y2="36" stroke="{THEME["border_subtle"]}" stroke-width="1"/>',
        '',
        '  <!-- Day Labels (Mon, Wed, Fri) -->',
        '  <g class="sub-label">',
    ]

    # Day labels
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for row_idx, name in day_labels:
        y_pos = grid_start_y + (row_idx * (cell_size + cell_gap)) + 8
        svg_content.append(f'    <text x="16" y="{y_pos}">{name}</text>')

    svg_content.append('  </g>')
    svg_content.append('')
    svg_content.append('  <!-- Month Labels -->')
    svg_content.append('  <g class="sub-label">')

    for month_name, col_idx in months_labels:
        x_pos = grid_start_x + (col_idx * (cell_size + cell_gap))
        svg_content.append(f'    <text x="{x_pos:.1f}" y="{grid_start_y - 6}">{month_name}</text>')

    svg_content.append('  </g>')
    svg_content.append('')
    svg_content.append('  <!-- Contribution Grid Cells -->')
    svg_content.append('  <g>')

    for col_idx, week in enumerate(weeks):
        x_pos = grid_start_x + (col_idx * (cell_size + cell_gap))
        delay = round(col_idx * 0.012, 3)
        
        for row_idx, day in enumerate(week.get("days", [])):
            y_pos = grid_start_y + (row_idx * (cell_size + cell_gap))
            level = day.get("level", 0)
            color = levels[min(level, 4)]
            
            cell_xml = (
                f'    <rect x="{x_pos:.1f}" y="{y_pos:.1f}" width="{cell_size}" height="{cell_size}" '
                f'rx="2" ry="2" fill="{color}" class="cell" '
                f'style="animation-delay: {delay}s;"/>'
            )
            svg_content.append(cell_xml)

    svg_content.extend([
        '  </g>',
        '',
        '  <!-- Footer / Legend -->',
        '  <g transform="translate(16, 158)">',
        f'    <text x="0" y="0" class="sub-label">activity log :: {total_contributions} contributions in past year</text>',
        '  </g>',
        '',
        f'  <g transform="translate({svg_width - 170}, 158)">',
        f'    <text x="0" y="0" class="sub-label">Less</text>',
    ])

    legend_start_x = 32
    for idx, col in enumerate(levels):
        lx = legend_start_x + (idx * 14)
        svg_content.append(
            f'    <rect x="{lx}" y="-9" width="10" height="10" rx="2" ry="2" fill="{col}"/>'
        )

    svg_content.extend([
        f'    <text x="{legend_start_x + 75}" y="0" class="sub-label">More</text>',
        '  </g>',
        '</svg>'
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_content) + "\n")
        
    print(f"[+] Rendered contribution heatmap SVG with real data -> {output_path}")


if __name__ == "__main__":
    data = load_contribution_data()
    render_heatmap_svg(data)
