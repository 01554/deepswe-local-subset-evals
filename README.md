# deepswe-local-subset-evals

Local-hardware evaluations of open models on [DeepSWE 1.1](https://github.com/datacurve-ai/deep-swe)
(113 original long-horizon SWE tasks, program-verified). Sister repo of
[swelancer-local-subset-evals](https://github.com/01554/swelancer-local-subset-evals),
same philosophy: we measure the axes official leaderboards never touch —
quantization, agent harnesses, single-GPU hardware, wall-clock reality.

**Measurement policy**: practical capability, not leaderboard parity. Rollout
caps are runaway guards, not conditions to optimize for — we run DeepSWE's
task caps ×4 (`cap21600` in column labels) and record every task's duration
instead. pass@1, one attempt per task; **resolved = every fail2pass AND
pass2pass test green** (partial credit is recorded in `campaigns/` but a 43/44
is still unresolved).

<!-- RESULTS:BEGIN -->
## Results

_Auto-generated from [`results/*.csv`](results/) by `scripts/render_results.py` — edit those, not this section._

✅ resolved (all fail2pass + pass2pass tests green) ❌ unresolved ⏱️ cap timeout 🔄 running — not run

_Per-task cells live in [`results/*.csv`](results/); f2p fractions and durations in [`campaigns/`](campaigns/); tables below aggregate by language._

### Leaderboard

| column | agent | environment | resolved | avg f2p | avg min/task | tool calls/task | errors | reasoning tok/task | output tok/task | cache hit |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [Qwen3.8-27B NVFP4 (Qwen Code)](models/qwen38-27b-nvfp4-qwencode.md) | Qwen Code CLI | rtx6000-96gb | 40/113 | 0.836 | 43.8 | ? | 5/113 | ? | ? | 96.8% |
| [Qwen3.8-27B NVFP4 (mini-swe)](models/qwen38-27b-nvfp4-miniswe.md) | mini-swe-agent | rtx6000-96gb | 39/113 | 0.703 | 35.0 | 144 | 12/113 | 77k | 119k | 97.4% |

_`errors` = harness/system errors (counted as unresolved). `cache hit` = server-side prefix-cache rate sampled every 10 min across the campaign window. `?` = not captured for that run (the qwen-code arm predates per-request usage logging; ATIF trajectories cover it from the mini-swe arm on)._

## rtx6000-96gb

| language (tasks) | [Qwen3.8-27B NVFP4 (Qwen Code)](models/qwen38-27b-nvfp4-qwencode.md) | [Qwen3.8-27B NVFP4 (mini-swe)](models/qwen38-27b-nvfp4-miniswe.md) |
|---|---|---|
| go (34) | 19/34 | 11/34 |
| javascript (5) | 0/5 | 1/5 |
| python (34) | 9/34 | 18/34 |
| rust (5) | 2/5 | 1/5 |
| typescript (35) | 10/35 | 8/35 |
| **resolved** | **40/113** | **39/113** |

<!-- RESULTS:END -->

## deepswe12 — 5-harness shootout on a fixed 12-task subset

Built from the two full campaigns: 6 tasks **both** harnesses resolved ("OK") and
6 tasks **neither** resolved ("NG"), each 3 shortest + 3 longest by mean minutes
([selection](campaigns/deepswe12_selection.json)). Same model/serving for all
five harnesses (Qwen3.8-27B NVFP4, temp 0.6, MTP, prefix cache, cap ×4), pass@1.

| harness | resolved | OK-group | NG-group | avg min/task | empty patches |
|---|---:|---:|---:|---:|---:|
| qwen-code † | 6/12 | 6/6 | 0/6 | 77.9 | — |
| mini-swe † | 6/12 | 6/6 | 0/6 | 32.9 | — |
| OpenCode | 3/12 | 2/6 | 1/6 | 32.0 | 4 |
| **Claude Code** | **6/12** | 2/6 | **4/6** | 129.9 | 0 |
| pi | 5/12 | 3/6 | 2/6 | **27.3** | 4 |

† reference values from the full-113 campaigns (the subset is defined by these two).

Findings ([per-task CSVs](campaigns/)):

- **Claude Code cracked 4 of the 6 "neither-solved" tasks** (abs-module-cache-flags,
  testem-per-launcher-reports, ts-pattern-match-each, valibot-recursive-schema-composition —
  the last at 359 min, just under the 6 h cap), at ~4× the wall-clock of the fastest
  harnesses. It paradoxically dropped 4 of the 6 "easy" tasks (httpx at f2p 0.992).
- pi is the **fastest** harness (27 min avg) and still took 2 NG tasks; its single-shot
  `-p` loop ends on the first non-tool-call response.
- **Empty patches** (agent never committed → graded 0 regardless of work done):
  OpenCode 4/12, pi 4/12, Claude Code 0/12. The task instructions end with an explicit
  "commit everything" — instruction-following is worth points here.
- Union of all five harnesses: **10/12** — only opa-template-string-reconstruction and
  textual-kitty-key-phases resisted everyone.
- Solve-time gradient (mini-swe 33 min → qwen-code 78 → Claude Code 130) tracks
  NG-group success (0 → 0 → 4): on this model, harder tasks fall when the harness
  lets the model spend longer.

- Environment & serving conditions: [`environments.md`](environments.md)
- Per-model/harness commentary: [`models/`](models/)
- Raw per-task data (f2p fractions, minutes, errors): [`campaigns/`](campaigns/)
- Harness plumbing (Pier custom agents, proxy shim): see
  [swelancer-local-subset-evals/deepswe-pilot](https://github.com/01554/swelancer-local-subset-evals/tree/main/deepswe-pilot)

Column naming: `<model>_<quant>_<agent>_<condition labels>`. Conditions that
deviate from the benchmark's defaults are always part of the label.
