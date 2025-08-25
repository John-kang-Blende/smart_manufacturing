#!/usr/bin/env python
# scripts/secom_open_and_inspect.py
"""
SECOM opener & inspector
------------------------
功能：
1) 讀取 UCI SECOM 的 secom.data（特徵）與 secom_labels.data（標籤+時間戳）
2) 自動建立欄名 s1..sN、將 label 轉為 fail=1/pass=0
3) 輸出兩個檔案：
   - out/secom_merged_head.csv（前20筆，方便用Excel檢視）
   - out/secom_headered.csv（完整資料，第一欄為 fail，之後 s1..sN）
4) 列印資料形狀、類別比例，以及缺失率摘要；另存為 out/missingness_summary.json
5) 若 data/secom.names 存在，輸出前 200 行預覽到 out/secom_names_preview.txt

使用範例：
    python scripts/secom_open_and_inspect.py --data_dir data --out_dir out
"""

import argparse
from pathlib import Path
import pandas as pd

def read_secom(data_dir: Path):
    """讀取 SECOM 的特徵與標籤檔，回傳 (X, y_df)。"""
    X = pd.read_csv(data_dir / "secom.data", sep=r"\s+", header=None, na_values=["NaN","nan"])
    y = pd.read_csv(data_dir / "secom_labels.data", sep=r"\s+", header=None, names=["label","timestamp"])
    # 建立欄名 s1..sN
    X.columns = [f"s{i}" for i in range(1, X.shape[1] + 1)]
    # UCI慣例：label = -1 表 Fail，1 表 Pass；轉為 fail 二元標籤
    y["fail"] = (y["label"] == 1).astype(int)
    return X, y

def preview_names_if_exists(data_dir: Path, out_dir: Path):
    """若存在 secom.names，輸出前200行到 out/secom_names_preview.txt。"""
    names_path = data_dir / "secom.names"
    if names_path.exists():
        txt = names_path.read_text(errors="ignore")
        lines = txt.splitlines()
        head = "\n".join(lines[:200])
        out = out_dir / "secom_names_preview.txt"
        out.write_text(head, encoding="utf-8")
        print(f"[INFO] Saved names preview -> {out} (lines: {min(200,len(lines))}/{len(lines)})")
    else:
        print("[INFO] No secom.names found (this dataset often ships without it).")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", type=str, default="data", help="資料夾，包含 secom.data / secom_labels.data / (secom.names)")
    ap.add_argument("--out_dir", type=str, default="out", help="輸出資料夾")
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 讀取資料
    X, y = read_secom(data_dir)

    # 2) 基本資訊
    print("[SHAPE] X:", X.shape, "  y:", y.shape)
    print("[CLASS BALANCE]\n", y["fail"].value_counts())

    # 3) 合併與輸出樣本（前20筆，便於人工檢視）
    merged = pd.concat([y["fail"], X], axis=1)
    sample_path = out_dir / "secom_merged_head.csv"
    merged.head(20).to_csv(sample_path, index=False)
    print(f"[SAVE] Sample head -> {sample_path}")

    # 4) 輸出完整 headered CSV（可用Excel/Sheets開啟）
    full_path = out_dir / "secom_headered.csv"
    merged.to_csv(full_path, index=False)
    print(f"[SAVE] Full headered CSV -> {full_path}")

    # 5) 缺失率摘要（描述統計），另存 JSON 版
    na_ratio = X.isna().mean()  # 每欄缺失比例
    desc = na_ratio.describe()
    print("[MISSINGNESS] per-feature NA ratio summary:\n", desc)
    (out_dir / "missingness_summary.json").write_text(desc.to_json(), encoding="utf-8")
    print(f"[SAVE] Missingness summary JSON -> {out_dir/'missingness_summary.json'}")

    # 6) .names 預覽（如果有）
    preview_names_if_exists(data_dir, out_dir)

if __name__ == "__main__":
    main()
