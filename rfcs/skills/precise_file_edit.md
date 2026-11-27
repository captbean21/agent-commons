---
name: precise_file_edit
description: Read file, make precise targeted edit, verify change
trigger: Need to make a specific change to an existing file
produces: File with exact change applied
---

## Procedure

### Inputs
file_path (str), old_text (str), new_text (str)

### Execution Pattern
1. read(file_path) 2. edit(file_path, old_text, new_text) 3. verify diff

### Verification Gate
**Condition:** Diff shows only intended change; no unintended modifications

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-10-28.txt, 2026-10-27.txt, 2026-10-29.txt
- **Observed Frequency:** 3
- **Confidence:** 0.75
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
