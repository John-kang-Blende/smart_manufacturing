# ---------------------------------------------
# Project A - Data Generator (Synthetic IIoT)
# ---------------------------------------------
# Hyperparameters
CFG = {
    "machines": 3,
    "freq_hz": 10,          # sampling frequency
    "seconds": 300,         # total duration
    "n_sensors": 4,         # per machine
    "fault_prob": 0.02,     # probability of fault onset per 1000 steps
    "drift_scale": 0.0005,
    "noise_std": 0.05,
    "outdir": "projects/A_IIoT_Anomaly_RUL/out"
}

import os, argparse, numpy as np, pandas as pd

def generate_signals(machines, freq, seconds, n_sensors, fault_prob, drift_scale, noise_std):
    steps = freq * seconds
    t = np.arange(steps) / freq
    dfs = []
    rng = np.random.default_rng(42)
    for m in range(machines):
        base = rng.normal(0, 1, (steps, n_sensors)).cumsum(axis=0) * drift_scale
        # add sinus + noise
        signal = base + np.sin(2*np.pi*0.1*t)[:,None] + rng.normal(0, noise_std, (steps, n_sensors))
        # occasional faults: add bias & variance
        faulty = np.zeros(steps, dtype=int)
        for s in range(1, steps):
            if rng.random() < fault_prob/1000.0:
                # persistent fault till end
                bias = rng.normal(1.5, 0.3, n_sensors)
                signal[s:, :] += bias
                faulty[s:] = 1
                break
        df = pd.DataFrame(signal, columns=[f"s{i+1}" for i in range(n_sensors)])
        df.insert(0, "t", t)
        df["machine"] = f"M{m+1}"
        df["faulty"] = faulty
        dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)
    return data

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--machines", type=int, default=CFG["machines"])
    ap.add_argument("--freq", type=int, default=CFG["freq_hz"])
    ap.add_argument("--seconds", type=int, default=CFG["seconds"])
    ap.add_argument("--n_sensors", type=int, default=CFG["n_sensors"])
    ap.add_argument("--outdir", type=str, default=CFG["outdir"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = generate_signals(args.machines, args.freq, args.seconds, args.n_sensors,
                          CFG["fault_prob"], CFG["drift_scale"], CFG["noise_std"])
    path = os.path.join(args.outdir, "signals.csv")
    df.to_csv(path, index=False)
    print(f"[OK] Saved: {path}, shape={df.shape}")
