#!/usr/bin/env python3
"""
mail_brief.py - Fetch Gmail messages using gog CLI

Discovers Google accounts via gog auth, classifies them as personal or work,
then fetches email messages for the specified time period.
Outputs JSON with message summaries.
"""

import argparse
import datetime
import json
import subprocess
import sys


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch Gmail messages for personal/work accounts"
    )

    # Account specification
    parser.add_argument(
        "--personal",
        type=str,
        metavar="EMAIL",
        help="Personal account email (optional, auto-discovers if not provided)"
    )
    parser.add_argument(
        "--work",
        type=str,
        metavar="EMAIL",
        help="Work account email (optional, auto-discovers if not provided)"
    )

    # Date range specification (mutually exclusive)
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--today",
        action="store_true",
        help="Fetch messages from today (default)"
    )
    date_group.add_argument(
        "--yesterday",
        action="store_true",
        help="Fetch messages from yesterday"
    )
    date_group.add_argument(
        "--this-week",
        action="store_true",
        help="Fetch messages from this week (Sunday to today)"
    )
    date_group.add_argument(
        "--last-week",
        action="store_true",
        help="Fetch messages from last week (Sunday to Saturday)"
    )
    date_group.add_argument(
        "--date",
        type=str,
        metavar="YYYY-MM-DD",
        help="Fetch messages from a specific date"
    )

    args = parser.parse_args()

    # Default to --today if no date option specified
    if not any([args.today, args.yesterday, args.this_week, args.last_week, args.date]):
        args.today = True

    return args


def discover_accounts():
    """
    Discover Google accounts using gog CLI.

    Returns:
        List of email addresses
    """
    try:
        result = subprocess.run(
            ["gog", "auth", "list", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        return [a["email"] for a in data.get("accounts", [])]

    except Exception:
        return []


def classify_account(email):
    """
    Classify an email account as personal or work.

    Personal domains: gmail.com, naver.com, daum.net, hanmail.net, yahoo.com,
                     hotmail.com, outlook.com, icloud.com, kakao.com, nate.com

    Args:
        email: Email address to classify

    Returns:
        "personal" or "work"
    """
    personal_domains = {
        "gmail.com",
        "naver.com",
        "daum.net",
        "hanmail.net",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com",
        "kakao.com",
        "nate.com"
    }

    domain = email.split("@")[-1].lower()
    return "personal" if domain in personal_domains else "work"


def resolve_accounts(args):
    """
    Resolve which accounts to query based on args.

    Args:
        args: Parsed command-line arguments

    Returns:
        List of account dicts with "email" and "type" keys
    """
    accounts = []

    # If explicit accounts provided, use them
    if args.personal:
        accounts.append({"email": args.personal, "type": "personal"})
    if args.work:
        accounts.append({"email": args.work, "type": "work"})

    # If no explicit accounts, auto-discover
    if not accounts:
        for email in discover_accounts():
            accounts.append({"email": email, "type": classify_account(email)})

    return accounts


def build_gmail_query(args):
    """
    Build Gmail search query based on date arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Gmail search query string
    """
    today = datetime.date.today()

    if args.today:
        return "newer_than:1d"

    elif args.yesterday:
        yesterday = today - datetime.timedelta(days=1)
        after = yesterday.strftime("%Y/%m/%d")
        before = today.strftime("%Y/%m/%d")
        return f"after:{after} before:{before}"

    elif args.this_week:
        # Sunday of current week to tomorrow
        days_since_sunday = (today.weekday() + 1) % 7  # Sun=0
        sunday = today - datetime.timedelta(days=days_since_sunday)
        tomorrow = today + datetime.timedelta(days=1)
        after = sunday.strftime("%Y/%m/%d")
        before = tomorrow.strftime("%Y/%m/%d")
        return f"after:{after} before:{before}"

    elif args.last_week:
        # Previous Sunday to this Sunday
        days_since_sunday = (today.weekday() + 1) % 7
        this_sunday = today - datetime.timedelta(days=days_since_sunday)
        last_sunday = this_sunday - datetime.timedelta(days=7)
        after = last_sunday.strftime("%Y/%m/%d")
        before = this_sunday.strftime("%Y/%m/%d")
        return f"after:{after} before:{before}"

    elif args.date:
        # Specific date to next day
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
            next_day = target_date + datetime.timedelta(days=1)
            after = target_date.strftime("%Y/%m/%d")
            before = next_day.strftime("%Y/%m/%d")
            return f"after:{after} before:{before}"
        except ValueError:
            raise ValueError(f"Invalid date format: {args.date}. Use YYYY-MM-DD")

    # Default to today
    return "newer_than:1d"


def fetch_messages(account_email, query):
    """
    Fetch Gmail messages using gog CLI.

    Args:
        account_email: Email address of the account
        query: Gmail search query

    Returns:
        List of message dictionaries

    Raises:
        RuntimeError: If gog command fails
    """
    try:
        cmd = [
            "gog", "gmail", "messages", "search",
            query,
            "--json",
            "--max=50",
            f"--account={account_email}"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise RuntimeError(f"gog gmail search failed: {result.stderr}")

        data = json.loads(result.stdout)
        return data.get("messages", [])

    except subprocess.TimeoutExpired:
        raise RuntimeError(f"gog gmail search timed out after 30 seconds for {account_email}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse gog output for {account_email}: {e}")


def parse_from(raw):
    """
    Parse 'From' header into display name and email.

    Handles formats:
    - "Display Name <email@domain.com>"
    - "email@domain.com"

    Args:
        raw: Raw 'From' header value

    Returns:
        Tuple of (display_name, email)
    """
    raw = raw.strip()

    # Check for "Name <email>" format
    if "<" in raw and ">" in raw:
        name_part = raw[:raw.index("<")].strip()
        email_part = raw[raw.index("<") + 1:raw.index(">")].strip()
        return (name_part, email_part)

    # Bare email address
    return (raw, raw)


def simplify_message(msg, account_type):
    """
    Simplify message to essential fields.

    Args:
        msg: Raw message dictionary from gog
        account_type: "personal" or "work"

    Returns:
        Simplified message dictionary
    """
    # Parse from field
    from_raw = msg.get("from", "")
    from_name, from_email = parse_from(from_raw)

    # Filter labels and detect unread status
    labels = msg.get("labels", [])
    is_unread = "UNREAD" in labels
    filtered_labels = [label for label in labels if label != "UNREAD"]

    return {
        "date": msg.get("date", ""),
        "subject": msg.get("subject", "(No subject)"),
        "from_name": from_name,
        "from_email": from_email,
        "labels": filtered_labels,
        "is_unread": is_unread,
        "account_type": account_type
    }


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()

        # Resolve accounts
        accounts = resolve_accounts(args)

        if not accounts:
            json.dump(
                {"error": "No accounts found. Use --personal/--work or configure gog auth."},
                sys.stdout,
                ensure_ascii=False,
                indent=2
            )
            sys.exit(1)

        # Build Gmail query
        query = build_gmail_query(args)

        # Fetch messages for each account
        all_messages = []
        errors = []

        for account in accounts:
            try:
                messages = fetch_messages(account["email"], query)
                all_messages.extend(
                    simplify_message(m, account["type"]) for m in messages
                )
            except Exception as e:
                errors.append({"email": account["email"], "error": str(e)})

        # Output results
        output = {
            "accounts": [{"email": a["email"], "type": a["type"]} for a in accounts],
            "messages": all_messages,
        }
        if errors:
            output["errors"] = errors

        json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
        sys.exit(0)

    except Exception as e:
        # Top-level error handling
        error_output = {
            "error": str(e)
        }
        json.dump(error_output, sys.stdout, ensure_ascii=False, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    main()
