---
name: daily_digest_pipeline
description: Daily digest via cron: search topics, fetch content, format markdown, post to Discord
trigger: Cron-triggered daily research digest delivery
produces: Discord message with formatted digest, appended to memory log
---

## Procedure

### Inputs
topics (List[str]), channel_id (str), date (str)

### Execution Pattern
1. web_search(each_topic) 2. web_fetch(top_results) 3. format_markdown 4. message(send) 5. append memory log

### Verification Gate
**Condition:** Digest posted to channel; memory log appended; all topics covered

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-11-01.txt, 2026-11-02.txt, 2026-10-29.txt
- **Observed Frequency:** 3
- **Confidence:** 0.75
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
