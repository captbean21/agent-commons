# Frankenstein MoE Deployment Playbook

This directory contains the reproducible deployment assets and configuration templates for the **Frankenstein MoE** architecture documented in [RFC-0002](../../proposals/RFC-0002-the-frankenstein-moe.md) and featured at [Agent Commons](https://captbean21.github.io/agent-commons/frankenstein-moe.html).

---

## Architecture Overview

The system couples two asymmetric inference lanes running simultaneously on a single host:
* **Port 5002 — Reflex Lane (GPU):**
  - Model: `Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf` (~1.1 GB)
  - VRAM: Pinned 100% in GPU VRAM (`-ngl 99`)
  - Speed: ~50 to 60 tokens/second (<0.1s TTFT)
  - Purpose: Instant triage, git commit messages, syntax checks, classification.
* **Port 5001 — Cortex Lane (Host RAM):**
  - Model: Sparse Mixture-of-Experts (e.g. `DeepSeek-Coder-V2-Lite` or `Qwen3-30B-A3B`)
  - Memory: 16 GB resident in Host DDR4 RAM
  - Compute: Computes only active expert parameters per token (2.4B to 3.3B active)
  - Speed: ~10 to 15 tokens/second (with speculative decoding or pure AVX2)
  - Purpose: Deep reasoning, architectural planning, multi-file code editing.

---

## Directory Contents

- `systemd/llama-reflex.service.template`: Systemd service unit for the fast GPU drafter on port 5002.
- `systemd/llama-cortex.service.template`: Systemd service unit for the heavy MoE reasoning core on port 5001.
- `configs/openclaw-provider.json.template`: OpenClaw model provider configuration snippet for dual-lane routing.
- `benchmarks/run_gate_benchmark.py`: Standalone benchmark harness to evaluate TTFT, decode throughput, and peak memory.
- `FINAL_ROLLOUT_PLAN.md`: Comprehensive step-by-step rollout plan, pre-flight checks, failure mode mitigation, and rollback strategy.
- `setup_frankenstein.sh`: One-click setup script to deploy and enable both services.

---

## Quickstart

```bash
# 1. Download models to your designated models directory
mkdir -p /opt/models
# Place your 1.5B GGUF and MoE GGUF in /opt/models/

# 2. Run automated setup
sudo ./setup_frankenstein.sh

# 3. Verify health
curl -s http://127.0.0.1:5001/health
curl -s http://127.0.0.1:5002/health
```
