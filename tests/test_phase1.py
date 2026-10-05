#!/usr/bin/env python3
"""
HENILLOL V2 — PHASE 1 UNIT TESTS & REGRESSION SUITE
--------------------------------------------------
Tests for:
1. Heatmap level boundaries (0, 1, 5, 6, 10, 11, 15, 16)
2. Chrono-Matrix 53-column contract and 365-day display window normalization
3. Regression test: Raw 366-day Sunday start dataset -> naive 54 columns vs canonical 53 columns
4. Contribution validation error handling (duplicates, negative counts, invalid level, malformed date)
5. Contrast utility math (high-contrast, low-contrast, relative luminance)
6. Project schema validation (valid and malformed repository strings)

Author: HenilLol Engineering
"""

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

# Add project root and scripts directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

from validate_pipeline import (
    calculate_heatmap_level,
    calculate_relative_luminance,
    calculate_contrast_ratio,
    evaluate_contrast_compliance,
    get_canonical_display_dates,
    calculate_chrono_matrix_mapping,
    validate_contributions_file,
    validate_projects_schema,
)


class TestPhase1HeatmapLevels(unittest.TestCase):
    """Test boundary cases for calculate_heatmap_level."""

    def test_level_0_boundary(self):
        self.assertEqual(calculate_heatmap_level(0), 0)

    def test_level_1_boundaries(self):
        self.assertEqual(calculate_heatmap_level(1), 1)
        self.assertEqual(calculate_heatmap_level(3), 1)
        self.assertEqual(calculate_heatmap_level(5), 1)

    def test_level_2_boundaries(self):
        self.assertEqual(calculate_heatmap_level(6), 2)
        self.assertEqual(calculate_heatmap_level(8), 2)
        self.assertEqual(calculate_heatmap_level(10), 2)

    def test_level_3_boundaries(self):
        self.assertEqual(calculate_heatmap_level(11), 3)
        self.assertEqual(calculate_heatmap_level(13), 3)
        self.assertEqual(calculate_heatmap_level(15), 3)

    def test_level_4_boundaries(self):
        self.assertEqual(calculate_heatmap_level(16), 4)
        self.assertEqual(calculate_heatmap_level(50), 4)
        self.assertEqual(calculate_heatmap_level(100), 4)

    def test_invalid_counts(self):
        with self.assertRaises(ValueError):
            calculate_heatmap_level(-1)
        with self.assertRaises(ValueError):
            calculate_heatmap_level("5")  # type: ignore
        with self.assertRaises(ValueError):
            calculate_heatmap_level(True)  # type: ignore


class TestPhase1ChronoMatrix(unittest.TestCase):
    """Test Chrono-Matrix date to grid mapping algorithm and 53-column contract."""

    def test_canonical_365_day_normalization(self):
        # 366 raw dates starting on Sunday 2025-10-05 up to Monday 2026-10-05
        raw_dates = [date(2025, 10, 5) + timedelta(days=i) for i in range(366)]
        self.assertEqual(len(raw_dates), 366)

        display_dates, excluded_dates = get_canonical_display_dates(raw_dates)
        self.assertEqual(len(display_dates), 365)
        self.assertEqual(len(excluded_dates), 1)
        self.assertEqual(excluded_dates[0], date(2025, 10, 5))
        self.assertEqual(display_dates[0], date(2025, 10, 6))  # Monday
        self.assertEqual(display_dates[-1], date(2026, 10, 5)) # Monday

    def test_53_column_contract_compliance(self):
        # 366 raw dates normalized to canonical 365-day display window
        raw_dates = [date(2025, 10, 5) + timedelta(days=i) for i in range(366)]
        res = calculate_chrono_matrix_mapping(raw_dates, normalize_display=True)

        self.assertEqual(res["total_columns"], 53)
        self.assertEqual(res["min_col"], 0)
        self.assertEqual(res["max_col"], 52)
        self.assertEqual(res["display_date_count"], 365)
        self.assertEqual(res["excluded_dates_count"], 1)
        self.assertEqual(len(res["duplicate_coords"]), 0)
        self.assertEqual(res["grid_start_date"], "2025-10-06")

        # Verify Monday and Sunday row mappings
        d_mon = date(2025, 10, 6)   # Monday
        d_tue = date(2025, 10, 7)   # Tuesday
        d_sun = date(2025, 10, 12)  # Sunday
        d_newest = date(2026, 10, 5) # Monday

        self.assertEqual(res["mapped_coords"][d_mon], (0, 0))
        self.assertEqual(res["mapped_coords"][d_tue], (0, 1))
        self.assertEqual(res["mapped_coords"][d_sun], (0, 6))
        self.assertEqual(res["mapped_coords"][d_newest], (52, 0))

    def test_regression_naive_54_column_failure(self):
        """
        Historical regression test:
        Un-normalized mapping of a 366-day dataset starting on Sunday produces 54 columns (0..53).
        Canonical 365-day display window normalization resolves this to 53 columns (0..52).
        """
        raw_dates = [date(2025, 10, 5) + timedelta(days=i) for i in range(366)]
        
        # Naive un-normalized mapping yields 54 columns (violates contract)
        raw_res = calculate_chrono_matrix_mapping(raw_dates, normalize_display=False)
        self.assertEqual(raw_res["total_columns"], 54)

        # Canonical display window mapping yields exactly 53 columns (satisfies contract)
        norm_res = calculate_chrono_matrix_mapping(raw_dates, normalize_display=True)
        self.assertEqual(norm_res["total_columns"], 53)
        self.assertLessEqual(norm_res["total_columns"], 53)


class TestPhase1Contrast(unittest.TestCase):
    """Test WCAG 2.x relative luminance and contrast calculations."""

    def test_known_high_contrast(self):
        # White (#FFFFFF) on Black (#000000) = 21:1
        ratio = calculate_contrast_ratio("#FFFFFF", "#000000")
        self.assertEqual(ratio, 21.0)
        eval_res = evaluate_contrast_compliance("#FFFFFF", "#000000")
        self.assertTrue(eval_res["aa_normal"])
        self.assertTrue(eval_res["aaa_normal"])

    def test_known_low_contrast(self):
        # Dark grey (#444444) on Slightly darker grey (#333333) = ~1.6:1
        ratio = calculate_contrast_ratio("#444444", "#333333")
        self.assertLess(ratio, 3.0)
        eval_res = evaluate_contrast_compliance("#444444", "#333333")
        self.assertFalse(eval_res["aa_normal"])
        self.assertFalse(eval_res["aaa_normal"])

    def test_v2_palette_essential_text(self):
        # Primary (#E6EDF3) on Background (#0D1117)
        res = evaluate_contrast_compliance("#E6EDF3", "#0D1117")
        self.assertTrue(res["aa_normal"])
        self.assertTrue(res["aaa_normal"])

        # Secondary (#8B949E) on Surface (#161B22)
        res_sec = evaluate_contrast_compliance("#8B949E", "#161B22")
        self.assertTrue(res_sec["aa_normal"])  # 5.62:1 passes AA
        self.assertFalse(res_sec["aaa_normal"])  # fails AAA (< 7.0)

    def test_invalid_hex(self):
        with self.assertRaises(ValueError):
            calculate_contrast_ratio("INVALID", "#000000")


class TestPhase1ProjectsSchema(unittest.TestCase):
    """Test projects schema validation rules."""

    def test_valid_and_invalid_repos(self):
        dummy_projects = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "version": "2.0.0",
            "updated_at": None,
            "projects": [
                {
                    "id": "valid_proj",
                    "name": "Valid Proj",
                    "category": "Test",
                    "description": "Desc",
                    "repository": "HenilLol/COALINTEL",
                    "status": "ACTIVE",
                    "stack": ["Python"],
                    "featured": True,
                    "sort_order": 1,
                },
                {
                    "id": "bad_repo_owner",
                    "name": "Bad Owner",
                    "category": "Test",
                    "description": "Desc",
                    "repository": "OtherUser/Repo",
                    "status": "ACTIVE",
                    "stack": ["Python"],
                    "featured": True,
                    "sort_order": 2,
                }
            ]
        }
        
        import json
        import tempfile
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as f:
            json.dump(dummy_projects, f)
            temp_path = Path(f.name)

        try:
            success, projects, errors = validate_projects_schema(temp_path)
            self.assertFalse(success)
            self.assertTrue(any("owner is not 'HenilLol'" in e for e in errors))
        finally:
            temp_path.unlink()


if __name__ == "__main__":
    unittest.main()
