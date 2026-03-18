
#!/usr/bin/env python3
"""
build_elastic_profile_scores.py

test_scores.csv から Elastic Profile 分析結果
data/analysis/elastic_profile_scores.csv を生成する。
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Tuple

import pandas as pd

REQUIRED_COLUMNS = ["athlete", "session_date", "test", "raw_value", "radar_score"]

TARGET_MAPPING = {
    "cmj": ("cmj_raw", "vertical_power_index"),
    "rsi": ("rsi_raw", "elastic_index"),
    "standing_long_jump": ("slj_raw", "horizontal_power_index"),
    "10m_sprint": ("sprint10_raw", "sprint_index"),
}


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def load_test_scores(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"test_scores.csv に必須列がありません: {missing}")
    df = df.copy()
    df["session_date"] = pd.to_datetime(df["session_date"]).dt.date.astype(str)
    df["test"] = df["test"].astype(str)
    df["raw_value"] = pd.to_numeric(df["raw_value"], errors="coerce")
    df["radar_score"] = pd.to_numeric(df["radar_score"], errors="coerce")
    return df


def pivot_profile(df: pd.DataFrame) -> pd.DataFrame:
    target_df = df[df["test"].isin(TARGET_MAPPING.keys())].copy()
    if target_df.empty:
        raise ValueError("Elastic Profile 対象のテストが見つかりません。")

    raw_rows = []
    radar_rows = []

    for _, row in target_df.iterrows():
        raw_col, radar_col = TARGET_MAPPING[row["test"]]
        raw_rows.append({
            "athlete": row["athlete"],
            "session_date": row["session_date"],
            "metric": raw_col,
            "value": row["raw_value"],
        })
        radar_rows.append({
            "athlete": row["athlete"],
            "session_date": row["session_date"],
            "metric": radar_col,
            "value": row["radar_score"],
        })

    raw_df = pd.DataFrame(raw_rows)
    radar_df = pd.DataFrame(radar_rows)

    raw_wide = raw_df.pivot_table(
        index=["athlete", "session_date"], columns="metric", values="value", aggfunc="first"
    ).reset_index()
    radar_wide = radar_df.pivot_table(
        index=["athlete", "session_date"], columns="metric", values="value", aggfunc="first"
    ).reset_index()

    raw_wide.columns.name = None
    radar_wide.columns.name = None

    return raw_wide.merge(radar_wide, on=["athlete", "session_date"], how="outer")


def mean_available(row: pd.Series, cols) -> float:
    vals = [row[c] for c in cols if c in row.index and pd.notna(row[c])]
    if not vals:
        return math.nan
    return float(sum(vals) / len(vals))


def classify(row: pd.Series) -> Tuple[str, str, str, str]:
    sprint_index = row.get("sprint_index", math.nan)
    power_index = row.get("power_index", math.nan)
    elastic_index = row.get("elastic_index", math.nan)
    sprint_transfer_index = row.get("sprint_transfer_index", math.nan)
    power_elastic_balance = row.get("power_elastic_balance", math.nan)

    if pd.notna(sprint_transfer_index) and sprint_transfer_index >= 20 and pd.notna(power_index) and power_index < 50:
        return ("Skill-Driven Sprinter", "水平パワー強化", "RSI強化", "走技術先行型")
    if pd.notna(power_index) and power_index < 50 and pd.notna(sprint_index) and sprint_index >= 60:
        return ("Power Deficit Type", "Broad Jump / Bounding", "下肢爆発力", "パワー不足")
    if pd.notna(elastic_index) and elastic_index < 50 and pd.notna(sprint_index) and sprint_index >= 60:
        return ("Elastic Deficit Type", "Drop Jump / Pogo", "接地改善", "弾性不足")
    if pd.notna(power_index) and power_index >= 60 and pd.notna(sprint_index) and sprint_index < 60:
        return ("Transfer Deficit Type", "加速技術", "力の方向づけ", "転移不足")
    if pd.notna(sprint_transfer_index) and abs(sprint_transfer_index) < 10 and pd.notna(power_elastic_balance) and abs(power_elastic_balance) < 10:
        return ("Balanced Development Type", "総合維持", "次のボトルネック確認", "バランス型")
    return ("Unclassified", "要再確認", "追加測定", "")


def compute_indices(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["power_index"] = out.apply(
        lambda r: mean_available(r, ["vertical_power_index", "horizontal_power_index"]), axis=1
    )
    out["sprint_transfer_index"] = out["sprint_index"] - out["power_index"]
    out["elastic_transfer_index"] = out["sprint_index"] - out["elastic_index"]
    out["power_elastic_balance"] = out["power_index"] - out["elastic_index"]

    labels = out.apply(classify, axis=1, result_type="expand")
    labels.columns = ["elastic_profile_type", "training_priority_1", "training_priority_2", "notes"]
    out = pd.concat([out, labels], axis=1)
    return out


def finalize(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "athlete",
        "session_date",
        "cmj_raw",
        "rsi_raw",
        "slj_raw",
        "sprint10_raw",
        "vertical_power_index",
        "elastic_index",
        "horizontal_power_index",
        "sprint_index",
        "power_index",
        "sprint_transfer_index",
        "elastic_transfer_index",
        "power_elastic_balance",
        "elastic_profile_type",
        "training_priority_1",
        "training_priority_2",
        "notes",
    ]
    for c in columns:
        if c not in df.columns:
            df[c] = math.nan
    return df[columns].copy()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Elastic Profile Scores を生成します。")
    p.add_argument("--test-scores", default="data/analysis/test_scores.csv")
    p.add_argument("--output", default="data/analysis/elastic_profile_scores.csv")
    return p


def main() -> None:
    args = build_parser().parse_args()
    test_scores = load_test_scores(Path(args.test_scores))
    info(f"Loaded test scores: {len(test_scores)} rows")

    wide = pivot_profile(test_scores)
    result = compute_indices(wide)
    result = finalize(result)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")
    info(f"Built elastic profile rows: {len(result)}")
    info(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
