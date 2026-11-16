#!/bin/sh
# Taiwan-developed models for the cross-strait pilot: Breeze-7B (MediaTek Research) and Gemma-3-TAIDE-12b (TAIDE).
# Official weights from Hugging Face -> 4-bit MLX conversion -> mlx_lm.server on localhost:8080 -> run_cs.py.
# One model at a time (16 GB RAM).
cd "$(dirname "$0")/.." || exit 1
PY=".venv/bin/python"
MLX="${MLX_VENV:-$HOME/models/mlx-venv}/bin"   # a venv with mlx-lm installed
SRC="${MODEL_DIR:-$HOME/models}"            # Hugging Face downloads
OUT="${MLX_DIR:-$SRC/mlx}"                  # 4-bit MLX conversions (run.py reads MLX_DIR)
mkdir -p "$OUT"

shards_ok() {  # every shard named in the index exists and its safetensors header parses
  "$MLX/python" - "$1" <<'EOF'
import json, struct, sys, pathlib
d = pathlib.Path(sys.argv[1]); idx = json.loads((d / "model.safetensors.index.json").read_text())
for f in sorted(set(idx["weight_map"].values())):
    p = d / f
    with p.open("rb") as h:
        n = struct.unpack("<Q", h.read(8))[0]; hdr = json.loads(h.read(n))
    end = max(v["data_offsets"][1] for k, v in hdr.items() if k != "__metadata__")
    assert p.stat().st_size == 8 + n + end, f"{f} truncated"
print("shards ok")
EOF
}

run_model() {  # $1 = run_cs model name, $2 = download dir, $3 = mlx dir, $4 = curl url pattern
  echo "$(date '+%F %T') [$1] waiting for download"
  while pgrep -f "$4" >/dev/null; do sleep 60; done
  shards_ok "$2" || { echo "[$1] download incomplete, skipping"; return 1; }
  if [ ! -f "$3/config.json" ]; then
    echo "$(date '+%F %T') [$1] converting to 4-bit MLX (on CPU: the GPU is shared with Ollama, and a GPU convert timed out)"
    [ -d "$3" ] && rmdir "$3" 2>/dev/null  # an empty folder left by a failed convert
    "$MLX/python" -c "
import sys, mlx.core as mx
mx.set_default_device(mx.cpu)
from mlx_lm.convert import convert
convert(hf_path=sys.argv[1], mlx_path=sys.argv[2], quantize=True, q_bits=4, q_group_size=64)" "$2" "$3" || { echo "[$1] convert failed"; return 1; }
  fi
  echo "$(date '+%F %T') [$1] starting server"
  "$MLX/mlx_lm.server" --model "$3" --host 127.0.0.1 --port 8080 > "crossstrait/runs/_server_$1.log" 2>&1 &
  SP=$!
  for i in $(seq 1 60); do curl -sf http://127.0.0.1:8080/v1/models >/dev/null && break; sleep 5; done
  "$PY" crossstrait/run_cs.py --models "$1" --ids NC01 --langs tw > "crossstrait/runs/_smoke_$1.log" 2>&1
  echo "[$1] smoke test:"; tail -2 "crossstrait/runs/_smoke_$1.log"
  "$PY" crossstrait/run_cs.py --models "$1"
  "$PY" crossstrait/run_cs.py --models "$1"   # second pass retries any errored conversations
  kill "$SP"; wait "$SP" 2>/dev/null
  echo "$(date '+%F %T') [$1] done"
}

# TAIDE extends the Gemma-3 vocabulary to 318,080 tokens. Its config states this only in text_config, and mlx_lm's
# gemma3 wrapper overwrites text_config.vocab_size with a top-level default of 262,208, so the downloaded
# config.json got a top-level "vocab_size": 318080 (original kept as config.json.orig). Weights are unchanged.
for m in ${@:-breeze-7b taide-12b}; do
  case $m in
    breeze-7b) run_model breeze-7b "$SRC/Breeze-7B-Instruct-v1_0" "$OUT/breeze-7b-4bit" "Breeze-7B-Instruct-v1_0/resolve" ;;
    qwen2.5-7b) run_model qwen2.5-7b "$SRC/Qwen2.5-7B-Instruct" "$OUT/qwen2.5-7b-4bit" "Qwen2.5-7B-Instruct/resolve" ;;
    taide-12b) run_model taide-12b "$SRC/Gemma-3-TAIDE-12b-Chat-2602" "$OUT/taide-12b-4bit" "Gemma-3-TAIDE-12b-Chat-2602/resolve" ;;
  esac
done
echo finished
