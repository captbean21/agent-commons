---
name: meta_skill_writer_pipeline
description: Run meta-skill writer: Saturday scan → Sunday propose → Monday promote
trigger: Cron-triggered skill synthesis from workspace patterns
produces: Skill proposals in skills/proposals/, promoted skills via skill_workshop
---

## Procedure

### Inputs
scan_window_days (int, default 14), min_occurrences (int, default 3)

### Execution Pattern
1. scan memory/AGENTS.md/sessions 2. cluster patterns 3. draft proposals 4. post to #rook 5. promote approved via skill_workshop

### Verification Gate
**Condition:** Proposals created; reactions collected; approved skills appear in workshop

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-10-27.txt, 2026-10-28.txt
- **Observed Frequency:** 3
- **Confidence:** 0.70
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
