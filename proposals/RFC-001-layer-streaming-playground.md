# RFC 001: Layer Streaming Playground

- **Proposer**: @Castle (co-authored with @Rook in review)
- **Reviewer**: @Rook
- **Status**: Draft
- **Created**: 2026-11-23

---

## 1. Vision & Problem Statement
Layer-wise streaming (AirLLM-style) lets a tiny GPU run a huge model by shuttling one transformer layer at a time from system RAM over PCIe. It works — we are running a 30.5B MoE against a 5GB GPU right now — but the tradeoff is invisible. You can't *feel* why a 3.3B-active MoE streams gracefully while a dense 70B crawls.

We propose an interactive, public browser playground that makes the math tangible: pick a model, GPU VRAM, system RAM, PCIe generation, and quantization; watch layers stream in an animated pipeline; see predicted TTFT and decode tok/s. Then we calibrate the simulator against our own measured benchmark numbers, published as aggregate metrics.

## 2. Proposed Deliverables
- `playground/index.html` — interactive page: canvas animation of layer streaming + sliders (model, VRAM, PCIe gen, bits, context length)
- `playground/models.js` — public model spec sheet (sizes/layers/active params from public HF model cards)
- `playground/notes.md` — short writeup: streaming latency model, and sim-vs-measured comparison using our aggregate eval metrics (TTFT, tok/s, peak VRAM)
- Update to the landing page linking the playground

## 3. Division of Labor
- **Cas's Role**: scaffolding, canvas/UI, sliders + animation, Pages deployment, fast iteration and testing
- **Rook's Role**: streaming-latency math (PCIe bandwidth, quant sizing, KV cache), calibration of predictions against measured benchmarks, verification and reasoning review

## 4. Public Safety Check
- [x] No internal RFC1918 IPs (`192.168.*`, `10.99.*`, etc.)
- [x] No private API tokens or credentials
- [x] No proprietary private vault files, internal agent logs, or config files

## 5. Review & Agreement
- **Reviewer Comments**: (Rook — add streaming-latency math details and any corrections here)
- **Decision**: Pending review
"}