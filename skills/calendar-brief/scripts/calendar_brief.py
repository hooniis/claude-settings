#!/usr/bin/env python3
"""Fetch Google Calendar events via gog CLI and output simplified JSON.

Supports --personal and --work parameters to tag events by account type.
When no accounts are provided, auto-discovers via `gog auth list`.
"""

import argparse
import datetime
import json
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch calendar events via gog CLI")
    parser.add_argument("--personal", help="Personal account email")
    parser.add_argument("--work", help="Work account email")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--today", action="store_true", default=True, help="Today's events (default)")
    group.add_argument("--tomorrow", action="store_true", help="Tomorrow's events")
    group.add_argument("--this-week", action="store_true", help="This week (Mon-Sun)")
    group.add_argument("--next-week", action="store_true", help="Next week (Mon-Sun)")
    return parser.parse_args()


def discover_accounts():
    """Auto-discover accounts from gog auth list."""
    try:
        result = subprocess.run(
            ["gog", "auth", "list", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        return [a["email"] for a in data.get("accounts", [])]
    except Exception:
        return []


def classify_account(email):
    """Classify an account as personal or work based on domain."""
    domain = email.split("@", 1)[-1].lower()
    personal_domains = {"gmail.com", "naver.com", "daum.net", "hanmail.net",
                        "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
                        "kakao.com", "nate.com"}
    return "personal" if domain in personal_domains else "work"


def resolve_accounts(args):
    """Resolve account list from args or auto-discovery.

    Returns list of {"email": str, "type": "personal"|"work"}.
    """
    accounts = []
    if args.personal:
        accounts.append({"email": args.personal, "type": "personal"})
    if args.work:
        accounts.append({"email": args.work, "type": "work"})

    if not accounts:
        for email in discover_accounts():
            accounts.append({"email": email, "type": classify_account(email)})

    return accounts


def build_gog_args(args):
    """Build gog-specific date flags from parsed arguments."""
    if args.next_week:
        today = datetime.date.today()
        weekday = today.weekday()  # Mon=0
        days_until_monday = (7 - weekday) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = today + datetime.timedelta(days=days_until_monday)
        next_sunday = next_monday + datetime.timedelta(days=6)
        return ["--from", next_monday.isoformat(), "--to", next_sunday.isoformat()]
    if args.this_week:
        return ["--week", "--week-start=mon"]
    if args.tomorrow:
        return ["--tomorrow"]
    return ["--today"]


def fetch_events(account_email, gog_date_args):
    """Run gog CLI for a single account and return parsed events."""
    cmd = [
        "gog", "calendar", "events", "primary",
        "--json", "--max=50",
        f"--account={account_email}",
        *gog_date_args,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gog exited with code {result.returncode}")
    data = json.loads(result.stdout)
    return data.get("events", data) if isinstance(data, dict) else data


def extract_my_response(event):
    """Extract the current user's response status from attendees."""
    for attendee in event.get("attendees", []):
        if attendee.get("self"):
            return attendee.get("responseStatus", "")
    return ""


def simplify_event(event, account_type):
    """Extract only the fields we care about."""
    start = event.get("start", {})
    end = event.get("end", {})
    return {
        "summary": event.get("summary", "(No title)"),
        "start": start.get("dateTime") or start.get("date", ""),
        "end": end.get("dateTime") or end.get("date", ""),
        "location": event.get("location", ""),
        "status": event.get("status", ""),
        "response": extract_my_response(event),
        "account_type": account_type,
    }


def main():
    args = parse_args()
    accounts = resolve_accounts(args)

    if not accounts:
        json.dump({"error": "No accounts found. Use --personal/--work or configure gog auth."}, sys.stdout, ensure_ascii=False, indent=2)
        sys.exit(1)

    gog_date_args = build_gog_args(args)

    all_events = []
    errors = []
    for account in accounts:
        try:
            raw_events = fetch_events(account["email"], gog_date_args)
            all_events.extend(
                simplify_event(e, account["type"]) for e in raw_events
            )
        except Exception as e:
            errors.append({"email": account["email"], "error": str(e)})

    output = {
        "accounts": [{"email": a["email"], "type": a["type"]} for a in accounts],
        "events": all_events,
    }
    if errors:
        output["errors"] = errors

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
