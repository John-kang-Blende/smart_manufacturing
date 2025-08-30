# Project B — Smart SPC + Domain-Invariance
Simulate multiple production lines with drifts/offsets.
Compare **classical SPC** (Xbar, Western Electric rules) vs. a **toy domain-invariant classifier**.

**Run**
```bash
python simulate_process.py --lines 3 --points 2000
python baseline_spc.py
python domain_invariant_model.py   # fast demo; no GPU required
python compare_results.py
```
