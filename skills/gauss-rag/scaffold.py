#!/usr/bin/env python3
"""Create the Gauss/ working folder in the current directory.
    python3 scaffold.py [target_dir]     # default: ./Gauss
Drop documents into Gauss/docs/, then run: python3 Gauss/app.py
"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "Gauss")
for d in ("docs", "store"):
    os.makedirs(os.path.join(target, d), exist_ok=True)
# the engine travels with the folder so app.py is self-contained
shutil.copytree(os.path.join(HERE, "gaussrag"), os.path.join(target, "gaussrag"), dirs_exist_ok=True)
shutil.copy(os.path.join(HERE, "templates", "app.py"), os.path.join(target, "app.py"))
cfg = os.path.join(target, "gauss.toml")
if not os.path.exists(cfg):
    open(cfg, "w").write('''# Gauss RAG — low budget by default. Everything below is optional.
[embed]
enabled = false                 # true -> semantic vectors (one call per chunk); off = BM25 only, zero API calls
base_url = ""                   # any OpenAI-compatible server exposing /v1/embeddings (vLLM, litellm, OpenAI, Ollama)
model = "bge-m3"
api_key = ""

[ocr]
enabled = false                 # true -> OCR scanned PDFs with a vision model (one call per page); off = they are listed as needs_ocr
base_url = ""                   # any OpenAI-compatible server exposing /v1/chat/completions with image input
model = "qwen2.5-vl"
api_key = ""

[chunk]
min_chars = 500                 # pack runt sections up to this size
''')
open(os.path.join(target, "docs", "README.txt"), "w").write("Drop .md / .txt / .pdf / code files here, then run:  python3 ../app.py\n")
print("Gauss/ ready at", target)
print("  docs/      <- drop documents here")
print("  app.py     <- run this for search + visualization")
print("  gauss.toml <- embeddings/OCR are OFF by default (free); flip on when wanted")
