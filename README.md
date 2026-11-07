# PBOP Transcripts

Source of truth for the *People Being Other People* transcript pipeline: raw and corrected transcripts, wiki and stats records, canon registries, the master glossary, and the Squarespace-ready transcript pages.

## Layout

```
episodes.csv                 one row per episode: Transistor id, title, transcript URL, pipeline status
raw/<campaign>/              untouched Transistor output (-eNN.vtt, plus -eNN.txt when fetched via MCP)
corrected/<campaign>/        glossary-applied, speaker-fixed VTT (-eNN.vtt)
wiki/<campaign>/             per-episode wiki entries (-eNN-wiki.md)
stats/<campaign>/            per-episode stats pages (-eNN-stats.md)
canon/<campaign>/            running registries: npcs.md, locations.md, threads.md, items.md
pages/<campaign>/            Squarespace page spec (-eNN.json) and built page (-eNN.md)
glossary/                    master glossary per campaign
docs/conventions/            the load-bearing format rules (wiki, stats, VTT, page)
scripts/                     deterministic steps (fetch, parse, glossary, page build)
```

File stems are `<campaign>-eNN` (e.g. `cloudfall-e07`). Earlier deliverables used `cloudfall-s1eNN`; same episodes.

## Per-episode flow

1. **Fetch** the transcript into `raw/` with `scripts/transistor_fetch.py` (VTT URL preferred; MCP chunks as fallback).
2. **Parse** for talk focus: `scripts/parse_vtt.py`.
3. **Correct**: `scripts/apply_glossary.py`, then speaker fixes from a full read → `corrected/`.
4. **Write** wiki and stats per `docs/conventions/`, and update `canon/` registries.
5. **Page**: write `pages/<campaign>/<campaign>-eNN.json` (hook, summary, Parts), then `scripts/build_page.py` → `.md` ready to paste into Squarespace.
6. Update `episodes.csv` status and commit one episode per commit.
