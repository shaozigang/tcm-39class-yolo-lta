# 打出 Zenodo DOI（PeerJ 投稿用）

DOI 必须用你自己的 GitHub 账号授权 Zenodo 才能生成。仓库元数据（`CITATION.cff`、`.zenodo.json`）已写好。按下面做完约 3 分钟。

## 1. 用 GitHub 登录 Zenodo

1. 打开 https://zenodo.org/  
2. 右上 Log in → **Sign in with GitHub**  
3. 授权 Zenodo 读你的仓库

## 2. 开启这个库的自动归档

1. 打开 https://zenodo.org/account/settings/github/  
2. 找到 `shaozigang/tcm-39class-yolo-lta`  
3. 把开关打到 **ON**

如果列表里没有这个库：点 Sync now / Refresh，确认仓库是 **Public**（已经是公开的）。

## 3. 在 GitHub 发一个 Release

1. 打开 https://github.com/shaozigang/tcm-39class-yolo-lta/releases/new  
2. Choose a tag：输入 `v1.0.0` → Create new tag  
3. Release title：`v1.0.0 — PeerJ CS submission artefacts`  
4. 描述可以贴：

```
First archival release for the PeerJ Computer Science submission.
Includes the 4x3 multi-seed attention ablation CSVs, bootstrap intervals,
figures, and analysis notebooks. Image files remain on Figshare
DOI 10.6084/m9.figshare.31136233 and are not redistributed here.
```

5. 勾选 **Set as the latest release**  
6. 点 **Publish release**

## 4. 拿 DOI

1. 回 https://zenodo.org/account/settings/github/  
2. 几分钟内 `tcm-39class-yolo-lta` 旁边会出现一条记录  
3. 点进去，页面上会有：

`DOI: 10.5281/zenodo.xxxxxxx`

把这串发给我，我写进论文 Data availability。

若 10 分钟还没出现：确认第 2 步开关是 ON，然后把 Release 删掉重发一次同一个 tag 也行。

## 不要上传什么

- 不要把 Figshare 上的原始图片再传一遍  
- 不要把网盘里的 `.pt` 权重塞进 GitHub（仓库会超限，也不是 PeerJ 必须的）  
- 审稿人要的是逐图预测 CSV、bootstrap 表和笔记本，这些已经在库里
