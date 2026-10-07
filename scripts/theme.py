"""
Design System Tokens for HenilLol GitHub Profile SVG Assets.

Visual Direction:
Editorial Terminal x Minimalism x Engineering
Monochrome-first with one restrained cyan/teal accent.
"""

from typing import Dict, Any

THEME: Dict[str, Any] = {
    # Color Palette
    "bg": "#0D1117",            # Canvas near-black background
    "surface": "#161B22",       # Terminal box surface
    "surface_subtle": "#12171F",# Recessed container surface
    "border": "#30363D",        # Subtle window border
    "border_subtle": "#21262D", # Extremely subtle divider line
    
    # Typography Colors
    "text_primary": "#E6EDF3",  # High contrast crisp white/gray
    "text_secondary": "#8B949E",# Muted text for labels / subheadings
    "text_dim": "#484F58",      # Dim text for comments / borders
    
    # Accent Color System (Restrained Cyan / Teal)
    "accent": "#00C7B7",        # Primary teal accent
    "accent_dim": "#005F56",    # Muted teal for secondary accents
    "accent_subtle": "rgba(0, 199, 183, 0.10)", # Low opacity highlight
    
    # Typography Stack
    "font_mono": 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace',
    
    # Heatmap Level Colors (0 = Empty, 1-4 = Increasing Intensity)
    "heatmap_levels": [
        "#161B22",  # Level 0 (no activity)
        "#04383F",  # Level 1 (subtle teal)
        "#005F56",  # Level 2 (medium teal)
        "#008C7E",  # Level 3 (bright teal)
        "#00C7B7",  # Level 4 (primary accent teal)
    ]
}

# ==============================================================================
# V3 DESIGN SYSTEM: HENEOXY KERNEL // CYBERNETIC AVIONICS
# ==============================================================================
THEME_V3: Dict[str, Any] = {
    # Deep space void & avionics surface chassis
    "bg": "#050811",              # Cosmic void deep background
    "bg_gradient_start": "#04070D",
    "bg_gradient_end": "#0A1220",
    "surface": "#0C1424",         # Primary avionics module surface
    "surface_recessed": "#070D18",# Recessed instruments bay
    "surface_elevated": "#121E32",# Elevated tactical HUD card

    # Hairline structural borders & grid traces
    "border": "#1E2D44",          # Standard module chassis border
    "border_active": "#00F0FF",   # Illuminated cyan data bus border
    "border_subtle": "#111B2C",   # Hairline schematic grid traces
    "border_amber": "#FFB000",    # Warning/active build border
    "border_emerald": "#00E599",  # Verified hardware lock border

    # High-contrast WCAG AAA typography
    "text_primary": "#F0F6FC",    # Titanium white (18.4:1 contrast)
    "text_secondary": "#8B9BB4",  # Slate avionics readout (6.8:1 contrast)
    "text_muted": "#6E86AA",      # Micro-calibration index markings (4.95:1 WCAG AA)

    # Cybernetic Accents
    "cyan": "#00F0FF",            # Electric avionics cyan (13.5:1 contrast)
    "amber": "#FFB000",           # Neural amber alert/building status (10.8:1 contrast)
    "emerald": "#00E599",         # Quantum emerald telemetry lock (12.4:1 contrast)
    "ruby": "#FF3B69",            # Subsystem alert / critical telemetry

    # Typography Stack
    "font_mono": 'ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, "Liberation Mono", monospace',

    # V3 Temporal Memory Bus Heatmap Tiers
    "heatmap_levels": [
        "#0E1726",  # Level 0 (Dormant cell)
        "#004D66",  # Level 1 (Tier-1 pulse)
        "#0088A8",  # Level 2 (Tier-2 kinetic)
        "#00D0EB",  # Level 3 (Tier-3 radiant cyan)
        "#FFB000",  # Level 4 (Hyper-burst neural amber)
    ],
    "heatmap_borders": [
        "#16253B",  # Level 0 border
        "#007799",  # Level 1 border
        "#00C2EB",  # Level 2 border
        "#80F7FF",  # Level 3 border
        "#FFD166",  # Level 4 border
    ]
}
