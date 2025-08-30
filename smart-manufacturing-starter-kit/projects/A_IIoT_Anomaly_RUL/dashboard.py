# ---------------------------------------------
# Project A - Streamlit Dashboard
# ---------------------------------------------
import streamlit as st
import pandas as pd, numpy as np, json, os, matplotlib.pyplot as plt

OUTDIR = "projects/A_IIoT_Anomaly_RUL/out"
st.title("IIoT Anomaly & RUL Dashboard")

sig_path = os.path.join(OUTDIR, "signals.csv")
rep_path = os.path.join(OUTDIR, "anomaly_report.json")
err_path = os.path.join(OUTDIR, "win_errors.npy")
lbl_path = os.path.join(OUTDIR, "win_labels.npy")
rul_path = os.path.join(OUTDIR, "rul_estimates.csv")

if not os.path.exists(sig_path):
    st.warning("No data yet. Run data_gen.py and train_anomaly.py first.")
    st.stop()

sig = pd.read_csv(sig_path)
st.subheader("Raw Signals (sample)")
st.write(sig.head())

if os.path.exists(rep_path):
    rep = json.load(open(rep_path))
    st.metric("Anomaly AUC", f"{rep['auc']:.3f}")
    st.write(rep)

if os.path.exists(err_path):
    err = np.load(err_path)
    lbl = np.load(lbl_path)
    st.subheader("Window Reconstruction Error")
    fig = plt.figure()
    plt.plot(err)
    plt.axhline(rep.get("threshold", np.nan), linestyle="--")
    st.pyplot(fig)

if os.path.exists(rul_path):
    st.subheader("RUL Estimates")
    st.write(pd.read_csv(rul_path))
