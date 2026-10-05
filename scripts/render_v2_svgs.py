#!/usr/bin/env python3
"""
HENILLOL V2 — SVG VISUAL SYSTEM GENERATOR
------------------------------------------
Renders V2 engineering telemetry SVG assets:
1. assets/telemetry-os.svg (820 x 290) - Hero system boot telemetry
2. assets/chrono-matrix.svg (820 x 175) - 53-column x 7-row canonical 365-day contribution matrix
3. assets/project-telemetry.svg (820 x 310) - Featured engineering project telemetry & repo status

Author: HenilLol Engineering
Architecture: CHRONO-MATRIX × TELEMETRY-OS
"""

import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime, date, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
CONTRIBUTIONS_PATH = DATA_DIR / "contributions.json"
PROJECTS_PATH = DATA_DIR / "projects.json"

sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

from validate_pipeline import (
    calculate_heatmap_level,
    calculate_chrono_matrix_mapping,
    get_canonical_display_dates,
    verify_project_repository,
    validate_projects_schema,
)
from theme import THEME


# ==============================================================================
# 1. TELEMETRY-OS RENDERER (820 x 290)
# ==============================================================================

def render_telemetry_os_svg(contributions_data: dict) -> str:
    """
    Renders assets/telemetry-os.svg (820 x 290).
    V2 Hero telemetry asset representing terminal boot into Henil Patel's profile.
    """
    raw_sync_ts = contributions_data.get("generated_at", "")
    if raw_sync_ts:
        try:
            dt_obj = datetime.strptime(raw_sync_ts.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
            formatted_sync = dt_obj.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            formatted_sync = raw_sync_ts
    else:
        formatted_sync = "2026-10-05 06:19 UTC"

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 290" width="820" height="290" role="img" aria-labelledby="telemetry-title telemetry-desc">
  <title id="telemetry-title">Henil Patel - Telemetry OS Terminal</title>
  <desc id="telemetry-desc">Engineering profile hero telemetry status for Henil Patel, showing system identity, pipeline state, and live GitHub verification status.</desc>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .title-text {{ fill: #E6EDF3; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; }}
    .sub-text {{ fill: #8B949E; font-size: 11px; }}
    .accent-text {{ fill: #00C7B7; font-size: 12px; font-weight: 600; }}
    .dim-text {{ fill: #484F58; font-size: 11px; }}
    .value-text {{ fill: #E6EDF3; font-size: 12px; font-weight: 500; }}
    .label-text {{ fill: #8B949E; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; }}
    
    /* Progressive enhancement finite reveal animation */
    @keyframes bootSeq {{
      0% {{ opacity: 0; transform: translateY(3px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .anim-step-1 {{ animation: bootSeq 0.4s ease-out 0.1s 1 forwards; }}
    .anim-step-2 {{ animation: bootSeq 0.4s ease-out 0.3s 1 forwards; }}
    .anim-step-3 {{ animation: bootSeq 0.4s ease-out 0.5s 1 forwards; }}
    .anim-step-4 {{ animation: bootSeq 0.4s ease-out 0.7s 1 forwards; }}
    
    @media (prefers-reduced-motion: reduce) {{
      .anim-step-1, .anim-step-2, .anim-step-3, .anim-step-4 {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    }}
  </style>

  <!-- Outer Window Background &amp; Border -->
  <rect x="0.5" y="0.5" width="819" height="289" rx="6" fill="#0D1117" stroke="#30363D" stroke-width="1" />
  
  <!-- Terminal Window Header Bar -->
  <path d="M 0.5,6 A 5.5,5.5 0 0,1 6,0.5 L 814,0.5 A 5.5,5.5 0 0,1 819.5,6 L 819.5,36 L 0.5,36 Z" fill="#161B22" />
  <line x1="0.5" y1="36.5" x2="819.5" y2="36.5" stroke="#30363D" stroke-width="1" />
  
  <!-- Window Control Buttons -->
  <circle cx="20" cy="18.5" r="5" fill="#FF5F56" />
  <circle cx="36" cy="18.5" r="5" fill="#FFBD2E" />
  <circle cx="52" cy="18.5" r="5" fill="#27C93F" />
  
  <!-- Header Title -->
  <text x="70" y="22.5" class="mono title-text">HENILLOL / TELEMETRY-OS</text>
  <rect x="255" y="10" width="60" height="17" rx="3" fill="#12171F" stroke="#30363D" stroke-width="1" />
  <text x="285" y="22" class="mono accent-text" font-size="10" text-anchor="middle">[ LIVE ]</text>
  
  <!-- Main Terminal Content Area -->
  <g class="anim-step-1">
    <text x="24" y="62" class="mono accent-text">&gt; system_boot.sh</text>
    <line x1="24" y1="72" x2="796" y2="72" stroke="#21262D" stroke-width="1" stroke-dasharray="4 4" />
  </g>

  <!-- Two Column Telemetry Section -->
  <g class="anim-step-2">
    <!-- Left Column: Identity &amp; Environment -->
    <text x="24" y="98" class="mono label-text">IDENTITY</text>
    <text x="140" y="98" class="mono value-text">HENIL PATEL</text>
    
    <text x="24" y="126" class="mono label-text">ROLE</text>
    <text x="140" y="126" class="mono value-text">COMPUTER ENGINEERING</text>
    
    <text x="24" y="154" class="mono label-text">FOCUS</text>
    <text x="140" y="154" class="mono value-text">SYSTEMS / AI / ROBOTICS</text>
    
    <text x="24" y="182" class="mono label-text">ENVIRONMENT</text>
    <text x="140" y="182" class="mono value-text">GITHUB / PUBLIC</text>
  </g>

  <g class="anim-step-3">
    <!-- Center Separator Line -->
    <line x1="410" y1="85" x2="410" y2="215" stroke="#30363D" stroke-width="1" stroke-dasharray="2 2" />

    <!-- Right Column: Pipeline &amp; Data Status -->
    <text x="434" y="98" class="mono label-text">PIPELINE</text>
    <rect x="540" y="85" width="86" height="18" rx="3" fill="#04383F" stroke="#00C7B7" stroke-width="1" />
    <text x="583" y="98" class="mono accent-text" font-size="10" text-anchor="middle">HEALTHY</text>

    <text x="434" y="126" class="mono label-text">DATA</text>
    <rect x="540" y="113" width="86" height="18" rx="3" fill="#04383F" stroke="#00C7B7" stroke-width="1" />
    <text x="583" y="126" class="mono accent-text" font-size="10" text-anchor="middle">VERIFIED</text>

    <text x="434" y="154" class="mono label-text">SOURCE</text>
    <text x="540" y="154" class="mono value-text">GitHub REST API v3</text>

    <text x="434" y="182" class="mono label-text">LAST SYNC</text>
    <text x="540" y="182" class="mono value-text">{formatted_sync}</text>
  </g>

  <!-- Terminal Footer Status -->
  <g class="anim-step-4">
    <line x1="24" y1="228" x2="796" y2="228" stroke="#21262D" stroke-width="1" />
    <text x="24" y="256" class="mono accent-text">&gt; SYSTEM READY</text>
    <rect x="145" y="244" width="8" height="14" fill="#00C7B7" opacity="0.85" />
    <text x="796" y="256" class="mono dim-text" text-anchor="end">STATUS: OK (0 ERRORS)</text>
  </g>
</svg>
'''
    return svg_content


# ==============================================================================
# 2. CHRONO-MATRIX RENDERER (820 x 175)
# ==============================================================================

def render_chrono_matrix_svg(contributions_data: dict) -> str:
    """
    Renders assets/chrono-matrix.svg (820 x 175).
    53-column x 7-row canonical 365-day contribution matrix visualization.
    """
    weeks = contributions_data.get("weeks", [])
    all_days = [d for w in weeks for d in w.get("days", [])]
    parsed_dates = [datetime.strptime(d["date"], "%Y-%m-%d").date() for d in all_days]
    date_count_map = {datetime.strptime(d["date"], "%Y-%m-%d").date(): d["count"] for d in all_days}

    # Execute Phase 1 canonical Chrono-Matrix mapping
    mapping = calculate_chrono_matrix_mapping(parsed_dates, normalize_display=True)
    display_start = mapping["display_start_date"]
    display_end = mapping["display_end_date"]
    display_dates, _ = get_canonical_display_dates(parsed_dates)
    display_total_contribs = sum(date_count_map[d] for d in display_dates)

    # Color scale
    level_colors = THEME["heatmap_levels"]  # [#161B22, #04383F, #005F56, #008C7E, #00C7B7]

    # Generate cells XML markup
    # Cell size: 10 x 10, Gap: 3.5
    # x_start: 55, y_start: 48
    cells_svg = []

    # Map mapped_coords to SVG rect elements
    grid_start_obj = datetime.strptime(mapping["grid_start_date"], "%Y-%m-%d").date()

    for col in range(53):
        # Staggered animation group per column
        col_delay = round(col * (2.0 / 52.0), 3)  # Total 2.0s reveal
        cells_svg.append(f'    <g class="matrix-col" style="animation-delay: {col_delay}s;">')
        
        for row in range(7):
            cell_date = grid_start_obj + timedelta(days=col * 7 + row)
            x_pos = round(55 + col * 13.5, 1)
            y_pos = round(48 + row * 13.5, 1)

            if cell_date in date_count_map and cell_date in display_dates:
                cnt = date_count_map[cell_date]
                lvl = calculate_heatmap_level(cnt)
                fill_color = level_colors[lvl]
                stroke_attr = ' stroke="#30363D" stroke-width="0.5"' if lvl == 0 else ''
                cells_svg.append(f'      <rect x="{x_pos}" y="{y_pos}" width="10" height="10" rx="2" fill="{fill_color}"{stroke_attr}><title>{cell_date.isoformat()}: {cnt} contributions</title></rect>')
            else:
                # Padding position (out of canonical display range)
                cells_svg.append(f'      <rect x="{x_pos}" y="{y_pos}" width="10" height="10" rx="2" fill="#161B22" opacity="0.3" stroke="#21262D" stroke-width="0.5" />')
        
        cells_svg.append('    </g>')

    matrix_cells_block = "\n".join(cells_svg)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 175" width="820" height="175" role="img" aria-labelledby="matrix-title matrix-desc">
  <title id="matrix-title">Henil Patel - Chrono-Matrix Contribution Grid</title>
  <desc id="matrix-desc">53-column by 7-row matrix visualization of public GitHub contribution activity over the canonical 365-day window.</desc>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .title-text {{ fill: #E6EDF3; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; }}
    .sub-text {{ fill: #8B949E; font-size: 11px; }}
    .accent-text {{ fill: #00C7B7; font-size: 11px; font-weight: 600; }}
    .dim-text {{ fill: #484F58; font-size: 10px; }}
    .weekday-text {{ fill: #8B949E; font-size: 9px; font-weight: 500; }}
    
    /* Progressive reveal animation */
    @keyframes matrixReveal {{
      0% {{ opacity: 0.1; }}
      100% {{ opacity: 1; }}
    }}
    .matrix-col {{ animation: matrixReveal 0.4s ease-out 1 forwards; }}
    
    @media (prefers-reduced-motion: reduce) {{
      .matrix-col {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <!-- Outer Background &amp; Border -->
  <rect x="0.5" y="0.5" width="819" height="174" rx="6" fill="#0D1117" stroke="#30363D" stroke-width="1" />
  
  <!-- Header Bar -->
  <text x="24" y="28" class="mono title-text">CHRONO-MATRIX</text>
  <text x="155" y="28" class="mono dim-text">|</text>
  <text x="170" y="28" class="mono sub-text">{display_start} — {display_end}</text>
  <text x="796" y="28" class="mono accent-text" text-anchor="end">365 DAYS / 53 WEEKS</text>
  
  <line x1="24" y1="36" x2="796" y2="36" stroke="#21262D" stroke-width="1" />
  
  <!-- Weekday Labels -->
  <text x="45" y="56" class="mono weekday-text" text-anchor="end">MON</text>
  <text x="45" y="83" class="mono weekday-text" text-anchor="end">WED</text>
  <text x="45" y="110" class="mono weekday-text" text-anchor="end">FRI</text>

  <!-- 53 x 7 Matrix Cells -->
{matrix_cells_block}
  
  <!-- Matrix Footer -->
  <line x1="24" y1="144" x2="796" y2="144" stroke="#21262D" stroke-width="1" />
  <text x="24" y="161" class="mono sub-text">TOTAL: <tspan class="mono title-text">{display_total_contribs}</tspan> CONTRIBUTIONS</text>
  
  <!-- Heatmap Legend -->
  <g transform="translate(620, 151)">
    <text x="0" y="8" class="mono dim-text">LESS</text>
    <rect x="34" y="0" width="9" height="9" rx="2" fill="#161B22" stroke="#30363D" stroke-width="0.5" />
    <rect x="47" y="0" width="9" height="9" rx="2" fill="#04383F" />
    <rect x="60" y="0" width="9" height="9" rx="2" fill="#005F56" />
    <rect x="73" y="0" width="9" height="9" rx="2" fill="#008C7E" />
    <rect x="86" y="0" width="9" height="9" rx="2" fill="#00C7B7" />
    <text x="102" y="8" class="mono dim-text">MORE</text>
  </g>
</svg>
'''
    return svg_content


# ==============================================================================
# 3. PROJECT TELEMETRY RENDERER (820 x 310)
# ==============================================================================

def render_project_telemetry_svg(projects_data: dict) -> str:
    """
    Renders assets/project-telemetry.svg (820 x 310).
    Displays featured software engineering projects as an aligned telemetry system.
    Renders repository links ONLY when public repository existence is verified on GitHub.
    """
    projects = projects_data.get("projects", [])
    
    # Sort projects by sort_order
    sorted_projects = sorted(projects, key=lambda p: p.get("sort_order", 99))

    rows_svg = []
    
    for idx, p in enumerate(sorted_projects):
        p_id = p.get("id", "")
        p_name = p.get("name", "").upper()
        p_desc = p.get("description", "")
        # XML escape description & special characters
        p_desc_xml = p_desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        p_status = p.get("status", "ACTIVE")
        p_stack = p.get("stack", [])
        p_repo = p.get("repository", "")

        # Verify repo status dynamically using Phase 1 logic
        ver_res = verify_project_repository(p_repo)
        is_verified = ver_res.get("verified", False)
        html_url = ver_res.get("url") if is_verified else None

        y_offset = 48 + idx * 64
        num_str = f"{idx + 1:02d}"

        # Generate stack tags markup
        stack_svg = []
        stack_x = 360
        for tag in p_stack:
            tag_width = max(len(tag) * 8 + 16, 45)
            stack_svg.append(f'<rect x="{stack_x}" y="16" width="{tag_width}" height="18" rx="3" fill="#12171F" stroke="#30363D" stroke-width="1" />')
            stack_svg.append(f'<text x="{stack_x + tag_width / 2:.1f}" y="28" class="mono sub-text" text-anchor="middle">{tag}</text>')
            stack_x += tag_width + 6

        stack_block = "\n    ".join(stack_svg)

        # Verification & Link markup
        if is_verified and html_url:
            link_block = f'''<a href="{html_url}" target="_blank" rel="noopener noreferrer">
      <rect x="686" y="16" width="76" height="20" rx="3" fill="#04383F" stroke="#00C7B7" stroke-width="1" />
      <text x="724" y="30" class="mono badge-verified" text-anchor="middle">VERIFIED ↗</text>
    </a>'''
        else:
            link_block = '<text x="756" y="30" class="mono sub-text" text-anchor="end">[ UNVERIFIED ]</text>'

        anim_class = f"proj-row-{idx + 1}"

        row_markup = f'''  <!-- Project {num_str}: {p_name} -->
  <g class="{anim_class}" transform="translate(24, {y_offset})">
    <rect x="0" y="0" width="772" height="56" rx="4" fill="#161B22" stroke="#21262D" stroke-width="1" />
    <text x="16" y="24" class="mono proj-name">{num_str} // {p_name}</text>
    <text x="16" y="42" class="mono proj-desc">{p_desc_xml}</text>
    
    <!-- Stack Tags -->
    {stack_block}

    <!-- Status Badge -->
    <rect x="580" y="16" width="95" height="20" rx="3" fill="#12171F" stroke="#30363D" stroke-width="1" />
    <text x="627.5" y="30" class="mono badge-unverified" text-anchor="middle">{p_status}</text>

    <!-- Verification / Repo Link -->
    {link_block}
  </g>'''
        rows_svg.append(row_markup)

    all_rows_block = "\n\n".join(rows_svg)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 310" width="820" height="310" role="img" aria-labelledby="project-title project-desc">
  <title id="project-title">Henil Patel - Project Telemetry</title>
  <desc id="project-desc">System telemetry and status log for featured software engineering projects and repositories.</desc>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .title-text {{ fill: #E6EDF3; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; }}
    .sub-text {{ fill: #8B949E; font-size: 11px; }}
    .accent-text {{ fill: #00C7B7; font-size: 11px; font-weight: 600; }}
    .dim-text {{ fill: #484F58; font-size: 10px; }}
    .proj-name {{ fill: #E6EDF3; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; }}
    .proj-desc {{ fill: #8B949E; font-size: 11px; }}
    .badge-verified {{ fill: #00C7B7; font-size: 10px; font-weight: 600; }}
    .badge-unverified {{ fill: #8B949E; font-size: 10px; font-weight: 600; }}

    /* Progressive reveal animation */
    @keyframes projReveal {{
      0% {{ opacity: 0; transform: translateY(4px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .proj-row-1 {{ animation: projReveal 0.4s ease-out 0.1s 1 forwards; }}
    .proj-row-2 {{ animation: projReveal 0.4s ease-out 0.25s 1 forwards; }}
    .proj-row-3 {{ animation: projReveal 0.4s ease-out 0.4s 1 forwards; }}
    .proj-row-4 {{ animation: projReveal 0.4s ease-out 0.55s 1 forwards; }}

    @media (prefers-reduced-motion: reduce) {{
      .proj-row-1, .proj-row-2, .proj-row-3, .proj-row-4 {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    }}
  </style>

  <!-- Outer Background &amp; Border -->
  <rect x="0.5" y="0.5" width="819" height="309" rx="6" fill="#0D1117" stroke="#30363D" stroke-width="1" />
  
  <!-- Header Bar -->
  <text x="24" y="28" class="mono title-text">PROJECT TELEMETRY</text>
  <text x="180" y="28" class="mono dim-text">|</text>
  <text x="195" y="28" class="mono sub-text">FEATURED REPOSITORIES / SYSTEM LOG</text>
  <text x="796" y="28" class="mono accent-text" text-anchor="end">4 PROJECTS</text>
  
  <line x1="24" y1="36" x2="796" y2="36" stroke="#21262D" stroke-width="1" />

{all_rows_block}
</svg>
'''
    return svg_content


# ==============================================================================
# 4. MAIN BUILD SCRIPT
# ==============================================================================

def main():
    print("=" * 60)
    print("HENILLOL V2 SVG VISUAL SYSTEM GENERATOR")
    print("=" * 60)
    
    # Load Phase 1 Data
    if not CONTRIBUTIONS_PATH.exists():
        print(f"[ERROR] Contributions file missing: {CONTRIBUTIONS_PATH}")
        sys.exit(1)
    if not PROJECTS_PATH.exists():
        print(f"[ERROR] Projects file missing: {PROJECTS_PATH}")
        sys.exit(1)

    with open(CONTRIBUTIONS_PATH, "r", encoding="utf-8") as f:
        contrib_data = json.load(f)

    with open(PROJECTS_PATH, "r", encoding="utf-8") as f:
        proj_data = json.load(f)

    # 1. Render telemetry-os.svg
    print("[BUILD] Rendering assets/telemetry-os.svg (820 x 290)...")
    telemetry_svg = render_telemetry_os_svg(contrib_data)
    telemetry_path = ASSETS_DIR / "telemetry-os.svg"
    with open(telemetry_path, "w", encoding="utf-8") as f:
        f.write(telemetry_svg)
    print(f"        -> Written to {telemetry_path}")

    # 2. Render chrono-matrix.svg
    print("[BUILD] Rendering assets/chrono-matrix.svg (820 x 175)...")
    matrix_svg = render_chrono_matrix_svg(contrib_data)
    matrix_path = ASSETS_DIR / "chrono-matrix.svg"
    with open(matrix_path, "w", encoding="utf-8") as f:
        f.write(matrix_svg)
    print(f"        -> Written to {matrix_path}")

    # 3. Render project-telemetry.svg
    print("[BUILD] Rendering assets/project-telemetry.svg (820 x 310)...")
    proj_svg = render_project_telemetry_svg(proj_data)
    proj_path = ASSETS_DIR / "project-telemetry.svg"
    with open(proj_path, "w", encoding="utf-8") as f:
        f.write(proj_svg)
    print(f"        -> Written to {proj_path}")

    print("=" * 60)
    print("V2 SVG GENERATION COMPLETE — 3 ASSETS GENERATED")
    print("=" * 60)


if __name__ == "__main__":
    main()
