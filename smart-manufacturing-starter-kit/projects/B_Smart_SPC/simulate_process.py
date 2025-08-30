# ---------------------------------------------
# Project B - Process Simulator
# ---------------------------------------------
# Hyperparameters
CFG = {
    "lines": 3,
    "points": 2000,
    "mu": 0.0,
    "sigma": 1.0,
    "drift_sigma": 0.001,
    "outdir": "projects/B_Smart_SPC/out"
}

import os, argparse, numpy as np, pandas as pd

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", type=int, default=CFG["lines"])
    ap.add_argument("--points", type=int, default=CFG["points"])
    ap.add_argument("--outdir", type=str, default=CFG["outdir"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    rng = np.random.default_rng(7)
    rows = []
    for L in range(args.lines):
        mu_offset = rng.normal(0, 0.5)
        x = [CFG["mu"] + mu_offset]
        for i in range(1, args.points):
            x.append(x[-1] + rng.normal(0, CFG["drift_sigma"]))
        x = np.array(x) + rng.normal(0, CFG["sigma"], size=args.points)
        # inject out-of-control segments
        ooc = np.zeros(args.points, dtype=int)
        for k in range(3):
            s = rng.integers(args.points//4, args.points-100)
            x[s:s+50] += rng.normal(3.0, 0.2)  # mean shift
            ooc[s:s+50] = 1
        df = pd.DataFrame({"line": f"L{L+1}", "x": x, "ooc": ooc})
        rows.append(df)
    data = pd.concat(rows, ignore_index=True)
    data.to_csv(os.path.join(args.outdir, "process.csv"), index=False)
    print("[OK] Saved process.csv", data.shape)
