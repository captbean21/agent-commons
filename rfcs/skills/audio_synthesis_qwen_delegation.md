---
name: audio_synthesis_qwen_delegation
description: Generate DSP audio via qwen_coder delegation, compile, test, post WAV
trigger: Need to create instrumental synth audio track
produces: WAV file at output_path, playable and correctly synthesized
---

## Procedure

### Inputs
prompt (str), duration_sec (int), output_path (str)

### Execution Pattern
1. python3 tools/qwen_coder.py --prompt --out 2. gcc -O2 -o binary source.c -lm 3. ./binary 4. message(send, channel, audio.wav)

### Verification Gate
**Condition:** WAV file exists; file header valid; plays without error; posted to Discord

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-10-27.txt, 2026-10-28.txt
- **Observed Frequency:** 3
- **Confidence:** 0.70
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
