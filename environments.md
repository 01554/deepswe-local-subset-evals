# Environments

| environment | hardware | serving | typical decode |
|---|---|---|---|
| rtx6000-96gb | RTX PRO 6000 Blackwell 96 GB, DDR4 host, Ubuntu 26.04 | vLLM (Docker), NVFP4 checkpoint, MTP speculative n=3, prefix caching on | 60–85 tok/s per stream; 150–300 tok/s aggregate at 3 concurrent trials |

Server-side counters are sampled every 10 min during campaigns
(prefix-cache hit rate, aggregate throughput, MTP draft acceptance);
observed during the qwen-code campaign: cache 96–97%, draft acceptance 77–91%.

Agent sandboxes egress through Pier's squid proxy (allowlist: ports 80/443,
`dstdomain` only), so the LLM endpoint is exposed on **port 80** under
`<bridge-ip>.sslip.io`; node-based CLIs whose proxy client is broken go
through a localhost forwarder shim instead (see the pilot notes).

## Per-run conditions

<!-- RUNCONDITIONS:BEGIN -->
| column | agent | ctx | sampling | avg min/task |
|---|---|---|---|---:|
| qwen38_27b_nvfp4_qwencode_cap21600 | Qwen Code CLI | 131072 | temp 0.6 / top-p 0.95 + MTP + prefix cache | 43.8 |
<!-- RUNCONDITIONS:END -->
