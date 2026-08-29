# Toxic Chinese Herbal Medicine Classification — 39-Class Benchmark

**Headline result: lightweight attention modules produced no reproducible accuracy gain on
this benchmark.**

An earlier single-seed run in this repository measured a +1.42 pp Top-1 improvement from a
Lightweight Texture Attention (LTA) module inserted into YOLOv12s-cls. A subsequent
4 × 3 factorial experiment (four attention variants × three random seeds, twelve training
runs) showed that this gain does not reproduce. All nine paired within-seed bootstrap 95%
confidence intervals include zero. The repository keeps both the original and the
multi-seed results so the change of conclusion is fully auditable.

Associated manuscript: submitted to *PeerJ Computer Science* as
"No reproducible accuracy gain from lightweight attention modules in fine-grained
classification of 39 toxic Chinese herbal medicines: a multi-seed, bootstrap-interval
evaluation of YOLOv12-cls and EfficientNet-B0".

Archived snapshot: release v1.0.0 of this repository is permanently archived on Zenodo,
DOI [10.5281/zenodo.22153695](https://doi.org/10.5281/zenodo.22153695). Citation
metadata: `CITATION.cff`.

---

## 1. Dataset

- Source: public Figshare deposit of real-world toxic Chinese herbal medicine images,
  CC BY, DOI [10.6084/m9.figshare.31136233](https://doi.org/10.6084/m9.figshare.31136233),
  released with Zhu et al. (2026), *PLOS ONE* 21:e0344262.
- This work uses a **plant-derived-only 39-class subset**. Excluded: 5 animal-derived
  classes (banmao, chansu, jinqian baihuashe, quanxie, wugong) and 3 mineral classes
  (baifan, xionghuang, zhusha). Exact class list: `data/class_subset_definition.json`.
- Splits: **1,981 train / 634 validation / 636 test**. Per-class counts 25–66 images.
- **Data-quality finding:** the supplementary `test_subset` partition (476 images) shipped
  with the copy we obtained is **MD5-identical to the validation split**. It is excluded.
  Any study that treated it as held-out data would report validation accuracy as test
  accuracy with no visible symptom.
- All experiments run behind a hard precondition gate that aborts unless the dataset is
  exactly 39 classes with 1,981/634/636 images. Items that are not one of the 39 classes —
  in the copy we obtained, six `.ipynb_checkpoints` directories holding 35 duplicated
  images — are quarantined before counting; every such item is listed in
  `environment/environment_and_protocol.json`.

## 2. Key results

### 2.1 Multi-seed attention ablation (YOLOv12s-cls, n = 636 test, seeds 42/123/2026)

| Variant | Top-1 mean ± SD | Top-5 mean ± SD | Δ Top-1 vs. baseline | Params | GFLOPs | Latency (ms/img) |
|---|---|---|---|---|---|---|
| Baseline (no attention) | 82.49% ± 0.09 | 96.02% ± 0.40 | — | 6,034,663 | 1.5130 | 0.856 |
| SE | 82.55% ± 0.57 | 95.96% ± 0.36 | +0.05 ± 0.65 pp | 6,067,431 | 1.5132 | 0.849 |
| CBAM | 82.29% ± 1.18 | 96.12% ± 0.48 | −0.21 ± 1.18 pp | 6,067,529 | 1.5132 | 0.863 |
| LTA | 82.18% ± 0.74 | 96.38% ± 0.57 | −0.31 ± 0.69 pp | 6,067,529 | 1.5132 | 0.864 |

Two of three attention variants sit **below** the no-attention baseline. The
within-variant seed spread (up to 2.36 pp for CBAM) exceeds every between-variant mean
difference by roughly an order of magnitude.

### 2.2 Paired within-seed bootstrap tests (10,000 paired resamples)

All nine comparisons non-significant; Δ ranges −1.42 pp to +0.94 pp; two-sided
p = 0.258–0.976; **every 95% CI includes zero**. See
`results/multiseed_attention_ablation/bootstrap_paired_differences.csv`.

### 2.3 Benchmark resolution limit

At ~82% accuracy on 636 test images, a bootstrap 95% CI spans about **±2.9 pp**. Effects
of 1–3 pp — the size of most published attention gains in this domain — are not
resolvable on a test set of this size, regardless of model design.

### 2.4 Honest disclosure about LTA

In the unified factorial harness, **LTA is structurally identical to CBAM** — same
dual-pooling channel branch, reduction ratio 16, 7×7 spatial kernel, identical parameter
count (6,067,529). The only difference is that the final layer of each attention branch is
zero-initialized. The LTA-vs-CBAM contrast is therefore an initialization-only contrast,
and the 0.10 pp gap between their three-seed means is an empirical **noise floor** for this
pipeline at zero structural change.

### 2.5 What the benchmark does resolve

| Factor | Effect | Verdict |
|---|---|---|
| Augmentation strength (strong vs. none) | +5.19 pp | Large, actionable |
| Architecture robustness (EfficientNet-B0 vs. YOLOv12s-cls mean drop) | 46.17 pp vs. 23.38–25.69 pp | Large, actionable |
| Inference latency (EfficientNet-B0 vs. YOLO-cls) | 1.74 ms vs. 0.86 ms/img | Large, actionable |
| Attention insertion | ≤0.31 pp, CI includes zero | Not resolvable |

EfficientNet-B0 has the highest clean accuracy (84.43%) and the fewest parameters
(4.06 M) but collapses to 19.18% under Gaussian noise. YOLOv12s-cls variants are roughly
twice as robust and roughly twice as fast.

## 3. Repository layout

```
CITATION.cff                                   # citation metadata
.zenodo.json                                   # Zenodo archival metadata
data/
  class_subset_definition.json                 # exact 39-class list + split counts
notebooks/
  01_cross_architecture_training_and_evaluation.ipynb
  02_multiseed_attention_ablation.ipynb
environment/
  environment_and_protocol.json                # versions, seeds, split counts,
                                               # pretrained-checkpoint MD5,
                                               # quarantined non-39-class items
  excluded_non39_items_audit.csv               # the quarantined items, as a table
  training_task_status.csv                     # completion status of all 12 runs
  result_manifest.json                         # size + MD5 of every other released
                                               # file, paths relative to the repo root
results/
  cross_architecture/                          # first campaign, single seed (42)
    test_set_results.csv                       # six models, Top-1/Top-5/params
    augmentation_regime_comparison.csv         # none / light / strong augmentation
    synthetic_robustness.csv                   # clean + 3 perturbations, 3 models
    training_curves/                           # per-epoch logs, 4 of the runs
  multiseed_attention_ablation/                # primary experiment, 12 runs
    attention_ablation_metrics.csv             # all 12 runs, per-run metrics
    multiseed_summary.csv                      # variant-level mean +/- SD
    multiseed_delta_summary.csv                # deltas vs. baseline
    bootstrap_model_accuracy_ci.csv            # per-run bootstrap 95% CIs
    bootstrap_paired_differences.csv           # paired within-seed tests + p-values
    efficientnet_b0_metrics_complete.csv       # EfficientNet-B0 reference metrics
    predictions/                               # 13 files x 636 rows, per-image records
  confusion_matrices/                          # single-seed Standard vs. LTA, 39x39
  gradcam_corrected_cases/                     # descriptive only, see caveat below
figures/
  fig_multiseed_attention_ci.png               # Figure 1
  fig_paired_bootstrap_deltas.png              # Figure 2
  fig_accuracy_robustness_latency.png          # Figure 3
  make_figures.py                              # regenerates all three figures
```

### 3.1 Where each manuscript item comes from

| Manuscript item | File in this repository |
|---|---|
| Table 1 — six architectures, single seed | `results/cross_architecture/test_set_results.csv` |
| Table 2 — augmentation regimes | `results/cross_architecture/augmentation_regime_comparison.csv` |
| Table 3 — 12 runs with bootstrap CIs | `results/multiseed_attention_ablation/attention_ablation_metrics.csv` + `bootstrap_model_accuracy_ci.csv` |
| Table 4 — variant means across seeds | `results/multiseed_attention_ablation/multiseed_summary.csv` |
| Table 5 — paired within-seed differences | `results/multiseed_attention_ablation/bootstrap_paired_differences.csv` (+ `multiseed_delta_summary.csv`) |
| Table 6 — per-image discordance, McNemar | notebook 01, step 13 (outputs retained in the notebook) |
| Table 7 — robustness and latency | `results/cross_architecture/synthetic_robustness.csv` |
| Figures 1–3 | `figures/*.png`, regenerated by `figures/make_figures.py` |
| Environment, seeds, checkpoint MD5 | `environment/environment_and_protocol.json` |

Every Top-1 and Top-5 value in Table 3 and in `attention_ablation_metrics.csv` can be
recomputed from `results/multiseed_attention_ablation/predictions/` alone, for example:

```python
import pandas as pd
d = pd.read_csv("results/multiseed_attention_ablation/predictions/"
                "v12s_lta_seed42_test_predictions.csv")
print(len(d), 100 * d.top1_correct.mean(), 100 * d.top5_correct.mean())
# 636 83.01886792452831 95.75471698113208
```

### 3.2 Verifying the release

```python
import hashlib, json, pathlib
m = json.load(open("environment/result_manifest.json"))
bad = [e["path"] for e in m["files"]
       if hashlib.md5(pathlib.Path(e["path"]).read_bytes()).hexdigest() != e["md5"]]
print(m["file_count"], "files;", len(bad), "checksum mismatches")
```

## 4. Experimental protocol

- Training: 50 epochs max, batch 32, imgsz 224, early-stopping patience 15 on validation
  Top-1. Best-validation checkpoint retained. **The test set was never used for model
  selection or hyperparameter tuning.**
- Hardware: single Tesla T4 (Google Colab) for every run.
- Software, first campaign (notebook 01): Python 3.12.13, Ultralytics 8.4.117,
  PyTorch 2.11.0 (CUDA 12.8).
- Software, factorial campaign (notebook 02): Python 3.13.15, Ultralytics 8.4.131,
  PyTorch 2.11.0 (CUDA 12.8), as recorded in
  `environment/environment_and_protocol.json`. Colab's default image advanced between the
  two campaigns; all twelve factorial runs share one environment, so the attention
  comparison is internally consistent.
- Pretrained YOLOv12s-cls checkpoint MD5: `eef2947ef14ce9a4a728453f3c15fb9a`.
- Bootstrap: `N_BOOT = 10000`, `BOOTSTRAP_SEED = 20260827`, `numpy.random.default_rng`.
- Latency: batch 32, CUDA-synchronized, amortized per image, Tesla T4.
- Robustness perturbations (fixed seed 42): Gaussian blur radius 2.5; additive Gaussian
  noise σ = 25 (0–255 scale); brightness × 0.5.
- Runs without a verified completion marker are renamed `*_INVALID_OR_INCOMPLETE_*` and
  excluded, never reused.

## 5. Caveats

- Three seeds per variant establishes that seed spread exceeds variant differences; it does
  not estimate variance precisely. The baseline's SD of 0.09 pp reflects only three runs.
- This is a **failure to detect** an effect on this benchmark, not proof that lightweight
  attention never helps.
- Robustness and augmentation numbers are single-run point estimates.
- The Grad-CAM and error-decomposition artefacts describe two specific checkpoints. Since
  the aggregate effect is not established, they are **not** evidence that attention helps.
  `results/gradcam_corrected_cases/` contains ten of the twenty-four images the LTA
  checkpoint corrected, selected in the order they appear in the test set.
- Parameter counts differ slightly between the original pipeline (backbone-only count) and
  the unified factorial harness (full assembled model). All attention conclusions rest on
  the unified harness.
- `results/cross_architecture/training_curves/` holds per-epoch logs for four of the first
  campaign's runs (YOLOv12n-cls, YOLOv12n-cls+LTA, YOLOv12s-cls, YOLOv12s-cls+LTA). They
  are provenance for convergence and early stopping only; no manuscript table or figure is
  derived from them.
- Notebook 01 is kept as the executed record of the first campaign, including its original
  console output. Its log messages are in Chinese, the working language of that campaign;
  translating them would break the correspondence between source lines and stored output.
  Notebook 02 stores no outputs and is fully in English.

## 6. Reproducing the analysis

```bash
# regenerate all three manuscript figures from the released CSVs
python figures/make_figures.py
```

The factorial experiment itself is reproduced by running
`notebooks/02_multiseed_attention_ablation.ipynb` on a Colab T4, after steps 1, 2 and 5 of
`notebooks/01_cross_architecture_training_and_evaluation.ipynb` have mounted Drive,
unpacked the dataset and installed Ultralytics. It re-runs all twelve trainings and
recomputes every bootstrap interval and p-value reported above.

## 7. Citation

If you use this benchmark or its results, please cite both the source dataset and this
work:

> Zhu G, Joo J, Park S, Kim SC. 2026. Toxic Chinese herbal medicine recognition in
> real-world images via multi-scale and attention-enhanced EfficientNetV2. *PLOS ONE*
> 21:e0344262. https://doi.org/10.1371/journal.pone.0344262

> Shao Z. No reproducible accuracy gain from lightweight attention modules in fine-grained
> classification of 39 toxic Chinese herbal medicines: a multi-seed, bootstrap-interval
> evaluation of YOLOv12-cls and EfficientNet-B0. Submitted to *PeerJ Computer Science*.

## 8. License

Code and analysis in this repository: see `LICENSE`. The underlying image dataset is CC BY
and remains the property of its original authors.

## Contact

Zigang Shao — The Second Affiliated Hospital of Heilongjiang University of Chinese
Medicine, Harbin, China — shaozigang@163.com — ORCID
[0009-0008-9105-1861](https://orcid.org/0009-0008-9105-1861)
