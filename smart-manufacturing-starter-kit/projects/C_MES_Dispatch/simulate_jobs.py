# ---------------------------------------------
# Project C - Job generator & simulator
# ---------------------------------------------
import os, argparse, numpy as np, pandas as pd, simpy, heapq, random, statistics as stats
from dispatch_policies import priority

CFG = {
    "jobs": 200,
    "routes": 3,
    "machines": 4,
    "seed": 123,
    "outdir": "projects/C_MES_Dispatch/out"
}

def gen_jobs(n, routes, rng):
    jobs = []
    for j in range(n):
        r = rng.integers(1, routes+1)
        ops = rng.integers(2, 5)  # 2-4 ops
        route = rng.choice(range(1, routes+1))
        due = rng.integers(200, 400)
        jobs.append({"id": j, "route": route, "ops": ops, "due": due, "arrive_t": rng.integers(0, 50)})
    return jobs

def sim(policy, jobs, machines=4, seed=123, horizon=10000):
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    machine_queues = {m: [] for m in range(machines)}
    busy_until = {m: 0 for m in range(machines)}
    now = 0
    done = []
    # Expand jobs into operations
    ops = []
    for jb in jobs:
        t = jb["arrive_t"]
        for k in range(jb["ops"]):
            m = rng.integers(0, machines)
            p = int(rng.integers(5, 30))
            ops.append({"job": jb["id"], "op_idx": k, "op_machine": m, "proc_time": p,
                        "due": jb["due"], "arrive_t": t})
            t += rng.integers(0, 10)
    # Event loop (discrete-time)
    for now in range(horizon):
        # enqueue arrived ops
        for op in [x for x in ops if x["arrive_t"] == now]:
            heapq.heappush(machine_queues[op["op_machine"]], (priority(policy, op, now, {m: len(q) for m,q in machine_queues.items()}), op))
        # release finished ops
        for m in range(machines):
            if busy_until[m] == now:
                busy_until[m] = 0
        # start next ops
        for m in range(machines):
            if busy_until[m] == 0 and machine_queues[m]:
                _, op = heapq.heappop(machine_queues[m])
                start = now
                end = now + op["proc_time"]
                busy_until[m] = end
                done.append({"job": op["job"], "op_machine": m, "start": start, "end": end, "due": op["due"], "policy": policy})
        # stop condition
        if len(done) == len(ops):
            break
    return done, now

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=CFG["jobs"])
    ap.add_argument("--routes", type=int, default=CFG["routes"])
    ap.add_argument("--seed", type=int, default=CFG["seed"])
    ap.add_argument("--outdir", type=str, default=CFG["outdir"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    jobs = gen_jobs(args.jobs, args.routes, rng)
    pd.DataFrame(jobs).to_csv(os.path.join(args.outdir, "jobs.csv"), index=False)
    print("[OK] Saved jobs.csv", len(jobs))
