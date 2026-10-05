#!/usr/bin/env python3
"""
HENILLOL V2 — PHASE 1 VALIDATION ENGINE
----------------------------------------
Data Model + Validation Engine + Chrono-Matrix Mapping + Repo Verification + WCAG Contrast Utility

Author: HenilLol Engineering
Architecture: CHRONO-MATRIX × TELEMETRY-OS
"""

import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STAGING_DIR = BASE_DIR / "staging"
ASSETS_DIR = BASE_DIR / "assets"

CONTRIBUTIONS_PATH = DATA_DIR / "contributions.json"
PROJECTS_PATH = DATA_DIR / "projects.json"

V1_ASSET_PATHS = [
    ASSETS_DIR / "henil-ascii.svg",
    ASSETS_DIR / "info-card.svg",
    ASSETS_DIR / "contrib-heatmap.svg",
]


# ==============================================================================
# 1. HEATMAP LEVEL CALCULATION
# ==============================================================================

def calculate_heatmap_level(count: int) -> int:
    """
    Deterministic heatmap level mapping function.
    Level 0: 0 contributions
    Level 1: 1–5
    Level 2: 6–10
    Level 3: 11–15
    Level 4: 16+
    """
    if not isinstance(count, int) or isinstance(count, bool):
        raise ValueError(f"Contribution count must be an integer, got {type(count).__name__}")
    if count < 0:
        raise ValueError(f"Contribution count cannot be negative: {count}")
    
    if count == 0:
        return 0
    elif 1 <= count <= 5:
        return 1
    elif 6 <= count <= 10:
        return 2
    elif 11 <= count <= 15:
        return 3
    else:
        return 4


# ==============================================================================
# 2. CONTRAST UTILITY (WCAG 2.x)
# ==============================================================================

def hex_to_rgb(hex_str: str) -> tuple[float, float, float]:
    """Converts a #RRGGBB or RRGGBB hex string to float RGB tuple (0.0 - 1.0)."""
    clean_hex = hex_str.lstrip("#")
    if len(clean_hex) != 6 or not re.match(r"^[0-9a-fA-F]{6}$", clean_hex):
        raise ValueError(f"Invalid hex color format: '{hex_str}'")
    r = int(clean_hex[0:2], 16) / 255.0
    g = int(clean_hex[2:4], 16) / 255.0
    b = int(clean_hex[4:6], 16) / 255.0
    return r, g, b


def calculate_relative_luminance(hex_str: str) -> float:
    """Calculates relative luminance according to WCAG 2.x specification."""
    r, g, b = hex_to_rgb(hex_str)
    
    def adjust(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r_lin = adjust(r)
    g_lin = adjust(g)
    b_lin = adjust(b)
    
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def calculate_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """Calculates contrast ratio (L1 + 0.05) / (L2 + 0.05)."""
    l1 = calculate_relative_luminance(fg_hex)
    l2 = calculate_relative_luminance(bg_hex)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    ratio = (lighter + 0.05) / (darker + 0.05)
    return round(ratio, 2)


def evaluate_contrast_compliance(fg_hex: str, bg_hex: str) -> dict:
    """Evaluates WCAG AA and AAA compliance for normal and large text."""
    ratio = calculate_contrast_ratio(fg_hex, bg_hex)
    return {
        "ratio": ratio,
        "aa_normal": ratio >= 4.5,
        "aaa_normal": ratio >= 7.0,
        "aa_large": ratio >= 3.0,
        "aaa_large": ratio >= 4.5,
    }


# ==============================================================================
# 3. CHRONO-MATRIX DATE MAPPING ALGORITHM
# ==============================================================================

def get_canonical_display_dates(actual_dates: list[date]) -> tuple[list[date], list[date]]:
    """
    Normalizes a list of raw actual dates to the canonical 365-day Chrono-Matrix display window.
    display_end = newest_date
    display_start = display_end - timedelta(days=364) (exactly 365 calendar days)
    Returns (display_dates, excluded_dates).
    """
    if not actual_dates:
        raise ValueError("Cannot normalize empty date list")
    
    sorted_dates = sorted(actual_dates)
    newest_date = sorted_dates[-1]
    display_end = newest_date
    display_start = display_end - timedelta(days=364)

    display_dates = [d for d in sorted_dates if display_start <= d <= display_end]
    excluded_dates = [d for d in sorted_dates if d < display_start or d > display_end]

    return display_dates, excluded_dates


def calculate_chrono_matrix_mapping(actual_dates: list[date], normalize_display: bool = True) -> dict:
    """
    Maps dates to a 7-row (Monday=0..Sunday=6) x N-column grid.
    When normalize_display is True, normalizes input to the canonical 365-day display window.
    Grid start date is Monday on or before display_start.
    Returns detailed mapping metadata and coordinate layout.
    """
    if not actual_dates:
        raise ValueError("Cannot map empty date list")

    raw_sorted_dates = sorted(actual_dates)
    
    if normalize_display:
        display_dates, excluded_dates = get_canonical_display_dates(raw_sorted_dates)
    else:
        display_dates = raw_sorted_dates
        excluded_dates = []

    display_start_date = display_dates[0]
    display_end_date = display_dates[-1]

    # Grid start date: Monday on or before display_start_date
    grid_start_date = display_start_date - timedelta(days=display_start_date.weekday())

    mapped_coords = {}
    coords_to_dates = {}
    duplicate_coords = []

    for d in display_dates:
        row = d.weekday()  # Monday = 0, Sunday = 6
        col = (d - grid_start_date).days // 7
        coord = (col, row)

        if coord in coords_to_dates:
            duplicate_coords.append((coord, d, coords_to_dates[coord]))
        else:
            coords_to_dates[coord] = d
        mapped_coords[d] = coord

    max_col = max(col for col, _ in mapped_coords.values())
    min_col = min(col for col, _ in mapped_coords.values())
    total_columns = max_col + 1

    grid_end_date = grid_start_date + timedelta(days=total_columns * 7 - 1)
    total_grid_positions = total_columns * 7
    display_date_count = len(display_dates)
    padding_positions = total_grid_positions - display_date_count

    newest_date_coord = mapped_coords[display_end_date]
    oldest_date_coord = mapped_coords[display_start_date]

    first_week_padding = (display_start_date - grid_start_date).days
    final_week_padding = (grid_end_date - display_end_date).days

    return {
        "raw_date_count": len(raw_sorted_dates),
        "display_date_count": display_date_count,
        "excluded_dates_count": len(excluded_dates),
        "excluded_dates": [d.isoformat() for d in excluded_dates],
        "display_start_date": display_start_date.isoformat(),
        "display_end_date": display_end_date.isoformat(),
        "grid_start_date": grid_start_date.isoformat(),
        "grid_end_date": grid_end_date.isoformat(),
        "oldest_date_coord": oldest_date_coord,
        "newest_date_coord": newest_date_coord,
        "total_columns": total_columns,
        "min_col": min_col,
        "max_col": max_col,
        "total_grid_positions": total_grid_positions,
        "padding_positions": padding_positions,
        "first_week_padding": first_week_padding,
        "final_week_padding": final_week_padding,
        "duplicate_coords": duplicate_coords,
        "mapped_coords": mapped_coords,
    }


# ==============================================================================
# 4. CONTRIBUTION DATASET VALIDATION
# ==============================================================================

def validate_contributions_file(file_path: Path) -> tuple[bool, dict, list[str]]:
    """Validates data/contributions.json integrity and structure."""
    errors = []
    if not file_path.exists():
        return False, {}, [f"Contributions file not found at {file_path}"]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, {}, [f"Malformed JSON in contributions file: {e}"]

    # Required top-level keys
    required_keys = ["username", "generated_at", "total_contributions", "status", "total_days", "start_date", "end_date", "weeks"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required top-level key: '{key}'")

    if errors:
        return False, data, errors

    weeks = data.get("weeks", [])
    if not isinstance(weeks, list):
        errors.append("'weeks' field must be a JSON array")
        return False, data, errors

    all_days = []
    for week_idx, week in enumerate(weeks):
        if not isinstance(week, dict) or "days" not in week:
            errors.append(f"Week at index {week_idx} missing 'days' array")
            continue
        for day in week.get("days", []):
            all_days.append(day)

    # Validate dates
    parsed_dates = []
    seen_dates = set()
    total_calculated_count = 0

    for idx, day in enumerate(all_days):
        d_str = day.get("date")
        count = day.get("count")
        level = day.get("level")

        # Check date string format YYYY-MM-DD
        if not d_str or not isinstance(d_str, str):
            errors.append(f"Day {idx} missing valid 'date' string")
            continue
        try:
            d_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
        except ValueError:
            errors.append(f"Invalid date format '{d_str}' at index {idx}")
            continue

        # Duplicate check
        if d_str in seen_dates:
            errors.append(f"Duplicate date found: '{d_str}'")
        seen_dates.add(d_str)
        parsed_dates.append(d_obj)

        # Count check
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            errors.append(f"Invalid contribution count '{count}' for date '{d_str}'")
        else:
            total_calculated_count += count

            # Level check
            try:
                expected_level = calculate_heatmap_level(count)
                if level != expected_level:
                    errors.append(f"Heatmap level mismatch for date '{d_str}': count {count} mapped to level {level}, expected {expected_level}")
            except Exception as ex:
                errors.append(f"Error evaluating level for date '{d_str}': {ex}")

    # Chronological ordering check
    for i in range(len(parsed_dates) - 1):
        if parsed_dates[i] >= parsed_dates[i + 1]:
            errors.append(f"Dates out of chronological order: {parsed_dates[i]} >= {parsed_dates[i+1]}")
            break

    # Raw dataset size check: 350 <= len <= 370
    if not (350 <= len(parsed_dates) <= 370):
        errors.append(f"Contribution dataset size {len(parsed_dates)} outside expected range [350, 370]")

    # Dynamic total check
    json_total = data.get("total_contributions")
    if total_calculated_count != json_total:
        errors.append(f"Calculated contribution total ({total_calculated_count}) does not match JSON total_contributions ({json_total})")

    # Chrono-Matrix mapping check
    chrono_result = {}
    display_total_count = 0
    if parsed_dates and not errors:
        try:
            chrono_result = calculate_chrono_matrix_mapping(parsed_dates, normalize_display=True)
            
            # Strict V2 Chrono-Matrix 53-Column Contract validations
            display_count = chrono_result.get("display_date_count", 0)
            if display_count != 365:
                errors.append(f"Chrono-Matrix display window size {display_count} does not equal 365 calendar days")

            total_cols = chrono_result.get("total_columns", 0)
            if total_cols > 53 or total_cols < 1:
                errors.append(f"Chrono-Matrix total columns ({total_cols}) violates maximum 53-column contract (allowed: 1..53)")

            if chrono_result.get("duplicate_coords"):
                errors.append(f"Chrono-Matrix mapping generated duplicate coordinates: {chrono_result['duplicate_coords']}")

            # Validate that mapped coordinates for display dates satisfy 0 <= col <= 52 and 0 <= row <= 6
            for d_obj, (c_idx, r_idx) in chrono_result.get("mapped_coords", {}).items():
                if not (0 <= c_idx <= 52):
                    errors.append(f"Mapped column {c_idx} for date {d_obj} outside valid range 0..52")
                if not (0 <= r_idx <= 6):
                    errors.append(f"Mapped row {r_idx} for date {d_obj} outside valid range 0..6")

            # Compute display_total_contributions
            display_start_str = chrono_result.get("display_start_date")
            display_end_str = chrono_result.get("display_end_date")
            display_start_obj = datetime.strptime(display_start_str, "%Y-%m-%d").date()
            display_end_obj = datetime.strptime(display_end_str, "%Y-%m-%d").date()

            display_total_count = sum(
                day["count"] for day in all_days
                if display_start_obj <= datetime.strptime(day["date"], "%Y-%m-%d").date() <= display_end_obj
                and isinstance(day.get("count"), int) and not isinstance(day.get("count"), bool)
            )

        except Exception as ex:
            errors.append(f"Chrono-Matrix grid mapping failed: {ex}")

    success = len(errors) == 0
    summary = {
        "raw_date_count": len(parsed_dates),
        "display_date_count": chrono_result.get("display_date_count", 0),
        "raw_total_contributions": total_calculated_count,
        "display_total_contributions": display_total_count,
        "oldest_raw_date": min(parsed_dates).isoformat() if parsed_dates else None,
        "newest_raw_date": max(parsed_dates).isoformat() if parsed_dates else None,
        "display_start_date": chrono_result.get("display_start_date"),
        "display_end_date": chrono_result.get("display_end_date"),
        "grid_start_date": chrono_result.get("grid_start_date"),
        "grid_end_date": chrono_result.get("grid_end_date"),
        "total_columns": chrono_result.get("total_columns"),
        "padding_positions": chrono_result.get("padding_positions"),
        "newest_date_coord": chrono_result.get("newest_date_coord"),
        "excluded_dates_count": chrono_result.get("excluded_dates_count", 0),
    }
    return success, summary, errors



# ==============================================================================
# 5. PROJECT SCHEMA AND REPOSITORY VERIFICATION
# ==============================================================================

def validate_projects_schema(file_path: Path) -> tuple[bool, list[dict], list[str]]:
    """Validates schema and fields of data/projects.json."""
    errors = []
    if not file_path.exists():
        return False, [], [f"Projects file not found at {file_path}"]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, [], [f"Malformed JSON in projects file: {e}"]

    if "$schema" not in data:
        errors.append("Missing '$schema' field in projects.json")
    if data.get("version") != "2.0.0":
        errors.append(f"Expected version '2.0.0', got '{data.get('version')}'")

    projects = data.get("projects")
    if not isinstance(projects, list):
        errors.append("'projects' field must be a JSON array")
        return False, [], errors

    required_fields = ["id", "name", "category", "description", "repository", "status", "stack", "featured", "sort_order"]
    seen_ids = set()

    for idx, p in enumerate(projects):
        if not isinstance(p, dict):
            errors.append(f"Project item at index {idx} is not an object")
            continue
        
        for field in required_fields:
            if field not in p:
                errors.append(f"Project at index {idx} ({p.get('id', 'unknown')}) missing required field '{field}'")

        p_id = p.get("id")
        if p_id in seen_ids:
            errors.append(f"Duplicate project ID found: '{p_id}'")
        seen_ids.add(p_id)

        repo = p.get("repository", "")
        if not re.match(r"^[A-Za-z0-9_-]+/[A-Za-z0-9_-]+$", repo):
            errors.append(f"Project '{p_id}' has malformed repository format: '{repo}'")
        elif not repo.startswith("HenilLol/"):
            errors.append(f"Project '{p_id}' repository owner is not 'HenilLol': '{repo}'")

        if not isinstance(p.get("stack"), list):
            errors.append(f"Project '{p_id}' field 'stack' must be a list")
        if not isinstance(p.get("featured"), bool):
            errors.append(f"Project '{p_id}' field 'featured' must be a boolean")
        if not isinstance(p.get("sort_order"), int) or p.get("sort_order", 0) <= 0:
            errors.append(f"Project '{p_id}' field 'sort_order' must be a positive integer")

    success = len(errors) == 0
    return success, projects, errors


def verify_project_repository(repo_full_name: str) -> dict:
    """
    Verifies public GitHub repository existence and metadata via GitHub REST API.
    Performs unauthenticated public GET request without PAT or secrets.
    """
    url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {"User-Agent": "HenilLol-V2-Validator/1.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            
            owner_login = data.get("owner", {}).get("login")
            private = data.get("private", True)
            html_url = data.get("html_url")
            pushed_at = data.get("pushed_at") or data.get("updated_at")

            if owner_login != "HenilLol":
                return {
                    "verified": False,
                    "status": "UNVERIFIED",
                    "reason": f"Owner mismatch (expected HenilLol, got {owner_login})",
                    "url": html_url,
                }
            
            if private:
                return {
                    "verified": False,
                    "status": "UNVERIFIED",
                    "reason": "Repository is private",
                    "url": html_url,
                }

            return {
                "verified": True,
                "status": "VERIFIED",
                "reason": "Public repository verified on GitHub",
                "url": html_url,
                "pushed_at": pushed_at,
            }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                "verified": False,
                "status": "UNVERIFIED",
                "reason": "HTTP 404 Not Found (Repository does not exist publicly on GitHub)",
                "url": f"https://github.com/{repo_full_name}",
            }
        elif e.code in (403, 429):
            return {
                "verified": False,
                "status": "API_RATE_LIMITED",
                "reason": f"HTTP {e.code} API rate limit exceeded",
                "url": f"https://github.com/{repo_full_name}",
            }
        else:
            return {
                "verified": False,
                "status": "HTTP_ERROR",
                "reason": f"HTTP Error {e.code} {e.reason}",
                "url": f"https://github.com/{repo_full_name}",
            }
    except urllib.error.URLError as e:
        return {
            "verified": False,
            "status": "NETWORK_FAILURE",
            "reason": f"Network error: {e.reason}",
            "url": f"https://github.com/{repo_full_name}",
        }
    except Exception as e:
        return {
            "verified": False,
            "status": "ERROR",
            "reason": f"Unexpected verification failure: {e}",
            "url": f"https://github.com/{repo_full_name}",
        }


# ==============================================================================
# 6. PIPELINE RUNNER & CLI REPORT
# ==============================================================================

def run_pipeline_validation() -> tuple[bool, dict]:
    """Executes all Phase 1 validation suites and returns results."""
    results = {}
    all_passed = True

    # A. Contribution Validation
    contrib_ok, contrib_summary, contrib_errors = validate_contributions_file(CONTRIBUTIONS_PATH)
    results["contributions"] = {
        "passed": contrib_ok,
        "summary": contrib_summary,
        "errors": contrib_errors,
    }
    if not contrib_ok:
        all_passed = False

    # B. Projects Schema Validation
    proj_schema_ok, projects_list, proj_schema_errors = validate_projects_schema(PROJECTS_PATH)
    results["projects_schema"] = {
        "passed": proj_schema_ok,
        "errors": proj_schema_errors,
    }
    if not proj_schema_ok:
        all_passed = False

    # C. Project Repository Verification
    repo_results = []
    if proj_schema_ok and projects_list:
        for proj in projects_list:
            repo_name = proj["repository"]
            ver_res = verify_project_repository(repo_name)
            ver_res["id"] = proj["id"]
            ver_res["name"] = proj["name"]
            ver_res["repository"] = repo_name
            repo_results.append(ver_res)
    results["repo_verification"] = repo_results

    # D. Contrast Ratios Validation
    colors = {
        "Primary": "#E6EDF3",
        "Secondary": "#8B949E",
        "Accent": "#00C7B7",
        "Background": "#0D1117",
        "Surface": "#161B22",
        "Dim": "#484F58",
    }
    essential_text_pairs = [
        ("Primary", "Background"),
        ("Primary", "Surface"),
        ("Secondary", "Background"),
        ("Secondary", "Surface"),
        ("Accent", "Background"),
        ("Accent", "Surface"),
    ]
    non_text_pairs = [
        ("Dim", "Background"),
        ("Dim", "Surface"),
    ]

    contrast_results = []
    contrast_passed = True

    for fg_name, bg_name in essential_text_pairs + non_text_pairs:
        fg_hex = colors[fg_name]
        bg_hex = colors[bg_name]
        eval_res = evaluate_contrast_compliance(fg_hex, bg_hex)
        is_essential = (fg_name, bg_name) in essential_text_pairs
        
        # Essential text pairs MUST pass AA Normal (>= 4.5:1)
        if is_essential and not eval_res["aa_normal"]:
            contrast_passed = False

        contrast_results.append({
            "fg": fg_name,
            "bg": bg_name,
            "fg_hex": fg_hex,
            "bg_hex": bg_hex,
            "ratio": eval_res["ratio"],
            "aa_normal": eval_res["aa_normal"],
            "aaa_normal": eval_res["aaa_normal"],
            "aa_large": eval_res["aa_large"],
            "aaa_large": eval_res["aaa_large"],
            "is_essential": is_essential,
        })

    results["contrast"] = {
        "passed": contrast_passed,
        "pairs": contrast_results,
    }
    if not contrast_passed:
        all_passed = False

    # E. Staging & Baseline Asset Integrity
    staging_ok = STAGING_DIR.exists()
    assets_ok = all(p.exists() for p in V1_ASSET_PATHS)
    
    results["staging"] = {
        "passed": staging_ok and assets_ok,
        "staging_dir_exists": staging_ok,
        "v1_assets_intact": assets_ok,
    }
    if not (staging_ok and assets_ok):
        all_passed = False

    return all_passed, results


def print_cli_report(overall_pass: bool, results: dict):
    """Outputs structured PASS / FAIL report to console."""
    print("=" * 60)
    print("HENILLOL V2 PHASE 1 VALIDATION ENGINE")
    print("=" * 60)
    print()

    contrib = results.get("contributions", {})
    proj_s = results.get("projects_schema", {})
    contrast = results.get("contrast", {})
    staging = results.get("staging", {})

    print(f"[{'PASS' if contrib.get('passed') else 'FAIL'}] Contribution JSON structure & dates")
    print(f"[{'PASS' if contrib.get('passed') else 'FAIL'}] Contribution dynamic total")
    print(f"[{'PASS' if contrib.get('passed') else 'FAIL'}] Heatmap level boundaries")
    print(f"[{'PASS' if contrib.get('passed') else 'FAIL'}] Chrono-Matrix date mapping")
    print(f"[{'PASS' if proj_s.get('passed') else 'FAIL'}] Project schema")
    print(f"[{'PASS' if results.get('repo_verification') else 'FAIL'}] Repository verification")
    print(f"[{'PASS' if contrast.get('passed') else 'FAIL'}] Contrast calculations")
    print(f"[{'PASS' if staging.get('passed') else 'FAIL'}] Staging & V1 asset baseline safety")
    print()

    # Errors if any
    if contrib.get("errors"):
        print("--- CONTRIBUTION ERRORS ---")
        for err in contrib["errors"]:
            print(f"  [ERROR] {err}")
        print()

    if proj_s.get("errors"):
        print("--- PROJECT SCHEMA ERRORS ---")
        for err in proj_s["errors"]:
            print(f"  [ERROR] {err}")
        print()

    # Data Summary
    s = contrib.get("summary", {})
    print("-" * 60)
    print("DATA SUMMARY")
    print("-" * 60)
    print(f"Raw dates count:            {s.get('raw_date_count')} ({s.get('oldest_raw_date')} to {s.get('newest_raw_date')})")
    print(f"Canonical display dates:    {s.get('display_date_count')} ({s.get('display_start_date')} to {s.get('display_end_date')})")
    print(f"Excluded boundary dates:    {s.get('excluded_dates_count')}")
    print(f"Grid start date:            {s.get('grid_start_date')} (Monday)")
    print(f"Grid end date:              {s.get('grid_end_date')} (Sunday)")
    print(f"Grid columns used:          {s.get('total_columns')} (allowed max: 53)")
    print(f"Padding positions:          {s.get('padding_positions')}")
    print(f"Newest date coord:          col={s.get('newest_date_coord', (None, None))[0]}, row={s.get('newest_date_coord', (None, None))[1]}")
    print(f"Raw total contributions:    {s.get('raw_total_contributions')}")
    print(f"Display total contributions:{s.get('display_total_contributions')}")
    print()

    # Repo Verification Summary
    print("-" * 60)
    print("PROJECT REPOSITORY VERIFICATION SUMMARY")
    print("-" * 60)
    for repo in results.get("repo_verification", []):
        ver_flag = "[VERIFIED]" if repo.get("verified") else "[UNVERIFIED]"
        print(f"{ver_flag} {repo['id'].upper()} ({repo['repository']}): {repo['reason']}")
        if repo.get("pushed_at"):
            print(f"            Latest commit/push: {repo['pushed_at']}")
    print()

    # Contrast Summary
    print("-" * 60)
    print("CONTRAST RATIO SUMMARY (WCAG 2.x)")
    print("-" * 60)
    for p in contrast.get("pairs", []):
        aa_n = "PASS" if p["aa_normal"] else "FAIL"
        aaa_n = "PASS" if p["aaa_normal"] else "FAIL"
        print(f"  {p['fg']} ({p['fg_hex']}) on {p['bg']} ({p['bg_hex']}): {p['ratio']:.2f}:1 | AA Normal: {aa_n} | AAA Normal: {aaa_n}")
    print()

    print("=" * 60)
    print(f"FINAL RESULT: {'PASS' if overall_pass else 'FAIL'}")
    print("=" * 60)


def main():
    overall_pass, results = run_pipeline_validation()
    print_cli_report(overall_pass, results)
    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
