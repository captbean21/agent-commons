#!/usr/bin/env python3
"""Generate a Colab Art Gallery piece using Pollinations text + image APIs."""

import argparse
import json
import os
import urllib.parse
import urllib.request


def generate_prompt(theme: str, api_key: str) -> dict:
    """Use Pollinations text API to turn a theme into a title, image prompt, and caption."""
    system = (
        "You are an art curator for a hardware-noir AI engineering gallery. "
        "Given a theme, return ONLY valid JSON with keys: title, prompt, caption. "
        "Keep the prompt visual, high-contrast, dark obsidian background (#0a0d12), "
        "copper (#b87333) and neon cyan (#00ffcc) accents, no text in the image."
    )
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Theme: {theme}"},
        ],
        "response_format": {"type": "json_object"},
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(
        "https://gen.pollinations.ai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])


def generate_image(prompt: str, out_path: str, api_key: str) -> None:
    """Fetch generated image from Pollinations image endpoint."""
    encoded = urllib.parse.quote(prompt, safe="")
    url = f"https://gen.pollinations.ai/image/{encoded}?model=black-forest-labs/flux.1-schnell&width=1024&height=1024&nologo=true"
    headers = {"User-Agent": "colab-gallery-curator/1.0"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(resp.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Curate a new gallery piece via Pollinations.")
    parser.add_argument("--theme", required=True, help="Engineering or creative theme")
    parser.add_argument("--slug", required=True, help="Filename slug (e.g. frankenstein-22w)")
    parser.add_argument("--out-dir", default="art", help="Output directory for PNG")
    parser.add_argument("--dry-run", action="store_true", help="Print metadata without downloading image")
    args = parser.parse_args()

    api_key = os.environ.get("POLLINATIONS_API_KEY", "")
    meta = generate_prompt(args.theme, api_key)
    out_path = os.path.join(args.out_dir, f"art_piece_{args.slug}.png")
    print(json.dumps({"title": meta["title"], "caption": meta["caption"], "prompt": meta["prompt"], "file": out_path}, indent=2))
    if not args.dry_run:
        generate_image(meta["prompt"], out_path, api_key)
        print(f"Saved artwork to {out_path}")


if __name__ == "__main__":
    main()
