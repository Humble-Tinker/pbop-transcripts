#!/usr/bin/env python3
"""
Apply the Cloudfall master glossary to a VTT transcript as word-boundary,
case-aware regex replacements, and report every "Suspicious Words to Watch" hit
so nothing slips past into the corrected VTT unflagged.

This is a mechanical first pass. It does NOT decide new canonical spellings or
correct speakers — those need Tim's confirmation and a full read. Treat its
suspicious-word report as a checklist for the "Glossary Flags" table.

The glossary markdown uses tables like:
    | Canonical | Also Appears As | Notes |
    | Bismyte   | bismite · bismide · biz mite | Core material |
We read the first two columns; variants are split on "·". Entries whose variant
cell is "(correct)" or empty contribute no replacement (nothing to fix), but the
canonical term is still tracked.

Usage:
    python apply_glossary.py transcript.vtt cloudfall-master-glossary.md \
        --out corrected.vtt
"""
import argparse
import re
import sys

# Variants that are ALSO valid in their own right (informal address, spell names
# that share a stem, etc.). Auto-replacing these corrupts correct text, so we
# never apply them silently — we only REPORT them for a human context check.
# Match against the lowercased variant string. Extend as the glossary grows.
AMBIGUOUS_VARIANTS = {
    "nimbus",   # informal for Libera Cambria Nimbus, but used bare constantly
    "libera",   # ditto
    "silvery",  # "Silvery Barbs" (spell) vs Cilivry (place)
    "break",    # "Break Day" vs the ordinary verb
    "gove",     # cockney address, intentionally left as-is
}

# Patterns from the glossary's "Suspicious Words to Watch" section. Keep in sync
# with the glossary; these are the recurring Transistor failure modes.
SUSPICIOUS = [
    (re.compile(r"\bbism\w*", re.I), "likely Bismyte"),
    (re.compile(r"\brol(?:l)?and\b", re.I), "→ Rolan (Transistor adds a trailing 'd')"),
    (re.compile(r"\bsilvery\b", re.I), "standalone 'silvery' → likely Cilivry (not Silvery Barbs)"),
    (re.compile(r"\bphenom\w*", re.I), "→ Phynom Green"),
    (re.compile(r"\bprotobuf\b|\bproto puff\b", re.I), "→ Pronto Puff"),
    (re.compile(r"\bfae bud\b|\bfay bud\b|\bfaye bud\b|\bfae bug\b", re.I), "→ Feybud"),
    (re.compile(r"\btr[ei]ndle\b|\btrundle\b", re.I), "→ Tryndle"),
    (re.compile(r"\blot[ae]m\b|\bloedem\b", re.I), "→ Lodom"),
    (re.compile(r"\bsir bo\b|\bservo\b|\bserbo\b", re.I), "→ Sir Beau"),
]


def parse_glossary(md):
    """Yield (canonical, [variants]) from markdown tables."""
    entries = []
    for line in md.split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        canonical, variant_cell = cells[0], cells[1]
        # skip header / separator rows
        if canonical.lower() in ("canonical", "what was said", "") or set(canonical) <= set("-: "):
            continue
        variants = []
        for v in variant_cell.split("·"):
            v = v.strip()
            if not v or v.lower().startswith("(correct") or "correct" in v.lower():
                continue
            # strip trailing parentheticals like "Nimbus (informal)"
            v = re.sub(r"\s*\(.*?\)\s*$", "", v).strip()
            if v and v.lower() != canonical.lower():
                variants.append(v)
        entries.append((canonical, variants))
    return entries


def case_preserving_sub(text, variant, canonical):
    """Replace variant with canonical on word boundaries, case-aware.
    If the matched text is Titlecase/UPPER, mirror onto the canonical."""
    pattern = re.compile(r"\b" + re.escape(variant) + r"\b", re.I)

    def repl(m):
        matched = m.group(0)
        if matched.isupper():
            return canonical.upper()
        if matched[0].isupper():
            return canonical[0].upper() + canonical[1:]
        return canonical

    return pattern.sub(repl, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("glossary")
    ap.add_argument("--out", help="write corrected text here")
    args = ap.parse_args()

    with open(args.transcript, encoding="utf-8") as f:
        text = f.read()
    with open(args.glossary, encoding="utf-8") as f:
        gloss_md = f.read()

    entries = parse_glossary(gloss_md)
    change_log = []
    review_log = []  # ambiguous variants: found, but NOT auto-replaced
    for canonical, variants in entries:
        for v in variants:
            n = len(re.findall(r"\b" + re.escape(v) + r"\b", text, re.I))
            if n == 0:
                continue
            if v.lower() in AMBIGUOUS_VARIANTS:
                review_log.append((v, canonical, n))
                continue
            text = case_preserving_sub(text, v, canonical)
            change_log.append((v, canonical, n))

    print("Glossary replacements applied:")
    if change_log:
        for v, c, n in sorted(change_log, key=lambda x: -x[2]):
            print(f"  {v!r} -> {c!r}  ({n}x)")
    else:
        print("  (none)")

    if review_log:
        print("\nAmbiguous — NOT auto-replaced, check context by hand:")
        for v, c, n in sorted(review_log, key=lambda x: -x[2]):
            print(f"  {v!r} (canonical {c!r}) appears {n}x — replace only where it's the proper noun")

    print("\nSuspicious-word hits (verify against context — do NOT auto-fix):")
    any_hit = False
    for pat, note in SUSPICIOUS:
        hits = sorted(set(m.group(0) for m in pat.finditer(text)))
        if hits:
            any_hit = True
            print(f"  {note}: {', '.join(hits)}")
    if not any_hit:
        print("  (none)")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nWrote glossary-applied transcript to {args.out}")
    else:
        print("\n(no --out given; not writing file)")


if __name__ == "__main__":
    main()
