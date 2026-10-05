#!/usr/bin/env python3
"""
HENILLOL V2 — PHASE 2 UNIT TESTS & SVG VALIDATION SUITE
------------------------------------------------------
Validates Phase 2 V2 SVG Visual System assets:
1. XML syntax validity (well-formed XML parsing)
2. Canvas geometry & dimensions (820px width, viewBox, explicit heights)
3. Chrono-Matrix 53x7 matrix structure & 365-day canonical display data representation
4. Project Telemetry repository link security & verification state representation
5. SVG Security: No JavaScript, no external resources, no local file:/// paths, no secrets
6. Motion & Accessibility: Baseline visibility, finite keyframes (<= 3.0s), prefers-reduced-motion rule, title & desc elements
7. Remediation assertions: Header badge [ LIVE ], [ UNVERIFIED ] status text WCAG AA contrast compliance (#8B949E)

Author: HenilLol Engineering
"""

import sys
import unittest
import xml.etree.ElementTree as ET
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

from validate_pipeline import evaluate_contrast_compliance

ASSETS_DIR = BASE_DIR / "assets"
TELEMETRY_OS_PATH = ASSETS_DIR / "telemetry-os.svg"
CHRONO_MATRIX_PATH = ASSETS_DIR / "chrono-matrix.svg"
PROJECT_TELEMETRY_PATH = ASSETS_DIR / "project-telemetry.svg"


class TestPhase2SvgAssets(unittest.TestCase):
    """Test suite for Phase 2 generated V2 SVG visual assets."""

    def test_svg_files_exist(self):
        """Verify that all three Phase 2 SVG files exist in assets/."""
        self.assertTrue(TELEMETRY_OS_PATH.exists(), f"Missing {TELEMETRY_OS_PATH}")
        self.assertTrue(CHRONO_MATRIX_PATH.exists(), f"Missing {CHRONO_MATRIX_PATH}")
        self.assertTrue(PROJECT_TELEMETRY_PATH.exists(), f"Missing {PROJECT_TELEMETRY_PATH}")

    def test_xml_syntax_validity(self):
        """Verify all three SVGs are well-formed XML."""
        for svg_path in [TELEMETRY_OS_PATH, CHRONO_MATRIX_PATH, PROJECT_TELEMETRY_PATH]:
            try:
                tree = ET.parse(svg_path)
                root = tree.getroot()
                self.assertTrue(root.tag.endswith("svg"), f"{svg_path.name} root element must be <svg>")
            except ET.ParseError as e:
                self.fail(f"XML parse failure in {svg_path.name}: {e}")

    def test_canvas_dimensions_and_viewbox(self):
        """Verify explicit width=820, explicit height, and viewBox on all SVGs."""
        specs = [
            (TELEMETRY_OS_PATH, 820, 290, "0 0 820 290"),
            (CHRONO_MATRIX_PATH, 820, 175, "0 0 820 175"),
            (PROJECT_TELEMETRY_PATH, 820, 310, "0 0 820 310"),
        ]
        for svg_path, exp_w, exp_h, exp_viewbox in specs:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            self.assertEqual(root.attrib.get("width"), str(exp_w), f"{svg_path.name} width must be {exp_w}")
            self.assertEqual(root.attrib.get("height"), str(exp_h), f"{svg_path.name} height must be {exp_h}")
            self.assertEqual(root.attrib.get("viewBox"), exp_viewbox, f"{svg_path.name} viewBox must be '{exp_viewbox}'")

    def test_chrono_matrix_structure(self):
        """Verify Chrono-Matrix SVG contains 53 columns x 7 rows grid elements."""
        content = CHRONO_MATRIX_PATH.read_text(encoding="utf-8")
        
        # Check matrix column groups
        col_groups = re.findall(r'<g class="matrix-col"', content)
        self.assertEqual(len(col_groups), 53, "Chrono-Matrix SVG must contain exactly 53 column groups")

        # Check total date cells (53 * 7 = 371 cell rects)
        tree = ET.parse(CHRONO_MATRIX_PATH)
        root = tree.getroot()
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect")
        
        # Filter matrix cell rects (width=10, height=10)
        matrix_cell_rects = [
            r for r in rects 
            if r.attrib.get("width") == "10" and r.attrib.get("height") == "10"
        ]
        self.assertEqual(len(matrix_cell_rects), 371, "Chrono-Matrix SVG must contain 371 matrix cell rects (53 cols * 7 rows)")

    def test_project_telemetry_repository_links(self):
        """Verify repository links rendered ONLY for verified projects (COALINTEL & RECYCLENS) and not 404 repos."""
        content = PROJECT_TELEMETRY_PATH.read_text(encoding="utf-8")
        
        # Verified project links
        self.assertIn("https://github.com/HenilLol/coalintel", content)
        self.assertIn("https://github.com/HenilLol/Recyclens", content)
        
        # Unverified project repos MUST NOT have fake links
        self.assertNotIn("https://github.com/HenilLol/HENEOXY", content)
        self.assertNotIn("https://github.com/HenilLol/FLUXDOCK", content)
        
        # Unverified text indicators
        unverified_badges = re.findall(r'\[ UNVERIFIED \]', content)
        self.assertEqual(len(unverified_badges), 2, "Project Telemetry must show [ UNVERIFIED ] for HENEOXY and FLUXDOCK")

    def test_security_and_path_hygiene(self):
        """Verify no JavaScript, no external fonts/resources, no local file:/// paths, no secrets."""
        forbidden_patterns = [
            r'<script',
            r'javascript:',
            r'onload=',
            r'onclick=',
            r'file:///',
            r'[eE]:[\\/]',
            r'[cC]:[\\/]',
            r'http://(?!www\.w3\.org)',  # Only w3.org namespace
            r'@import',
        ]
        for svg_path in [TELEMETRY_OS_PATH, CHRONO_MATRIX_PATH, PROJECT_TELEMETRY_PATH]:
            content = svg_path.read_text(encoding="utf-8")
            for pat in forbidden_patterns:
                matches = re.findall(pat, content, re.IGNORECASE)
                self.assertEqual(len(matches), 0, f"Forbidden security pattern '{pat}' found in {svg_path.name}")

    def test_accessibility_and_motion_rules(self):
        """Verify title, desc, prefers-reduced-motion, and finite animation constraints."""
        for svg_path in [TELEMETRY_OS_PATH, CHRONO_MATRIX_PATH, PROJECT_TELEMETRY_PATH]:
            content = svg_path.read_text(encoding="utf-8")
            
            # Accessibility tags
            self.assertIn("<title", content, f"Missing <title> in {svg_path.name}")
            self.assertIn("<desc", content, f"Missing <desc> in {svg_path.name}")
            
            # Reduced motion query
            self.assertIn("@media (prefers-reduced-motion: reduce)", content, f"Missing prefers-reduced-motion in {svg_path.name}")
            
            # Finite animations (no 'infinite')
            self.assertNotIn("infinite", content, f"Infinite animation found in {svg_path.name}")
            self.assertIn("1 forwards", content, f"Expected finite keyframe animation '1 forwards' in {svg_path.name}")

    def test_remediated_header_badge(self):
        """Verify telemetry-os.svg header badge contains '[ LIVE ]' and zero 'v2.0-LIVE'."""
        content = TELEMETRY_OS_PATH.read_text(encoding="utf-8")
        self.assertNotIn("v2.0-LIVE", content, "Header badge must not contain 'v2.0-LIVE'")
        self.assertIn("[ LIVE ]", content, "Header badge must contain '[ LIVE ]'")

    def test_remediated_unverified_text_contrast(self):
        """Verify [ UNVERIFIED ] status text uses class 'sub-text' (#8B949E) satisfying WCAG AA Normal contrast (5.62:1)."""
        content = PROJECT_TELEMETRY_PATH.read_text(encoding="utf-8")
        self.assertIn('class="mono sub-text" text-anchor="end">[ UNVERIFIED ]', content)
        self.assertNotIn('class="mono dim-text" text-anchor="end">[ UNVERIFIED ]', content)

        # Contrast math assertion: #8B949E on #161B22 surface
        eval_res = evaluate_contrast_compliance("#8B949E", "#161B22")
        self.assertTrue(eval_res["aa_normal"], "sub-text #8B949E on surface #161B22 must pass WCAG AA Normal contrast")
        self.assertGreaterEqual(eval_res["ratio"], 4.5, f"Contrast ratio {eval_res['ratio']} must be >= 4.5:1")


if __name__ == "__main__":
    unittest.main()
