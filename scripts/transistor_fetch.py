#!/usr/bin/env python3
"""
Turn Transistor transcript output into the repo's raw files.

Two input routes, both deterministic:

  1. VTT (preferred). Download the episode's transcript_url
     (https://share.transistor.fm/s/<id>/transcription.vtt) straight to
     raw/<campaign>/<campaign>-eNN.vtt. Real start AND end times; zero context
     cost. Requires share.transistor.fm on the session's network allowlist.

         python scripts/transistor_fetch.py vtt <transcript_url> --ep 1

  2. MCP "llm" chunks. get_episode_transcript returns JSON chunks with lines like
     "[23:14] Speaker: text". Large chunks are saved by the harness as JSON files
     in tool-results/; pass every chunk file (in order) to stitch them.
     Start times only, so end = next line's start (last line ends at duration).

         python scripts/transistor_fetch.py llm chunk1.json chunk2.json --ep 1

Both routes write raw/<campaign>/<campaign>-eNN.vtt. Route 2 also keeps the
stitched llm text as -eNN.txt, since its line segmentation is what the
published Squarespace pages follow.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINE = re.compile(r"^\[(?:(\d+):)?(\d{1,2}):(\d{2})\]\s+([^:]+?):\s?(.*)$")


def secs(h, m, s):
    return int(h or 0) * 3600 + int(m) * 60 + int(s)


def ts(t):
    h, rem = divmod(float(t), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def load_chunk(path):
    """Accept a raw MCP JSON object, or the harness's persisted [{type,text}] wrapper."""
    data = json.loads(pathlib.Path(path).read_text())
    if isinstance(data, list):
        data = json.loads(data[0]["text"])
    return data


def parse_llm(text):
    cues = []
    for raw in text.splitlines():
        m = LINE.match(raw.strip())
        if m:
            h, mi, s, spk, body = m.groups()
            cues.append({"start": secs(h, mi, s), "speaker": spk.strip(), "text": body.strip()})
        elif raw.strip() and cues:  # continuation line
            cues[-1]["text"] += " " + raw.strip()
    return cues


def cues_to_vtt(cues, duration=None):
    out = ["WEBVTT", ""]
    for i, c in enumerate(cues):
        end = cues[i + 1]["start"] if i + 1 < len(cues) else (duration or c["start"] + 5)
        if end <= c["start"]:
            end = c["start"] + 1
        out += [f"{ts(c['start'])} --> {ts(end)}", f"<v {c['speaker']}>{c['text']}", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("route", choices=["vtt", "llm"])
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--ep", type=int, required=True)
    ap.add_argument("--campaign", default="cloudfall")
    ap.add_argument("--allow-partial", action="store_true", help="testing only")
    a = ap.parse_args()

    dest = ROOT / "raw" / a.campaign
    dest.mkdir(parents=True, exist_ok=True)
    stem = dest / f"{a.campaign}-e{a.ep:02d}"

    if a.route == "vtt":
        r = subprocess.run(["curl", "-sSfL", "-o", f"{stem}.vtt", a.inputs[0]])
        if r.returncode:
            sys.exit("Download failed. Is share.transistor.fm on the network allowlist?")
        print(f"wrote {stem}.vtt")
        return

    chunks = [load_chunk(p) for p in a.inputs]
    if chunks[-1].get("next_offset") is not None and not a.allow_partial:
        sys.exit(f"Incomplete: last chunk has next_offset={chunks[-1]['next_offset']}")
    text = "".join(c["transcript"] for c in chunks)
    duration = chunks[0].get("episode", {}).get("duration")
    cues = parse_llm(text)
    (stem.with_suffix(".txt")).write_text(text)
    (stem.with_suffix(".vtt")).write_text(cues_to_vtt(cues, duration))
    print(f"wrote {stem}.txt and {stem}.vtt ({len(cues)} lines, end times derived)")


if __name__ == "__main__":
    main()
