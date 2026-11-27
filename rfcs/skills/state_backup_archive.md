---
name: state_backup_archive
description: Create workspace state archive and upload to Discord
trigger: Need to backup workspace state and deliver via Discord
produces: Tar.gz archive uploaded to Discord channel
---

## Procedure

### Inputs
workspace_path (str), output_channel (str)

### Execution Pattern
1. exec(scripts/state-backup.sh) 2. message(upload-file, channel, archive)

### Verification Gate
**Condition:** Archive created; upload succeeds; file size reasonable

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-10-27.txt, 2026-10-28.txt
- **Observed Frequency:** 3
- **Confidence:** 0.75
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
