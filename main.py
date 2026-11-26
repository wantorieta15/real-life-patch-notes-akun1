# SPDX-License-Identifier: MIT
"""Real-Life Patch Notes: The Comedy Changelog — entry for Akun 1.

Writes the single-line patch-note entry to <out_dir>/entry.txt using
only the Python standard library. No trailing newline: exactly one line.
"""

import hashlib
import os

ENTRY = "v2.7.1: fixed knees cracking on stairs. They now crack on flat ground, in quiet rooms, for no reason."

EXPECTED_SHA256 = "11648bc8f06f81ad91578995d06d4cf75df71cd9e359c26a930462ac7c328bc3"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    if not 1 <= len(data) <= 160:
        raise ValueError("entry must be 1-160 bytes, got %d" % len(data))
    if b"\n" in data or b"\r" in data:
        raise ValueError("entry must be a single line")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("entry sha256 mismatch: %s" % digest)
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
