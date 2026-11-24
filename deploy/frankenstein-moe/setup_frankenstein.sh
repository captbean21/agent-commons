#!/usr/bin/env bash
# ==============================================================================
# Frankenstein MoE Automated Setup Script
# Co-Authored by Cas & Rook (Agent Commons)
# ==============================================================================
set -euo pipefail

MODELS_DIR="${MODELS_DIR:-/models}"
LLAMA_BIN="${LLAMA_BIN:-/opt/llama.cpp/build/bin/llama-server}"
SERVICE_USER="${SERVICE_USER:-rook}"

echo "=== Frankenstein MoE Installer ==="
echo "Models Directory: ${MODELS_DIR}"
echo "llama-server Binary: ${LLAMA_BIN}"

if [ ! -f "${LLAMA_BIN}" ]; then
    echo "ERROR: llama-server not found at ${LLAMA_BIN}"
    exit 1
fi

# Deploy Reflex service (Port 5002, GPU-resident fast lane)
cat <<EOF > /etc/systemd/system/llama-reflex.service
[Unit]
Description=Frankenstein MoE - Reflex Fast Lane (1.5B GPU)
After=network.target

[Service]
Type=simple
User=${SERVICE_USER}
ExecStart=${LLAMA_BIN} \\
  -m ${MODELS_DIR}/qwen2.5-1.5b-instruct-q4_k_m.gguf \\
  -c 4096 \\
  -ngl 99 \\
  --flash-attn \\
  -ctk q8_0 \\
  -ctv q8_0 \\
  --host 0.0.0.0 \\
  --port 5002 \\
  --parallel 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Deploy Cortex service (Port 5001, 30B MoE hybrid lane, 64K ctx)
cat <<EOF > /etc/systemd/system/llama-cortex.service
[Unit]
Description=Llama Cortex Reasoning Engine (30B MoE)
After=network.target

[Service]
Type=simple
User=${SERVICE_USER}
ExecStart=${LLAMA_BIN} \\
  -m ${MODELS_DIR}/Qwen3-Coder-30B-A3B-Instruct.Q4_K_M.gguf \\
  -c 65536 \\
  --flash-attn \\
  -ctk q4_0 \\
  -ctv q4_0 \\
  -t 6 \\
  --host 0.0.0.0 \\
  --port 5001 \\
  --parallel 1 \\
  --cont-batching
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo "Systemd units llama-reflex.service and llama-cortex.service deployed."
echo "Setup complete. Enable with: systemctl enable --now llama-reflex.service llama-cortex.service"
echo "Verify health: curl http://127.0.0.1:5002/health && curl http://127.0.0.1:5001/health"
