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
- Segment nuclei on H&E with StarDist and rescue cells from gene expression
- Group 2 µm bins into **single cells** (`b2c.bin_to_cell`)
- Annotate cell types with CellTypist (public CRC model, optional 2-model combine)
- quantify which cell types sit together with squidpy **neighbourhood enrichment** and **co-occurrence**

**Notebook 2 — TissueTag2**
- Annotate tissue regions: gene-expression seeds → Random-Forest pixel classifier → interactive drawing
- Compute per-spot **distances** to each region
- Build the **pia → white-matter** cortical axis and split the cortex into **layers**
- Find **genes graded along** the cortical axis

## Setup

The two notebooks have conflicting dependencies, so **each has its own environment** — create both.
Examples use `mamba`; `conda` works identically.

```bash
# 1) create the two environments
mamba env create -f env/environment_notebook1.yml   # NB1: bin2cell / CellTypist / squidpy
mamba env create -f env/environment_notebook2.yml   # NB2: TissueTag2

# 2) register a Jupyter kernel for each
mamba run -n spatial-course-2026-nb1 python -m ipykernel install --user \
  --name spatial-course-2026-nb1 --display-name "Python (spatial NB1: bin2cell)"
mamba run -n spatial-course-2026-nb2 python -m ipykernel install --user \
  --name spatial-course-2026-nb2 --display-name "Python (spatial NB2: TissueTag2)"

# 3) download the data (several GB — do this before the session)
bash scripts/download_data.sh            # or:  ... crc   /   ... brain

# 4) launch
jupyter lab
```

Then, in each notebook:

- **Select the matching kernel** — NB1 → *Python (spatial NB1: bin2cell)*, NB2 → *Python (spatial NB2: TissueTag2)*.
- **Set `DATA_DIR`** at the top of the notebook to where you downloaded the data (the paths `download_data.sh` prints at the end, e.g. `data/crc` and `data/mouse_brain`).

Notes:

- **Apple Silicon:** NB1's env installs `tensorflow-macos` automatically — the plain `tensorflow` wheel segfaults on import on M-series Macs. Nothing for you to do; the env file handles it per platform.
- **TissueTag2** is installed from its `main` branch by NB2's env file, which carries the current distance/axis API used in Notebook 2. The notebook follows the teaching flow of the `oa_update` mouse-brain tutorial but calls the `main`-branch functions.
- A single combined `env/environment.yml` is kept for reference, but the two per-notebook files above are the recommended setup.

## Credits & references
- **bin2cell** — Polański et al., *Bioinformatics* 2024. https://github.com/Teichlab/bin2cell
- **TissueTag2** — Amsalem, Yayon, Yang. https://github.com/DRPTSB/TissueTag2
- **CellTypist** — https://www.celltypist.org
- **squidpy** — Palla et al., *Nature Methods* 2022. https://github.com/scverse/squidpy
- Datasets © 10x Genomics (Visium HD Human Colon Cancer; Visium HD Mouse Brain Fresh Frozen).

*Teaching materials — for the France 2026 summer school.*
