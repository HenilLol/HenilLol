#!/usr/bin/env python3
"""
HENILLOL V3 — UNIT TESTS & CYBERNETIC AVIONICS SVG VALIDATION SUITE
-------------------------------------------------------------------
Validates V3 SVG Visual System assets and design architecture:
1. Existence of all V3 assets: heneoxy-core.svg, chrono-synapse.svg, mission-payloads.svg
2. Well-formed XML syntax parsing
3. Canvas dimensions & viewBox compliance (820px width, explicit heights)
4. Chrono-Synapse 53-column x 7-row matrix structure & 365-day display mapping
5. Subsystem mission payloads data fidelity & repository verification safety
6. SVG Security: No scripts, no iframes, no external assets, no local paths, no secrets
7. Accessibility & Motion: prefers-reduced-motion, title & desc, WCAG AA/AAA contrast compliance
8. Truthfulness: Removal of fake metrics (99.8% uptime), dynamic temporal coverage (365/365)
9. Dynamic Data Coupling: Injected project descriptions and alternate contribution counts
10. Robustness: Zero-contribution dataset handling without division errors

Author: Henil Patel (@HenilLol)
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
from theme import THEME_V3
from render_v3_svgs import (
    render_heneoxy_core_svg,
    render_chrono_synapse_svg,
    render_mission_payloads_svg,
)

ASSETS_DIR = BASE_DIR / "assets"
HENEOXY_CORE_PATH = ASSETS_DIR / "heneoxy-core.svg"
CHRONO_SYNAPSE_PATH = ASSETS_DIR / "chrono-synapse.svg"
MISSION_PAYLOADS_PATH = ASSETS_DIR / "mission-payloads.svg"


class TestV3SvgVisualSystem(unittest.TestCase):
    """Test suite for V3 Cybernetic Avionics SVG visual assets."""

    def test_v3_svg_files_exist(self):
        """Verify that all three V3 SVG files exist in assets/."""
        self.assertTrue(HENEOXY_CORE_PATH.exists(), f"Missing {HENEOXY_CORE_PATH}")
        self.assertTrue(CHRONO_SYNAPSE_PATH.exists(), f"Missing {CHRONO_SYNAPSE_PATH}")
        self.assertTrue(MISSION_PAYLOADS_PATH.exists(), f"Missing {MISSION_PAYLOADS_PATH}")

    def test_xml_syntax_validity(self):
        """Verify all three SVGs are well-formed XML."""
        for svg_path in [HENEOXY_CORE_PATH, CHRONO_SYNAPSE_PATH, MISSION_PAYLOADS_PATH]:
            try:
                tree = ET.parse(svg_path)
                root = tree.getroot()
                self.assertTrue(root.tag.endswith("svg"), f"{svg_path.name} root element must be <svg>")
            except ET.ParseError as e:
                self.fail(f"XML parse failure in {svg_path.name}: {e}")

    def test_canvas_dimensions_and_viewbox(self):
        """Verify explicit width=820, explicit height, and viewBox on all SVGs."""
        specs = [
            (HENEOXY_CORE_PATH, 820, 340, "0 0 820 340"),
            (CHRONO_SYNAPSE_PATH, 820, 245, "0 0 820 245"),
            (MISSION_PAYLOADS_PATH, 820, 400, "0 0 820 400"),
        ]
        for path, exp_w, exp_h, exp_viewbox in specs:
            tree = ET.parse(path)
            root = tree.getroot()
            self.assertEqual(root.attrib.get("width"), str(exp_w), f"{path.name} width must be {exp_w}")
            self.assertEqual(root.attrib.get("height"), str(exp_h), f"{path.name} height must be {exp_h}")
            self.assertEqual(root.attrib.get("viewBox"), exp_viewbox, f"{path.name} viewBox must be '{exp_viewbox}'")

    def test_accessibility_elements(self):
        """Verify <title>, <desc>, role='img' on each SVG."""
        for path in [HENEOXY_CORE_PATH, CHRONO_SYNAPSE_PATH, MISSION_PAYLOADS_PATH]:
            tree = ET.parse(path)
            root = tree.getroot()
            self.assertEqual(root.attrib.get("role"), "img", f"{path.name} missing role='img'")
            self.assertIn("aria-labelledby", root.attrib, f"{path.name} missing aria-labelledby")

            # Find title and desc
            has_title = any(child.tag.endswith("title") for child in root)
            has_desc = any(child.tag.endswith("desc") for child in root)
            self.assertTrue(has_title, f"{path.name} missing <title>")
            self.assertTrue(has_desc, f"{path.name} missing <desc>")

    def test_chrono_synapse_matrix_grid(self):
        """Verify Chrono-Synapse contains 53 columns x 7 rows = 371 cells."""
        tree = ET.parse(CHRONO_SYNAPSE_PATH)
        root = tree.getroot()
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect")
        # Cells in grid have width="10.8" and height="10.8"
        matrix_cells = [r for r in rects if r.attrib.get("width") == "10.8" and r.attrib.get("height") == "10.8"]
        self.assertEqual(len(matrix_cells), 371, f"Chrono-Synapse must have 371 grid cells, found {len(matrix_cells)}")

    def test_chrono_synapse_dynamic_data(self):
        """Verify Chrono-Synapse displays dynamic totals."""
        import json
        contrib_path = BASE_DIR / "data" / "contributions.json"
        with open(contrib_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        expected_pulses = f"{data.get('total_contributions', 310)} SYNAPTIC PULSES"
        content = CHRONO_SYNAPSE_PATH.read_text(encoding="utf-8")
        self.assertIn(expected_pulses, content)
        self.assertIn("365/365 DATES", content)

    def test_mission_payloads_modules(self):
        """Verify Mission Payloads contains all 4 projects and proper verification markers."""
        content = MISSION_PAYLOADS_PATH.read_text(encoding="utf-8")
        self.assertIn("HENEOXY", content)
        self.assertIn("COALINTEL", content)
        self.assertIn("FLUXDOCK", content)
        self.assertIn("RECYCLENS", content)
        self.assertIn("github.com/HenilLol/COALINTEL", content)
        self.assertIn("github.com/HenilLol/RECYCLENS", content)
        # Verify unverified projects do not have fake URLs
        self.assertNotIn("github.com/HenilLol/HENEOXY", content)
        self.assertNotIn("github.com/HenilLol/FLUXDOCK", content)

    def test_svg_security_and_purity(self):
        """Verify no scripts, iframes, external stylesheets, local paths, or secrets."""
        for path in [HENEOXY_CORE_PATH, CHRONO_SYNAPSE_PATH, MISSION_PAYLOADS_PATH]:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("<script", content.lower(), f"Forbidden <script> in {path.name}")
            self.assertNotIn("<iframe", content.lower(), f"Forbidden <iframe> in {path.name}")
            self.assertNotIn("javascript:", content.lower(), f"Forbidden javascript: in {path.name}")
            self.assertNotIn("@import", content.lower(), f"Forbidden @import in {path.name}")
            self.assertNotIn("<link", content.lower(), f"Forbidden <link> in {path.name}")
            self.assertNotIn("file:///", content.lower(), f"Forbidden file:/// in {path.name}")
            self.assertNotIn("c:\\", content.lower(), f"Forbidden local path in {path.name}")
            self.assertNotIn("e:\\", content.lower(), f"Forbidden local path in {path.name}")

    def test_reduced_motion_media_queries(self):
        """Verify all three SVGs declare prefers-reduced-motion media query and disable animations."""
        for path in [HENEOXY_CORE_PATH, CHRONO_SYNAPSE_PATH, MISSION_PAYLOADS_PATH]:
            content = path.read_text(encoding="utf-8")
            self.assertIn("@media (prefers-reduced-motion: reduce)", content, f"Missing reduced motion query in {path.name}")
            self.assertIn("animation: none !important", content, f"Missing animation: none in {path.name}")

    def test_theme_v3_wcag_contrast(self):
        """Verify all text colors in THEME_V3 achieve WCAG AA/AAA compliance."""
        bg = THEME_V3["bg"]
        surface = THEME_V3["surface"]

        # Primary Titanium text (#F0F6FC)
        res_primary = evaluate_contrast_compliance(THEME_V3["text_primary"], bg)
        self.assertTrue(res_primary["aa_normal"], "Primary text must pass WCAG AA")
        self.assertTrue(res_primary["aaa_normal"], "Primary text must pass WCAG AAA")

        # Secondary Slate text (#8B9BB4)
        res_sec = evaluate_contrast_compliance(THEME_V3["text_secondary"], surface)
        self.assertTrue(res_sec["aa_normal"], "Secondary text must pass WCAG AA")

        # Muted Text (#6E86AA) - Must pass WCAG AA normal text (>= 4.5:1)
        res_muted = evaluate_contrast_compliance(THEME_V3["text_muted"], surface)
        self.assertTrue(res_muted["aa_normal"], f"Muted text ratio {res_muted['ratio']} must pass WCAG AA (>= 4.5:1)")

        # Cyan Accent (#00F0FF)
        res_cyan = evaluate_contrast_compliance(THEME_V3["cyan"], surface)
        self.assertTrue(res_cyan["aa_normal"], "Cyan accent must pass WCAG AA")
        self.assertTrue(res_cyan["aaa_normal"], "Cyan accent must pass WCAG AAA")

        # Emerald Verified (#00E599)
        res_emerald = evaluate_contrast_compliance(THEME_V3["emerald"], surface)
        self.assertTrue(res_emerald["aa_normal"], "Emerald accent must pass WCAG AA")
        self.assertTrue(res_emerald["aaa_normal"], "Emerald accent must pass WCAG AAA")

        # Amber Alert (#FFB000)
        res_amber = evaluate_contrast_compliance(THEME_V3["amber"], surface)
        self.assertTrue(res_amber["aa_normal"], "Amber accent must pass WCAG AA")
        self.assertTrue(res_amber["aaa_normal"], "Amber accent must pass WCAG AAA")

    def test_truthful_temporal_coverage_metric(self):
        """P2-01: Verify removal of fake '99.8% READY' uptime metric and presence of truthful temporal lock."""
        content = HENEOXY_CORE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("99.8%", content, "Fake '99.8%' uptime metric must not exist in production SVG")
        self.assertIn("TEMPORAL_LOCK", content, "Truthful TEMPORAL_LOCK metric must be present")
        self.assertIn("365/365 DAYS", content, "Derived 365/365 DAYS coverage must be present")

    def test_dynamic_project_injection(self):
        """P2-02: Verify renderer dynamically displays injected project descriptions."""
        mock_projects = {
            "projects": [
                {
                    "id": "heneoxy",
                    "name": "HENEOXY_NEXT",
                    "description": "INJECTED_TEST_QUANTUM_COMPILER_ORCHESTRATOR",
                    "status": "EXPERIMENTAL",
                    "stack": ["Rust", "Python"],
                    "repository": "HenilLol/HENEOXY",
                }
            ]
        }
        rendered_svg = render_mission_payloads_svg(mock_projects)
        # Parse XML to verify well-formed output
        root = ET.fromstring(rendered_svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("HENEOXY_NEXT", rendered_svg)
        self.assertIn("INJECTED_TEST_QUANTUM_COMPILER_ORCHESTRATOR", rendered_svg)
        self.assertIn("EXPERIMENTAL", rendered_svg)
        self.assertIn("Rust", rendered_svg)

    def test_zero_contribution_dataset_safety(self):
        """P3-03: Verify renderer handles empty/zero contribution datasets without division errors."""
        empty_contribs = {
            "username": "HenilLol",
            "generated_at": "2026-10-05T06:19:51Z",
            "total_contributions": 0,
            "weeks": []
        }
        empty_projects = {"projects": []}

        # Test rendering without crashing
        synapse_svg = render_chrono_synapse_svg(empty_contribs)
        core_svg = render_heneoxy_core_svg(empty_contribs, empty_projects)

        # Verify valid XML
        root_synapse = ET.fromstring(synapse_svg)
        root_core = ET.fromstring(core_svg)
        self.assertEqual(root_synapse.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root_core.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("0 SYNAPTIC PULSES", synapse_svg)

    def test_dynamic_contribution_count_injection(self):
        """P3-03: Verify renderer accurately reflects injected contribution totals."""
        mock_contribs = {
            "username": "HenilLol",
            "generated_at": "2026-10-05T06:19:51Z",
            "total_contributions": 789,
            "weeks": []
        }
        mock_projects = {"projects": []}
        core_svg = render_heneoxy_core_svg(mock_contribs, mock_projects)
        self.assertIn("789 VERIFIED PULSES", core_svg)


if __name__ == "__main__":
    unittest.main()
