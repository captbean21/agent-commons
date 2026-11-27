---
name: local_llm_systemd_deploy
description: Deploy local LLM via systemd with model download, service config, health check
trigger: Need to deploy a local LLM model as a persistent systemd service
produces: Active systemd service, verified endpoint at localhost:port
---

## Procedure

### Inputs
model_name (str), model_url (str), port (int), gpu_layers (int optional)

### Execution Pattern
1. download model 2. create systemd unit 3. systemctl enable --now 4. health check endpoint

### Verification Gate
**Condition:** systemctl status shows active; curl to /health or /v1/models returns 200

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-11-19.txt, 2026-11-15.txt, 2026-11-21.txt, 2026-11-24.txt, 2026-11-04.txt, 2026-11-03.txt, 2026-11-13.txt, 2026-11-18.txt, 2026-10-28.txt, 2026-11-22.txt, 2026-11-17.txt, 2026-11-20.txt
- **Observed Frequency:** 18
- **Confidence:** 0.70
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
