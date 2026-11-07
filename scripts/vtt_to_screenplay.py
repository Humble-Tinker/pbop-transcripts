#!/usr/bin/env python3
"""
Convert a corrected PBOP VTT into a screenplay-style SCAFFOLD for the readable
blog transcript. This produces a first-pass draft you then edit by hand — it
CANNOT do the two things that need judgment and a full read:

  1. GM disambiguation. Transistor tags everything Tim says as "Tim / GM", but
     that covers BOTH narration and in-character NPC dialogue. Deciding whether a
     given GM line is narration (-> italic stage direction) or a specific NPC
     (-> **Tic:**, **Clara:**, etc.) requires context — accent, scene, who was
     addressed, and the wiki. This script leaves every GM line marked
     `<<GM? narration-or-npc>>` so you can resolve each one. When a line is
     genuinely ambiguous, fall back to **GM:** rather than guessing an NPC name;
     a wrong name is worse than a neutral one, and inventing attributions is off
     limits.
  2. Scene anchors. Timestamps become SPARSE anchors at Part/scene boundaries
     (from the wiki), not per-cue. This script inserts a `## <<PART TITLE>> · MM:SS`
     placeholder roughly every few minutes; replace the count/titles with the
     wiki's actual Part structure.

Everything the players say (Journey, Poppy, Guy, Doran, Eryn) is attributed
directly from the VTT channel and needs no disambiguation — only GM does.

Output is Markdown (the primary paste target for Squarespace — see
references/seo-post.md). Speaker names bold, narration italic.

Usage:
    python vtt_to_screenplay.py corrected.vtt > screenplay_scaffold.md
"""
import re
import sys

VOICE = re.compile(r"<v\s+([^>]+)>(.*)", re.DOTALL)
TS = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.\d{3}\s*-->", )


def secs(h, m, s):
    return int(h) * 3600 + int(m) * 60 + int(s)


def mmss(total):
    m, s = divmod(int(total), 60)
    return f"{m:02d}:{s:02d}"


def parse(raw):
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    cues = []
    for block in re.split(r"\n\s*\n", raw):
        lines = [ln for ln in block.split("\n") if ln.strip()]
        ts_line = next((ln for ln in lines if "-->" in ln), None)
        if not ts_line:
            continue
        m = TS.search(ts_line)
        if not m:
            continue
        start = secs(*m.groups())
        body = " ".join(lines[lines.index(ts_line) + 1:]).strip()
        mv = VOICE.match(body)
        if mv:
            speaker = mv.group(1).strip()
            text = mv.group(2).strip()
        else:
            speaker = "Tim / GM"
            text = body
        cues.append((start, speaker, text))
    return cues


def character(speaker):
    """'Tara / Journey' -> 'Journey'. GM stays flagged."""
    if "/" in speaker:
        left, right = [p.strip() for p in speaker.split("/", 1)]
        if right.upper() == "GM" or right == "":
            return None  # GM: needs disambiguation
        return right
    return speaker


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cues = parse(open(sys.argv[1], encoding="utf-8").read())

    ANCHOR_EVERY = 180  # seconds; drop a placeholder scene anchor ~every 3 min
    last_anchor = -ANCHOR_EVERY
    part_n = 0

    print("<!-- SCREENPLAY SCAFFOLD — edit before publishing. -->")
    print("<!-- Resolve every <<GM? ...>> into either italic narration or **NPCName:** -->")
    print("<!-- Replace <<PART ...>> placeholders with the wiki's real Part titles/ranges. -->\n")

    for start, speaker, text in cues:
        if start - last_anchor >= ANCHOR_EVERY:
            part_n += 1
            print(f"\n## <<PART {part_n} TITLE>> · {mmss(start)}\n")
            last_anchor = start

        char = character(speaker)
        if char is None:
            # GM line — could be narration or an NPC. Flag for the human.
            print(f"<<GM? narration-or-npc>> {text}\n")
        else:
            print(f"**{char}:** {text}\n")


if __name__ == "__main__":
    main()
