# Spatial Transcriptomics — Summer School (France 2026)

Tutorial materials for a hands-on session on **Visium HD** spatial transcriptomics, taught by
Nadav Yayon (Cambridge Stem Cell Institute / Teichmann Lab). Two notebooks take you from raw
Visium HD data to single cells, cell types, and quantitative tissue architecture.

| Notebook | Topic | Tools |
|----------|-------|-------|
| [`01_bin2cell_crc_celltypist_squidpy`](notebooks/01_bin2cell_crc_celltypist_squidpy.ipynb) | Reconstruct single cells from Visium HD, annotate them, and measure spatial proximity | **bin2cell**, scanpy, **CellTypist**, **squidpy** |
| [`02_tissuetag2_mouse_brain_regions`](notebooks/02_tissuetag2_mouse_brain_regions.ipynb) | Annotate brain regions, compute distances, build the pia→white-matter axis and cortical layers | **TissueTag2**, bin2cell, scanpy |

Notebook 1 uses the 10x **Human Colorectal Cancer** dataset; Notebook 2 uses the 10x
**Mouse Brain (Fresh Frozen)** dataset. Both follow the official `bin2cell` and `TissueTag2`
tutorials and use only functions built into those packages.

## What you'll learn

**Notebook 1 — bin2cell → CellTypist → squidpy**
- Correct the Visium HD "stripe" artefact (`b2c.destripe`)
- Segment nuclei on H&E with StarDist and rescue cells from gene expression
- Group 2 µm bins into **single cells** (`b2c.bin_to_cell`)
- Annotate cell types with CellTypist (public CRC model, optional 2-model combine)
- **New:** quantify which cell types sit together with squidpy **neighbourhood enrichment** and **co-occurrence**

**Notebook 2 — TissueTag2**
- Annotate tissue regions: gene-expression seeds → Random-Forest pixel classifier → interactive drawing
- Compute per-spot **distances** to each region
- Build the **pia → white-matter** cortical axis and split the cortex into **layers**
- Find **genes graded along** the cortical axis

## Setup

```bash
# 1) create the environment (conda recommended)
conda env create -f env/environment.yml
conda activate spatial-course-2026
# TissueTag2 is installed from its main branch by the env file.
# (pip-only alternative: python -m venv .venv && pip install -r env/requirements.txt)

# 2) download the data (several GB — do this before the session)
bash scripts/download_data.sh          # or: ... crc  /  ... brain

# 3) launch
jupyter lab
```

> **TissueTag2 is installed from the `main` branch** (`pip install "git+https://github.com/DRPTSB/TissueTag2.git@main"`),
> which carries the current distance/axis API used in Notebook 2. The notebook follows the teaching flow of the
> `oa_update` mouse-brain tutorial but calls the `main`-branch functions.

### Notes & caveats
- **StarDist needs TensorFlow.** On Apple Silicon use `tensorflow-macos` (+ optional `tensorflow-metal`); on HPC a CUDA build is much faster. Segmentation of a whole capture area is the slowest step.
- **scikit-image is pinned `<0.25`** because the TissueTag2 tutorial's Random-Forest helper uses `skimage.future.trainable_segmentation`.
- The **interactive annotator** (Notebook 2) needs a running Jupyter/Panel server; on a remote server set `host` to the port in your browser's address bar.
- Running everything live is slow — use the **pre-computed checkpoints** (see below).

## Running live vs. pre-computed checkpoints

Each notebook check-points its expensive steps to `data/checkpoints/` and can load them to skip ahead.
Generate the bin2cell checkpoints once with `python scripts/prep_checkpoints.py`, and save your
TissueTag annotation `.h5` from Notebook 2. Host these small files on a **GitHub Release** or shared
Drive/Zenodo for students to download before the session. See [`data/README.md`](data/README.md).

## Repository layout

```
notebooks/   the two tutorial notebooks
scripts/     download_data.sh, prep_checkpoints.py, vis_hd_aux_func.py (TissueTag2 helpers)
env/         environment.yml, requirements.txt
data/        (git-ignored) datasets + checkpoints — see data/README.md
```

## Credits & references
- **bin2cell** — Polański et al., *Bioinformatics* 2024. https://github.com/Teichlab/bin2cell
- **TissueTag2** — Amsalem, Yayon, Yang. https://github.com/DRPTSB/TissueTag2
- **CellTypist** — https://www.celltypist.org
- **squidpy** — Palla et al., *Nature Methods* 2022. https://github.com/scverse/squidpy
- Datasets © 10x Genomics (Visium HD Human Colon Cancer; Visium HD Mouse Brain Fresh Frozen).

*Teaching materials — for the France 2026 summer school.*
