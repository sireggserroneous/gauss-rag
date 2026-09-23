#!/usr/bin/env python3
"""Code-Gauss: a program's typed edges as crossings — 'the loops of a program'.
Reads an architecture-map.json (teworker shape) and emits one chunk per symbol plus STRUCTURED
crossings (no regex): job --publishes--> notification, handler --handles--> notification,
module --consumes/exposes--> contract. construct() over them yields an execution/data-flow trace
(job -> the event it publishes -> the module that handles it) in dependency order.
"""
import json, os


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def archmap(path):
    """-> (chunks, edges). chunks: {doc,pos,label,kind,text,symbol}. edges: (over_sym, under_sym, kind, label)."""
    m = load(path)
    doc = os.path.abspath(path)
    chunks, edges, seen = [], [], {}

    def sym(name, category, text):
        if name in seen:
            return
        seen[name] = len(chunks)
        chunks.append({"doc": doc, "pos": len(chunks), "kind": "code", "symbol": name,
                       "label": f"{os.path.basename(path)} › {category} › {name}",
                       "text": f"{category}: {name}\n{text}"})

    for mod in m.get("modules", []):
        sym(mod, "module", f"module {mod}")
    for n in (m.get("notifications") or {}).get("notifications", []):
        name = n.get("name")
        if not name:
            continue
        sym(name, "notification", f"defined in {n.get('definedIn')}; publishers {n.get('publishers')}; handlers {n.get('handlers')}")
        for p in n.get("publishers") or []:
            sym(p, "module", f"module {p}"); edges.append((p, name, "publishes", f"{p} publishes {name}"))
        for h in n.get("handlers") or []:
            sym(h, "module", f"module {h}"); edges.append((h, name, "handles", f"{h} handles {name}"))
    jobs = m.get("jobs") or []
    # real archmap: {module: [ {name, publishedNotifications}, ... ]}; also accept a flat list
    job_items = [(mod, j) for mod, lst in jobs.items() for j in (lst or [])] if isinstance(jobs, dict) \
        else [(None, j) for j in jobs]
    for mod, j in job_items:
        if isinstance(j, str):
            j = {"name": j}
        name = j.get("name")
        if not name:
            continue
        sym(name, "job", f"in module {mod}; publishes {j.get('publishedNotifications')}")
        if mod:
            sym(mod, "module", f"module {mod}"); edges.append((mod, name, "owns", f"{mod} owns job {name}"))
        for pn in j.get("publishedNotifications") or []:
            sym(pn, "notification", f"notification {pn}"); edges.append((name, pn, "publishes", f"{name} publishes {pn}"))
    for mod, c in (m.get("contracts") or {}).items():
        sym(mod, "module", f"module {mod}")
        for k in c.get("consumes") or []:
            sym(k, "contract", f"contract {k}"); edges.append((mod, k, "consumes", f"{mod} consumes {k}"))
        for k in c.get("exposes") or []:
            sym(k, "contract", f"contract {k}"); edges.append((mod, k, "exposes", f"{mod} exposes {k}"))
    return chunks, edges


def add_edges(kn, chunks, edges, base_idx=0):
    """Append structured crossings to a knot (symbols -> global chunk idx)."""
    idx = {c["symbol"]: base_idx + k for k, c in enumerate(chunks) if "symbol" in c}
    nid = len(kn["crossings"])
    seen = {(x["over"], x["under"], x["kind"]) for x in kn["crossings"]}
    for o, u, kind, label in edges:
        if o in idx and u in idx and idx[o] != idx[u] and (idx[o], idx[u], kind) not in seen:
            nid += 1; seen.add((idx[o], idx[u], kind))
            kn["crossings"].append({"id": nid, "over": idx[o], "under": idx[u], "kind": kind, "label": label})
    return kn


def demo():
    import tempfile
    m = {"modules": ["Approvals", "Notifications"],
         "notifications": {"notifications": [{"name": "ApprovalChainSent", "definedIn": "Approvals",
                                              "publishers": ["FreezeApprovalDocumentSetJob"], "handlers": ["Notifications"]}]},
         "jobs": {"Approvals": [{"name": "FreezeApprovalDocumentSetJob", "publishedNotifications": ["ApprovalChainSent"]}]},
         "contracts": {"Approvals": {"consumes": ["IApprovalDocumentProvider"], "exposes": []}}}
    p = os.path.join(tempfile.gettempdir(), "am.json"); json.dump(m, open(p, "w"))
    chunks, edges = archmap(p)
    kn = {"docs": {chunks[0]["doc"]: list(range(len(chunks)))}, "toc": {}, "crossings": [], "dangling": []}
    add_edges(kn, chunks, edges)
    kinds = {x["kind"] for x in kn["crossings"]}
    assert {"publishes", "handles", "consumes", "owns"} <= kinds, kinds
    from . import knot as K
    job = next(i for i, c in enumerate(chunks) if c["symbol"] == "FreezeApprovalDocumentSetJob")
    plan = K.construct(job, kn, chunks)
    vias = [c["via"].split(" ")[0] for c in plan]
    assert "references" in vias, plan          # job -> the notification it publishes
    print("ok  code demo: %d symbols, %d typed crossings; job trace steps: %s" % (len(chunks), len(kn["crossings"]), [c["label"].split(" › ")[-1] for c in plan[:3]]))


if __name__ == "__main__":
    demo()
