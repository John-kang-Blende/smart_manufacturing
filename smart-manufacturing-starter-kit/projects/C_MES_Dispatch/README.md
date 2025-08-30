# Project C — MES Dispatch Simulator (SimPy)
Simulate a small factory with multiple machines and routes.
Compare **EDD / SPT / Bottleneck priority / FIFO** on **TAT, tardiness, WIP, utilization (OEE-lite)**.

**Run**
```bash
python simulate_jobs.py --jobs 200 --routes 3
python evaluate.py --policies EDD SPT BOTTLENECK FIFO
```
