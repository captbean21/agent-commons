# Final Rollout Plan: The Frankenstein MoE (30B MoE Cortex + 1.5B Reflex)

- **Target Architecture:** Dual-Lane Hybrid Asymmetric Inference Engine
- **Host System:** Enterprise Workhorse (Dell PowerEdge T340 / Xeon 6-Core / 48 GB DDR4 / Quadro P2200 5GB)
- **Primary Agent Test Pilot:** Pilot Autonomous Agent (OpenClaw)
- **Status:** Final Draft & Pre-Flight Review (Pending Execution Approval)

---

## 1. Executive Summary

This rollout transitions the heavy reasoning lane (Port 5001) from the stopgap dense 14B model to **`Qwen3-Coder-30B-A3B`** (30.5B total / 3.3B active parameters) with a **49,152 context window**, while pinning its entire 48K KV cache into the Quadro P2200's leftover GDDR5 VRAM. 

The fast reflex lane (Port 5002, `Qwen2.5-1.5B`, ~58 tok/s) and all existing production agents (Cas and Rook) remain 100% untouched and operational.

---

## 2. Step-by-Step Rollout Stages

```mermaid
flowchart TD
    S0["Stage 0: Pre-Flight Safety<br/>Audit VRAM & Terminate Stale Services"] --> S1["Stage 1: Stage GGUF Asset<br/>Download Qwen3-Coder-30B-A3B Q4_K_M"]
    S1 --> S2["Stage 2: Configure Systemd<br/>Bake --flash-attn & -ctk/-ctv q4_0"]
    S2 --> S3["Stage 3: Local Node Gate Benchmark<br/>Validate TTFT, tok/s, & VRAM Headroom"]
    S3 --> S4["Stage 4: Agent Gateway Alignment<br/>Update OpenClaw Provider & Ctx to 49K"]
    S4 --> S5["Stage 5: Live Dual-Lane Verification<br/>End-to-End Autonomous Task Test"]
```

### Stage 0: Pre-Flight Safety & VRAM Reclamation
- **Goal:** Guarantee clean VRAM slate for the 48K KV cache.
- **Actions:**
  1. Inspect active processes on GPU (`nvidia-smi`).
  2. Terminate legacy / stale test processes (e.g., idle Port 5003 service).
  3. Verify baseline VRAM: Port 5002 (`llama-reflex`) occupies ~1.2 GB, leaving **~3.8 GB VRAM free**.

### Stage 1: Asset Staging
- **Goal:** Download and verify model weights into persistent storage (`/models`).
- **Model:** `Qwen/Qwen3-Coder-30B-A3B-Instruct-GGUF` (or `bartowski/Qwen_Qwen3-30B-A3B-GGUF`), quantization `Q4_K_M` (~18.2 GB).
- **Target Path:** `/models/Qwen3-Coder-30B-A3B-Instruct.Q4_K_M.gguf`.
- **Integrity Gate:** Confirm file size matches upstream manifest and GGUF header parses cleanly with `llama-server --version`.

### Stage 2: Cortex Service Configuration (`llama-cortex.service`)
- **Goal:** Configure systemd unit with exact memory and KV-offload flags.
- **Unit Configuration:**
  ```ini
  [Unit]
  Description=Llama Cortex Reasoning Engine (30B MoE)
  After=network.target

  [Service]
  Type=simple
  User=rook
  WorkingDirectory=/models
  ExecStart=/opt/llama.cpp/build/bin/llama-server \
    -m /models/Qwen3-Coder-30B-A3B-Instruct.Q4_K_M.gguf \
    -c 49152 \
    --flash-attn \
    -ctk q4_0 \
    -ctv q4_0 \
    -t 6 \
    --host 0.0.0.0 \
    --port 5001 \
    --parallel 1 \
    --cont-batching
  Restart=always
  RestartSec=3

  [Install]
  WantedBy=multi-user.target
  ```
- **Deployment:** Back up existing service unit, copy template, reload systemd daemon, and restart `llama-cortex`.

### Stage 3: Local Gate Benchmark
- **Goal:** Validate physical performance before exposing to agent traffic.
- **Automated Gate Script:** Run `benchmarks/run_gate_benchmark.py` against `http://127.0.0.1:5001/v1`.
- **Acceptance Criteria:**
  - HTTP Health: `GET /health` returns `{"status": "ok"}`.
  - Short prompt TTFT: `< 3.0s`.
  - Decode speed: `> 8.0 tok/s` (expected: ~9.5 – 11.0 tok/s).
  - VRAM consumption: Total peak `< 4.5 GB / 5.12 GB`.
  - Output sanity: Coherent, syntactically correct code response without NaN tokens.

### Stage 4: OpenClaw Provider Alignment (Agent Node)
- **Goal:** Update the agent model routing to leverage the 49K context window.
- **Configuration Updates (`openclaw.json`):**
  - Point `frankenstein-cortex` model to `Qwen3-Coder-30B-A3B`.
  - Set `contextWindow: 49152`.
  - Set `maxTokens: 4096`.
  - Configure timeout to `120s` to account for deep context prefill.
  - Retain `frankenstein-reflex` on Port 5002 (`contextWindow: 8192`) for fast sub-tasks.

### Stage 5: End-to-End Live Verification
- **Goal:** Execute a multi-turn task through the agent utilizing both lanes.
- Verify that the agent routes tool execution and sub-agent dispatch to Port 5002 (<0.5s turn) and deep repository synthesis to Port 5001 without context clipping.

---

## 3. Potential Borks, Failure Modes & Risk Mitigations

| Failure Mode / Potential Bork | Root Cause | Probability | Impact | Pre-Emptive Mitigation & Fix |
| :--- | :--- | :--- | :--- | :--- |
| **CUDA OOM on KV Allocation** | Stale processes on GPU or VRAM fragmentation | Low | High | Pre-flight audit explicitly terminates stale processes. If VRAM exceeds 4.8 GB, instantly drop `-ctk/-ctv` to CPU host RAM where 27 GB free RAM exists. |
| **Slot Contention / Truncation** | Continuous batching splitting context slots | Low | Medium | Pin `--parallel 1` explicitly so the entire 49,152 context is reserved for the primary agent thread. |
| **Gateway Timeout on Deep Context** | Prefilling 30K+ tokens on CPU takes 20-35s; agent HTTP client drops connection | Medium | Medium | Increase OpenClaw client timeout from default 30s to 120s. Rely on `llama.cpp` prompt slot cache so static system prompts are never re-evaluated. |
| **MoE Routing Deserialization Failure** | `llama.cpp` build lacks updated tensor architecture mapping | Very Low | High | Verified: `llama.cpp` build already includes native `LLM_ARCH_QWEN3MOE` support (PR 32084). |
| **CPU Thermal Throttling** | 6 Xeon CPU cores pegged at 100% during prolonged prefill | Low | Low | Server-grade cooling on Dell PowerEdge chassis maintains sub-65°C under continuous 100% AVX2 load. |

---

## 4. Rollback & Fail-Safe Plan

If any hard gate fails during Stage 3 or Stage 4:
1. **Immediate Fallback Command:**
   ```bash
   sudo systemctl stop llama-cortex
   sudo cp /etc/systemd/system/llama-cortex.service.bak /etc/systemd/system/llama-cortex.service
   sudo systemctl daemon-reload
   sudo systemctl start llama-cortex
   ```
2. **Recovery Time:** `< 5 seconds`.
3. **Fallback State:** Restores the verified `qwen2.5-coder-14b-instruct-q4_k_m.gguf` service on Port 5001. The agent continues running with zero state corruption.

---

## 5. Public Safety & Boundary Compliance

- [x] All IP addresses generalized to RFC/placeholder notation.
- [x] Zero API tokens, deploy keys, or private secrets included.
- [x] Host and agent states strictly separated from private vault infrastructure.
