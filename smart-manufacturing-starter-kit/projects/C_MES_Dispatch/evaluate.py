# ---------------------------------------------
# Project C - Evaluate policies
# ---------------------------------------------
import os, argparse, numpy as np, pandas as pd
from simulate_jobs import gen_jobs, sim, CFG

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--policies", nargs="+", default=["EDD","SPT","BOTTLENECK","FIFO"])
    ap.add_argument("--outdir", type=str, default=CFG["outdir"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    rng = np.random.default_rng(CFG["seed"])
    jobs = gen_jobs(CFG["jobs"], CFG["routes"], rng)

    rows = []
    for pol in args.policies:
        done, horizon = sim(pol, jobs, machines=4, seed=CFG["seed"])
        df = pd.DataFrame(done)
        # KPIs
        job_end = df.groupby("job")["end"].max()
        tardiness = (job_end - pd.Series({j["id"]: j["due"] for j in jobs})).clip(lower=0)
        tat = job_end - pd.Series({j["id"]: j["arrive_t"] for j in jobs})
        util = df.groupby("op_machine").apply(lambda g: (g["end"] - g["start"]).sum() / horizon).mean()
        rows.append({"policy": pol,
                     "TAT_mean": tat.mean(),
                     "TAT_p95": tat.quantile(0.95),
                     "Tardiness_rate": (tardiness > 0).mean(),
                     "Utilization": util})
    res = pd.DataFrame(rows).sort_values("TAT_mean")
    res.to_csv(os.path.join(args.outdir, "kpis.csv"), index=False)
    print(res)
