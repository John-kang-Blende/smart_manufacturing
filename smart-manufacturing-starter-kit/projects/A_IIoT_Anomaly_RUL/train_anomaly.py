# -------------------------------------------------------
# Project A - Conv1D Autoencoder for Anomaly Detection
# -------------------------------------------------------
# Hyperparameters
HP = {
    "window": 64,
    "stride": 8,
    "epochs": 3,
    "batch": 128,
    "val_split": 0.2,
    "outdir": "projects/A_IIoT_Anomaly_RUL/out"
}

import os, argparse, numpy as np, pandas as pd, json
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import tensorflow as tf
from tensorflow.keras import layers, models

def windowize(X, w, s):
    out = []
    for i in range(0, len(X)-w+1, s):
        out.append(X[i:i+w])
    return np.stack(out)

def build_autoencoder(n_feats, w):
    x = layers.Input(shape=(w, n_feats))
    h = layers.Conv1D(32, 3, padding="same", activation="relu")(x)
    h = layers.MaxPool1D(2)(h)
    h = layers.Conv1D(16, 3, padding="same", activation="relu")(h)
    h = layers.MaxPool1D(2)(h)
    h = layers.Conv1D(16, 3, padding="same", activation="relu")(h)
    h = layers.UpSampling1D(2)(h)
    h = layers.Conv1D(32, 3, padding="same", activation="relu")(h)
    h = layers.UpSampling1D(2)(h)
    y = layers.Conv1D(n_feats, 3, padding="same")(h)
    model = models.Model(x, y)
    model.compile(optimizer="adam", loss="mse")
    return model

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=HP["window"])
    ap.add_argument("--stride", type=int, default=HP["stride"])
    ap.add_argument("--epochs", type=int, default=HP["epochs"])
    ap.add_argument("--batch", type=int, default=HP["batch"])
    ap.add_argument("--outdir", type=str, default=HP["outdir"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    data = pd.read_csv(os.path.join(args.outdir, "signals.csv"))
    feat_cols = [c for c in data.columns if c.startswith("s")]
    X = data[feat_cols].values.astype("float32")
    y_fault = data["faulty"].values.astype("int32")

    W = args.window
    S = args.stride
    Xw = windowize(X, W, S)
    # window label: any faulty within window -> 1
    yw = (windowize(y_fault, W, S).sum(axis=1) > 0).astype("int32")

    # Use only normal windows for training
    Xn = Xw[yw == 0]
    Xtr, Xval = train_test_split(Xn, test_size=HP["val_split"], random_state=42)

    model = build_autoencoder(n_feats=Xw.shape[-1], w=W)
    model.fit(Xtr, Xtr, validation_data=(Xval, Xval),
              epochs=args.epochs, batch_size=args.batch, verbose=2)

    # Score all windows by reconstruction error
    Xhat = model.predict(Xw, verbose=0)
    err = ((Xw - Xhat)**2).mean(axis=(1,2))
    thr = float(np.percentile(err[yw == 0], 99))  # robust threshold on normal
    auc = float(roc_auc_score(yw, err))

    # Save artifacts
    np.save(os.path.join(args.outdir, "win_errors.npy"), err)
    np.save(os.path.join(args.outdir, "win_labels.npy"), yw)
    model.save(os.path.join(args.outdir, "ae.keras"))
    with open(os.path.join(args.outdir, "anomaly_report.json"), "w") as f:
        json.dump({"window": W, "stride": S, "auc": auc, "threshold": thr}, f, indent=2)
    print(f"[REPORT] AUC={auc:.3f}, thr={thr:.4f}")
