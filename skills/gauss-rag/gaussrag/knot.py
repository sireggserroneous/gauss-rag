#!/usr/bin/env python3
"""A document as a knot: chunks on a ring, cross-references as crossings, read out as Gauss code.

Header-to-header chunks in reading order, closed into a RING (last wraps to first), are the strand.
A cross-reference — "see Section 27", a defined term used far from its definition, "subject to the
Instagram Terms of Use" — is a CROSSING: the strand passes OVER at the referrer (+c) and UNDER at
the referent (−c). Several documents that reference each other are a LINK, one strand each.
Gauss code is the walk around a strand writing down the signed crossings it meets:

    -2 -3 +1 +2 · -1 +3 +4@sideletter

As a data structure this is a cycle plus a signed edge list. What the knot framing keeps that a
bag of edges loses: the SIGN is dependency direction (over→under = what this clause depends on,
under→over = what cites it), the RING is reading order with wraparound, and the code is one line
an LLM can hold. No knot invariants are used; the crossing count is a free "how tangled" number.

Stdlib only. Input is index.py's chunk list; chunks carrying `doc` and `pos` lie on a strand,
everything else (C# symbols, archmap) is ignored here.

    python3 knot.py        # self-check on a toy document
"""
import os
import re

NUM = r"[0-9]+(?:\.[0-9]+)*|[IVXLC]+"
HEAD = re.compile(r"^#{1,4}\s*(?:(?:Article|ARTICLE|Section|SECTION|Chapter|CHAPTER|Part|PART)\s+)?(" + NUM + r")\b[.:]?\s", re.M)
REF = re.compile(r"\b(?:[Ss]ections?|[Aa]rticles?|[Cc]hapters?|[Pp]arts?|[Cc]lauses?|[Pp]aragraphs?|§)\s*(" + NUM + r")\b")
TERM = re.compile(r"[\"“]([A-Z][A-Za-z][A-Za-z ]{1,40}?)[\"”]")
HUB = 0.5      # ponytail: a term used in over half a document's arcs is noise ("Agreement"); sweep on the gold set
MIN_ALIAS = 8  # a title alias must be this long AND more than one word: "services" alone matched everything


def _norm(n):
    """'IV' -> '4', '2.' -> '2'. Arabic and dotted numbers pass through."""
    n = n.rstrip(".")
    if n[0].isdigit():
        return n
    val = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}
    total, prev = 0, 0
    for ch in reversed(n.lower()):
        x = val[ch]
        total = total - x if x < prev else total + x
        prev = x
    return str(total)


def _aliases(title):
    parts = [title] + title.split(" — ")
    out = []
    for p in parts:
        p = p.strip().lower()
        if len(p) >= MIN_ALIAS and " " in p and p not in out:
            out.append(p)
    return out


def build(chunks):
    """Rings, TOC index, crossings and dangling references for every chunk that has a `doc`."""
    docs = {}
    for i, c in enumerate(chunks):
        if "doc" in c:
            docs.setdefault(c["doc"], []).append(i)
    for arcs in docs.values():
        arcs.sort(key=lambda i: chunks[i]["pos"])

    toc = {}
    for d, arcs in docs.items():
        t = {}
        for i in arcs:
            for m in HEAD.finditer(chunks[i]["text"]):   # index EVERY numbered heading in the chunk,
                t.setdefault(_norm(m.group(1)), i)       # so packed sub-sections still resolve refs
        toc[d] = t
    titles = {d: _aliases(chunks[arcs[0]]["text"].split("\n", 1)[0]) for d, arcs in docs.items()}

    xs, dangling, seen = [], [], set()

    def add(over, under, kind, label):
        if over == under or (over, under, kind) in seen:
            return
        seen.add((over, under, kind))
        xs.append({"id": len(xs) + 1, "over": over, "under": under, "kind": kind, "label": label})

    for d, arcs in docs.items():
        for i in arcs:
            for m in REF.finditer(chunks[i]["text"]):
                num = _norm(m.group(1))
                j = toc[d].get(num)
                if j is None:
                    # knots-of-knots: resolve into another strand when exactly one linked doc has it
                    hits = [toc[o][num] for o in toc if o != d and num in toc[o]]
                    if len(hits) == 1:
                        j = hits[0]
                label = " ".join(m.group(0).split())          # "Section\n4.2" → "Section 4.2"
                if j is None:
                    dangling.append({"over": i, "kind": "section", "label": label})
                else:
                    add(i, j, "section", label)

        defs = {}
        for i in arcs:
            for m in TERM.finditer(chunks[i]["text"]):
                defs.setdefault(m.group(1), i)         # first quoted appearance is the definition
        for term, j in defs.items():
            pat = re.compile(r"\b" + re.escape(term) + r"\b")
            users = [i for i in arcs if i != j and pat.search(chunks[i]["text"])]
            if len(users) > HUB * len(arcs):
                continue
            for i in users:
                add(i, j, "term", term)

        for other, aliases in titles.items():
            if other == d:
                continue
            for i in arcs:
                low = chunks[i]["text"].lower()
                hit = next((a for a in aliases if a in low), None)
                if hit:
                    add(i, docs[other][0], "doc", hit)

    return {"docs": docs, "toc": toc, "crossings": xs, "dangling": dangling}


def expand(seeds, knot, limit=40, ring=True):
    """Arcs one step from the seeds, best first: what they depend on, what cites them, then (if ring) neighbours.
    ring=False is for the RRF leg: ring adjacency is document coherence, not relevance, and dilutes ranking."""
    over, under = {}, {}
    for x in knot["crossings"]:
        over.setdefault(x["over"], []).append(x["under"])
        under.setdefault(x["under"], []).append(x["over"])
    ringtab = {}
    for arcs in knot["docs"].values():
        n = len(arcs)
        for k, i in enumerate(arcs):
            ringtab[i] = (arcs[(k - 1) % n], arcs[(k + 1) % n])
    seeds = list(seeds)[:8]
    out, seen = [], set(seeds)
    tables = (over, under, ringtab) if ring else (over, under)
    for table in tables:
        for i in seeds:
            for j in table.get(i, ()):
                if j not in seen:
                    seen.add(j)
                    out.append(j)
    return out[:limit]


def construct(seed, kn, chunks, radius=2):
    """The assembly order for a document, seeded by one hit (chunk index).

    Semantic search finds the seed; THIS says what order to pull the rest of the doc so the model
    reads it the way the document cross-references itself, not just top-to-bottom:

        1. the seed
        2. what the seed depends on   (seed is the OVER pass: '+c' -> its referent)
        3. what cites the seed        (seed is the UNDER pass: '-c' -> its referrer)
        4. ring neighbours within +-radius, in reading order (local context)

    Returns [{pos, idx, label, via, text}] — an ordered fetch plan the caller executes by chunk#.
    """
    doc = chunks[seed].get("doc")
    arcs = kn["docs"].get(doc, [])
    # A long section is split across several chunks; the crossing attaches to whichever fragment
    # holds the reference text. Treat the seed's whole section (same label) as one unit so a hit on
    # its first fragment still surfaces references made anywhere in the section.
    label = chunks[seed].get("label")
    group = {j for j in arcs if chunks[j].get("label") == label} or {seed}
    over, under = {}, {}
    for x in kn["crossings"]:
        if x["over"] in group and x["under"] not in group:
            over.setdefault(x["under"], x)
        if x["under"] in group and x["over"] not in group:
            under.setdefault(x["over"], x)
    pos = chunks[seed].get("pos")
    ring = {}
    if pos is not None and arcs:
        k = arcs.index(seed) if seed in arcs else None
        if k is not None:
            for d in range(1, radius + 1):
                for j, sign in ((arcs[(k - d) % len(arcs)], -d), (arcs[(k + d) % len(arcs)], d)):
                    ring.setdefault(j, sign)

    order, seen = [], set()
    def add(idx, via):
        if idx in seen:
            return
        seen.add(idx)
        c = chunks[idx]
        order.append({"pos": c.get("pos"), "idx": idx, "label": c.get("label"),
                      "via": via, "text": c.get("text", "")})
    add(seed, "seed")
    for idx, x in over.items():
        add(idx, "references -> %s" % x["label"])
    for idx, x in under.items():
        add(idx, "cited by <- %s" % x["label"])
    # knots-of-knots: when a partner lives in ANOTHER document, keep reading there (its ring ±1)
    for idx in list(over) + list(under):
        d2 = chunks[idx].get("doc")
        if d2 and d2 != doc:
            arcs2 = kn["docs"].get(d2, [])
            if idx in arcs2 and len(arcs2) > 1:
                k2 = arcs2.index(idx)
                for dd in (-1, 1):
                    add(arcs2[(k2 + dd) % len(arcs2)], "linked ring %+d in %s" % (dd, _short(d2)))
    for idx, sign in sorted(ring.items(), key=lambda kv: abs(kv[1])):
        add(idx, "ring %+d" % sign)
    return order


def _short(doc):
    """'…/2025-q3-meta--appendix-b.md' → 'appendix-b': the component name pdf_to_md.py gave it."""
    return os.path.splitext(os.path.basename(doc))[0].split("--")[-1]


def gauss(knot, doc):
    """The Gauss code of one strand: signed crossing ids in ring order, '·' for an arc with none."""
    where = {i: d for d, arcs in knot["docs"].items() for i in arcs}
    out = []
    for i in knot["docs"][doc]:
        s = []
        for x in knot["crossings"]:
            if x["over"] == i:
                o = where[x["under"]]
                s.append(f"+{x['id']}" + ("" if o == doc else "@" + _short(o)))
            if x["under"] == i:
                o = where[x["over"]]
                s.append(f"-{x['id']}" + ("" if o == doc else "@" + _short(o)))
        out.append(" ".join(s) or "·")
    return " ".join(out)


def describe(knot, i, chunks):
    """Human/LLM-readable crossings at one arc: '+3 → 4.2 Account suspension (Section 4.2)'."""
    leaf = lambda c: c["label"].split(" › ")[-1]
    out = []
    for x in knot["crossings"]:
        if x["over"] == i:
            out.append(f"+{x['id']} → {leaf(chunks[x['under']])} ({x['label']})")
        if x["under"] == i:
            out.append(f"-{x['id']} ← {leaf(chunks[x['over']])} ({x['label']})")
    return out


def demo():
    T = [("## 1. Definitions", '"Widget" means a thing.'),
         ("## 2. Delivery", "Deliver per Section 5. See Section 9."),
         ("## 3. Payment", "Pay for each Widget."),
         ("## 4. Warranty", "No warranty."),
         ("## 5. Term", "Each Widget lasts a year."),
         ("## 6. Misc", "See the Side Letter for the rest.")]
    chunks = [{"doc": "T", "pos": k, "label": f"Toy › {h[3:]}", "text": f"Toy Contract\n\n{h}\n{b}"}
              for k, (h, b) in enumerate(T)]
    chunks.append({"doc": "U", "pos": 0, "label": "Appendix B — Side Letter › 1. Scope",
                   "text": "Appendix B — Side Letter\n\n## 1. Scope\nGoverns the rest."})
    kn = build(chunks)
    kinds = {(x["over"], x["under"]): x["kind"] for x in kn["crossings"]}
    assert kinds == {(1, 4): "section", (2, 0): "term", (4, 0): "term", (5, 6): "doc"}, kinds
    assert [d["label"] for d in kn["dangling"]] == ["Section 9"], kn["dangling"]
    assert expand([1], kn) == [4, 0, 2], expand([1], kn)          # depends-on, then ring neighbours
    assert expand([0], kn) == [2, 4, 5, 1], expand([0], kn)       # cited-by, then ring (wraps to 5)
    g = gauss(kn, "T")
    assert g == "-2 -3 +1 +2 · -1 +3 +4@U", g
    assert describe(kn, 1, chunks) == ["+1 → 5. Term (Section 5)"], describe(kn, 1, chunks)
    print("ok  gauss(T) =", g)
    print("    crossings:", len(kn["crossings"]), " dangling:", len(kn["dangling"]))


if __name__ == "__main__":
    demo()
