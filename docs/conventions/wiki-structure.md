# Wiki Entry Structure (`cloudfall-s1eNN-wiki.md`)

**Formatting philosophy:** short 2–4 word hierarchical labels, with full detail
only at the bottom (beat) level. Heavy nesting, bold on names/key terms, `·`
separators for compact attribute strings. Maximize visual scannability. Minimize
parentheticals in the narrative sections — no character hints, no damage numbers.
Damage and mechanics live in the stats file; the wiki is the story record.

Match the voice of the existing episodes in the Project. When in doubt, open the
prior episode's wiki and mirror it.

## Section order

### 1. Title + header line
```
# Cloudfall — S1ENN: "Episode Title"
**People Being Other People · Season 2 · Cloudfall · Episode N · Runtime ~H:MM**
```
(Title comes from Tim if he's named the episode; otherwise propose one from a
title-drop line or the episode's central image, and flag it as a suggestion.)

### 2. Full Summary
One paragraph. The complete episode arc start to finish — who did what, how it
resolved, where it leaves the party. Dense but readable prose. This is the thing
someone reads to remember the episode.

### 3. Key Events — nested hierarchy
```
### Part N — Name
*(HH:MM – HH:MM)*

- **Scene name**
  - Beat — a tangible action or hyper-summarized exchange
  - Beat — dialogue quoted sparingly with *italics*, attributed inline
```
- `### Part N — Name` = a major chapter of the episode, with a timestamp range.
- `- **Scene name**` = bolded bullet.
- `  - Beat` = sub-bullets. Tangible actions and compressed conversation. Roll
  results can appear compactly inline (e.g. `(Persuasion 18)`) since they're part
  of the beat, but keep damage numbers out — those go to stats.

### 4. NPCs
One `###` block per NPC introduced or meaningfully updated. Race/role **bolded**.
End with **Status** where relevant. Mark state in the header:
`### Name *(new)*` / `*(updated)*` / `*(deceased)*` / `*(new · fictional)*` for
disguises like Tryndle Breath. Use `·`-separated attribute strings.

### 5. Locations
Same pattern as NPCs. Only new or changed locations.

### 6. Lore & World
New world mechanics, item properties, faction details. `### Term *(resolved)*`
when a mystery closes this episode.

### 7. Unresolved Threads
Bolded thread name, em-dash, one-line state:
`- **Thread name** — one-line current state`
Carry forward unresolved threads from prior episodes when they're touched this
episode. Note first occurrences. (Cross-check against the prior wiki's thread
list so nothing silently drops.)

### 8. Quote Candidates
Table, 8–12 rows, **over-inclusive by design** — Tim culls for social clips.
```
| Time | Speaker | Quote | Why |
|------|---------|-------|-----|
| HH:MM:SS | Character | *"the line"* | one-line reason |
```
Selection heuristics — pull lines that are:
- Player reactions captured in transcript (laughter, echoes, callbacks)
- Character-defining
- Repeated back by other players later
- Comedic reversals, deadpan under absurd circumstances, **title drops**

Table reaction audio (laughter, groans) is NOT in the transcript. When a quote's
punch depends on the room's reaction, say so in the "Why" cell so Tim can judge
from memory.

### 9. Glossary Flags — New This Episode
Table of what to fix or watch:
```
| Correct | Transistor Output |
|---------|------------------|
| Tryndle | Trendle · Trindle · Trundle |
| Isle of Lor | Isle of Lor (correct — new, watch future episodes) |
```
Include confirmed-correct **new proper nouns**, marked
`(correct — watch future episodes)`, so they enter the glossary's watch list.
Everything here is a proposal until Tim confirms — present these as questions in
your closing message, don't silently canonize a spelling.
