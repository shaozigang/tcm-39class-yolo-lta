# Toxic Chinese Herbal Medicine Classification — 39-Class Benchmark

**Headline result: lightweight attention modules produced no reproducible accuracy gain on this benchmark.**

An earlier single-seed run in this repository measured a +1.42 pp Top-1 improvement from a
Lightweight Texture Attention (LTA) module inserted into YOLOv12s-cls. A subsequent
4 × 3 factorial experiment (four attention variants × three random seeds, twelve training
runs) showed that this gain does not reproduce. All nine paired within-seed bootstrap 95%
confidence intervals include zero. The repository keeps both the original and the
supplementary results so the change of conclusion is fully auditable.

Associated manuscript: submitted to *PeerJ Computer Science* as
"No reproducible accuracy gain from lightweight attention modules in fine-grained
classification of 39 toxic Chinese herbal medicines: a multi-seed, bootstrap-interval
evaluation of YOLOv12-cls and EfficientNet-B0".

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
  exactly 39 classes with 1,981/634/636 images.

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
`results/supplementary_attention_ablation/bootstrap_paired_differences.csv`.

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
data/
  class_subset_definition.json            # exact 39-class list + split counts
notebooks/
  training_and_evaluation_pipeline.ipynb   # original cross-architecture experiments
  supplementary_attention_ablation_pipeline.ipynb  # 4x3 factorial + bootstrap analysis
results/
  tables/                                  # original single-seed results (unchanged)
  supplementary_attention_ablation/        # multi-seed factorial results
    attention_ablation_metrics.csv         # all 12 runs, per-run metrics
    multiseed_summary.csv                  # variant-level mean +/- SD
    multiseed_delta_summary.csv            # deltas vs. baseline
    bootstrap_model_accuracy_ci.csv        # per-run bootstrap 95% CIs
    bootstrap_paired_differences.csv       # paired within-seed tests + p-values
    efficientnet_b0_metrics_complete.csv   # EfficientNet-B0 reference metrics
  confusion_matrices/                      # single-seed Standard vs. LTA
  gradcam_rescued_cases/                   # descriptive only, see caveat below
figures/
  fig_multiseed_attention_ci.png           # Figure 1
  fig_paired_bootstrap_deltas.png          # Figure 2
  fig_accuracy_robustness_latency.png      # Figure 3
  make_figures.py                          # regenerates all three figures
```

## 4. Experimental protocol

- Training: 50 epochs max, batch 32, imgsz 224, early-stopping patience 15 on validation
  Top-1. Best-validation checkpoint retained. **The test set was never used for model
  selection or hyperparameter tuning.**
- Hardware/software: Tesla T4 (Google Colab), Python 3.12.13, Ultralytics 8.4.118,
  PyTorch 2.11.0 (CUDA 12.8).
- Bootstrap: `N_BOOT = 10000`, `BOOTSTRAP_SEED = 20260827`, `numpy.random.default_rng`.
- Latency: batch 32, CUDA-synchronized, amortized per image, Tesla T4.
- Robustness perturbations (fixed seed 42): Gaussian blur radius 2.5; additive Gaussian
  noise σ = 25 (0–255 scale); brightness × 0.5.
- Runs without a verified completion marker are renamed and excluded, never reused.

## 5. Caveats

- Three seeds per variant establishes that seed spread exceeds variant differences; it does
  not estimate variance precisely. The baseline's SD of 0.09 pp reflects only three runs.
- This is a **failure to detect** an effect on this benchmark, not proof that lightweight
  attention never helps.
- Robustness and augmentation numbers are single-run point estimates.
- The Grad-CAM and error-decomposition artefacts describe two specific checkpoints. Since
  the aggregate effect is not established, they are **not** evidence that attention helps.
- Parameter counts differ slightly between the original pipeline (backbone-only count) and
  the unified factorial harness (full assembled model). All attention conclusions rest on
  the unified harness.

## 6. Reproducing the analysis

```bash
# regenerate all three manuscript figures from the released CSVs
python figures/make_figures.py
```

The factorial experiment itself is reproduced by running
`notebooks/supplementary_attention_ablation_pipeline.ipynb` on a Colab T4 with the dataset
mounted; it re-runs all twelve trainings and recomputes every bootstrap interval and
p-value reported above.

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
