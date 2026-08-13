# TCM-39: Fine-Grained Classification of Toxic Chinese Herbal Decoction Pieces with YOLOv12-cls and a Lightweight Triple Attention (LTA) Module

This repository accompanies a manuscript (in preparation / under review) on fine-grained image classification of 39 classes of Traditional Chinese Medicine (TCM) decoction pieces, with a focus on visually similar and potentially toxic herb pairs. It contains the training/evaluation code, the resulting metrics tables, confusion matrices, and Grad-CAM visualizations reported in the paper, so that reviewers and readers can inspect and reproduce the reported results.

> Status: results and code are frozen as reported in the manuscript. This repository will be updated with the DOI/citation of the accepted paper once available.

## Dataset

- **Source**: [Image dataset of toxic Chinese herbal medicines](https://figshare.com/articles/dataset/Image_dataset_of_toxic_Chinese_herbal_medicines/31136233?file=61286866), Figshare, 2026.
- **Dataset DOI**: [10.6084/m9.figshare.31136233](https://doi.org/10.6084/m9.figshare.31136233)
- **License**: The original dataset is distributed under a **CC BY** license by its authors. All usage in this repository/manuscript complies with that license; the original dataset is **not redistributed** here — only derived metrics, trained-model outputs, and code are included.
- **Modifications made for this study**: The original dataset contains 47 classes. For this study we retained only the **39 plant-material classes** and excluded:
  - 5 animal-derived material classes
  - 3 mineral-derived material classes

  This exclusion was made because the modeling approach and augmentation pipeline in this study are designed and validated for plant-material (dried herb/decoction-piece) images; animal- and mineral-derived materials have different visual/texture characteristics that were out of scope for this work.
- **Splits used**: train (1981 images) / val (634 images) / test (636 images). An additional `test_subset` (476 images) provided with the original dataset was found to be byte-identical (MD5-identical) to the validation split during our data-quality checks and was therefore discarded; robustness was instead assessed via synthetic perturbations (see below).

## What's in this repository

```
notebooks/
  training_and_evaluation_pipeline.ipynb   # End-to-end Colab pipeline: data prep, training of all 5 models,
                                            # LTA module implementation, evaluation, Grad-CAM, confusion
                                            # matrices, augmentation study, synthetic robustness testing

results/
  tables/
    test_set_final_results.csv                  # Final test-set Top-1/Top-5 for all 5 models
    augmentation_comparison_final_v2.csv         # no_aug / light_aug / strong_aug comparison (YOLOv12s-cls)
    synthetic_robustness_final_combined.csv      # Gaussian blur / noise / brightness robustness, 3 models
    synthetic_robustness_efficientnet_b0.csv     # Robustness breakdown for the EfficientNet-B0 baseline
    efficientnet_b0_baseline_result.json         # EfficientNet-B0 baseline summary (params, clean top-1, n_test)
    training_curve_yolov12n_cls.csv              # Per-epoch training/validation curve, YOLOv12n-cls
    training_curve_yolov12n_cls_lta.csv          # Per-epoch training/validation curve, YOLOv12n-cls + LTA
    training_curve_yolov12s_cls.csv              # Per-epoch training/validation curve, YOLOv12s-cls
    training_curve_yolov12s_cls_lta.csv          # Per-epoch training/validation curve, YOLOv12s-cls + LTA

  confusion_matrices/
    confusion_matrix_yolov12s_cls_standard.jpg   # Row-normalized 39x39 confusion matrix, YOLOv12s-cls
    confusion_matrix_yolov12s_cls_lta.jpg        # Row-normalized 39x39 confusion matrix, YOLOv12s-cls + LTA

  gradcam_rescued_cases/
    rescued_*.jpg   # Grad-CAM 3-panel comparisons (original | Standard attention | +LTA attention) for test
                     # images that YOLOv12s-cls (Standard) misclassified but YOLOv12s-cls+LTA classified
                     # correctly. Filenames indicate the ground-truth class.
```

## Models evaluated

| Model | Test Top-1 (%) | Test Top-5 (%) | Params |
|---|---|---|---|
| YOLOv11n-cls | 82.08 | 96.70 | 1,575,983 |
| YOLOv12n-cls | 79.25 | 95.60 | 1,729,647 |
| YOLOv12n-cls + LTA | 76.57 | 95.91 | 1,737,937 |
| YOLOv12s-cls | 82.39 | 96.07 | 6,018,231 |
| YOLOv12s-cls + LTA | 83.81 | 95.28 | 6,051,097 |
| EfficientNet-B0 (baseline) | 84.43 | — | 4,060,000 |

Full numbers, per-condition breakdowns, and robustness results are in `results/tables/`.

## LTA (Lightweight Triple Attention) module

A lightweight channel + spatial attention block (`ChannelAttention` -> `SpatialAttention`) is injected at the second-to-last layer of the YOLOv12-cls backbone via an Ultralytics training callback (`on_pretrain_routine_end`). The wrapper class preserves the attributes required by Ultralytics' internal graph/serialization machinery so the augmented model remains fully trainable and checkpoint-compatible. See `notebooks/training_and_evaluation_pipeline.ipynb` for the full implementation and injection logic.

YOLOv12 classification weights are not hosted on Ultralytics' official release assets and were obtained from the upstream authors' release page: `https://github.com/sunsmarterjie/yolov12/releases/download/cls/`.

## Reproducing the results

The notebook is written for Google Colab. To reproduce:

1. Obtain the dataset from the Figshare source above and prepare it as a 39-class ImageFolder-style directory (train/val/test), excluding the 5 animal and 3 mineral classes as described.
2. Open `notebooks/training_and_evaluation_pipeline.ipynb` in Colab (or a local Jupyter environment with a GPU), mount your data, and run the cells in order — each stage (baseline training, LTA training, evaluation, augmentation study, robustness study, Grad-CAM, confusion matrices) is self-contained in its own cell/section.
3. Random seeds and augmentation/perturbation parameters used for the reported results are fixed in the notebook (e.g., synthetic robustness perturbations use seed=42, Gaussian blur radius=2.5, Gaussian noise sigma=25, brightness factor=0.5).

## License

- **Code** in this repository (`notebooks/`) is released under the MIT License — see [LICENSE](LICENSE).
- **Result artifacts** (`results/`) generated by the authors from model training/evaluation are released under CC BY 4.0.
- **Dataset**: not redistributed here. Refer to the original Figshare CC BY license for the source dataset.

## Citation

A citation block with the full paper reference and DOI will be added here once the manuscript is accepted and indexed.

For the dataset, please cite:

> Image dataset of toxic Chinese herbal medicines. Figshare. https://doi.org/10.6084/m9.figshare.31136233
