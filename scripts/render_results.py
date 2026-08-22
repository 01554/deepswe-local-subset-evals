#!/usr/bin/env python3
"""Render results/*.csv into the README.md results section.

Same convention as swelancer-local-subset-evals: replaces the section between
the RESULTS:BEGIN / RESULTS:END markers; per-run conditions go between the
RUNCONDITIONS markers in environments.md.
Cell vocabulary: pass / fail / timeout / running / not_run (or empty).
Run from the repo root: python3 scripts/render_results.py
"""
import csv
import glob
import os

SYM = {"pass": "✅", "fail": "❌", "timeout": "⏱️", "running": "🔄", "not_run": "—", "": "·"}
BEGIN, END = "<!-- RESULTS:BEGIN -->", "<!-- RESULTS:END -->"

meta = {}
if os.path.exists("results/columns.csv"):
    for r in csv.DictReader(open("results/columns.csv")):
        meta[r["column"]] = r


def disp(col):
    m = meta.get(col, {})
    target = m.get("page") or m.get("url")
    if m.get("display") and target:
        return f"[{m['display']}]({target})"
    return col


out = [
    "_Auto-generated from [`results/*.csv`](results/) by `scripts/render_results.py` — edit those, not this section._",
    "",
    "✅ resolved (all fail2pass + pass2pass tests green) ❌ unresolved ⏱️ cap timeout 🔄 running — not run",
    "",
    "_Per-task cells live in [`results/*.csv`](results/); f2p fractions and durations in [`campaigns/`](campaigns/); tables below aggregate by language._",
    "",
]

summary = []
for path in sorted(glob.glob("results/*.csv")):
    env = os.path.basename(path)[:-4]
    if env == "columns":
        continue
    rows = list(csv.reader(open(path)))
    header, data = rows[0], rows[1:]
    cols = header[2:]
    langs = sorted({r[1] for r in data})
    out.append(f"## {env}")
    out.append("")
    out.append("| language (tasks) | " + " | ".join(disp(c) for c in cols) + " |")
    out.append("|---|" + "---|" * len(cols))
    for lang in langs:
        lrows = [r for r in data if r[1] == lang]
        cells = []
        for i in range(len(cols)):
            p = sum(1 for r in lrows if r[2 + i] == "pass")
            n = sum(1 for r in lrows if r[2 + i] in ("pass", "fail", "timeout"))
            cells.append(f"{p}/{n}" if n else "—")
        out.append(f"| {lang} ({len(lrows)}) | " + " | ".join(cells) + " |")
    totals = []
    for i in range(len(cols)):
        p = sum(1 for r in data if r[2 + i] == "pass")
        n = sum(1 for r in data if r[2 + i] in ("pass", "fail", "timeout"))
        totals.append(f"**{p}/{n}**")
        summary.append((env, cols[i], p, n))
    out.append("| **resolved** | " + " | ".join(totals) + " |")
    out.append("")

lb = ["### Leaderboard", "", "| column | agent | environment | resolved | avg f2p | avg min/task |",
      "|---|---|---|---:|---:|---:|"]
for env, col, p, n in sorted(summary, key=lambda s: -s[2]):
    m = meta.get(col, {})
    g = lambda k: m.get(k) or "?"
    lb.append(f"| {disp(col)} | {g('agent')} | {env} | {p}/{n} | {g('avg_f2p')} | {g('avg_min_all113')} |")
lb.append("")
out[6:6] = lb

section = "\n".join([BEGIN, "## Results", ""] + out + [END])
readme = open("README.md").read()
assert BEGIN in readme and END in readme, "markers not found in README.md"
head, rest = readme.split(BEGIN, 1)
_, tail = rest.split(END, 1)
open("README.md", "w").write(head + section + tail)
print(f"README.md results section updated ({len(summary)} columns)")

# per-run conditions -> environments.md
EB, EE = "<!-- RUNCONDITIONS:BEGIN -->", "<!-- RUNCONDITIONS:END -->"
lines = ["| column | agent | ctx | sampling | avg min/task |", "|---|---|---|---|---:|"]
for env, col, p, n in summary:
    m = meta.get(col, {})
    g = lambda k: m.get(k) or "?"
    lines.append(f"| {col} | {g('agent')} | {g('ctx')} | {g('sampling')} | {g('avg_min_all113')} |")
if os.path.exists("environments.md"):
    envmd = open("environments.md").read()
    if EB in envmd and EE in envmd:
        head, rest = envmd.split(EB, 1)
        _, tail = rest.split(EE, 1)
        open("environments.md", "w").write(head + "\n".join([EB] + lines + [EE]) + tail)
        print("environments.md updated")
