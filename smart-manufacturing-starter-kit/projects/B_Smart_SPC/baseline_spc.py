# ---------------------------------------------
# Project B - Baseline SPC (Xbar + Western Electric)
# ---------------------------------------------
import os, numpy as np, pandas as pd
from sklearn.metrics import precision_recall_fscore_support

OUTDIR = "projects/B_Smart_SPC/out"
path = os.path.join(OUTDIR, "process.csv")
df = pd.read_csv(path)

# Compute baseline mean/std per line from first 200 points (Phase I)
def detect_we(x, mu, sigma):
    UCL = mu + 3*sigma
    LCL = mu - 3*sigma
    rule1 = (x > UCL) | (x < LCL)
    # Two-of-three beyond 2σ, simplified rolling
    z = (x - mu)/sigma
    r3 = pd.Series(z).rolling(3).apply(lambda s: np.sum(np.abs(s) > 2) >= 2, raw=False).fillna(0).astype(bool)
    return rule1 | r3

pred = []
true = []
for line, g in df.groupby("line"):
    base = g.iloc[:200]["x"]
    mu, sigma = base.mean(), base.std(ddof=0)
    yhat = detect_we(g["x"].values, mu, sigma)
    pred.extend(yhat.astype(int).tolist())
    true.extend(g["ooc"].astype(int).tolist())

p, r, f1, _ = precision_recall_fscore_support(true, pred, average="binary", zero_division=0)
pd.Series({"precision": p, "recall": r, "f1": f1}).to_csv(os.path.join(OUTDIR, "spc_metrics.csv"))
print("[SPC] P=%.3f R=%.3f F1=%.3f" % (p, r, f1))
