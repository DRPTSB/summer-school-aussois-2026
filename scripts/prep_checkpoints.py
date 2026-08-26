#!/usr/bin/env python
"""
Pre-generate the Notebook 1 checkpoints (bin2cell single cells + CellTypist annotation)
so students can skip the slow segmentation during the live session.

Run once, ideally on a machine with a GPU (StarDist) and enough RAM:
    python scripts/prep_checkpoints.py

Outputs (into data/checkpoints/):
    crc_b2c.h5ad             - reconstructed single cells
    crc_b2c_annotated.h5ad   - + CellTypist labels, UMAP, leiden

Edit the paths in the CONFIG block first.
"""
import os
import numpy as np
import scanpy as sc
import bin2cell as b2c
import cv2

# ----------------------------- CONFIG -----------------------------
DATA_DIR = "data/crc"
PATH_2UM = f"{DATA_DIR}/binned_outputs/square_002um/"
SOURCE_IMAGE = f"{DATA_DIR}/Visium_HD_Human_Colon_Cancer_tissue_image.btf"
CKPT_DIR = "data/checkpoints"
HEALTHY_GUT_MODEL = None   # optional local .pkl for the 2-model combine
UP_DOWN, RIGHT_LEFT = -5, 0  # H&E/GEX alignment shift (inspect in the notebook first!)
# ------------------------------------------------------------------

os.makedirs(CKPT_DIR, exist_ok=True)
os.makedirs("stardist", exist_ok=True)


def segment():
    adata = b2c.read_visium(PATH_2UM, source_image_path=SOURCE_IMAGE)
    adata.var_names_make_unique()
    sc.pp.filter_genes(adata, min_cells=3)
    sc.pp.filter_cells(adata, min_counts=1)

    b2c.destripe(adata)
    adata.obsm["spatial"][:, 1] += UP_DOWN
    adata.obsm["spatial"][:, 0] += RIGHT_LEFT

    mpp = 0.3
    b2c.scaled_he_image(adata, mpp=mpp, save_path="stardist/he.tiff")
    b2c.stardist(image_path="stardist/he.tiff", labels_npz_path="stardist/he.npz",
                 stardist_model="2D_versatile_he", prob_thresh=0.1)
    b2c.insert_labels(adata, labels_npz_path="stardist/he.npz", basis="spatial",
                      spatial_key="spatial_cropped", mpp=mpp, labels_key="labels_he")
    b2c.expand_labels(adata, labels_key="labels_he",
                      expanded_labels_key="labels_he_expanded", max_bin_distance=4)

    img = b2c.grid_image(adata, "n_counts_adjusted", mpp=mpp, sigma=5)
    cv2.imwrite("stardist/gex.tiff", img)
    b2c.stardist(image_path="stardist/gex.tiff", labels_npz_path="stardist/gex.npz",
                 stardist_model="2D_versatile_fluo", prob_thresh=0.01, nms_thresh=0.1)
    b2c.insert_labels(adata, labels_npz_path="stardist/gex.npz", basis="array",
                      mpp=mpp, labels_key="labels_gex")
    b2c.salvage_secondary_labels(adata, primary_label="labels_he_expanded",
                                 secondary_label="labels_gex", labels_key="labels_joint")

    cdata = b2c.bin_to_cell(adata, labels_key="labels_joint",
                            spatial_keys=["spatial", "spatial_cropped"])
    cdata.write_h5ad(f"{CKPT_DIR}/crc_b2c.h5ad")
    print("saved", f"{CKPT_DIR}/crc_b2c.h5ad")
    return cdata


def annotate(cdata):
    import celltypist
    from celltypist import models

    cdata = cdata[cdata.obs["bin_count"] > 5].copy()
    cdata.X.data = np.round(cdata.X.data)
    cdata.raw = cdata.copy()
    sc.pp.filter_genes(cdata, min_cells=3)
    sc.pp.filter_cells(cdata, min_genes=100)
    sc.pp.calculate_qc_metrics(cdata, inplace=True)
    sc.pp.highly_variable_genes(cdata, n_top_genes=5000, flavor="seurat_v3")
    sc.pp.normalize_total(cdata, target_sum=1e4)
    sc.pp.log1p(cdata)

    models.download_models(model=["Human_Colorectal_Cancer.pkl"], force_update=False)
    pred = celltypist.annotate(cdata, model="Human_Colorectal_Cancer.pkl", majority_voting=False)
    cdata = pred.to_adata()
    cdata.obs["predicted_labels_crc"] = cdata.obs["predicted_labels"]
    cdata.obs["conf_score_crc"] = cdata.obs["conf_score"]

    if HEALTHY_GUT_MODEL:
        tmp = celltypist.annotate(cdata, model=HEALTHY_GUT_MODEL, majority_voting=False).to_adata()
        cdata.obs["predicted_labels_healthy"] = tmp.obs["predicted_labels"]
        cdata.obs["conf_score_healthy"] = tmp.obs["conf_score"]
        higher = cdata.obs["conf_score_healthy"] < cdata.obs["conf_score_crc"]
        higher[cdata.obs["predicted_labels_crc"] == "Unknown"] = False
        labels = cdata.obs["predicted_labels_healthy"].astype("object")
        labels[higher] = cdata.obs.loc[higher, "predicted_labels_crc"]
        conf = cdata.obs["conf_score_healthy"].copy()
        conf[higher] = cdata.obs.loc[higher, "conf_score_crc"]
        cdata.obs["predicted_labels"] = labels.astype("category")
        cdata.obs["conf_score"] = conf
    else:
        cdata.obs["predicted_labels"] = cdata.obs["predicted_labels_crc"].astype("category")
        cdata.obs["conf_score"] = cdata.obs["conf_score_crc"]

    emb = cdata[:, cdata.var["highly_variable"]].copy()
    sc.pp.scale(emb, max_value=10)
    sc.pp.pca(emb, use_highly_variable=True)
    sc.pp.neighbors(emb)
    sc.tl.umap(emb)
    sc.tl.leiden(emb, resolution=2.0, key_added="leiden")
    cdata.obsm["X_umap"] = emb.obsm["X_umap"]
    cdata.obs["leiden"] = emb.obs["leiden"].values

    cdata.write_h5ad(f"{CKPT_DIR}/crc_b2c_annotated.h5ad")
    print("saved", f"{CKPT_DIR}/crc_b2c_annotated.h5ad")


if __name__ == "__main__":
    annotate(segment())
