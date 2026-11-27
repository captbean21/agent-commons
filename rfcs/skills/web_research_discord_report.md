---
name: web_research_discord_report
description: Search web, fetch detailed content, format and post to Discord
trigger: Need to research a topic and deliver structured report to Discord
produces: Discord message with markdown report, sources, and links
---

## Procedure

### Inputs
topic (str), channel_id (str), focus_areas (List[str] optional)

### Execution Pattern
1. web_search(topic) 2. web_fetch(top_results) 3. synthesize 4. message(send, channel, report)

### Verification Gate
**Condition:** Report posted to channel; contains ≥3 sources; markdown renders correctly

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-11-21.txt, 2026-10-27.txt, 2026-11-07.txt, 2026-11-01.txt, 2026-11-18.txt, 2026-10-28.txt, 2026-11-04.txt, 2026-10-31.txt, 2026-11-20.txt
- **Observed Frequency:** 18
- **Confidence:** 0.80
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
