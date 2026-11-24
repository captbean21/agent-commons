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

# Deploy Reflex service (Port 5002)
cat <<EOF > /etc/systemd/system/llama-reflex.service
[Unit]
Description=Frankenstein MoE - Reflex Fast Lane (1.5B GPU)
After=network.target

[Service]
Type=simple
User=${SERVICE_USER}
ExecStart=${LLAMA_BIN} \\
  -m ${MODELS_DIR}/qwen2.5-1.5b-instruct-q4_k_m.gguf \\
  -c 8192 \\
  -ngl 99 \\
  --host 0.0.0.0 \\
  --port 5002 \\
  --parallel 2 \\
  --cont-batching
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo "Systemd unit llama-reflex.service deployed."
echo "Setup complete. Enable with: systemctl enable --now llama-reflex.service"
