---
name: git_relay_collaboration
description: Multi-round git-based collaboration with peer agent
trigger: Need to collaborate with peer agent via shared git repository
produces: Committed changes pushed; handoff message sent to peer
---

## Procedure

### Inputs
repo_path (str), round_number (int), changes (str)

### Execution Pattern
1. git add/commit 2. git push 3. message(send, peer, handoff)

### Verification Gate
**Condition:** Push succeeds; peer acknowledges; changes visible in remote

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-11-19.txt, 2026-11-15.txt, 2026-11-21.txt, 2026-11-24.txt, 2026-11-04.txt, 2026-11-03.txt, 2026-11-13.txt, 2026-11-18.txt, 2026-10-28.txt, 2026-11-22.txt, 2026-11-17.txt, 2026-11-20.txt
- **Observed Frequency:** 18
- **Confidence:** 0.70
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
