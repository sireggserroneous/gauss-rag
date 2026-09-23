#!/usr/bin/env python3
"""Analysis lenses over the knot — pure functions on {crossings, dangling}. No models.
  hubs     : arcs many others bend around (high in-degree)  -> the clause everything depends on
  fanout   : arcs that branch (high out-degree)             -> a branchy requirement, referenced in prose
  cycles   : A depends on B depends back on A (bounded)     -> contention / circular definitions
  dangling : references to nothing, per document            -> drafting holes
"""
from collections import Counter, defaultdict
import os


def analyze(kn, chunks, top=12, max_cycle=4):
    xs = kn["crossings"]
    out_d, in_d = Counter(x["over"] for x in xs), Counter(x["under"] for x in xs)
    adj = defaultdict(set)
    for x in xs:
        adj[x["over"]].add(x["under"])
    leaf = lambda i: chunks[i]["label"].split(" › ")[-1]
    doc = lambda i: os.path.basename(chunks[i].get("doc", ""))
    hubs = [{"idx": i, "label": leaf(i), "doc": doc(i), "in": n} for i, n in in_d.most_common(top)]
    fanout = [{"idx": i, "label": leaf(i), "doc": doc(i), "out": n} for i, n in out_d.most_common(top)]
    # bounded cycle search: paths over->under that return to the start
    cycles, seen = [], set()
    def dfs(start, node, path):
        if len(path) > max_cycle:
            return
        for nxt in adj.get(node, ()):
            if nxt == start and len(path) >= 2:
                key = frozenset(path)
                if key not in seen:
                    seen.add(key); cycles.append(list(path))
            elif nxt not in path:
                dfs(start, nxt, path + [nxt])
    for s in list(adj):
        dfs(s, s, [s])
    cyc = [{"arcs": c, "labels": [leaf(i) for i in c], "doc": doc(c[0])} for c in cycles[:top]]
    dang = defaultdict(list)
    for d in kn["dangling"]:
        dang[doc(d["over"])].append(d["label"])
    return {"hubs": hubs, "fanout": fanout, "cycles": cyc,
            "dangling_by_doc": {k: sorted(set(v)) for k, v in dang.items()},
            "totals": {"crossings": len(xs), "dangling": len(kn["dangling"]), "cycles": len(cycles)}}


def demo():
    chunks = [{"label": f"T › {i}", "doc": "T"} for i in range(4)]
    kn = {"crossings": [{"over": 0, "under": 1, "kind": "section", "label": "s1"},
                        {"over": 1, "under": 0, "kind": "section", "label": "s0"},
                        {"over": 2, "under": 1, "kind": "term", "label": "t"},
                        {"over": 3, "under": 1, "kind": "term", "label": "t"}],
          "dangling": [{"over": 3, "kind": "section", "label": "Section 9"}]}
    a = analyze(kn, chunks)
    assert a["hubs"][0]["idx"] == 1 and a["hubs"][0]["in"] == 3, a["hubs"]
    assert a["totals"]["cycles"] == 1 and set(a["cycles"][0]["arcs"]) == {0, 1}, a["cycles"]
    assert a["dangling_by_doc"] == {"T": ["Section 9"]}
    print("ok  analyze demo: hub=1, one 2-cycle, one dangling")


if __name__ == "__main__":
    demo()
