# Corrected VTT Rules (`cloudfall-s1eNN-corrected.vtt`)

The corrected VTT is the cleaned transcript. It stays valid WebVTT and preserves
every cue's timestamps exactly — you're fixing words and speaker attribution, not
re-timing or rewriting the episode.

## What to change

1. **Glossary replacements** — word-boundary, case-aware regex for every variant
   in `cloudfall-master-glossary.md` (see `scripts/apply_glossary.py`). Case is
   preserved: a Titlecase match maps to Titlecase canonical, UPPER to UPPER.

2. **Speaker correction:**
   - Reassign a `Tara / Journey` line to `Maggie / Poppy` when it has
     Poppy-specific markers (cookies, baking, Pinch, Rolling Pin, Grease, butter,
     dough) **and** no Journey-specific markers (Feybuds, hand axe, bow, Firbolg,
     Hunter's Mark, moss/nature framing). Ambiguous → leave as-is.
   - `UNKNOWN` / untagged cue text → `Tim / GM` (Transistor drops the speaker tag
     on GM narration). The parser already does this reassignment; keep it in the
     output.

3. **Accent handling:** Diver and Tic speak cockney, which Transistor mangles
   (e.g. "In the flesh" → "Aim for flesh"). Correct when confident from context;
   flag when not. **"Gove" is a cockney term of address, not a name — leave it
   transcribed as-is.**

## What NOT to change

- **Never invent dialogue.** If crosstalk destroyed a line, leave what Transistor
  captured. Don't smooth it into something plausible.
- Don't alter timestamps, cue ordering, or the `WEBVTT` header.
- Don't "clean up" filler, stutters, or false starts unless they're clearly a
  transcription artifact — the actual-play voice is part of the record.

## Format

Preserve the exact Transistor cue shape:
```
WEBVTT

00:00:00.960 --> 00:00:36.360
<v Tim / GM>text of the cue...

00:00:37.380 --> 00:01:17.740
<v Tara / Journey>next cue...
```
Every cue: blank line, `HH:MM:SS.mmm --> HH:MM:SS.mmm`, then `<v Player / Character>`
followed by the (corrected) text on the same logical line.

## Conflict rule

When Transistor's transcription and the narrative context conflict, **context
wins — but flag the correction** in your closing message so Tim can audit it.
Retroactive corrections (a name that was wrong in an earlier episode) ripple to
all prior files; note which files are affected.
