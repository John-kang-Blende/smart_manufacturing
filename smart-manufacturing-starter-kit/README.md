# Smart Manufacturing Starter Kit (Python + VBA + SQL)
**Version:** 0.1.0 — Generated 2025-08-30

This kit contains five ready-to-run mini projects tailored for *data‑driven smart manufacturing* roles:

- **A. IIoT Time-Series: Anomaly Detection & RUL Dashboard (Python, Streamlit)**
- **B. Smart SPC with Domain-Invariance (Python)** — compare classical control charts vs. domain‑robust ML
- **C. MES Dispatch Simulator (Python, SimPy)** — compare EDD/SPT/Bottleneck policies on TAT/WIP/OEE
- **D. Excel VBA Macros (VBA)** — Xbar‑R charts & simple ODBC pull into Excel
- **E. SQL Schema & Queries (SQL)** — manufacturing schema, analytic views, TimescaleDB/Influx‑like patterns

> **Why these?** They map your IMU/TCN/domain‑invariance strengths to factory language: time‑series, SPC, MES, dispatch, KPIs.

## Quick Start
```bash
# 1) Create environment
python -m venv .venv && source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Run a sample (A) anomaly detection on simulated data
python projects/A_IIoT_Anomaly_RUL/data_gen.py --machines 3 --freq 10 --seconds 300
python projects/A_IIoT_Anomaly_RUL/train_anomaly.py --window 64 --epochs 3
streamlit run projects/A_IIoT_Anomaly_RUL/dashboard.py

# 3) Run (B) Smart SPC comparison
python projects/B_Smart_SPC/simulate_process.py --lines 3 --points 2000
python projects/B_Smart_SPC/baseline_spc.py
python projects/B_Smart_SPC/domain_invariant_model.py  # (toy GRL; quick demo)
python projects/B_Smart_SPC/compare_results.py

# 4) Run (C) MES dispatch sim
python projects/C_MES_Dispatch/simulate_jobs.py --jobs 200 --routes 3
python projects/C_MES_Dispatch/evaluate.py --policies EDD SPT BOTTLENECK FIFO

# 5) VBA macros (D) import the .bas into Excel (Alt+F11 → File → Import)
#    SQL (E) use schema + queries on Postgres/Timescale or your RDBMS
```

## Python Requirements
See `requirements.txt` for pinned versions tested on Python 3.10–3.12.

## Structure
```
smart-manufacturing-starter-kit/
  README.md
  requirements.txt
  projects/
    A_IIoT_Anomaly_RUL/
    B_Smart_SPC/
    C_MES_Dispatch/
  vba/
    Mod_SPC.bas
    Mod_SQL.bas
  sql/
    01_schema.sql
    02_views.sql
    03_examples.sql
    04_timescaledb.sql
```
