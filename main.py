#!/usr/bin/env python3
"""Command-line interface for the CBOM scanner."""

import argparse
import json
import sys
from pathlib import Path

from report import build_report, save_report
from scanner import scan_directory


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="CBOM regex scanner using patterns.py")
    parser.add_argument("target", help="Directory to scan")
    parser.add_argument("--output", "-o", help="Output JSON file path (optional)")
    return parser.parse_args()


def main() -> int:
    """Execute the scanner and write the report."""
    args = parse_args()
    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: directory '{args.target}' does not exist.")
        return 1
    if not target_path.is_dir():
        print(f"Error: '{args.target}' is not a directory.")
        return 1

    findings = scan_directory(target_path)
    report = build_report(findings, target_path)

    if args.output:
        try:
            save_report(report, args.output)
            print(f"CBOM report generated: {args.output}")
        except OSError as exc:
            print(f"Error writing output file '{args.output}': {exc}")
            return 2
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())