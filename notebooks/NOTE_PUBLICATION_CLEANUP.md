# Notebook publication cleanup

The two Colab notebooks under `notebooks/` were cleaned for PeerJ submission.

Removed conversational / AI-consultation phrases such as:

- `【这是最终版本，请只用这一份】`
- `截图发给我看结果`
- `请把上面的汇总表发给我`
- `请把这个 ZIP 文件发给我，不要只发截图`
- `我会据此决定`

Kept:

- executable training / evaluation / ablation code
- scientific comments and protocol notes
- step structure for Colab

Outputs were stripped so the committed notebooks stay small and reviewable.
