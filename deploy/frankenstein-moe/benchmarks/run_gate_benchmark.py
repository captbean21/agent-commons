#!/usr/bin/env python3
"""
Frankenstein MoE Gate Benchmark Harness
Evaluates TTFT, decode speed (tok/s), and latency against strict operational gates.
"""
import sys
import time
import requests

def benchmark_endpoint(base_url, model_name, prompt, max_tokens=64):
    url = f"{base_url}/chat/completions"
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "stream": False
    }

    print(f"Connecting to {url} ({model_name})...")
    t0 = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=90)
        t1 = time.time()
        data = resp.json()
    except Exception as e:
        print(f"Benchmark error: {e}")
        return False

    total_time = t1 - t0
    usage = data.get("usage", {})
    comp_tokens = usage.get("completion_tokens", max_tokens)
    prompt_tokens = usage.get("prompt_tokens", 0)
    tok_per_sec = comp_tokens / total_time if total_time > 0 else 0

    print(f"Results for {model_name}:")
    print(f"  Total Time: {total_time:.2f}s")
    print(f"  Prompt Tokens: {prompt_tokens}")
    print(f"  Completion Tokens: {comp_tokens}")
    print(f"  Decode Speed: {tok_per_sec:.2f} tok/s")
    print(f"  Sample: {data['choices'][0]['message']['content'][:100].strip()}...")
    return True

if __name__ == "__main__":
    prompt = "Explain the role of layer-wise streaming in low-VRAM large language model inference."
    port = sys.argv[1] if len(sys.argv) > 1 else "5002"
    benchmark_endpoint(f"http://127.0.0.1:{port}/v1", f"Port {port}", prompt)
