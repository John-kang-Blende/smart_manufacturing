# ---------------------------------------------
# Project B - Toy Domain-Invariant Classifier (GRL-like)
# ---------------------------------------------
# A minimal demo: learn to predict OOC vs OK while confusing line identity.
# (Lightweight: custom gradient reversal via tf.identity with gradient scale -λ)
import os, numpy as np, pandas as pd, tensorflow as tf
from tensorflow.keras import layers, models, losses, optimizers
from sklearn.metrics import precision_recall_fscore_support

OUTDIR = "projects/B_Smart_SPC/out"
df = pd.read_csv(os.path.join(OUTDIR, "process.csv"))

# window features
W = 16
def windowize(arr, w=W):
    x = []
    for i in range(len(arr)-w+1):
        x.append(arr[i:i+w])
    return np.stack(x)

Xs, Ys, Ds = [], [], []
for line, g in df.groupby("line"):
    xw = windowize(g["x"].values)
    yw = (windowize(g["ooc"].values).sum(axis=1) > 0).astype("int32")
    dw = np.full(len(yw), int(line[1:])-1)  # domain id 0..L-1
    Xs.append(xw[..., None])
    Ys.append(yw)
    Ds.append(dw)
X = np.concatenate(Xs, axis=0).astype("float32")
Y = np.concatenate(Ys, axis=0).astype("int32")
D = np.concatenate(Ds, axis=0).astype("int32")
n_domains = len(df["line"].unique())

inputs = layers.Input(shape=(W,1))
h = layers.Conv1D(16, 3, activation="relu")(inputs)
h = layers.GlobalAveragePooling1D()(h)
feat = layers.Dense(16, activation="relu", name="feat")(h)

# label head
yhat = layers.Dense(1, activation="sigmoid", name="yhat")(feat)

# domain head with GRL
lambda_grl = tf.Variable(0.5, trainable=False)
@tf.custom_gradient
def grl(x):
    def grad(dy):
        return -lambda_grl * dy
    return x, grad

dom = layers.Lambda(grl)(feat)
dhat = layers.Dense(n_domains, activation="softmax", name="dhat")(dom)

model = models.Model(inputs, [yhat, dhat])
model.compile(optimizer=optimizers.Adam(1e-3),
              loss={"yhat": losses.BinaryCrossentropy(),
                    "dhat": losses.SparseCategoricalCrossentropy()},
              loss_weights={"yhat": 1.0, "dhat": 0.2},
              metrics={"yhat": "accuracy", "dhat": "accuracy"})

model.fit(X, {"yhat": Y, "dhat": D}, epochs=5, batch_size=256, verbose=2)
y_pred = (model.predict(X, verbose=0)[0].ravel() > 0.5).astype("int32")
p, r, f1, _ = precision_recall_fscore_support(Y, y_pred, average="binary", zero_division=0)
pd.Series({"precision": p, "recall": r, "f1": f1}).to_csv(os.path.join(OUTDIR, "grl_metrics.csv"))
print("[GRL] P=%.3f R=%.3f F1=%.3f" % (p, r, f1))
