#!/usr/bin/env bash
# Download the two 10x Genomics Visium HD datasets used in the course.
# These are several GB each — run ahead of the session on a good connection.
#
#   bash scripts/download_data.sh            # downloads both
#   bash scripts/download_data.sh crc        # colorectal cancer only (Notebook 1)
#   bash scripts/download_data.sh brain      # mouse brain only (Notebook 2)
set -euo pipefail

WHICH="${1:-all}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA="$ROOT/data"
mkdir -p "$DATA"

dl () { echo ">> $1"; curl -L -O "$1"; }

# ---------- Notebook 1: Human Colorectal Cancer (Space Ranger 3.0.0) ----------
if [[ "$WHICH" == "all" || "$WHICH" == "crc" ]]; then
  echo "== Colorectal cancer (Visium HD) =="
  mkdir -p "$DATA/crc" && cd "$DATA/crc"
  BASE=https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Human_Colon_Cancer
  dl "$BASE/Visium_HD_Human_Colon_Cancer_binned_outputs.tar.gz"
  dl "$BASE/Visium_HD_Human_Colon_Cancer_tissue_image.btf"
  tar -xzf Visium_HD_Human_Colon_Cancer_binned_outputs.tar.gz
fi

# ---------- Notebook 2: Mouse Brain Fresh Frozen (Space Ranger 3.1.1) ----------
if [[ "$WHICH" == "all" || "$WHICH" == "brain" ]]; then
  echo "== Mouse brain (Visium HD) =="
  mkdir -p "$DATA/mouse_brain" && cd "$DATA/mouse_brain"
  BASE=https://cf.10xgenomics.com/samples/spatial-exp/3.1.1/Visium_HD_Mouse_Brain_Fresh_Frozen
  dl "$BASE/Visium_HD_Mouse_Brain_Fresh_Frozen_binned_outputs.tar.gz"
  dl "$BASE/Visium_HD_Mouse_Brain_Fresh_Frozen_spatial.tar.gz"
  tar -xzf Visium_HD_Mouse_Brain_Fresh_Frozen_binned_outputs.tar.gz
  tar -xzf Visium_HD_Mouse_Brain_Fresh_Frozen_spatial.tar.gz
  # Full-resolution image (optional; Notebook 2 defaults to the Space Ranger hi-res PNG).
  # If you have the original tissue image used as Space Ranger input, place it here as
  #   Visium_HD_Mouse_Brain_Fresh_Frozen_tissue_image.tif
fi

echo "Done. See data/README.md for the expected layout and checkpoints."
