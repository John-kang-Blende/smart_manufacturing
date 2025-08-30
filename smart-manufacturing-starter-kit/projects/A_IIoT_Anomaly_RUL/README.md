# Project A — IIoT Time-Series: Anomaly Detection & RUL Dashboard

**Goal:** Simulate multi-machine sensors (1–100Hz), detect anomalies via Conv1D autoencoder,
and produce a simple RUL estimate; visualize in a Streamlit dashboard.

**Key Files**
- `data_gen.py`: Synthetic OPC‑like signals with drifts/faults → CSV
- `train_anomaly.py`: Train a Conv1D autoencoder; export thresholds & metrics
- `rul_baseline.py`: Simple health index → naive RUL
- `dashboard.py`: Streamlit dashboard for live plots & predictions

**Run**
```bash
python data_gen.py --machines 3 --freq 10 --seconds 300
python train_anomaly.py --window 64 --epochs 3
python rul_baseline.py
streamlit run dashboard.py
```
