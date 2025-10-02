#!/usr/bin/env python3

import argparse
import os
import sys
from typing import Optional

try:
	from deep_translator import LibreTranslator
except Exception as import_error:  # pragma: no cover
	print("Error: deep-translator is required. Install with 'pip install -r requirements.txt'", file=sys.stderr)
	raise import_error

try:
	from langdetect import detect
except Exception as import_error:  # pragma: no cover
	print("Error: langdetect is required. Install with 'pip install -r requirements.txt'", file=sys.stderr)
	raise import_error


SUPPORTED_LANGS = {"en": "English", "es": "Spanish"}
DEFAULT_LOCAL_LT_URL = os.getenv("LT_LOCAL_URL", "http://localhost:5000")
DEFAULT_LOCAL_SHORT_ENABLED = os.getenv("LT_DISABLE_LOCAL_SHORT", "0") not in {"1", "true", "True"}
DEFAULT_LOCAL_SHORT_THRESHOLD = int(os.getenv("LT_LOCAL_SHORT_THRESHOLD", "200"))


def auto_detect_language(text: str) -> str:
	"""Detect language code (en/es) from text, defaulting to en if uncertain."""
	code = detect(text)
	# Map generic codes to our supported set
	if code.startswith("en"):
		return "en"
	if code.startswith("es"):
		return "es"
	# Fallback: if contains many ASCII words, guess English, else Spanish
	ascii_ratio = sum(c.isascii() for c in text) / max(len(text), 1)
	return "en" if ascii_ratio > 0.9 else "es"


def count_words(text: str) -> int:
	return len([w for w in text.strip().split() if w])


def translate_text(text: str, source: Optional[str], target: Optional[str], api_url: Optional[str]) -> str:
	"""
	Translate between English and Spanish using LibreTranslate via deep-translator.
	- If source or target not provided, auto-detect/choose the opposite.
	- Optional custom LibreTranslate API URL.
	"""
	if not text.strip():
		return ""

	if source is None:
		source = auto_detect_language(text)

	if target is None:
		target = "es" if source == "en" else "en"

	if source == target:
		return text

	translator = LibreTranslator(source=source, target=target, api_url=api_url) if api_url else LibreTranslator(source=source, target=target)
	return translator.translate(text)


def build_arg_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Translate text between Spanish and English (auto-detect by default).",
	)
	parser.add_argument("text", nargs="?", help="Text to translate. If omitted, read from stdin.")
	parser.add_argument("-s", "--source", choices=list(SUPPORTED_LANGS.keys()), help="Source language code (en or es). Defaults to auto-detect.")
	parser.add_argument("-t", "--target", choices=list(SUPPORTED_LANGS.keys()), help="Target language code (en or es). Defaults to the opposite of source.")
	parser.add_argument("-u", "--api-url", help="LibreTranslate API URL (optional). If not set, may use local for short texts.")
	parser.add_argument("--local-url", default=DEFAULT_LOCAL_LT_URL, help=f"Local LibreTranslate URL (env LT_LOCAL_URL). Default: {DEFAULT_LOCAL_LT_URL}")
	parser.add_argument("--no-local-short", action="store_true", help="Disable preferring local server for short texts (< threshold). Or set LT_DISABLE_LOCAL_SHORT=1.")
	parser.add_argument("--short-threshold", type=int, default=DEFAULT_LOCAL_SHORT_THRESHOLD, help="Word threshold for using local server. Env LT_LOCAL_SHORT_THRESHOLD. Default: 200")
	return parser


def main(argv: Optional[list[str]] = None) -> int:
	parser = build_arg_parser()
	args = parser.parse_args(argv)

	if args.text is None:
		# Read entire stdin
		input_text = sys.stdin.read()
	else:
		input_text = args.text

	# Determine which API URL to use
	chosen_api_url: Optional[str] = args.api_url
	if chosen_api_url is None:
		use_local_short = DEFAULT_LOCAL_SHORT_ENABLED and not args.no_local_short
		if use_local_short and count_words(input_text) <= args.short_threshold:
			chosen_api_url = args.local_url

	try:
		# Try with selected api_url (may be local). If it fails and it was local, fallback to default (None)
		output = translate_text(
			text=input_text,
			source=args.source,
			target=args.target,
			api_url=chosen_api_url,
		)
	except Exception:
		if chosen_api_url and chosen_api_url == args.local_url:
			try:
				output = translate_text(
					text=input_text,
					source=args.source,
					target=args.target,
					api_url=None,
				)
			except Exception as error:  # pragma: no cover
				print(f"Translation failed: {error}", file=sys.stderr)
				return 1
		else:
			print("Translation failed: unable to reach translation service.", file=sys.stderr)
			return 1

	# Print raw translated text
	sys.stdout.write(output)
	return 0


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())
