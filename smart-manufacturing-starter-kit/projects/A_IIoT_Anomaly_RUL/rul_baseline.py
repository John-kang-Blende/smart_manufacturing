# ---------------------------------------------
# Project A - Naive RUL Baseline
# ---------------------------------------------
# Idea: compute a health index HI per machine = zscore(s1) smoothed;
# when HI exceeds anomaly threshold, estimate RUL by slope-to-threshold.
import os, numpy as np, pandas as pd, json

OUTDIR = "projects/A_IIoT_Anomaly_RUL/out"
sig = pd.read_csv(os.path.join(OUTDIR, "signals.csv"))
with open(os.path.join(OUTDIR, "anomaly_report.json")) as f:
    rep = json.load(f)

def ema(x, alpha=0.05):
    y = np.zeros_like(x, dtype=float)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = alpha*x[i] + (1-alpha)*y[i-1]
    return y

rows = []
for mid, g in sig.groupby("machine"):
    hi = (g["s1"] - g["s1"].mean())/g["s1"].std(ddof=0)
    hi = ema(hi.values, 0.03)
    # simple slope-based RUL: steps until HI likely crosses (thr_norm)
    thr_norm = (rep["threshold"] - 0.0) / max(1e-6, np.var(hi))
    slope = np.gradient(hi)
    avg_slope = np.maximum(1e-6, np.mean(slope[-100:]))
    est = max(0.0, (thr_norm - hi[-1]) / avg_slope)
    rows.append({"machine": mid, "HI_last": float(hi[-1]), "RUL_steps_est": float(est)})

pd.DataFrame(rows).to_csv(os.path.join(OUTDIR, "rul_estimates.csv"), index=False)
print("[OK] Saved RUL to", os.path.join(OUTDIR, "rul_estimates.csv"))
