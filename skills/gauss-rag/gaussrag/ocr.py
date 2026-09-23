#!/usr/bin/env python3
"""Opt-in OCR for scanned PDFs (no text layer) via any OpenAI-compatible vision chat endpoint.
Off by default — a vision call per page is the one expensive step in this tool. Configure in
gauss.toml [ocr]: base_url (e.g. a vLLM / litellm / OpenAI /v1), model, api_key. Needs pdftoppm.
"""
import base64, glob, json, os, re, subprocess, tempfile, urllib.request

PROMPT = ("Transcribe this document page to clean GitHub-flavored Markdown. Use # / ## / ### for heading "
          "levels matching the page's numbering (e.g. '3.2 Title' -> '### 3.2 Title'). Keep running text and "
          "cross-references verbatim (e.g. 'see Section 4.2', 'Chapter 3'). Render math as readable LaTeX or "
          "plain text. For a figure or diagram emit one line '[Figure: brief description]'. Output ONLY the "
          "markdown, no commentary, no page numbers.")


def ocr_image(png, base_url, model, api_key="", timeout=240):
    b64 = base64.b64encode(open(png, "rb").read()).decode()
    body = {"model": model, "max_tokens": 3000, "temperature": 0, "messages": [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
        {"type": "text", "text": PROMPT}]}]}
    h = {"Content-Type": "application/json", "User-Agent": "gaussrag/0.1"}
    if api_key:
        h["Authorization"] = "Bearer " + api_key
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        base_url.rstrip("/") + "/v1/chat/completions", data=json.dumps(body).encode(), headers=h), timeout=timeout))
    md = r["choices"][0]["message"]["content"].strip()
    return re.sub(r"\s*```$", "", re.sub(r"^```(?:markdown)?\s*", "", md))


def ocr_pdf(pdf, base_url, model, api_key="", dpi=150, log=print):
    """Rasterize + OCR every page -> one markdown string with an H1 title. Pages OCR'd in order."""
    title = os.path.splitext(os.path.basename(pdf))[0]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), pdf, os.path.join(tmp, "pg")], check=True)
        pages = sorted(glob.glob(os.path.join(tmp, "pg-*.png")))
        out = [f"# {title}", ""]
        for i, p in enumerate(pages, 1):
            try:
                out.append(ocr_image(p, base_url, model, api_key))
            except Exception as ex:
                out.append(f"[[OCR-ERROR page {i}: {ex}]]")
            if i % 10 == 0 or i == len(pages):
                log(f"  ocr {title}: {i}/{len(pages)}")
    return "\n\n".join(out)
