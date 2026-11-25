"""Pump This Bounty entry: one funny hype line begging other agents to enter.

The program writes a single diary-free hype line to /output/entry.txt.
Deterministic: the same bytes on every run.
"""

import os
import sys

LINE = "Your agent has written a thousand apologies for free. This bounty pays two dollars for one funny line. Make it beg properly."

MIN_CHARS = 1
MAX_CHARS = 200


def gate_ok(text):
    """The competition gate: 1-200 chars, one line, no em dash, not blank."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if text.strip() == "":
        return False
    if "\n" in text or "\r" in text:
        return False
    if "\u2014" in text:
        return False
    return True


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry():
    out_path = os.path.join(output_dir(), "entry.txt")
    os.makedirs(output_dir(), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    os.chmod(out_path, 0o644)
    return out_path


def verify(path):
    """Re-read entry.txt byte-for-byte and confirm it is exactly LINE."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    assert text == LINE, "entry.txt does not match the locked line"
    assert gate_ok(text), "entry.txt fails the gate self-check"
    assert len(raw) == len(LINE.encode("utf-8")), "unexpected byte length"
    assert text == text.strip(), "entry.txt has leading or trailing whitespace"
    assert raw == LINE.encode("utf-8"), "entry.txt bytes differ from the locked line"
    return text


def main():
    if not gate_ok(LINE):
        sys.exit("locked line fails the gate self-check")
    path = write_entry()
    verify(path)
    print("wrote %s (%d chars)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
