# SPDX-License-Identifier: MIT
"""Real-Life Patch Notes: The Comedy Changelog — entry for Akun 1.

Writes the single-line patch-note entry to <out_dir>/entry.txt using
only the Python standard library. No trailing newline: exactly one line.

Reviser note: restructured around build_entry() with tightened
validation (length, printable ASCII, single line, exact sha256) so the
output stays byte-identical to the builder's entry.
"""

import hashlib
import os
import string

ENTRY = (
    "v2.7.1: fixed knees cracking on stairs. "
    "They now crack on flat ground, in quiet rooms, for no reason."
)

EXPECTED_SHA256 = (
    "11648bc8f06f81ad91578995d06d4cf75df71cd9e359c26a930462ac7c328bc3"
)

MAX_CHARS = 160
_ALLOWED = set(string.printable) - set(string.whitespace)


def build_entry():
    """Assemble and validate the entry; returns the exact bytes to write."""
    text = ENTRY
    if not text:
        raise ValueError("entry must not be empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry too long: %d chars, max %d" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    bad = sorted({ch for ch in text if ch not in _ALLOWED and ch != " "})
    if bad:
        raise ValueError("entry has disallowed characters: %r" % bad)
    data = text.encode("utf-8")
    if not 1 <= len(data) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d bytes, got %d" % (MAX_CHARS, len(data)))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("entry sha256 mismatch: %s" % digest)
    return data


def write_entry(out_dir, data):
    """Write bytes directly to <out_dir>/entry.txt, mode 0644."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    return path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    data = build_entry()
    write_entry(out_dir, data)


if __name__ == "__main__":
    main()
