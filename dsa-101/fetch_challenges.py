#!/usr/bin/env python3
"""
HackerRank Contest Challenge Scraper / Fetcher
Used to download challenge details and test cases from HackerRank contests.
Requires the session cookie (_hr_session) for private contests.

Usage:
    python3 fetch_contest.py --cookie "<_hr_session_cookie_value>"
Or:
    python3 fetch_contest.py --contest dsa-101-homework --cookie "<cookie>"
"""

import urllib.request
import json
import argparse
import os
import sys

def fetch_challenges(contest_slug, cookie_str=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    if cookie_str:
        if not cookie_str.startswith("_hr_session="):
            headers["Cookie"] = f"_hr_session={cookie_str}"
        else:
            headers["Cookie"] = cookie_str

    url = f"https://www.hackerrank.com/rest/contests/{contest_slug}/challenges?offset=0&limit=100"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Error fetching contest challenges: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch HackerRank Contest Challenges")
    parser.add_argument("--contest", default="dsa-101-homework", help="Contest slug")
    parser.add_argument("--cookie", default=None, help="HackerRank _hr_session cookie")
    args = parser.parse_args()

    data = fetch_challenges(args.contest, args.cookie)
    if not data:
        print("Failed to retrieve data.")
        sys.exit(1)

    models = data.get("models", [])
    if not models:
        print(f"No challenges found or contest '{args.contest}' is private.")
        print("Please provide a valid session cookie with --cookie '<_hr_session>'")
        sys.exit(1)

    print(f"Found {len(models)} challenges in contest '{args.contest}':\n")
    for idx, ch in enumerate(models, 1):
        slug = ch.get("slug")
        name = ch.get("name")
        difficulty = ch.get("difficulty_name", "N/A")
        max_score = ch.get("max_score", "N/A")
        print(f"{idx:2d}. [{slug}] {name} (Difficulty: {difficulty}, Score: {max_score})")

if __name__ == "__main__":
    main()
