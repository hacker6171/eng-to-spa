#!/usr/bin/env python3
"""
eng_to_spa.py
Simple English -> Spanish translator utility using deep-translator.
Usage:
  python eng_to_spa.py "Hello world"
  python eng_to_spa.py -f input.txt -o output.txt
  echo "Hello\nHow are you?" | python eng_to_spa.py --stdin
"""

import argparse
import sys
import json
from pathlib import Path
from deep_translator import GoogleTranslator
from typing import List

# Simple JSON cache file (stored next to the script)
CACHE_FILE = Path(__file__).with_suffix(".cache.json")

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_cache(cache: dict) -> None:
    try:
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"Warning: failed to save cache: {e}", file=sys.stderr)

def translate_texts(texts: List[str], source: str = "auto", target: str = "es") -> List[str]:
    """
    Translate a list of texts. Uses a local JSON cache to avoid repeated API calls.
    """
    cache = load_cache()
    translator = GoogleTranslator(source=source, target=target)
    results = []

    for t in texts:
        key = t.strip()
        if not key:
            results.append("")  # preserve blank lines
            continue

        # check cache
        if key in cache:
            results.append(cache[key])
            continue

        # attempt translation
        try:
            translated = translator.translate(key)
        except Exception as e:
            # On failure, return a descriptive error message for that item
            translated = f"[ERROR: {e}]"
        # store in cache even if error text (so we don't retry exact failing strings)
        cache[key] = translated
        results.append(translated)

    save_cache(cache)
    return results

def parse_args():
    p = argparse.ArgumentParser(prog="eng_to_spa", description="English -> Spanish translator (deep-translator).")
    p.add_argument("text", nargs="?", help="Text to translate (wrap in quotes).")
    p.add_argument("-f", "--file", type=str, help="Path to input text file (translates every line).")
    p.add_argument("-o", "--output", type=str, help="Write translations to output file (optional).")
    p.add_argument("--stdin", action="store_true", help="Read lines from stdin.")
    p.add_argument("--source", default="auto", help="Source language (default: auto-detect).")
    p.add_argument("--target", default="es", help="Target language (default: es for Spanish).")
    return p.parse_args()

def main():
    args = parse_args()

    inputs: List[str] = []

    if args.stdin:
        # Read all lines from stdin
        inputs = [line.rstrip("\n") for line in sys.stdin]
    elif args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"Input file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        inputs = p.read_text(encoding="utf-8").splitlines()
    elif args.text:
        inputs = [args.text]
    else:
        print("No input provided. Use a text argument, -f/--file, or --stdin. See -h for help.", file=sys.stderr)
        sys.exit(2)

    translations = translate_texts(inputs, source=args.source, target=args.target)

    # Prepare output: join with newlines to preserve line structure
    output_text = "\n".join(translations)

    if args.output:
        try:
            Path(args.output).write_text(output_text, encoding="utf-8")
            print(f"Saved translations to {args.output}")
        except Exception as e:
            print(f"Failed to write output file: {e}", file=sys.stderr)
            sys.exit(3)
    else:
        # Print to stdout
        print(output_text)

if __name__ == "__main__":
    main()
