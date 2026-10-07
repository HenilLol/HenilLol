#!/usr/bin/env python3
"""
HENILLOL V3 — CYBERNETIC AVIONICS // HENEOXY KERNEL SVG RENDERER
----------------------------------------------------------------
Generates state-of-the-art vector engineering artifacts:
1. assets/heneoxy-core.svg (820 x 340) - The Quantum Silicon "H" Nexus & Cockpit Avionics
2. assets/chrono-synapse.svg (820 x 245) - The 365-Day Temporal Memory Bus & Seismic Waveform
3. assets/mission-payloads.svg (820 x 400) - Aerospace Subsystem Payload Registry & Flow Schematics

Author: Henil Patel (@HenilLol)
Design System: THE HENEOXY RESEARCH ENGINE (Cybernetic Avionics)
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
from theme import THEME_V3


# Helper to wrap descriptions cleanly across two lines
def split_description_lines(desc: str, max_chars: int = 56) -> tuple[str, str]:
    if len(desc) <= max_chars:
        return desc, ""
    words = desc.split(" ")
    line1_words = []
    line2_words = []
    current_len = 0
    for w in words:
        if current_len + len(w) + (1 if line1_words else 0) <= max_chars:
            line1_words.append(w)
            current_len += len(w) + 1
        else:
            line2_words.append(w)
    return " ".join(line1_words), " ".join(line2_words)


# ==============================================================================
# 1. HENEOXY-CORE RENDERER (820 x 340)
# ==============================================================================

def render_heneoxy_core_svg(contributions_data: dict, projects_data: dict) -> str:
    """
    Renders assets/heneoxy-core.svg (820 x 340).
    The flagship hero asset representing the cybernetic avionics cockpit
    and the rotating Quantum-Silicon "H" Core Nexus.
    """
    total_contributions = contributions_data.get("total_contributions", 306)
    projects_list = projects_data.get("projects", [])
    num_projects = len(projects_list)

    # Extract canonical display window length from actual data
    weeks = contributions_data.get("weeks", [])
    all_days = [d for w in weeks for d in w.get("days", [])]
    if all_days:
        parsed_dates = [datetime.strptime(d["date"], "%Y-%m-%d").date() for d in all_days]
        display_dates, _ = get_canonical_display_dates(parsed_dates)
        display_days_count = len(display_dates)
    else:
        display_days_count = 365

    # Extract dynamic sync timestamp
    raw_sync_ts = contributions_data.get("generated_at", "")
    if raw_sync_ts:
        try:
            dt_obj = datetime.strptime(raw_sync_ts.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
            formatted_sync = dt_obj.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            formatted_sync = raw_sync_ts
        sync_date_str = raw_sync_ts.split("T")[0]
    else:
        formatted_sync = "2026-10-05 06:19 UTC"
        sync_date_str = "2026-10-05"

    muted_color = THEME_V3.get("text_muted", "#6E86AA")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 340" width="820" height="340" role="img" aria-labelledby="core-title core-desc">
  <title id="core-title">Henil Patel - Heneoxy Kernel Cybernetic Core</title>
  <desc id="core-desc">Cybernetic avionics flight deck and quantum-silicon H nexus for Henil Patel, featuring autonomous systems telemetry, core registers, and subsystem diagnostics.</desc>
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="core-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#04070D" />
      <stop offset="50%" stop-color="#060B14" />
      <stop offset="100%" stop-color="#091222" />
    </linearGradient>
    <linearGradient id="h-metal-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="50%" stop-color="#F0F6FC" />
      <stop offset="100%" stop-color="#0088A8" />
    </linearGradient>
    <radialGradient id="radar-beam" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.35" />
      <stop offset="60%" stop-color="#00F0FF" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0" />
    </radialGradient>

    <!-- Hairline Cybernetic Grid Pattern -->
    <pattern id="chassis-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#111B2C" stroke-width="0.8" />
      <circle cx="20" cy="20" r="0.75" fill="#1E2D44" />
    </pattern>

    <!-- Tactical Glow Filter -->
    <filter id="core-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .mono {{ font-family: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .title-primary {{ fill: #F0F6FC; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; }}
    .title-sub {{ fill: #8B9BB4; font-size: 11px; letter-spacing: 0.8px; }}
    .val-cyan {{ fill: #00F0FF; font-size: 11.5px; font-weight: 700; }}
    .val-amber {{ fill: #FFB000; font-size: 11.5px; font-weight: 700; }}
    .val-emerald {{ fill: #00E599; font-size: 11.5px; font-weight: 700; }}
    .val-titanium {{ fill: #F0F6FC; font-size: 11px; font-weight: 600; }}
    .label-muted {{ fill: #8B9BB4; font-size: 10px; font-weight: 600; letter-spacing: 0.5px; }}
    .micro-dim {{ fill: {muted_color}; font-size: 9.5px; }}

    /* Keyframe Animations */
    @keyframes spinClockwise {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    @keyframes spinCounterClockwise {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(-360deg); }}
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.9; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.96); }}
    }}
    @keyframes beaconBlink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
    }}
    @keyframes freqBounce1 {{
      0%, 100% {{ height: 4px; y: 16px; }}
      50% {{ height: 16px; y: 4px; }}
    }}
    @keyframes freqBounce2 {{
      0%, 100% {{ height: 14px; y: 6px; }}
      50% {{ height: 6px; y: 14px; }}
    }}
    @keyframes freqBounce3 {{
      0%, 100% {{ height: 8px; y: 12px; }}
      50% {{ height: 18px; y: 2px; }}
    }}

    /* Animation Classes */
    .anim-spin-cw {{ transform-origin: 135px 185px; animation: spinClockwise 28s linear infinite; }}
    .anim-spin-ccw {{ transform-origin: 135px 185px; animation: spinCounterClockwise 18s linear infinite; }}
    .anim-radar {{ transform-origin: 135px 185px; animation: spinClockwise 5s linear infinite; }}
    .anim-pulse {{ transform-origin: 135px 185px; animation: pulseGlow 3s ease-in-out infinite; }}
    .anim-beacon {{ animation: beaconBlink 1.8s ease-in-out infinite; }}

    .bar-1 {{ animation: freqBounce1 1.2s ease-in-out infinite; }}
    .bar-2 {{ animation: freqBounce2 1.5s ease-in-out infinite; }}
    .bar-3 {{ animation: freqBounce3 1.1s ease-in-out infinite; }}
    .bar-4 {{ animation: freqBounce1 1.7s ease-in-out infinite; }}
    .bar-5 {{ animation: freqBounce2 1.3s ease-in-out infinite; }}

    /* Prefers Reduced Motion Safety */
    @media (prefers-reduced-motion: reduce) {{
      .anim-spin-cw, .anim-spin-ccw, .anim-radar, .anim-pulse, .anim-beacon,
      .bar-1, .bar-2, .bar-3, .bar-4, .bar-5 {{
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
      }}
    }}
  </style>

  <!-- Outer Chassis & Cybernetic Grid -->
  <rect x="0.5" y="0.5" width="819" height="339" rx="8" fill="url(#core-bg-grad)" stroke="#1E2D44" stroke-width="1" />
  <rect x="1" y="1" width="818" height="338" rx="7" fill="url(#chassis-grid)" />

  <!-- Corner Precision Brackets -->
  <path d="M 6 24 L 6 6 L 24 6" fill="none" stroke="#00F0FF" stroke-width="1.8" />
  <path d="M 796 6 L 814 6 L 814 24" fill="none" stroke="#00F0FF" stroke-width="1.8" />
  <path d="M 6 316 L 6 334 L 24 334" fill="none" stroke="#00F0FF" stroke-width="1.8" />
  <path d="M 796 334 L 814 334 L 814 316" fill="none" stroke="#00F0FF" stroke-width="1.8" />

  <!-- ======================================================================== -->
  <!-- TOP AVIONICS STATUS HEADER                                               -->
  <!-- ======================================================================== -->
  <rect x="1" y="1" width="818" height="36" rx="7" fill="#0A1220" />
  <line x1="1" y1="37" x2="819" y2="37" stroke="#1E2D44" stroke-width="1" />

  <!-- Logo & System Designation -->
  <circle cx="18" cy="19" r="4.5" fill="#00F0FF" class="anim-beacon" />
  <text x="30" y="23" class="mono title-primary">HENEOXY</text>
  <text x="105" y="23" class="mono title-sub">// KERNEL ARCHITECTURE v3.0</text>

  <!-- Optical Alignment Marks (Truthful Calendar & Geo Telemetry) -->
  <line x1="330" y1="12" x2="330" y2="26" stroke="#1E2D44" stroke-width="1" />
  <text x="345" y="22.5" class="mono micro-dim">LOC [23.02°N 72.57°E]</text>
  <text x="475" y="22.5" class="mono micro-dim">GRID [53×7 MONDAY]</text>
  <text x="595" y="22.5" class="mono micro-dim">WINDOW [{display_days_count}D]</text>

  <!-- Flight Status Capsule -->
  <rect x="680" y="8" width="128" height="21" rx="10.5" fill="#091A14" stroke="#00E599" stroke-width="1" />
  <circle cx="693" cy="18.5" r="4" fill="#00E599" class="anim-beacon" />
  <text x="704" y="22.5" class="mono val-emerald" font-size="10.5">TELEMETRY LOCK</text>

  <!-- ======================================================================== -->
  <!-- LEFT: THE QUANTUM-SILICON "H" CORE NEXUS (Center: 135, 185)              -->
  <!-- ======================================================================== -->
  <g id="quantum-core">
    <!-- Outer Calibration Dial (r=86) -->
    <circle cx="135" cy="185" r="86" fill="none" stroke="#132238" stroke-width="1" />
    <circle cx="135" cy="185" r="76" fill="none" stroke="#162A45" stroke-width="1" stroke-dasharray="3, 5" />

    <!-- Rotating Compass Ticks Ring (CW) -->
    <g class="anim-spin-cw">
      <circle cx="135" cy="185" r="82" fill="none" stroke="#1E3554" stroke-width="1.2" stroke-dasharray="2, 19.4" />
      <path d="M 135 101 L 135 107 M 135 263 L 135 269 M 51 185 L 57 185 M 213 185 L 219 185" stroke="#00F0FF" stroke-width="1.5" />
    </g>

    <!-- Counter-Rotating Dashed Reticle (CCW) -->
    <g class="anim-spin-ccw">
      <circle cx="135" cy="185" r="66" fill="none" stroke="#00F0FF" stroke-width="1" stroke-dasharray="8, 12" opacity="0.8" />
      <polygon points="135,123 138,127 132,127" fill="#00F0FF" />
      <polygon points="135,247 138,243 132,243" fill="#00F0FF" />
    </g>

    <!-- Radar Sweep Beam (Continuous 360 Scan) -->
    <g class="anim-radar">
      <path d="M 135 185 L 185 135 A 70 70 0 0 1 195 185 Z" fill="url(#radar-beam)" />
    </g>

    <!-- Central Cybernetic Hexagon Housing -->
    <polygon points="135,135 178,160 178,210 135,235 92,210 92,160" fill="#08101E" stroke="#1E3554" stroke-width="2" />
    <polygon points="135,139 174,162 174,208 135,231 96,208 96,162" fill="#0B172A" stroke="#00F0FF" stroke-width="1.5" filter="url(#core-glow)" />

    <!-- THE BESPOKE GEOMETRIC "H" GLYPH -->
    <g id="h-monogram" class="anim-pulse">
      <!-- Left Pillar of H (Chamfered Geometry) -->
      <path d="M 112 153 L 122 153 L 122 217 L 112 217 Z" fill="url(#h-metal-grad)" />
      <!-- Right Pillar of H (Chamfered Geometry) -->
      <path d="M 148 153 L 158 153 L 158 217 L 148 217 Z" fill="url(#h-metal-grad)" />
      <!-- High-Energy Central Horizontal Bridge -->
      <rect x="122" y="180" width="26" height="10" fill="#00F0FF" />
      <!-- Central Quantum Core Diamond -->
      <polygon points="135,178 141,185 135,192 129,185" fill="#FFB000" />
      <circle cx="135" cy="185" r="2.5" fill="#F0F6FC" />
    </g>

    <!-- Precision Telemetry Callout Tags -->
    <!-- Callout 1: Core Frequency -->
    <polyline points="180,145 205,130 248,130" fill="none" stroke="#00F0FF" stroke-width="1" />
    <circle cx="180" cy="145" r="2" fill="#00F0FF" />
    <text x="210" y="125" class="mono micro-dim">CORE_CLK</text>
    <text x="210" y="139" class="mono val-cyan" font-size="10">4.80 GHz</text>

    <!-- Callout 2: Instruction Set -->
    <polyline points="180,225 205,240 248,240" fill="none" stroke="#00F0FF" stroke-width="1" />
    <circle cx="180" cy="225" r="2" fill="#00F0FF" />
    <text x="210" y="235" class="mono micro-dim">ISA_PROFILE</text>
    <text x="210" y="249" class="mono val-titanium" font-size="9.5">x86_64//NEURAL</text>

    <!-- Callout 3: Security Status -->
    <polyline points="90,145 65,130 25,130" fill="none" stroke="#00E599" stroke-width="1" />
    <circle cx="90" cy="145" r="2" fill="#00E599" />
    <text x="25" y="125" class="mono micro-dim">SECURITY_BUS</text>
    <text x="25" y="139" class="mono val-emerald" font-size="10">ENCLAVE_LOCK</text>
  </g>

  <!-- ======================================================================== -->
  <!-- CENTER & RIGHT: HUD AVIONICS DIAGNOSTIC BAYS                             -->
  <!-- ======================================================================== -->

  <!-- BAY 1: OPERATOR FIRMWARE & RUNTIME STACK (x=272, y=48, w=262, h=228) -->
  <g id="bay-firmware">
    <path d="M 272 48 L 518 48 L 534 64 L 534 276 L 272 276 Z" fill="#0B1322" stroke="#1E2D44" stroke-width="1.2" />
    <rect x="272" y="48" width="262" height="26" fill="#0F1A2D" />
    <line x1="272" y1="74" x2="534" y2="74" stroke="#1E2D44" stroke-width="1" />

    <!-- Bay Header -->
    <text x="284" y="65" class="mono val-cyan" font-size="11">[01] OPERATOR &amp; RUNTIME FIRMWARE</text>

    <!-- Operator & Role -->
    <text x="284" y="93" class="mono label-muted">OPERATOR</text>
    <text x="284" y="108" class="mono val-titanium">Henil Patel</text>
    <text x="365" y="108" class="mono micro-dim">(Computer Engineering)</text>

    <!-- Core Languages & Systems -->
    <text x="284" y="132" class="mono label-muted">SYSTEM LANGUAGES</text>
    <text x="284" y="147" class="mono val-cyan">C · C++ · Python · Web (TS/HTML)</text>

    <!-- Active Research & Architectures -->
    <text x="284" y="171" class="mono label-muted">ACTIVE RESEARCH &amp; VECTOR</text>
    <text x="284" y="186" class="mono val-amber">Agentic AI · RAG · Vision Control</text>

    <!-- Flagship Build -->
    <text x="284" y="210" class="mono label-muted">ACTIVE FLAGSHIP BUILD</text>
    <text x="284" y="225" class="mono val-emerald">HENEOXY (Personal Computing OS)</text>

    <!-- Dynamic Logic Bus Spectrum Analyzer -->
    <line x1="284" y1="242" x2="522" y2="242" stroke="#16253B" stroke-width="1" />
    <text x="284" y="260" class="mono micro-dim">LOGIC_BUS_FREQ</text>
    <g transform="translate(420, 246)">
      <rect x="0" y="6" width="4" height="14" rx="1" fill="#00F0FF" class="bar-1" />
      <rect x="8" y="10" width="4" height="10" rx="1" fill="#00F0FF" class="bar-2" />
      <rect x="16" y="4" width="4" height="16" rx="1" fill="#00E599" class="bar-3" />
      <rect x="24" y="8" width="4" height="12" rx="1" fill="#00F0FF" class="bar-4" />
      <rect x="32" y="14" width="4" height="6" rx="1" fill="#FFB000" class="bar-5" />
      <rect x="40" y="5" width="4" height="15" rx="1" fill="#00F0FF" class="bar-2" />
      <rect x="48" y="2" width="4" height="18" rx="1" fill="#00E599" class="bar-3" />
      <rect x="56" y="9" width="4" height="11" rx="1" fill="#00F0FF" class="bar-1" />
      <rect x="64" y="12" width="4" height="8" rx="1" fill="#00F0FF" class="bar-4" />
      <rect x="72" y="6" width="4" height="14" rx="1" fill="#FFB000" class="bar-5" />
    </g>
  </g>

  <!-- BAY 2: FLIGHT METRICS & REPOSITORY TELEMETRY (x=546, y=48, w=262, h=228) -->
  <g id="bay-telemetry">
    <path d="M 546 48 L 792 48 L 808 64 L 808 276 L 546 276 Z" fill="#0B1322" stroke="#1E2D44" stroke-width="1.2" />
    <rect x="546" y="48" width="262" height="26" fill="#0F1A2D" />
    <line x1="546" y1="74" x2="808" y2="74" stroke="#1E2D44" stroke-width="1" />

    <!-- Bay Header -->
    <text x="558" y="65" class="mono val-amber" font-size="11">[02] SUBSYSTEM INSTRUMENTATION</text>

    <!-- Annual Pulses (Dynamic) -->
    <text x="558" y="93" class="mono label-muted">ANNUAL CONTRIBUTIONS</text>
    <text x="558" y="108" class="mono val-cyan" font-size="12">{total_contributions} VERIFIED PULSES</text>

    <!-- Temporal Cycle -->
    <text x="558" y="132" class="mono label-muted">TEMPORAL SAMPLE WINDOW</text>
    <text x="558" y="147" class="mono val-titanium">{display_days_count} Days Active (Canonical)</text>

    <!-- Project Architecture Nodes (Dynamic) -->
    <text x="558" y="171" class="mono label-muted">SUBSYSTEM NODES</text>
    <text x="558" y="186" class="mono val-emerald">{num_projects} Registered Modules</text>

    <!-- Verification Audit -->
    <text x="558" y="210" class="mono label-muted">PUBLIC REPOSITORIES</text>
    <text x="558" y="225" class="mono val-cyan">COALINTEL + RECYCLENS (Live)</text>

    <!-- Temporal Coverage Parity Dial (Truthful Metric) -->
    <line x1="558" y1="242" x2="796" y2="242" stroke="#16253B" stroke-width="1" />
    <text x="558" y="260" class="mono micro-dim">TEMPORAL_LOCK</text>
    <text x="640" y="260" class="mono val-emerald" font-size="10">{display_days_count}/{display_days_count} DAYS</text>
    <g transform="translate(735, 255)">
      <circle cx="0" cy="0" r="12" fill="none" stroke="#16253B" stroke-width="2.5" />
      <circle cx="0" cy="0" r="12" fill="none" stroke="#00E599" stroke-width="2.5" stroke-dasharray="75.4, 75.4" stroke-linecap="round" />
      <circle cx="0" cy="0" r="2" fill="#00E599" />
    </g>
  </g>

  <!-- ======================================================================== -->
  <!-- BOTTOM TACTICAL DATA BUS STRIP (y=286 to y=330)                          -->
  <!-- ======================================================================== -->
  <rect x="12" y="286" width="796" height="42" rx="4" fill="#070D18" stroke="#16253B" stroke-width="1" />

  <text x="24" y="303" class="mono micro-dim">BUS_TELEMETRY:</text>
  <text x="110" y="303" class="mono val-cyan" font-size="9.5">CLK_REF: 100MHz</text>
  <text x="205" y="303" class="mono val-emerald" font-size="9.5">PARITY: 100% OK</text>
  <text x="300" y="303" class="mono val-amber" font-size="9.5">ENCLAVE: HARDWARE_ECC</text>

  <!-- Cryptographic Identity Hash & Binary Signature -->
  <text x="24" y="318" class="mono micro-dim">HEX_SIG: 0x48656E696C4C6F6C (HenilLol) · SYNC: {sync_date_str}</text>

  <!-- Subspace Transmission Heartbeat ECG Wave -->
  <path d="M 620 307 L 650 307 L 655 298 L 662 318 L 668 302 L 674 311 L 678 307 L 720 307" fill="none" stroke="#00F0FF" stroke-width="1.2" opacity="0.8" />
  <circle cx="720" cy="307" r="2" fill="#00F0FF" class="anim-beacon" />
  <text x="730" y="310" class="mono val-cyan" font-size="9.5">PULSE: LIVE</text>
</svg>'''
    return svg_content


# ==============================================================================
# 2. CHRONO-SYNAPSE RENDERER (820 x 245)
# ==============================================================================

def render_chrono_synapse_svg(contributions_data: dict) -> str:
    """
    Renders assets/chrono-synapse.svg (820 x 245).
    Elevates the 365-day contribution matrix into a tactical temporal memory bus,
    complete with an animated dynamic seismic activity waveform, 53-column grid,
    and a smooth horizontal scanning laser telemetry head.
    """
    weeks = contributions_data.get("weeks", [])
    all_days = [d for w in weeks for d in w.get("days", [])]
    if all_days:
        parsed_dates = [datetime.strptime(d["date"], "%Y-%m-%d").date() for d in all_days]
        date_count_map = {datetime.strptime(d["date"], "%Y-%m-%d").date(): d["count"] for d in all_days}
        mapping = calculate_chrono_matrix_mapping(parsed_dates, normalize_display=True)
        display_start = mapping["display_start_date"]
        display_end = mapping["display_end_date"]
        grid_start_obj = datetime.strptime(mapping["grid_start_date"], "%Y-%m-%d").date()
        display_dates, _ = get_canonical_display_dates(parsed_dates)
        display_total_contribs = sum(date_count_map.get(d, 0) for d in display_dates)
    else:
        # Fallback for empty dataset
        grid_start_obj = date(2025, 10, 6)
        display_start = "2025-10-06"
        display_end = "2026-10-05"
        date_count_map = {}
        display_dates = []
        display_total_contribs = 0

    # Compute weekly totals across the 53 columns for the seismic waveform
    weekly_sums = [0] * 53
    for col in range(53):
        for row in range(7):
            cell_date = grid_start_obj + timedelta(days=col * 7 + row)
            if cell_date in date_count_map and cell_date in display_dates:
                weekly_sums[col] += date_count_map[cell_date]

    max_weekly = max(weekly_sums) if max(weekly_sums) > 0 else 1
    wave_x_start = 280
    wave_width = 280
    wave_y_base = 32
    wave_max_h = 16

    path_points = []
    for i, count in enumerate(weekly_sums):
        x = wave_x_start + (i / 52.0) * wave_width
        norm_h = (count / max_weekly) * wave_max_h
        y = wave_y_base - norm_h
        path_points.append(f"{x:.1f},{y:.1f}")

    waveform_d = f"M {path_points[0]} " + " ".join([f"L {pt}" for pt in path_points[1:]])

    # Month markers across 53 columns
    month_markers = [
        ("OCT", 0), ("NOV", 4), ("DEC", 8), ("JAN", 13), ("FEB", 17),
        ("MAR", 21), ("APR", 26), ("MAY", 30), ("JUN", 34),
        ("JUL", 39), ("AUG", 43), ("SEP", 47), ("OCT", 52)
    ]

    muted_color = THEME_V3.get("text_muted", "#6E86AA")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 245" width="820" height="245" role="img" aria-labelledby="synapse-title synapse-desc">
  <title id="synapse-title">Henil Patel - Chrono-Synapse Temporal Memory Bus</title>
  <desc id="synapse-desc">365-day tactical contribution memory bus mapping 53 columns and 7 rows of GitHub commits, featuring seismic waveform telemetry and real-time activity tiers.</desc>
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="synapse-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#04070D" />
      <stop offset="60%" stop-color="#070D18" />
      <stop offset="100%" stop-color="#0A1424" />
    </linearGradient>

    <!-- Laser Scanner Gradient -->
    <linearGradient id="laser-glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0" />
      <stop offset="20%" stop-color="#00F0FF" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#F0F6FC" stop-opacity="1" />
      <stop offset="80%" stop-color="#00F0FF" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0" />
    </linearGradient>

    <!-- Cell Glow Filters -->
    <filter id="glow-cyan-sm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="glow-amber-sm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .mono {{ font-family: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .title-primary {{ fill: #F0F6FC; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; }}
    .title-sub {{ fill: #8B9BB4; font-size: 10px; }}
    .val-cyan {{ fill: #00F0FF; font-size: 11px; font-weight: 700; }}
    .val-amber {{ fill: #FFB000; font-size: 11px; font-weight: 700; }}
    .val-emerald {{ fill: #00E599; font-size: 11px; font-weight: 700; }}
    .label-muted {{ fill: #8B9BB4; font-size: 9.5px; font-weight: 600; }}
    .micro-dim {{ fill: {muted_color}; font-size: 9px; }}

    /* Scanning Laser Head Across Grid (x spans from 50 to 790 over 7.5s) */
    @keyframes sweepLaser {{
      0% {{ transform: translateX(50px); opacity: 0; }}
      5% {{ opacity: 0.9; }}
      95% {{ opacity: 0.9; }}
      100% {{ transform: translateX(795px); opacity: 0; }}
    }}
    .anim-laser {{ animation: sweepLaser 7.5s ease-in-out infinite; }}

    /* Prefers Reduced Motion Safety */
    @media (prefers-reduced-motion: reduce) {{
      .anim-laser {{ animation: none !important; opacity: 0 !important; }}
    }}
  </style>

  <!-- Outer Chassis & Frame -->
  <rect x="0.5" y="0.5" width="819" height="244" rx="8" fill="url(#synapse-bg-grad)" stroke="#1E2D44" stroke-width="1" />

  <!-- Header Bar -->
  <rect x="1" y="1" width="818" height="46" rx="7" fill="#0A1220" />
  <line x1="1" y1="47" x2="819" y2="47" stroke="#1E2D44" stroke-width="1" />

  <!-- Left: System Designation -->
  <text x="18" y="22" class="mono title-primary">CHRONO-SYNAPSE</text>
  <text x="145" y="22" class="mono title-sub">// 365-DAY TEMPORAL MEMORY BUS</text>
  <text x="18" y="38" class="mono micro-dim">BUS RANGE: {display_start} → {display_end} (53 COLUMNS × 7 TRACKS)</text>

  <!-- Center: Seismic Activity Waveform -->
  <g id="seismic-waveform">
    <!-- Waveform Baseline -->
    <line x1="{wave_x_start}" y1="{wave_y_base}" x2="{wave_x_start + wave_width}" y2="{wave_y_base}" stroke="#16253B" stroke-width="1" />
    <!-- Dynamic Waveform Path -->
    <path d="{waveform_d}" fill="none" stroke="#00F0FF" stroke-width="1.4" opacity="0.85" />
    <text x="{wave_x_start + 10}" y="14" class="mono micro-dim">ANNUAL ACTIVITY SEISMIC WAVE</text>
  </g>

  <!-- Right: Total Synaptic Events & Verification -->
  <text x="590" y="22" class="mono val-cyan">{display_total_contribs} SYNAPTIC PULSES</text>
  <text x="590" y="38" class="mono val-emerald">CANONICAL: 365/365 DATES</text>

  <!-- ======================================================================== -->
  <!-- 53 COLUMNS × 7 ROWS TACTICAL MATRIX                                      -->
  <!-- ======================================================================== -->
  <!-- Month Labels -->
  <g id="month-labels">'''

    for month_str, col_idx in month_markers:
        x_pos = 54 + col_idx * 13.9
        svg_content += f'\n    <text x="{x_pos:.1f}" y="63" class="mono micro-dim">{month_str}</text>'

    svg_content += '''
  </g>

  <!-- Day of Week Track Labels (Left Side) -->
  <text x="24" y="85" class="mono label-muted">MON</text>
  <text x="24" y="115" class="mono label-muted">WED</text>
  <text x="24" y="145" class="mono label-muted">FRI</text>
  <text x="24" y="175" class="mono label-muted">SUN</text>

  <!-- Matrix Cells -->
  <g id="synapse-cells">'''

    for col in range(53):
        for row in range(7):
            cell_date = grid_start_obj + timedelta(days=col * 7 + row)
            cx = round(54 + col * 13.9, 1)
            cy = round(75 + row * 15.0, 1)

            if cell_date in date_count_map and cell_date in display_dates:
                cnt = date_count_map[cell_date]
                lvl = calculate_heatmap_level(cnt)
                if lvl == 0:
                    fill_col = "#0E1726"
                    stroke_col = "#16253B"
                    extra_attr = ""
                elif lvl == 1:
                    fill_col = "#004D66"
                    stroke_col = "#007799"
                    extra_attr = ""
                elif lvl == 2:
                    fill_col = "#0088A8"
                    stroke_col = "#00C2EB"
                    extra_attr = ""
                elif lvl == 3:
                    fill_col = "#00D0EB"
                    stroke_col = "#80F7FF"
                    extra_attr = 'filter="url(#glow-cyan-sm)"'
                else:  # lvl >= 4
                    fill_col = "#FFB000"
                    stroke_col = "#FFD166"
                    extra_attr = 'filter="url(#glow-amber-sm)"'

                svg_content += f'\n    <rect x="{cx}" y="{cy}" width="10.8" height="10.8" rx="2" fill="{fill_col}" stroke="{stroke_col}" stroke-width="0.8" {extra_attr}><title>{cell_date.isoformat()}: {cnt} contributions</title></rect>'
            else:
                # Padding position (outside canonical display window)
                svg_content += f'\n    <rect x="{cx}" y="{cy}" width="10.8" height="10.8" rx="2" fill="#0A111C" opacity="0.3" stroke="#121D2D" stroke-width="0.5" />'

    svg_content += f'''
  </g>

  <!-- Scanning Optical Laser Head -->
  <line x1="0" y1="68" x2="0" y2="185" stroke="url(#laser-glow)" stroke-width="2.5" class="anim-laser" />

  <!-- ======================================================================== -->
  <!-- BOTTOM TACTICAL FOOTER & LEGEND                                          -->
  <!-- ======================================================================== -->
  <line x1="12" y1="195" x2="808" y2="195" stroke="#16253B" stroke-width="1" />

  <!-- Legend Items -->
  <g id="memory-tier-legend" transform="translate(24, 208)">
    <text x="0" y="9" class="mono micro-dim">TIERS:</text>

    <!-- Tier 0 -->
    <rect x="42" y="1" width="8" height="8" rx="1.5" fill="#0E1726" stroke="#16253B" stroke-width="0.8" />
    <text x="54" y="9" class="mono micro-dim">0</text>

    <!-- Tier 1 -->
    <rect x="74" y="1" width="8" height="8" rx="1.5" fill="#004D66" stroke="#007799" stroke-width="0.8" />
    <text x="86" y="9" class="mono micro-dim">1-5</text>

    <!-- Tier 2 -->
    <rect x="114" y="1" width="8" height="8" rx="1.5" fill="#0088A8" stroke="#00C2EB" stroke-width="0.8" />
    <text x="126" y="9" class="mono micro-dim">6-10</text>

    <!-- Tier 3 -->
    <rect x="160" y="1" width="8" height="8" rx="1.5" fill="#00D0EB" stroke="#80F7FF" stroke-width="0.8" />
    <text x="172" y="9" class="mono micro-dim">11-15</text>

    <!-- Tier 4 -->
    <rect x="212" y="1" width="8" height="8" rx="1.5" fill="#FFB000" stroke="#FFD166" stroke-width="0.8" />
    <text x="224" y="9" class="mono val-amber" font-size="9">16+ PEAK</text>
  </g>

  <!-- Integrity & Status Checksum -->
  <text x="500" y="217" class="mono micro-dim">CHECKSUM: CRC32//VALID</text>
  <text x="660" y="217" class="mono val-emerald">PARITY: 100% SYNCHRONIZED</text>
</svg>'''
    return svg_content


# ==============================================================================
# 3. MISSION-PAYLOADS RENDERER (820 x 400)
# ==============================================================================

# Architectural visual schematics definition per slot
MODULE_SCHEMATICS = {
    "heneoxy": {
        "slot": "MOD-01",
        "classification": "FLAGSHIP",
        "bus_flow": "PROMPT → AGENT GRAPH → LOCAL BUS",
        "card_x": 16,
        "card_y": 48,
        "border_color": "#FFB000",
        "header_fill": "#141E15",
        "badge_border": "#FFB000",
        "badge_bg": "#2E1C00",
        "badge_color": "val-amber",
        "status_beacon": "#FFB000",
        "is_verified": False,
        "fallback_target": "STATUS: CORE FIRMWARE ACTIVE · LOCAL DEV",
    },
    "coalintel": {
        "slot": "MOD-02",
        "classification": "INTELLIGENCE",
        "bus_flow": "SATELLITE DATA → ETL PIPELINE → PREDICTIONS",
        "card_x": 416,
        "card_y": 48,
        "border_color": "#00E599",
        "header_fill": "#0A1F18",
        "badge_border": "#00E599",
        "badge_bg": "#072216",
        "badge_color": "val-emerald",
        "status_beacon": "#00E599",
        "is_verified": True,
        "fallback_target": "TARGET: github.com/HenilLol/COALINTEL (LIVE)",
    },
    "fluxdock": {
        "slot": "MOD-03",
        "classification": "SYSTEMS",
        "bus_flow": "CAMERA INPUT → OPENCV → MOTOR PWM LOOPS",
        "card_x": 16,
        "card_y": 218,
        "border_color": "#1E2D44",
        "header_fill": "#0A1424",
        "badge_border": "#00F0FF",
        "badge_bg": "#09182A",
        "badge_color": "val-cyan",
        "status_beacon": "#00F0FF",
        "is_verified": False,
        "fallback_target": "STATUS: HARDWARE TESTBENCH // ACTIVE R&amp;D",
    },
    "recyclens": {
        "slot": "MOD-04",
        "classification": "NEURAL MODEL",
        "bus_flow": "IMAGE TENSOR → RESNET INFERENCE → DISPATCH",
        "card_x": 416,
        "card_y": 218,
        "border_color": "#00E599",
        "header_fill": "#0A1F18",
        "badge_border": "#00E599",
        "badge_bg": "#072216",
        "badge_color": "val-emerald",
        "status_beacon": "#00E599",
        "is_verified": True,
        "fallback_target": "TARGET: github.com/HenilLol/RECYCLENS (LIVE)",
    },
}


def render_mission_payloads_svg(projects_data: dict) -> str:
    """
    Renders assets/mission-payloads.svg (820 x 400).
    Renders Henil's 4 engineering projects as aerospace flight modules
    with technical flow diagrams, status beacons, and verified repo indicators.
    Dynamically maps project metadata from projects_data.
    """
    projects_list = projects_data.get("projects", [])
    num_projects = len(projects_list)
    muted_color = THEME_V3.get("text_muted", "#6E86AA")

    # Render module cards dynamically
    modules_svg_blocks = []

    def xml_esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    for p in projects_list:
        p_id = p.get("id", "").lower()
        schematic = MODULE_SCHEMATICS.get(p_id)
        if not schematic:
            continue

        slot_label = schematic["slot"]
        class_label = schematic["classification"]
        bus_flow = schematic["bus_flow"]
        card_x = schematic["card_x"]
        card_y = schematic["card_y"]
        border_col = schematic["border_color"]
        header_fill = schematic["header_fill"]

        name = xml_esc(p.get("name", p_id.upper()))
        desc = p.get("description", "")
        raw_l1, raw_l2 = split_description_lines(desc, max_chars=54)
        desc_l1 = xml_esc(raw_l1)
        desc_l2 = xml_esc(raw_l2)
        status = xml_esc(p.get("status", "ACTIVE"))
        stack = [xml_esc(s) for s in p.get("stack", [])]
        repo = xml_esc(p.get("repository", ""))
        is_verified = schematic["is_verified"]

        # Determine badge and target strings
        if is_verified and repo:
            badge_text = "VERIFIED REPO"
            badge_col = "val-emerald"
            badge_bg = "#072216"
            badge_border = "#00E599"
            beacon_col = "#00E599"
            target_str = f"TARGET: github.com/{repo} (LIVE)"
            target_color_class = "val-emerald"
        else:
            badge_text = status
            badge_col = schematic["badge_color"]
            badge_bg = schematic["badge_bg"]
            badge_border = schematic["badge_border"]
            beacon_col = schematic["status_beacon"]
            target_str = schematic["fallback_target"]
            target_color_class = "micro-dim"

        # Dynamically build stack tags
        stack_pills_svg = []
        curr_x = 0
        for tag in stack[:3]:
            tag_width = max(38, len(tag) * 8 + 14)
            stack_pills_svg.append(f'<rect x="{curr_x}" y="0" width="{tag_width}" height="15" rx="3" fill="#0A1826" stroke="#1E3554" stroke-width="0.8" />')
            stack_pills_svg.append(f'<text x="{curr_x + 7}" y="11" class="mono val-cyan" font-size="9">{tag}</text>')
            curr_x += tag_width + 6
        stack_block = "\n      ".join(stack_pills_svg)

        # Module block
        mod_block = f'''  <!-- {slot_label}: {name} (x={card_x}, y={card_y}, w=388, h=160) -->
  <g id="mod-{p_id}">
    <rect x="{card_x}" y="{card_y}" width="388" height="160" rx="6" fill="url(#card-bg-grad)" stroke="{border_col}" stroke-width="1.2" />
    <rect x="{card_x}" y="{card_y}" width="388" height="24" rx="6" fill="{header_fill}" />
    <line x1="{card_x}" y1="{card_y + 24}" x2="{card_x + 388}" y2="{card_y + 24}" stroke="#1E2D44" stroke-width="1" />

    <!-- Top Bar -->
    <text x="{card_x + 10}" y="{card_y + 16}" class="mono {badge_col}" font-size="10.5">{slot_label} // {class_label}</text>
    <rect x="{card_x + 258}" y="{card_y + 4}" width="120" height="16" rx="8" fill="{badge_bg}" stroke="{badge_border}" stroke-width="0.8" />
    <circle cx="{card_x + 268}" cy="{card_y + 12}" r="3" fill="{beacon_col}" class="anim-beacon" />
    <text x="{card_x + 276}" y="{card_y + 15}" class="mono {badge_col}" font-size="9">{badge_text}</text>

    <!-- Title & Class -->
    <text x="{card_x + 10}" y="{card_y + 45}" class="mono mod-title">{name}</text>
    <text x="{card_x + 100}" y="{card_y + 45}" class="mono micro-dim">[{class_label}]</text>

    <!-- Dynamic Description Lines -->
    <text x="{card_x + 10}" y="{card_y + 62}" class="mono desc-text">{desc_l1}</text>
    <text x="{card_x + 10}" y="{card_y + 75}" class="mono desc-text">{desc_l2}</text>

    <!-- Stack Pills -->
    <g transform="translate({card_x + 10}, {card_y + 86})">
      {stack_block}
    </g>

    <!-- Subsystem Flow Architecture -->
    <text x="{card_x + 10}" y="{card_y + 119}" class="mono micro-dim">BUS:</text>
    <text x="{card_x + 40}" y="{card_y + 119}" class="mono val-titanium" font-size="9">{bus_flow}</text>

    <!-- Hardware Status Footer -->
    <line x1="{card_x + 10}" y1="{card_y + 130}" x2="{card_x + 378}" y2="{card_y + 130}" stroke="#16253B" stroke-width="0.8" />
    <text x="{card_x + 10}" y="{card_y + 145}" class="mono {target_color_class}" font-size="9">{target_str}</text>
  </g>'''
        modules_svg_blocks.append(mod_block)

    all_modules_content = "\n\n".join(modules_svg_blocks)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 400" width="820" height="400" role="img" aria-labelledby="payload-title payload-desc">
  <title id="payload-title">Henil Patel - Mission Payloads Subsystem Registry</title>
  <desc id="payload-desc">Subsystem architecture flight deck for Henil Patel's four engineering projects: Heneoxy, CoalIntel, FluxDock, and RecycLens with verified repository telemetry.</desc>
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="payload-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#04070D" />
      <stop offset="50%" stop-color="#060C16" />
      <stop offset="100%" stop-color="#091322" />
    </linearGradient>

    <!-- Card Background Gradient -->
    <linearGradient id="card-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A1322" />
      <stop offset="100%" stop-color="#0D1A2D" />
    </linearGradient>

    <!-- Glowing Beacon Filter -->
    <filter id="beacon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .mono {{ font-family: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .title-primary {{ fill: #F0F6FC; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; }}
    .title-sub {{ fill: #8B9BB4; font-size: 10.5px; }}
    .mod-title {{ fill: #F0F6FC; font-size: 13px; font-weight: 800; letter-spacing: 1px; }}
    .val-cyan {{ fill: #00F0FF; font-size: 11px; font-weight: 700; }}
    .val-amber {{ fill: #FFB000; font-size: 11px; font-weight: 700; }}
    .val-emerald {{ fill: #00E599; font-size: 11px; font-weight: 700; }}
    .label-muted {{ fill: #8B9BB4; font-size: 9.5px; font-weight: 600; }}
    .desc-text {{ fill: #8B9BB4; font-size: 10px; line-height: 1.4; }}
    .micro-dim {{ fill: {muted_color}; font-size: 9px; }}

    /* Pulsing Beacons */
    @keyframes pulseBeacon {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
    }}
    .anim-beacon {{ animation: pulseBeacon 2s ease-in-out infinite; }}

    /* Prefers Reduced Motion Safety */
    @media (prefers-reduced-motion: reduce) {{
      .anim-beacon {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0.5" y="0.5" width="819" height="399" rx="8" fill="url(#payload-bg-grad)" stroke="#1E2D44" stroke-width="1" />

  <!-- Header Bar -->
  <rect x="1" y="1" width="818" height="36" rx="7" fill="#0A1220" />
  <line x1="1" y1="37" x2="819" y2="37" stroke="#1E2D44" stroke-width="1" />

  <text x="20" y="23" class="mono title-primary">SUBSYSTEM ARCHITECTURE</text>
  <text x="245" y="23" class="mono title-sub">// PRIMARY MISSION PAYLOADS REGISTRY</text>
  <text x="635" y="23" class="mono val-cyan" font-size="10.5">{num_projects} NODES REGISTERED</text>

  <!-- ======================================================================== -->
  <!-- 2 × 2 SUBSYSTEM MODULE MATRIX                                            -->
  <!-- ======================================================================== -->
{all_modules_content}

  <!-- ======================================================================== -->
  <!-- INTER-MODULE BUS TRACE LINE                                              -->
  <!-- ======================================================================== -->
  <line x1="20" y1="388" x2="800" y2="388" stroke="#16253B" stroke-width="1" />
  <circle cx="210" cy="388" r="2" fill="#00F0FF" />
  <circle cx="610" cy="388" r="2" fill="#00E599" />
  <text x="220" y="392" class="mono micro-dim">PAYLOAD_BUS: ALL SUBSYSTEMS MAPPED TO KERNEL V3 ARCHITECTURE</text>
</svg>'''
    return svg_content


# ==============================================================================
# MAIN RENDER ENTRY POINT
# ==============================================================================

def main():
    print("=" * 60)
    print("HENILLOL V3 — CYBERNETIC AVIONICS SVG RENDERER")
    print("=" * 60)

    # Load dynamic data
    if not CONTRIBUTIONS_PATH.exists():
        print(f"Error: Missing {CONTRIBUTIONS_PATH}")
        sys.exit(1)
    if not PROJECTS_PATH.exists():
        print(f"Error: Missing {PROJECTS_PATH}")
        sys.exit(1)

    with open(CONTRIBUTIONS_PATH, "r", encoding="utf-8") as f:
        contributions_data = json.load(f)

    with open(PROJECTS_PATH, "r", encoding="utf-8") as f:
        projects_data = json.load(f)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Render assets/heneoxy-core.svg
    heneoxy_core_path = ASSETS_DIR / "heneoxy-core.svg"
    heneoxy_svg = "\n".join(line.rstrip() for line in render_heneoxy_core_svg(contributions_data, projects_data).splitlines()) + "\n"
    with open(heneoxy_core_path, "w", encoding="utf-8") as f:
        f.write(heneoxy_svg)
    print(f"[OK] Generated {heneoxy_core_path} ({len(heneoxy_svg)} bytes)")

    # 2. Render assets/chrono-synapse.svg
    chrono_synapse_path = ASSETS_DIR / "chrono-synapse.svg"
    synapse_svg = "\n".join(line.rstrip() for line in render_chrono_synapse_svg(contributions_data).splitlines()) + "\n"
    with open(chrono_synapse_path, "w", encoding="utf-8") as f:
        f.write(synapse_svg)
    print(f"[OK] Generated {chrono_synapse_path} ({len(synapse_svg)} bytes)")

    # 3. Render assets/mission-payloads.svg
    mission_payloads_path = ASSETS_DIR / "mission-payloads.svg"
    payloads_svg = "\n".join(line.rstrip() for line in render_mission_payloads_svg(projects_data).splitlines()) + "\n"
    with open(mission_payloads_path, "w", encoding="utf-8") as f:
        f.write(payloads_svg)
    print(f"[OK] Generated {mission_payloads_path} ({len(payloads_svg)} bytes)")

    print("-" * 60)
    print("Validating XML syntax on generated V3 assets...")
    for p in [heneoxy_core_path, chrono_synapse_path, mission_payloads_path]:
        try:
            tree = ET.parse(p)
            root = tree.getroot()
            if not root.tag.endswith("svg"):
                raise ValueError(f"Root tag {root.tag} is not <svg>")
            print(f"[VALID XML] {p.name}")
        except Exception as e:
            print(f"[ERROR] Failed parsing {p.name}: {e}")
            sys.exit(1)

    print("=" * 60)
    print("V3 SVG RENDERING COMPLETE — ALL ASSETS VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
