# Combined SEO Post (`cloudfall-s1eNN-post.md`)

This is the publish-ready blog post for Squarespace — the human-facing, search-
optimized version of the episode. Structure is deliberately lean: a short summary
on top for SEO depth and keywords, then the full transcript underneath as the
long-tail searchable body. **Do not duplicate the wiki** — the "key events" and
"quote" material lives in the wiki; the post is just summary + transcript.

Produce this as **clean Markdown** — it's the primary paste target for Squarespace
(see "Pasting into Squarespace" below). Optionally also emit an HTML version
(`cloudfall-s1eNN-post.html`) for single-Code-Block pasting.

## Structure

Keep it to exactly these parts — no "What Happens" walkthrough, no "Notable
Quotes" section (both would duplicate the wiki), and **no footer/navigation note**:

```
# Cloudfall Episode N: "Title"
*People Being Other People · Season 2: Cloudfall*

[1–2 sentence hook: what happens this episode, written for a searcher/newcomer.]

## Episode Summary
[Several short, punchy, aimed paragraphs — NOT one wall of text. Break the wiki's
Full Summary into ~4–6 tight paragraphs, each covering one beat of the episode
(the meeting, the reward/catch, the shopping, the side encounter, the getaway).
Work in natural keywords: character names, the location, "actual play", "D&D
podcast", the arc name.]

## Full Transcript
[The labeled transcript — see "Transcript format" below. The long-tail SEO body.]
```

- The subtitle line is a **plain index**, not a tagline: exactly
  `*People Being Other People · Season 2: Cloudfall*`. No praise or descriptors.
- **No footer.** Do not append "New to People Being Other People? Start with
  Episode 1…" or any listen/nav links. The post ends with the last transcript line.

## Transcript format

The transcript is a labeled read of the corrected VTT — **not** a rewritten
screenplay. The cardinal rule:

> **Never invent language, and never prescribe emotion or action.** Every line is
> what was actually said. You do NOT author stage directions, performance notes,
> or emotional beats. If a character literally says the word "nervous," that's
> their dialogue — never convert it into a `*(nervous)*` direction. If Tim didn't
> narrate an action, it doesn't appear.

### Labels

- **`Player / Character:`** for players, using the full VTT channel label —
  `Tara / Journey`, `Maggie / Poppy`, `Thomas / Guy`, `John / Doran`,
  `Hannah / Eryn`. (The full `Player / Character` form matters: bare character
  names get confusing when players talk to each other at the table as themselves.)
- **`Tim / GM:`** for **everything Tim says** — narration, table-talk (dice calls,
  rulings), *and* NPC dialogue. Do **not** split out NPC voices.
- **No italics anywhere.** Plain text throughout.

### Do NOT split GM cues into NPC voices

Earlier versions tried to break a `Tim / GM` cue into `Tim / Libera`,
`Tim / Phynom`, etc., at speech tags ("she says", "he goes"). **This was dropped.**
The inconsistency — some NPC lines labeled, many untagged ones left as GM — was
more confusing than helpful. Now the rule is simple and consistent: **every cue
Tim speaks stays `Tim / GM`, verbatim, whole.** No speech-tag splitting, no
last-named-character tracking, no per-line NPC attribution. This is also much less
work and keeps the post's GM attribution identical to the corrected VTT.

(`scripts/vtt_to_screenplay.py` still exists but its NPC-splitting scaffold is no
longer used; a plain player-vs-GM pass is all that's needed.)

### Player lines

Players need no splitting — the channel names them. Watch only for crosstalk (one
player's line landing on another's channel, or a stray token like "100" that
belongs to the prior speaker); fix those against the read.

### Scene anchors

Timestamps become `### Part N — Name · MM:SS` headers at the wiki's Part
boundaries — reuse the exact Part titles and start times from the wiki.

### Spacing (load-bearing for Squarespace)

Separate **every** line (speaker lines and headers alike) with a **blank line**, so
each becomes its own `<p>` paragraph. Tim's site CSS applies a subtle `p + p {
margin-top: 1em }`, which gives clean, gentle padding between speakers. Do NOT use
trailing-space hard breaks between lines — those render as cramped non-breaking
returns with no padding. Blank-line paragraphs are correct.

### No cleanup that changes meaning

Apply the same glossary corrections as the VTT (canonical spellings), but do not
smooth stutters into new phrasings, and never rewrite or invent. Faithful-but-raw
beats polished-but-wrong.

## Pasting into Squarespace

**Spacing model (settled with Tim's live CSS).** Tim pastes into the default rich
text / **Text Block** editor, and his site has a collection CSS override that adds
`p + p { margin-top: 1em }` (subtle padding between adjacent paragraphs). So the
correct output is: **every line separated by a blank line**, making each its own
`<p>`. The CSS then supplies gentle, even spacing between speakers. Do **not** use
trailing-space hard breaks — those render as cramped non-breaking returns with no
padding. (This is the reverse of a naive "single line break" approach; the CSS is
what makes blank-line paragraphs the right call.)

**Heading spacing** is controlled by CSS, not Markdown — Squarespace applies its
own heading margins regardless of blank lines. To make each heading read as
connected to the paragraph *below* it and separated from content *above*, give Tim
a CSS snippet scoped to his collection, e.g.:

```css
.collection-XXXX h1, .collection-XXXX h2, .collection-XXXX h3 {
  margin-top: 1.75em; margin-bottom: 0.15em; line-height: 1.2;
}
.collection-XXXX h1:first-child, .collection-XXXX h2:first-child { margin-top: 0; }
```

Squarespace (7.1) has no blog API, so every post is a manual paste. Three targets,
in order of preference:

1. **Markdown Block (preferred).** Paste the Markdown straight in. It strips hidden
   HTML formatting on the way in (no mess from copying between editors) and inherits
   your site's text styles. Squarespace supports basic Markdown — headers, bold,
   italic, blockquotes, lists, links — which covers this whole post. The edit box is
   small, so paste rather than type. (Or set Settings → Advanced → Default Text
   Editor → Markdown to make the main Text Block accept Markdown.)
2. **Text Block.** The default rich editor and the strongest SEO container (cleanest
   crawlable headings/paragraphs). Fine if you paste plain and re-apply headers, but
   pasting styled HTML here can drag in junk formatting — route through Markdown to
   avoid that.
3. **Code Block (HTML fallback).** Use the emitted `.html` when you want the entire
   post self-contained in one block or want styling (e.g. speaker-colored names)
   that survives regardless of theme. ~300,000-char limit easily fits an episode.
   Weaker as an SEO container than a Text/Markdown block, so prefer it only when you
   have a specific reason.

For SEO hygiene on each post: set the post's SEO title and description in post
settings, give it a clean URL slug (e.g. `cloudfall-episode-3`), and tag/categorize
by arc (Farewell) and characters so posts cluster.
