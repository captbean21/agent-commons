---
name: hybrid_youtube_summarizer
description: Fetch YouTube transcript, summarize via local LLM, deliver report
trigger: Need to summarize a YouTube video without downloading
produces: Markdown summary with timestamps, key points, source link
---

## Procedure

### Inputs
video_url (str), focus (str optional), summarize (bool)

### Execution Pattern
1. tools/yt_transcript.py --summarize 2. parse output 3. message(send, channel, summary)

### Verification Gate
**Condition:** Summary generated; contains key points; posted to channel

**Test:** Run the skill on a held-out task matching the trigger pattern. Verify the output spec is met and verification condition passes.

## Metadata

- **Source Sessions:** 2026-10-27.txt, 2026-10-28.txt
- **Observed Frequency:** 3
- **Confidence:** 0.70
- **Extracted:** Auto-distilled from session traces via Trace2Skill-inspired parser
