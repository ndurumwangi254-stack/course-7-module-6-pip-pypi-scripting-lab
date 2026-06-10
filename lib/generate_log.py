from datetime import datetime
import argparse
import os

import requests


def generate_log(data, filename=None):
    """Write a list of log entries to a dated text file and return the filename."""
    if not isinstance(data, list):
        raise ValueError("data must be a list of log entries")

    if filename is None:
        today = datetime.now().strftime("%Y%m%d")
        filename = f"log_{today}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        for entry in data:
            file.write(f"{entry}\n")

    return filename


def fetch_remote_entries(count=3):
    """Fetch a short list of remote entries from a public API."""
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, params={"_limit": count}, timeout=10)
    response.raise_for_status()
    posts = response.json()
    return [post.get("title", "Untitled entry") for post in posts]


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Generate a dated log file from local or remote entries.")
    parser.add_argument(
        "--use-api",
        action="store_true",
        help="Fetch log entries from a remote API before writing the file.",
    )
    parser.add_argument(
        "--entries",
        nargs="+",
        help="Custom log entries to write to the file.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of API entries to fetch when using --use-api.",
    )
    parser.add_argument(
        "--output",
        help="Optional output filename. Defaults to log_YYYYMMDD.txt.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)

    if parsed.use_api:
        entries = fetch_remote_entries(count=parsed.count)
    elif parsed.entries:
        entries = parsed.entries
    else:
        entries = [
            "User logged in",
            "User updated profile",
            "Report exported",
        ]

    filename = generate_log(entries, filename=parsed.output)
    print(f"Log written to {filename}")
    return filename


if __name__ == "__main__":
    main()
