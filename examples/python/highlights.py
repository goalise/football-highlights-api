"""Print football highlights for a competition, a team or a match.

Usage:
    export GOALISE_TOKEN=your_api_token
    python highlights.py --league 646
    python highlights.py --team 404 --category goal-clip
    python highlights.py --match 466659

Needs Python 3.8+ and nothing else.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.goalise.com/api/v3/highlights"


def fetch(params):
    request = urllib.request.Request(
        API + "?" + urllib.parse.urlencode(params),
        headers={
            "Authorization": "Bearer " + os.environ.get("GOALISE_TOKEN", ""),
            "Accept": "application/json",
            "User-Agent": "goalise-examples/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            return json.load(error)  # errors use the same JSON envelope
        except ValueError:
            sys.exit("HTTP {} from the API".format(error.code))


def main():
    parser = argparse.ArgumentParser(description="Football highlights from the Goalise API")
    parser.add_argument("--league", type=int, help="league_id, for example 646 (Serie A)")
    parser.add_argument("--team", type=int, help="team_id, for example 404 (Cagliari)")
    parser.add_argument("--match", type=int, help="match_id, for example 466659")
    parser.add_argument("--category", help="match-highlights, goal-clip, press-conference, ...")
    args = parser.parse_args()

    params = {
        "league_id": args.league,
        "team_id": args.team,
        "match_id": args.match,
        "category": args.category,
    }
    params = {key: value for key, value in params.items() if value is not None}
    if not {"league_id", "team_id", "match_id"} & params.keys():
        parser.error("pass at least one of --league, --team or --match")

    data = fetch(params)
    if data["status"] != "success":
        sys.exit("API error: " + ", ".join(error["code"] for error in data["errors"]))

    for clip in data["response"]:
        match = clip["match"] or {}
        home = (match.get("home_team") or {}).get("name", "?")
        away = (match.get("away_team") or {}).get("name", "?")
        can_embed = clip["restriction"]["embeddable"] is True and clip["embed_url"]
        link = clip["embed_url"] if can_embed else clip["url"]
        print("{:<34} {:<18} {}".format((home + " - " + away)[:34], clip["category"], link))

    page = data["pagination"]
    print("\npage {} of {}, {} clips in total".format(page["current_page"], page["page_count"], page["total_count"]))


if __name__ == "__main__":
    main()
