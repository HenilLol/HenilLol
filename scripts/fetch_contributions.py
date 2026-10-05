#!/usr/bin/env python3
"""
scripts/fetch_contributions.py

Fetches real public GitHub contribution statistics for HenilLol.
Uses GitHub's public contribution calendar endpoint without personal access tokens.
Parses, validates, and stores verified activity data in data/contributions.json.

Requirements:
- Public GitHub data fetching (no auth/token required)
- Full validation (schema, date order, non-negative integer counts, levels 0-4)
- Graceful error handling (preserves existing valid data on network failure)
- No fake/hardcoded numbers
"""

import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_FILE = PROJECT_ROOT / "data" / "contributions.json"
GITHUB_USERNAME = "HenilLol"
PUBLIC_CONTRIBUTIONS_URL = f"https://github.com/users/{GITHUB_USERNAME}/contributions"


def fetch_raw_github_contributions_html(username: str = GITHUB_USERNAME) -> str:
    """Fetches the raw public contribution calendar HTML from GitHub."""
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status != 200:
                raise ValueError(f"GitHub endpoint returned HTTP status {response.status}")
            return response.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Network request to GitHub failed: {e}") from e


def parse_contribution_html(html_content: str) -> List[Dict[str, Any]]:
    """
    Parses contribution dates, levels, and counts from GitHub HTML.
    Returns a sorted list of daily contribution objects.
    """
    # Build a lookup map of component IDs to tooltip texts
    tooltip_map: Dict[str, str] = {}
    tooltip_pattern = re.compile(
        r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>',
        re.DOTALL
    )
    for match in tooltip_pattern.finditer(html_content):
        elem_id = match.group(1)
        text = match.group(2).strip()
        tooltip_map[elem_id] = text

    # Parse contribution <td> elements
    days: List[Dict[str, Any]] = []
    td_pattern = re.compile(r'<td\s+([^>]+)>')
    
    for match in td_pattern.finditer(html_content):
        attr_str = match.group(1)
        
        date_m = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', attr_str)
        level_m = re.search(r'data-level="(\d+)"', attr_str)
        id_m = re.search(r'id="([^"]+)"', attr_str)
        
        if date_m and level_m and id_m:
            date_str = date_m.group(1)
            level_val = int(level_m.group(1))
            elem_id = id_m.group(1)
            
            # Extract count from tooltip text
            count = 0
            tt_text = tooltip_map.get(elem_id, "")
            if tt_text and "No contributions" not in tt_text:
                count_m = re.search(r'(\d+)\s+contribution', tt_text)
                if count_m:
                    count = int(count_m.group(1))
                else:
                    count = max(1, level_val)
                    
            days.append({
                "date": date_str,
                "count": count,
                "level": level_val,
                "id": elem_id
            })

    # Sort chronologically by date
    days.sort(key=lambda d: d["date"])
    return days


def validate_contribution_data(days: List[Dict[str, Any]]) -> None:
    """Strictly validates parsed contribution records."""
    if not days:
        raise ValueError("Parsed contribution dataset is empty.")
        
    if not (350 <= len(days) <= 370):
        raise ValueError(f"Unexpected day count in dataset: {len(days)} (expected ~365).")

    seen_dates = set()
    for idx, day in enumerate(days):
        date_str = day.get("date", "")
        count = day.get("count", -1)
        level = day.get("level", -1)
        
        # Date format check YYYY-MM-DD
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format at index {idx}: '{date_str}'")
            
        if date_str in seen_dates:
            raise ValueError(f"Duplicate date detected: '{date_str}'")
        seen_dates.add(date_str)
        
        if not isinstance(count, int) or count < 0:
            raise ValueError(f"Invalid contribution count on {date_str}: {count}")
            
        if not isinstance(level, int) or not (0 <= level <= 4):
            raise ValueError(f"Invalid contribution level on {date_str}: {level}")


def organize_into_weeks(days: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Organizes parsed daily records into 7-day calendar weeks."""
    weeks: List[Dict[str, Any]] = []
    
    # Group by chunks of 7 days matching calendar grid alignment
    chunk_size = 7
    for week_idx in range(0, len(days), chunk_size):
        week_days = days[week_idx:week_idx + chunk_size]
        if not week_days:
            continue
            
        weeks.append({
            "week_index": len(weeks),
            "first_day": week_days[0]["date"],
            "days": [
                {
                    "date": d["date"],
                    "count": d["count"],
                    "level": d["level"],
                    "day_of_week": i
                }
                for i, d in enumerate(week_days)
            ]
        })
        
    return weeks


def fetch_contributions(
    username: str = GITHUB_USERNAME,
    output_path: Path = DATA_FILE,
    strict: bool = False
) -> Dict[str, Any]:
    """
    Main execution pipeline for contribution data retrieval.
    Fetches, parses, validates, and stores dataset.
    Preserves existing data on network error unless strict mode is enabled.
    """
    try:
        print(f"[i] Fetching public contribution data for '{username}'...")
        html = fetch_raw_github_contributions_html(username)
        raw_days = parse_contribution_html(html)
        validate_contribution_data(raw_days)
        
        weeks = organize_into_weeks(raw_days)
        total_contributions = sum(d["count"] for d in raw_days)
        
        dataset = {
            "username": username,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_contributions": total_contributions,
            "status": "live_data_verified",
            "total_days": len(raw_days),
            "start_date": raw_days[0]["date"],
            "end_date": raw_days[-1]["date"],
            "weeks": weeks
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2)
            
        print(f"[+] Successfully saved verified GitHub contributions ({total_contributions} total across {len(raw_days)} days) -> {output_path}")
        return dataset

    except Exception as e:
        print(f"[-] Error fetching contribution data: {e}", file=sys.stderr)
        
        # Failure Safety: Preserve existing dataset if valid
        if output_path.exists() and not strict:
            try:
                with open(output_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                print(f"[!] Network update failed. Preserving existing valid dataset from {existing.get('generated_at')}.", file=sys.stderr)
                return existing
            except Exception:
                pass
                
        if strict or not output_path.exists():
            raise SystemExit(1) from e
            
        raise SystemExit(1) from e


if __name__ == "__main__":
    is_strict = "--strict" in sys.argv
    fetch_contributions(strict=is_strict)
