#!/usr/bin/env python3

import argparse
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
	parser.add_argument("-u", "--api-url", help="LibreTranslate API URL (optional). Defaults to the public endpoint used by deep-translator.")
	return parser


def main(argv: Optional[list[str]] = None) -> int:
	parser = build_arg_parser()
	args = parser.parse_args(argv)

	if args.text is None:
		# Read entire stdin
		input_text = sys.stdin.read()
	else:
		input_text = args.text

	try:
		output = translate_text(
			text=input_text,
			source=args.source,
			target=args.target,
			api_url=args.api_url,
		)
	except Exception as error:  # pragma: no cover
		print(f"Translation failed: {error}", file=sys.stderr)
		return 1

	# Print raw translated text
	sys.stdout.write(output)
	return 0


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())
