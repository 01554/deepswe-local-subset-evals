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

| column | agent | environment | resolved | avg f2p | avg min/task |
|---|---|---|---:|---:|---:|
| [Qwen3.8-27B NVFP4 (Qwen Code)](models/qwen38-27b-nvfp4-qwencode.md) | Qwen Code CLI | rtx6000-96gb | 40/113 | 0.836 | 43.8 |

## rtx6000-96gb

| language (tasks) | [Qwen3.8-27B NVFP4 (Qwen Code)](models/qwen38-27b-nvfp4-qwencode.md) |
|---|---|
| go (34) | 19/34 |
| javascript (5) | 0/5 |
| python (34) | 9/34 |
| rust (5) | 2/5 |
| typescript (35) | 10/35 |
| **resolved** | **40/113** |

<!-- RESULTS:END -->

- Environment & serving conditions: [`environments.md`](environments.md)
- Per-model/harness commentary: [`models/`](models/)
- Raw per-task data (f2p fractions, minutes, errors): [`campaigns/`](campaigns/)
- Harness plumbing (Pier custom agents, proxy shim): see
  [swelancer-local-subset-evals/deepswe-pilot](https://github.com/01554/swelancer-local-subset-evals/tree/main/deepswe-pilot)

Column naming: `<model>_<quant>_<agent>_<condition labels>`. Conditions that
deviate from the benchmark's defaults are always part of the label.
