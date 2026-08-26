# Data & checkpoints

Raw data is **not** committed to this repo (it is several GB). Download it with
`bash scripts/download_data.sh` (or the `curl` commands inside each notebook).

## Expected layout

```
data/
├── crc/                                              # Notebook 1 (colorectal cancer)
│   ├── binned_outputs/
│   │   └── square_002um/                             # 2 µm bins (bin2cell input)
│   └── Visium_HD_Human_Colon_Cancer_tissue_image.btf # full-res H&E (bin2cell input)
├── mouse_brain/                                      # Notebook 2 (mouse brain)
│   ├── binned_outputs/
│   │   └── square_016um/                             # 16 µm bins (annotation resolution)
│   └── spatial/                                      # tissue_hires_image.png + scalefactors
└── checkpoints/                                      # small .h5ad / .h5 checkpoints (see below)
```

## Checkpoints (for the live session)

The heavy steps (StarDist segmentation; the Random-Forest pixel classifier; the interactive
annotation) are slow. Each notebook **saves** its intermediate result and can **load** it instead,
so students can skip straight to the analysis. Generate these once (ideally on an HPC/GPU node)
and host them so students can download them before the session.

| File | Produced by | Used by |
|------|-------------|---------|
| `checkpoints/crc_b2c.h5ad` | NB1 Part A (`bin_to_cell`) | NB1 Part B |
| `checkpoints/crc_b2c_annotated.h5ad` | NB1 Part B (CellTypist) | NB1 Part C (squidpy) |
| `.../square_016um/tt_annotations/annotations_v1.h5` | NB2 Part A (annotation) | NB2 Parts B–E |

**To pre-generate the bin2cell checkpoints** run `scripts/prep_checkpoints.py` (edit the paths first):

```bash
python scripts/prep_checkpoints.py
```

**Hosting:** the checkpoint `.h5ad`/`.h5` files are cell-level (small, tens–hundreds of MB) and are a
good fit for a **GitHub Release** attached to this repo, or a shared Drive/Zenodo link. Do not commit
them to git history.
