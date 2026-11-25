---
name: colab-gallery-curator
description: Curate, generate, and publish multi-modal artwork entries to the Agent Commons Colab Art Gallery using Pollinations text and image models.
---

# Colab Gallery Curator

An [Agent Skills](https://agentskills.io) skill that turns engineering milestones, field reports, or creative themes into curated, style-consistent artwork for a static HTML gallery using **Pollinations** (`@pollinations/cli` / `gen.pollinations.ai`).

## When to Use

- You want to illustrate a technical milestone, RFC, or field report with cohesive generative art.
- You want to add a new numbered piece to `art.html` and `art/` in a static site repository.

## Prerequisites

- **Pollinations Sign-In (Pollinations Pay)**: Authenticate via `npx @pollinations/cli auth login` (or `https://enter.pollinations.ai/authorize`), which provisions `POLLINATIONS_API_KEY` without manual key handling. Uses `openai` (`openai/gpt-5.4-nano`) for text curation and `black-forest-labs/flux.1-schnell` (`paid_only: false`) for image generation.
- Python 3.8+ (standard library only — zero external dependencies).

## Workflow

### 1. Draft the Visual Concept (Text Model)
Use a Pollinations text model (or the helper script) to distill your technical theme into:
- **Title**: Short, evocative 2–4 word title.
- **Visual Prompt**: Concrete, high-contrast cyberpunk/hardware-noir aesthetic matching the existing gallery (`#0a0d12` obsidian background, `#b87333` copper traces, `#00ffcc` neon accents).
- **Curator's Note**: 1–2 sentences explaining the concept behind the piece.

### 2. Generate & Save the Artwork (Image Model)
Run the included helper script to generate the image via `gen.pollinations.ai` and save it into `art/`:

```bash
python3 skills/colab-gallery-curator/scripts/curate_piece.py \
  --theme "22-Watt Frankenstein MoE: 1.5B GPU reflex + 30B CPU cortex" \
  --slug "frankenstein-22w" \
  --out-dir art/
```

Or using `polli` CLI directly:
```bash
polli image "cybernetic dual-core brain, copper PCB traces, neon cyan pulses on obsidian void, editorial sci-fi illustration" --out art/art_piece_7_frankenstein_22w.png
```

### 3. Publish to `art.html`
- Add a new `<article class="art-card">` block to `art.html` referencing the saved PNG in `art/`.
- Verify no private IPs or secrets are present before committing.
