# Stats File Structure (`cloudfall-s1eNN-stats.md`)

**Emphasis: cumulative totals across all episodes, organized by arc.** Every
cumulative table shows per-episode columns so errors are auditable:
`| Character | E01 | E02 | E03 | **Total** |`. The latest episode's stats file
doubles as the cumulative record.

Damage numbers are **verified manually from the reading, never regex-extracted**.
The parser gives you line counts and air time only.

## Header
```
# Cloudfall — S1ENN Stats & Metrics
**People Being Other People · Season 2 · Cloudfall · Episode N · "Title"**
```

## Sections

### 1. Talk Focus
Per character: `| Character | Player | Lines | Air Time | Share |`, sorted by air
time descending. Computed from `parse_vtt.py` (timestamp durations). GM share is
typically **45–65%**. Follow the table with a `>` blockquote noting anything that
skews the numbers — mis-attribution corrected, a combat-heavy vs social-heavy
episode, one player driving all the social encounters, etc.

### 2. Combat (this episode)
- **Damage Dealt:** `| Character | Target | Damage | Method |` — one row per hit.
- **Damage Taken:** `| Character | Source | Damage | Effect/Notes |`.
- **Kills.**
If there's no combat, say so explicitly (`*No combat this episode.*`) rather than
omitting the section — its absence is itself a data point. Add a `>` blockquote
for anything notable (a survival-by-exact-margin, a specter destroyed by
environment, etc.).

### 3. Cumulative tables
Damage Dealt, Kills, Damage Taken — each with **per-episode columns** and a
**Total**. Build these by taking the prior episode's stats file and appending the
new episode's column. Do NOT recompute history from scratch; the whole point of
the per-episode columns is auditability against prior files.
- Damage Dealt / Kills: full `| Character | E01 | ... | EN | **Total** |` grids.
- Damage Taken can use `| Character | Total Taken | Notable Hits |` if that's how
  the prior file did it — match the established shape.
- Include familiars (e.g. Pinch) as their own rows with `—` for episodes they
  weren't present.

### 4. NPC Status at Episode End
Table of every NPC whose status changed this episode.

### 5. Spells & Abilities Used (this episode)
`| Character | Ability | Count |`. Count actual uses only. Damage numbers here are
from your manual reading, never regex-trusted.

### 6. Special Counters (cumulative — always include, even at zero)
These are running gags/threads the show tracks. Present each as a small
per-episode table with a season total.
- **"Natural 20, Bitch" — Maggie** — the exact phrase (or a close variant) said by
  **Maggie only**. Document near-misses in the notes column (e.g. E03's
  *"19, bitch"*). Still at zero through E03 — keep the counter alive and note the
  watch.
- **Head Losses — Guy** — Guy's Dullahan head detaching.
- Other counters that have emerged in prior files (e.g. Pronto Puffs Consumed,
  Nat 20s This Episode across all players) — carry them forward if the prior file
  had them.
- **Propose a new counter when a pattern appears twice**, but ask before adding it
  permanently.

### 7. Rolls of Note
`| Time | Character | Roll | Result | Outcome |` — nat 20s, nat 1s, clutch saves,
dramatic failures, and (in social-heavy episodes) pivotal skill checks. In a
no-combat episode, social checks are the main mechanical action — say so.

### 8. Mission Outcome
Objectives table with ✅ / ❌ / ⚠️ per objective:
`| Objective | Result |`.

### 9. Arc Summary (arc-closing episodes only)
Totals for the arc — damage, kills, NPCs introduced, locations established,
counters, mission success (⚠️ Partial / ✅ / ❌). Arc 1 is **Farewell**.
Only include this section on the episode that closes an arc.
