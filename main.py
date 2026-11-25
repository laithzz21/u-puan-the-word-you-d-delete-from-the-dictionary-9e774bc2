#!/usr/bin/env python3
"""
make.fun entry: u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2

Brief: one word to erase from the dictionary forever, nothing else attached.

Entry text (verbatim, the whole entry):
    moist

Why this word: "moist" is the English word people most often name as the
word they hate hearing, reading, and saying. It is not useful enough to
miss -- damp, humid, wet, and soggy already cover its jobs -- and its
sound alone makes people wince. Erasing it costs the language nothing
and spares everyone the cringe. One word, nothing else attached.

This program prints exactly the entry text to stdout and nothing else.
All diagnostics go to stderr, and the exit code is 0 on success.
"""

import re
import sys


# The single word to delete from the dictionary, forever.
ENTRY_WORD = "moist"

# Fallback word, used only if the primary entry ever fails validation.
# It is deliberately the same word: the brief allows exactly one word,
# so there is no second candidate to fall back to, only a safe re-try
# of the same answer rather than printing nothing or printing an error.
FALLBACK_WORD = "moist"

# The brief's hard limits, encoded as data so they can be checked.
MAX_WORDS = 1
MIN_WORD_LENGTH = 1
MAX_WORD_LENGTH = 50

# A word is letters only: no spaces, punctuation, digits, or hyphens.
WORD_PATTERN = re.compile(r"^[a-z]+$")


def is_single_word(text):
    """Return True only if text is exactly one lowercase alphabetic word."""
    if text is None:
        return False
    if not isinstance(text, str):
        return False
    if text != text.strip():
        return False
    if not text:
        return False
    if len(text.split()) != 1:
        return False
    if " " in text or "\t" in text or "\n" in text:
        return False
    if not WORD_PATTERN.match(text):
        return False
    if not MIN_WORD_LENGTH <= len(text) <= MAX_WORD_LENGTH:
        return False
    return True


def count_words(text):
    """Count whitespace-separated tokens in text."""
    if not isinstance(text, str):
        return 0
    return len(text.split())


def validate_entry(word):
    """
    Validate the entry against the brief.

    Raises ValueError with a clear message if any rule is broken.
    Returns the word unchanged when every rule passes.
    """
    if word is None:
        raise ValueError("entry word must not be None")
    if not isinstance(word, str):
        raise ValueError("entry word must be a string")
    if word == "":
        raise ValueError("entry word must not be empty")
    if word != word.strip():
        raise ValueError("entry word must not have leading/trailing whitespace")
    if count_words(word) != MAX_WORDS:
        raise ValueError(
            "entry must be exactly one word, got %d words" % count_words(word)
        )
    if not WORD_PATTERN.match(word):
        raise ValueError("entry must be letters only, got %r" % word)
    if word != word.lower():
        raise ValueError("entry word must be lowercase")
    if not MIN_WORD_LENGTH <= len(word) <= MAX_WORD_LENGTH:
        raise ValueError("entry word length out of range")
    return word


def resolve_entry_word():
    """
    Resolve the entry word, with a fallback.

    Try ENTRY_WORD first. If it somehow fails validation, try the
    fallback word. If that also fails, raise -- never silently print
    an unvalidated or multi-word answer.
    """
    try:
        return validate_entry(ENTRY_WORD)
    except ValueError:
        print("warning: primary entry failed validation, using fallback",
              file=sys.stderr)
        return validate_entry(FALLBACK_WORD)


def verify_output(output, expected_word):
    """
    Verify a built stdout payload before it is printed.

    The payload must be exactly the expected word plus one newline,
    with no extra words, spaces, or lines attached.
    """
    if not isinstance(output, str):
        raise ValueError("output must be a string")
    if not output.endswith("\n"):
        raise ValueError("output must end with exactly one newline")
    if output.count("\n") != 1:
        raise ValueError("output must contain exactly one newline")
    stripped = output.rstrip("\n")
    if stripped != expected_word:
        raise ValueError("output does not match the entry word")
    if not is_single_word(stripped):
        raise ValueError("output is not exactly one word")
    if count_words(stripped) != MAX_WORDS:
        raise ValueError("output must be exactly one word")
    return True


def get_entry_text():
    """Return the validated entry text, using the fallback if needed."""
    return resolve_entry_word()


def build_output(word):
    """Build the exact stdout payload: the word plus one trailing newline."""
    validated = validate_entry(word)
    return validated + "\n"


def main(argv=None):
    """Validate the entry, verify the output, then print it and only it."""
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        print("error: this entry takes no arguments", file=sys.stderr)
        return 2

    try:
        entry = get_entry_text()
        output = build_output(entry)
    except ValueError as exc:
        print("error: invalid entry: %s" % exc, file=sys.stderr)
        return 1

    # Final guard before anything reaches stdout: run the full output
    # verification helper, which checks the payload is exactly one
    # word plus one newline, with nothing else attached.
    try:
        verify_output(output, entry)
    except ValueError as exc:
        print("error: output failed final verification: %s" % exc,
              file=sys.stderr)
        return 1

    sys.stdout.write(output)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
