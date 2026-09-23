#!/usr/bin/env python3
"""Ingest: parse documents with the cheapest tier that works, chunk header-to-header, pack runts.

Tiers (all local, no model):
  .md/.txt/.rst/code  -> read directly
  .pdf with text layer -> pdftotext (poppler)
  .pdf scanned          -> flagged needs_ocr (VL-OCR is opt-in, never automatic)

Chunking is lifted from vizlab/index.py (proven): split on ## .. #### so each section is a chunk,
label = TOC path, H1 prepended as context, `doc`/`pos` stamped for the knot's ring, runt sections
packed up to `min_chars`. Incremental by content hash.
"""
import hashlib
import os
import re
import subprocess

MAX_CHARS = 1800          # a section longer than this splits on paragraph boundaries
TEXT_EXT = {".md", ".markdown", ".txt", ".rst", ".py", ".js", ".ts", ".tsx", ".cs", ".java",
            ".go", ".rs", ".c", ".h", ".cpp", ".rb", ".sh", ".toml", ".yaml", ".yml", ".json"}
CODE_EXT = TEXT_EXT - {".md", ".markdown", ".txt", ".rst"}


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


# ── parsing tiers ─────────────────────────────────────────────────────────────

def pdf_text(path):
    """pdftotext output, or '' when the PDF has no text layer."""
    try:
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True,
                             timeout=300).stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    return out if len(out.strip()) > 200 else ""


HEAD_NUM = re.compile(r"^\s*((?:Article|ARTICLE|Section|SECTION|Chapter|CHAPTER)\s+[\dIVXLC]+|\d+(?:\.\d+)*)[.:)]?\s+(\S.*)$")


def text_to_markdown(text, title):
    """Turn flat PDF text into markdown with heading guesses from numbering (contract/book style)."""
    out = [f"# {title}", ""]
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            out.append("")
            continue
        m = HEAD_NUM.match(s)
        if m and len(s) < 160:
            num = m.group(1)
            depth = num.count(".") + 2 if num[0].isdigit() else 2
            out.append(("#" * min(depth, 4)) + " " + s)
        else:
            out.append(s)
    return "\n".join(out)


def parse(path):
    """-> (markdown_text, needs_ocr). Cheapest tier first."""
    ext = os.path.splitext(path)[1].lower()
    title = os.path.splitext(os.path.basename(path))[0]
    if ext == ".pdf":
        t = pdf_text(path)
        if not t:
            return "", True
        return text_to_markdown(t, title), False
    if ext in TEXT_EXT or ext == "":
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                t = f.read()
        except OSError:
            return "", False
        if ext in CODE_EXT:
            return f"# {title}\n\n```\n{t}\n```", False
        if not re.search(r"^#\s", t, re.M):
            t = f"# {title}\n\n{t}"
        return t, False
    return "", False


# ── chunking (lifted from vizlab/index.py) ────────────────────────────────────

def split_long(text, path, label, kind):
    if len(text) <= MAX_CHARS:
        yield {"path": path, "label": label, "kind": kind, "text": text}
        return
    buf, size = [], 0
    for para in text.split("\n\n"):
        if size + len(para) > MAX_CHARS and buf:
            yield {"path": path, "label": label, "kind": kind, "text": "\n\n".join(buf)}
            buf, size = [], 0
        buf.append(para)
        size += len(para) + 2
    if buf:
        yield {"path": path, "label": label, "kind": kind, "text": "\n\n".join(buf)}


def chunk_markdown(text, path, kind, min_chars=0):
    """Header-to-header chunks with TOC-path labels, ring positions, and runt packing."""
    m = re.search(r"^#\s+(.+)$", text, re.M)
    title = m.group(1).strip() if m else os.path.basename(path)
    stack, secs = [title], []
    for part in re.split(r"\n(?=#{2,4}\s)", text):
        body = part.strip()
        if len(body) < 40:
            continue
        h = re.match(r"(#{2,4})\s*(.+)", body)
        if h:
            stack = stack[:len(h.group(1)) - 1] + [h.group(2).strip()]
        secs.extend(split_long(f"{title}\n\n{body}", path, " › ".join(stack), kind))
    out, buf, pos = [], None, 0
    for c in secs:
        if min_chars and buf is not None and len(buf["text"]) < min_chars:
            buf["text"] += "\n\n" + c["text"]
            continue
        if buf is not None:
            buf["doc"], buf["pos"] = path, pos
            pos += 1
            out.append(buf)
        buf = c
    if buf is not None:
        buf["doc"], buf["pos"] = path, pos
        out.append(buf)
    return out


def ingest_dir(root, min_chars=500, want_ocr=False):
    """Walk a docs folder -> (chunks, needs_ocr_paths). Kind is 'code' for source, else 'doc'."""
    chunks, needs_ocr = [], []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if fn == "architecture-map.json":
                continue                      # handled by code.py as typed edges, not prose
            p = os.path.join(dirpath, fn)
            text, ocr = parse(p)
            if ocr:
                needs_ocr.append(p)
                continue
            if not text:
                continue
            kind = "code" if os.path.splitext(fn)[1].lower() in CODE_EXT else "doc"
            chunks.extend(chunk_markdown(text, p, kind, min_chars=min_chars))
    return chunks, needs_ocr


def demo():
    md = "# T\n\n## 1. A\nalpha body text that is long enough to keep.\n\n## 2. B\nbeta body text that is long enough to keep, see Section 1.\n"
    c = chunk_markdown(md, "t.md", "doc")
    assert len(c) == 2 and c[0]["pos"] == 0 and c[1]["pos"] == 1 and c[1]["label"] == "T › 2. B", c
    packed = chunk_markdown(md, "t.md", "doc", min_chars=500)
    assert len(packed) == 1, packed          # two runts pack into one
    assert text_to_markdown("1 Intro\nbody\n1.2 Sub\nmore", "X").count("\n#") == 2
    print("ok  ingest demo")


if __name__ == "__main__":
    demo()
