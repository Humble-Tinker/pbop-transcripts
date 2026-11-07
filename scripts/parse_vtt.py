#!/usr/bin/env python3
"""
Parse a Transistor-exported WebVTT transcript for the PBOP Cloudfall pipeline.

Deterministic bookkeeping only:
  - splits cues into (start, end, speaker, text) tuples
  - untagged cues continue the last tagged speaker (Transistor omits the
    tag when a line spills across a cue boundary)
  - computes per-speaker line counts and air time (sum of end - start)

It does NOT correct speakers, apply the glossary, or interpret combat — those
need judgment and a full read of the transcript. This just gives you the numbers
so Talk Focus is accurate and auditable.

Usage:
    python parse_vtt.py input.vtt                 # print talk-focus summary
    python parse_vtt.py input.vtt --json out.json # also dump parsed cues as JSON
"""
import argparse
import json
import re
import sys

TS = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
)
VOICE = re.compile(r"<v\s+([^>]+)>(.*)", re.DOTALL)
GM = "Tim / GM"


def to_seconds(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def fmt_clock(total_seconds):
    total = int(round(total_seconds))
    m, s = divmod(total, 60)
    return f"{m}m {s:02d}s"


def fmt_ts(total_seconds):
    total = int(total_seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def parse(raw):
    """Return list of cues: {start, end, dur, speaker, text}."""
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n\s*\n", raw)
    cues = []
    last_speaker = GM
    for block in blocks:
        lines = [ln for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        ts_line = next((ln for ln in lines if "-->" in ln), None)
        if not ts_line:
            continue
        mt = TS.search(ts_line)
        if not mt:
            continue
        g = mt.groups()
        start = to_seconds(*g[0:4])
        end = to_seconds(*g[4:8])
        # text lines are everything after the timestamp line
        idx = lines.index(ts_line)
        text_lines = lines[idx + 1 :]
        text = " ".join(text_lines).strip()
        mv = VOICE.match(text)
        if mv:
            speaker = mv.group(1).strip()
            body = mv.group(2).strip()
        else:
            # Untagged cue: Transistor drops the tag when a speaker's sentence
            # spills across a cue boundary, so it continues the last tagged
            # speaker (fix found in E07). Only a cue with no prior speaker
            # falls back to GM.
            speaker = last_speaker
            body = text
        last_speaker = speaker
        cues.append(
            {
                "start": start,
                "end": end,
                "dur": max(0.0, end - start),
                "ts": fmt_ts(start),
                "speaker": speaker,
                "text": body,
            }
        )
    return cues


def talk_focus(cues):
    stats = {}
    for c in cues:
        s = stats.setdefault(c["speaker"], {"lines": 0, "air": 0.0})
        s["lines"] += 1
        s["air"] += c["dur"]
    total_air = sum(s["air"] for s in stats.values()) or 1.0
    rows = []
    for speaker, s in stats.items():
        rows.append(
            {
                "speaker": speaker,
                "lines": s["lines"],
                "air_seconds": s["air"],
                "air": fmt_clock(s["air"]),
                "share_pct": round(100 * s["air"] / total_air, 1),
            }
        )
    rows.sort(key=lambda r: r["air_seconds"], reverse=True)
    return rows, total_air


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vtt")
    ap.add_argument("--json", help="dump parsed cues to this path")
    args = ap.parse_args()

    with open(args.vtt, encoding="utf-8") as f:
        raw = f.read()

    cues = parse(raw)
    rows, total_air = talk_focus(cues)

    runtime = cues[-1]["end"] if cues else 0
    print(f"Cues parsed: {len(cues)}")
    print(f"Episode runtime (last cue end): {fmt_ts(runtime)}")
    print(f"Total speaking air time: {fmt_clock(total_air)}\n")
    print(f"{'Speaker':<24}{'Lines':>7}{'Air':>10}{'Share':>8}")
    print("-" * 49)
    for r in rows:
        print(f"{r['speaker']:<24}{r['lines']:>7}{r['air']:>10}{r['share_pct']:>7}%")

    # Sanity signal for speaker-correction: how many lines are UNKNOWN-ish or
    # landed under a single-name channel worth double-checking.
    gm_share = next((r["share_pct"] for r in rows if r["speaker"] == GM), 0)
    print(f"\nGM share: {gm_share}%  (typical range 45-65%)")
    if not (40 <= gm_share <= 70):
        print("  ^ outside typical range — worth a sanity check on attribution.")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"cues": cues, "talk_focus": rows}, f, indent=2)
        print(f"\nWrote parsed cues to {args.json}")


if __name__ == "__main__":
    main()
