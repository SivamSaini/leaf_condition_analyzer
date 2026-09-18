"""Command-line entry point for the leaf condition analyzer."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import cv2

from src.analyzer import analyze_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a leaf image using OpenCV colour segmentation.")
    parser.add_argument("--image", required=True, help="Path to a JPG, JPEG, or PNG image.")
    parser.add_argument("--output", default="results/annotated_leaf.png", help="Where to save the annotated image.")
    parser.add_argument("--json", action="store_true", help="Print the analysis result as JSON.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result, annotated = analyze_path(args.image)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(output), annotated):
            raise OSError(f"Could not write output image: {output}")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print("Leaf Condition Analysis")
        print(f"Classification : {result.label}")
        print(f"Confidence     : {result.confidence:.1f}%")
        print(f"Leaf coverage  : {result.leaf_percent:.1f}%")
        print(f"Green / Yellow / Brown: {result.green_percent:.1f}% / {result.yellow_percent:.1f}% / {result.brown_percent:.1f}%")
        print(f"Advice         : {result.message}")
        print(f"Annotated image: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
