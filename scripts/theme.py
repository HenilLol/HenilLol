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
