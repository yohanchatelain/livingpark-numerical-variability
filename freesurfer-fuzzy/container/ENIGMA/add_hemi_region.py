#!/usr/bin/env python3
"""
Add a column built as <Hemisphere>_<Region> to a CSV.
Maps hemisphere values: 'lh' -> 'L', 'rh' -> 'R' (case-insensitive).
Usage: add_hemi_region.py input.csv [--output out.csv] [--hemi-col hemisphere] [--region-col region] [--new-col hemi_region] [--overwrite]
"""
import argparse
import sys
import pandas as pd


def normalize_hemi(val):
    if pd.isna(val):
        return ""
    s = str(val).strip().lower()
    if s.startswith("lh") or s == "lh":
        return "L"
    if s.startswith("rh") or s == "rh":
        return "R"
    if s in ("l", "left"):
        return "L"
    if s in ("r", "right"):
        return "R"
    # fallback: uppercase first char if present
    return s[:1].upper() if s else ""


def normalize_subcortical_volume(val):
    if pd.isna(val):
        return ""
    return str(val).strip()


def main():
    p = argparse.ArgumentParser(description="Add hemisphere_region column to CSV")
    p.add_argument("input", help="Input CSV file")
    p.add_argument(
        "--output",
        "-o",
        help="Output CSV file (default: overwrite input)",
        default=None,
    )
    p.add_argument(
        "--hemi-col",
        default="hemisphere",
        help="Name of hemisphere column (default: hemisphere)",
    )
    p.add_argument(
        "--region-col", default="region", help="Name of region column (default: region)"
    )
    p.add_argument(
        "--new-col",
        default="Structure",
        help="Name of new column to add (default: Structure)",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite input file (same as not passing --output)",
    )
    p.add_argument(
        "--subcortical-volume",
        action="store_true",
        help="Whether to add subcortical volume information",
    )
    args = p.parse_args()

    inp = args.input
    out = args.output if args.output else inp

    try:
        df = pd.read_csv(inp)
    except Exception as e:
        print(f"Error reading '{inp}': {e}", file=sys.stderr)
        sys.exit(2)

    if args.hemi_col not in df.columns and not args.subcortical_volume:
        print(
            f"Warning: hemisphere column '{args.hemi_col}' not found. Creating empty values.",
            file=sys.stderr,
        )
        df[args.hemi_col] = ""

    if args.region_col not in df.columns:
        print(
            f"Error: region column '{args.region_col}' not found in CSV.",
            file=sys.stderr,
        )
        sys.exit(3)

    if args.subcortical_volume:
        df[args.new_col] = df[args.region_col].apply(normalize_subcortical_volume)
    else:
        hemi_mapped = df[args.hemi_col].apply(normalize_hemi)
        region_vals = df[args.region_col].astype(str).str.strip().fillna("")
        df[args.new_col] = hemi_mapped + "_" + region_vals

    try:
        df.to_csv(out, index=False)
    except Exception as e:
        print(f"Error writing '{out}': {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
