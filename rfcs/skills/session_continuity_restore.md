---
name: session_continuity_restore
description: Restore session state from git-backed daemon state files
trigger: Starting new session (/new) need to recover previous session context
produces: Restored task list, decisions, git diffs, memory file name
---

## Procedure

### Inputs
state_dir (str, default: .claude/state)

### Execution Pattern
1. python3 spikes/001-session-continuity-daemon/restore.py 2. parse output 3. resume from continuity block

### Verification Gate
**Condition:** Restore script runs without error; outputs recognizable tasks/decisions from prior session

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-11-21.txt, 2026-10-27.txt, 2026-11-07.txt, 2026-11-01.txt, 2026-11-18.txt, 2026-10-28.txt, 2026-11-04.txt, 2026-10-31.txt, 2026-11-20.txt
- **Observed Frequency:** 18
- **Confidence:** 0.70
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
