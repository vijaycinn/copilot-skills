"""
Read Account Alignment XLSX via Excel automation.

Supports both:
1. pywin32 when it is installed, and
2. a PowerShell Excel COM fallback on managed Windows machines.

Usage:
    python read_account_xlsx.py --path "Account Sales Team ACR.xlsx" --output account_alignment.json
    python read_account_xlsx.py --path "Account Sales Team ACR.xlsx"  # prints to stdout
"""

import argparse
import json
import sys

from analyze_territory import load_account_xlsx


def main():
    parser = argparse.ArgumentParser(description="Read XLSX via Excel automation")
    parser.add_argument("--path", required=True, help="Path to XLSX file")
    parser.add_argument("--output", help="Output JSON path (default: print to stdout)")
    args = parser.parse_args()

    print(f"Reading: {args.path}", file=sys.stderr)
    rows = load_account_xlsx(args.path)
    print(f"Read {len(rows)} data rows, {len(rows[0]) if rows else 0} columns", file=sys.stderr)

    if rows:
        print(f"Columns: {list(rows[0].keys())}", file=sys.stderr)

    output_json = json.dumps(rows, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Written to: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
