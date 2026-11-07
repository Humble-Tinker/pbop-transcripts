#!/usr/bin/env python3
"""
Build the Squarespace transcript page for one episode.

Mechanical assembly only. The judgment parts (hook, summary paragraphs, Part
names and start times) come from a small JSON spec written after the full read;
the transcript body comes verbatim from the corrected VTT.

Spec (pages/<campaign>/<campaign>-eNN.json):
    {
      "episode": 1,
      "title": "This Is Farewell",
      "hook": "One or two sentences for a newcomer.",
      "summary": ["Paragraph one with **Bold** names.", "Paragraph two."],
      "parts": [{"name": "Gathering at Clara's Bar", "start": "00:00"},
                {"name": "Doran's Dream", "start": "18:00"}]
    }

Output format matches pboppodcast.com/transcripts-cloudfall/cloudfall-episode-1:
every line its own paragraph (blank-line separated), `**Player / Character:**`
labels, `### Part N — Name · MM:SS` headers (minutes may exceed 59), no
italics in the body, no footer.

    python scripts/build_page.py corrected/cloudfall/cloudfall-e01.vtt \
        pages/cloudfall/cloudfall-e01.json
"""
import argparse
import json
import pathlib
import re

TS = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.\d{3}\s*-->")
VOICE = re.compile(r"<v\s+([^>]+)>(.*)")
GM = "Tim / GM"
SEASON = {"cloudfall": "Season 2: Cloudfall", "cursebreaker": "Season 1: Cursebreaker"}


def read_cues(vtt_path):
    cues, start, last = [], None, GM
    for line in pathlib.Path(vtt_path).read_text().splitlines():
        m = TS.match(line)
        if m:
            h, mi, s = map(int, m.groups())
            start = h * 3600 + mi * 60 + s
            continue
        if start is None or not line.strip() or line.startswith("WEBVTT"):
            continue
        v = VOICE.match(line)
        spk, text = (v.group(1).strip(), v.group(2).strip()) if v else (last, line.strip())
        last = spk
        cues.append((start, spk, text))
    return cues


def mmss(value):
    mi, s = value.split(":")[-2:]
    return int(mi) * 60 + int(s)


def build(cues, spec, campaign):
    n = spec["episode"]
    name = campaign.capitalize()
    out = [
        f'# {name} Episode {n}: "{spec["title"]}"',
        f"*People Being Other People · {SEASON.get(campaign, campaign)}*",
        spec["hook"],
        "## Episode Summary",
        *spec["summary"],
        "## Full Transcript",
    ]
    parts = sorted(spec["parts"], key=lambda p: mmss(p["start"]))
    pi = 0
    for start, spk, text in cues:
        while pi < len(parts) and (pi == 0 or start >= mmss(parts[pi]["start"])):
            p = parts[pi]
            out.append(f"### Part {pi + 1} — {p['name']} · {p['start']}")
            pi += 1
        out.append(f"**{spk}:** {text}")
    return "\n\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vtt")
    ap.add_argument("spec")
    ap.add_argument("--campaign", default="cloudfall")
    ap.add_argument("--out")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    page = build(read_cues(a.vtt), spec, a.campaign)
    out = pathlib.Path(a.out or pathlib.Path(a.spec).with_suffix(".md"))
    out.write_text(page)
    print(f"wrote {out} ({page.count('**') // 2} labeled lines)")


if __name__ == "__main__":
    main()
