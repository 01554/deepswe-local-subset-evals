# Qwen3.8-27B — NVFP4, Qwen Code CLI (cap21600)

| | |
|---|---|
| checkpoint | [unsloth/Qwen3.8-27B-NVFP4](https://huggingface.co/unsloth/Qwen3.8-27B-NVFP4) (22.6 GB) |
| serving | vLLM, temp 0.6 · top-p 0.95, MTP speculative n=3, prefix caching, stock chat template (thinking at model default) |
| agent | Qwen Code CLI (`@qwen-code/qwen-code`), Pier custom agent + proxy shim, `--prompt=` form |
| cap | task caps ×4 (`--agent-timeout-multiplier 4` → 6 h ceiling); durations recorded per task |
| score | **40/113 resolved (35.4%)** · avg f2p 0.836 · avg p2p ~0.998 · avg 43.8 min/task |

## Read (English)

**35.4% resolved on a single consumer-class GPU**, against the official model
card's 42.2 (Claude Code harness, 4×B300 TP4, 256K ctx). The gap bundles
quantization-vs-serving differences, harness, temperature, and context limits —
this repo exists to unbundle exactly that.

The shape of the failures is informative: average f2p across all 113 tasks is
0.836 with p2p ≈ 1.0 — the agent almost never breaks existing behavior and
usually passes *most* of the new tests, but DeepSWE's all-or-nothing verifier
pays nothing for 43/44. The unresolved tail is dominated by big multi-file
feature builds (the benchmark's stated design: prompts half the size of
SWE-bench Pro, solutions 5.5× larger).

## 寸評(日本語)

**コンシューマ級 GPU 1枚で 35.4%**(公式カードは 42.2 — Claude Code ハーネス+4×B300)。差分には量子化・ハーネス・温度・ctx が絡み合っており、それを解きほぐすのがこのリポジトリの仕事。

失敗の形が特徴的で、全113問平均の f2p は 0.836、p2p はほぼ 1.0 — 「既存を壊さず、新規テストの大半は通すが、全通しに届かない」パターンが大量にある。43/44 でも0点という DeepSWE の all-or-nothing 採点が、SWE-Lancer との最大の性格差。未解決の尾は大型マルチファイル実装(プロンプトは短く、解は SWE-bench Pro の5.5倍というベンチ設計どおりの重さ)に集中している。
