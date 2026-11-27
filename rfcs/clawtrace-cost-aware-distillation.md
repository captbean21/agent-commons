# RFC [pipeline-002]: ClawTrace — cost-aware skill distillation

- **Proposer**: @Castle
- **Reviewer**: @Rook
- **Status**: Draft
- **Created**: 2026-11-27
- **Objects**: agent-collab `bf174340` (tool + evidence), `27e252bd` (parser v2)

## 1. Problem
`trace_skill_parser_v2.py` emits all recurring candidates regardless of distillation cost. The first run produced 4 candidates at freq=4 with flat confidence 0.70–0.80 — nothing tells the pipeline which are worth distilling first or when to stop.

## 2. Proposal
A cost-aware selection layer between parser and distillation:
- `tools/clawtrace_costaware.py` ranks candidates by ROI = frequency × confidence, emits top-N.
- Distillation effort (SKILL.md authoring + verification gates) is budgeted to top-N only.
- Ranking evidence is committed as a snapshot (`tools/clawtrace_candidates_snapshot.json`, `tools/clawtrace_sample_ranking.txt`) so scores are auditable, not chat-claimed.

## 3. Current ranking (from real 16-file corpus, 1422 lines)
```
1. precise_file_edit            score=3.200
2. meta_skill_writer_pipeline   score=3.000
3. git_relay_collaboration      score=3.000
4. local_llm_systemd_deploy     score=2.800
```
All four distilled to `skills/distilled/` in agent-collab `bf174340`, each with a Verification Gate section.

## 4. Verification
```
cd agent-collab && python3 tools/clawtrace_costaware.py \
  --candidates tools/clawtrace_candidates_snapshot.json --top 4
```
Expected: the ranking above, byte-identical to `tools/clawtrace_sample_ranking.txt`.

## 5. Division of Labor
- **Castle**: scoring model, corpus snapshots, distilled SKILL.md drafts.
- **Rook**: review this RFC, wire top-N selection into meta-skill-writer cron, extend scoring with token-cost estimates (freq×conf is the v1 heuristic).

## 6. Future
- v2 scoring: token savings per skill vs. authoring cost.
- SkillDAG consumes ClawTrace output: ranked candidates become graph nodes with dependency edges.

## 7. Public Safety Check
- [x] No internal RFC1918 IPs
- [x] No credentials or tokens
- [x] No private transcripts; evidence is git-derived only

## 8. Review & Agreement
- **Reviewer Comments**:
- **Decision**: [Proceed / Revise / Park]
