#!/usr/bin/env python3
"""
Remap source code by position ID modulo N using an alpha mapping.

Steps:
1. Load solution.cpp into memory (buffer).
2. Hash buffer (SHA256) for reference.
3. For each character in buffer:
   - If newline, preserve it.
   - Else, take its index ID (position in buffer).
   - Reduce ID modulo M (default: 12).
   - Replace char with symbol from alpha.txt at that reduced index.
4. Save result to out.txt
"""

import hashlib
from pathlib import Path
import argparse

def load_alpha(alpha_path: Path) -> list[str]:
    lines = alpha_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError("alpha.txt is empty.")
    # use the first character of each line as symbol
    return [line[0] if line else "" for line in lines]

#def remap_by_index(src: str, alpha: list[str], modulo: int = 12) -> str:
def remap_by_index(src: str, alpha: list[str], modulo: int = 12, offset: int = 0) -> str:
    out_chars = []
    for i, ch in enumerate(src):
        if ch == "\n" or ch == "\t":
            out_chars.append(ch)
            continue
        #reduced = i % modulo
        reduced = (i + offset) % modulo
        out_chars.append(alpha[reduced])
    return "".join(out_chars)

def main():
    parser = argparse.ArgumentParser(description="Remap file by ID modulo alpha")
    parser.add_argument("-i", "--input", required=True, help="Path to input source (e.g., solution.cpp)")
    parser.add_argument("-a", "--alpha", required=True, help="Path to alpha.txt")
    parser.add_argument("-o", "--output", required=True, help="Path to write out.txt")
    parser.add_argument("-m", "--modulo", type=int, default=12, help="Modulo value (default 12)")
    parser.add_argument("--offset", type=int, help="Optional fixed offset (overrides SHA256-derived offset)")
    args = parser.parse_args()

    src_path = Path(args.input)
    alpha_path = Path(args.alpha)
    out_path = Path(args.output)

    # buffer + hash
    buf = src_path.read_text(encoding="utf-8")
    sha256 = hashlib.sha256(buf.encode("utf-8")).hexdigest()
    if args.offset is not None:
        offset = args.offset % args.modulo
    else:
        offset = int(sha256[:8], 16) % args.modulo

    # load alpha
    alpha = load_alpha(alpha_path)

    # remap
    #out_text = remap_by_index(buf, alpha, args.modulo)
    out_text = remap_by_index(buf, alpha, args.modulo, offset)
    out_path.write_text(out_text, encoding="utf-8")

    print(f"Buffer length: {len(buf)}")
    print(f"SHA256: {sha256}")
    print(f"Offset: {offset} ({'user-specified' if args.offset is not None else 'sha256-derived'})")

    print(f"Modulo: {args.modulo}")
    print(f"Output written: {out_path}")

if __name__ == "__main__":
    main()
