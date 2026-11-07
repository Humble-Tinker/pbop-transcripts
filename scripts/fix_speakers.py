#!/usr/bin/env python3
"""
Second correction pass: tag every cue and apply the episode's reviewed fixes.

1. Every cue gets an explicit <v Speaker> tag. Untagged cues continue the last
   tagged speaker (Transistor drops the tag when a line spills across a cue).
2. Reviewed fixes from a JSON file are applied, so every judgment call made
   during the read is recorded and auditable:

    {
      "speakers": {"00:12:05.330": "Maggie / Poppy"},
      "text": [["01:33:20.035", "Aim for flesh", "In the flesh"]]
    }

   Keys are cue start timestamps exactly as they appear in the VTT. A text fix
   must match inside that cue or the script stops, so nothing silently misses.

    python scripts/fix_speakers.py glossaried.vtt fixes.json --out corrected.vtt
"""
import argparse
import json
import pathlib
import re
import sys

TS = re.compile(r"^(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->")
VOICE = re.compile(r"^<v\s+([^>]+)>(.*)$")
GM = "Tim / GM"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vtt")
    ap.add_argument("fixes", nargs="?")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    fixes = json.loads(pathlib.Path(a.fixes).read_text()) if a.fixes else {}
    spk_fix = dict(fixes.get("speakers", {}))
    txt_fix = {}
    for ts, old, new in fixes.get("text", []):
        txt_fix.setdefault(ts, []).append((old, new))

    blocks = re.split(r"\n\s*\n", pathlib.Path(a.vtt).read_text().replace("\r\n", "\n").strip())
    out, last, applied_s, applied_t = ["WEBVTT"], GM, set(), 0
    for b in blocks:
        lines = [l for l in b.split("\n") if l.strip()]
        ts_i = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if ts_i is None:
            continue
        ts_line = lines[ts_i]
        start = TS.match(ts_line).group(1)
        body = " ".join(lines[ts_i + 1:]).strip()
        m = VOICE.match(body)
        spk, text = (m.group(1).strip(), m.group(2).strip()) if m else (last, body)
        if start in spk_fix:
            spk = spk_fix[start]
            applied_s.add(start)
        for old, new in txt_fix.get(start, []):
            if old not in text:
                sys.exit(f"text fix not found at {start}: {old!r}")
            text = text.replace(old, new, 1)
            applied_t += 1
        last = spk
        out += ["", ts_line, f"<v {spk}>{text}"]

    missing = set(spk_fix) - applied_s
    if missing:
        sys.exit(f"speaker fixes with no matching cue: {sorted(missing)}")
    pathlib.Path(a.out).write_text("\n".join(out) + "\n")
    print(f"wrote {a.out} · {len(applied_s)} speaker fixes · {applied_t} text fixes")


if __name__ == "__main__":
    main()
