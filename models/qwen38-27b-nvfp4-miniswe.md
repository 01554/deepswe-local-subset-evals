# Qwen3.8-27B — NVFP4, mini-swe-agent (cap21600)

| | |
|---|---|
| checkpoint | [unsloth/Qwen3.8-27B-NVFP4](https://huggingface.co/unsloth/Qwen3.8-27B-NVFP4) (22.6 GB) |
| serving | vLLM, temp 0.6 · top-p 0.95, MTP speculative n=3, prefix caching, ctx 262144 (model native) |
| agent | mini-swe-agent (bash-only, single tool), default 150-step limit |
| cap | task caps ×4 (`--agent-timeout-multiplier 4`); durations recorded per task |
| score | **39/113 resolved (34.5%)** · avg f2p 0.703 · avg 35.0 min/task |
| tokens/task | output 119k · reasoning 77k (measured via tokenizer over trajectory `reasoning_content`) |
| tool calls/task | 144 avg — **52/112 trials (46%) ran into the 150-step limit** (16 of those still resolved) |
| server metrics | prefix-cache hit 97.3% (server, 133 samples) / 97.4% (client, cached÷prompt tokens) · MTP draft acceptance 79.7% |
| errors | 12× NonZeroAgentExitCodeError (harness exit-code noise — 1 of them still resolved; verifier is independent), 1× VerifierTimeout — re-verified manually on the unchanged patch: the coalescing implementation leaks a non-daemon thread, so pytest finishes (44/50 f2p, p2p clean) but never exits; graded fail from the rerun reports |

## Read (English)

Near-parity with Qwen Code on resolved rate, from a radically simpler agent:
mini-swe-agent is a single bash tool in a loop, no file-edit affordances, no
planner. It is also ~20% faster per task (34.5 vs 43.8 min) and its failures
look different — avg f2p 0.701 vs 0.836 means it earns much less partial
credit, but it fully lands the tasks it can do.

The dominant cap is **steps, not time**: 46% of trials hit the default
150-step limit. Nearly half the campaign ended by exhaustion rather than
submission, so a step-limit sweep (150 → 300) is the obvious next experiment —
some unresolved-with-high-f2p tasks likely just needed more turns.

The discordant set vs Qwen Code (tasks exactly one harness solved) is large —
low-20s of 113 — confirming harness choice is a first-order variable at this
model scale, and giving deepswe12 a rich both-failed pool.

## 寸評(日本語)

bash 1本しか持たない最小構成エージェントが、Qwen Code CLI とほぼ互角の
resolved 率を出した(しかもタスクあたり2割速い)。部分点(avg f2p)は 0.701 と
明確に低いのに解決数で並ぶ — 「解ける問題は解き切り、解けない問題は部分点も
稼がない」という、qwen-code(f2p 0.836 で 43/44 落ち多発)と正反対の性格。

律速は時間ではなく**ステップ上限**: 46% のトライアルがデフォルト 150 ステップを
使い切って終了(それでも 16 問は resolved)。時間キャップより先にステップ
キャップに当たる構造なので、150→300 に上げた再走が次の実験候補。

ハーネス間の食い違い(片方だけ解けた問題)は 113 問中 20 問超。この規模の
モデルではハーネス選択が一次変数であることの再確認であり、deepswe12 の
「両方失敗」プール選定にとっては好材料。
