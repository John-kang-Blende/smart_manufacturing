# ---------------------------------------------
# Project B - Compare SPC vs GRL demo
# ---------------------------------------------
import os, pandas as pd

OUTDIR = "projects/B_Smart_SPC/out"
spc = pd.read_csv(os.path.join(OUTDIR, "spc_metrics.csv"), index_col=0, header=None).squeeze("columns")
grl = pd.read_csv(os.path.join(OUTDIR, "grl_metrics.csv"), index_col=0, header=None).squeeze("columns")
df = pd.DataFrame({"SPC": spc, "GRL_demo": grl})
print(df)
df.to_csv(os.path.join(OUTDIR, "compare.csv"))
print("[OK] Saved compare.csv")
