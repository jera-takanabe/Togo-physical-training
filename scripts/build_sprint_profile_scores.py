
#!/usr/bin/env python3
"""
build_sprint_profile_scores.py v4

実データ構造:
- athlete
- session_date
- test
- raw_value
- unit
- score
- radar_score
- score_band
- domain
- gap_to_next_level

から Sprint Profile 用の分析テーブル
data/analysis/sprint_profile_scores.csv を生成する。

この版は以下に対応:
- benchmark_values.csv の実列構造
- 5m / 30m / Fly がまだ test_scores.csv に無い場合でも「部分プロファイル」を出力
- sprint_df から raw_value と radar_score を同一キーで pivot する
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict, List

import pandas as pd

REQUIRED_TEST_SCORE_COLUMNS = ["athlete", "session_date", "test", "raw_value", "radar_score"]
REQUIRED_BENCHMARK_COLUMNS = ["test", "floor_anchor", "world_elite_p50"]

DEFAULT_TEST_MAPPING = {
    "5m_sprint": "time_5m",
    "10m_sprint": "time_10m",
    "20m_sprint": "time_20m",
    "30m_sprint": "time_30m",
    "fly5": "fly5_time",
    "fly_5m": "fly5_time",
    "fly5_sprint": "fly5_time",
    "fly10": "fly10_time",
    "fly_10m": "fly10_time",
    "fly10_sprint": "fly10_time",
}

OUTPUT_COLUMNS = [
    "athlete",
    "session_date",
    "time_5m",
    "time_10m",
    "time_20m",
    "time_30m",
    "fly5_time",
    "fly10_time",
    "split_0_5",
    "split_5_10",
    "split_10_20",
    "split_20_30",
    "v_0_5",
    "v_5_10",
    "v_10_20",
    "v_20_30",
    "v_fly5",
    "v_fly10",
    "radar_5m",
    "radar_10m",
    "radar_20m",
    "radar_30m",
    "radar_fly5",
    "radar_fly10",
    "radar_20_30_seg",
    "acceleration_index",
    "max_velocity_index",
    "speed_reserve_index_basic",
    "split_balance_index",
    "elastic_support_score",
    "engine_support_score",
    "sprint_profile_type",
    "validation_flag",
    "validation_notes",
]


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def safe_div(numerator: float, denominator: float) -> float:
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return math.nan
    return numerator / denominator


def clamp_0_100(x: float) -> float:
    if pd.isna(x):
        return math.nan
    return max(0.0, min(100.0, float(x)))


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")
    return pd.read_csv(path)


def load_test_scores(path: Path) -> pd.DataFrame:
    df = load_csv(path)
    missing = [c for c in REQUIRED_TEST_SCORE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"test_scores.csv に必須列がありません: {missing}")
    df = df.copy()
    df["session_date"] = pd.to_datetime(df["session_date"]).dt.date.astype(str)
    df["test"] = df["test"].astype(str)
    df["raw_value"] = pd.to_numeric(df["raw_value"], errors="coerce")
    df["radar_score"] = pd.to_numeric(df["radar_score"], errors="coerce")
    return df


def load_benchmarks(path: Path) -> pd.DataFrame:
    df = load_csv(path)
    missing = [c for c in REQUIRED_BENCHMARK_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"benchmark_values.csv に必須列がありません: {missing}")
    df = df.copy()
    df["test"] = df["test"].astype(str)
    df["floor_anchor"] = pd.to_numeric(df["floor_anchor"], errors="coerce")
    df["world_elite_p50"] = pd.to_numeric(df["world_elite_p50"], errors="coerce")
    return df


def build_benchmark_lookup(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    lookup = {}
    for _, row in df.iterrows():
        lookup[str(row["test"])] = {
            "floor_anchor": float(row["floor_anchor"]),
            "world_elite_p50": float(row["world_elite_p50"]),
        }
    return lookup


def filter_sprint_tests(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["profile_key"] = out["test"].map(DEFAULT_TEST_MAPPING)
    return out[out["profile_key"].notna()].copy()


def pivot_values(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.pivot_table(
            index=["athlete", "session_date"],
            columns="profile_key",
            values="raw_value",
            aggfunc="first",
        )
        .reset_index()
    )
    out.columns.name = None
    return out


def pivot_radar_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.pivot_table(
            index=["athlete", "session_date"],
            columns="profile_key",
            values="radar_score",
            aggfunc="first",
        )
        .reset_index()
    )
    out.columns.name = None
    return out.rename(columns={
        "time_5m": "radar_5m",
        "time_10m": "radar_10m",
        "time_20m": "radar_20m",
        "time_30m": "radar_30m",
        "fly5_time": "radar_fly5",
        "fly10_time": "radar_fly10",
    })


def ensure_base_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in [
        "time_5m", "time_10m", "time_20m", "time_30m", "fly5_time", "fly10_time",
        "radar_5m", "radar_10m", "radar_20m", "radar_30m", "radar_fly5", "radar_fly10"
    ]:
        if c not in out.columns:
            out[c] = math.nan
    return out


def compute_splits(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["split_0_5"] = out["time_5m"]
    out["split_5_10"] = out["time_10m"] - out["time_5m"]
    out["split_10_20"] = out["time_20m"] - out["time_10m"]
    out["split_20_30"] = out["time_30m"] - out["time_20m"]
    return out


def compute_velocities(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["v_0_5"] = out["split_0_5"].apply(lambda x: safe_div(5, x))
    out["v_5_10"] = out["split_5_10"].apply(lambda x: safe_div(5, x))
    out["v_10_20"] = out["split_10_20"].apply(lambda x: safe_div(10, x))
    out["v_20_30"] = out["split_20_30"].apply(lambda x: safe_div(10, x))
    out["v_fly5"] = out["fly5_time"].apply(lambda x: safe_div(5, x))
    out["v_fly10"] = out["fly10_time"].apply(lambda x: safe_div(10, x))
    return out


def calc_radar_score_velocity(value: float, bm: Dict[str, float]) -> float:
    floor = bm["floor_anchor"]
    world = bm["world_elite_p50"]
    if pd.isna(value) or pd.isna(floor) or pd.isna(world) or world == floor:
        return math.nan
    return clamp_0_100(100 * (value - floor) / (world - floor))


def compute_segment_radar(df: pd.DataFrame, benchmark_lookup: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    out = df.copy()
    if "sprint_20_30_segment_velocity" not in benchmark_lookup:
        warn("benchmark_values.csv に sprint_20_30_segment_velocity が無いため、radar_20_30_seg は空欄にします。")
        out["radar_20_30_seg"] = math.nan
        return out
    bm = benchmark_lookup["sprint_20_30_segment_velocity"]
    out["radar_20_30_seg"] = out["v_20_30"].apply(lambda x: calc_radar_score_velocity(x, bm))
    return out


def merge_support_scores(df: pd.DataFrame, test_scores: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["elastic_support_score"] = math.nan
    out["engine_support_score"] = math.nan

    if "domain" not in test_scores.columns:
        return out

    tmp = test_scores.copy()
    tmp["domain"] = tmp["domain"].astype(str)
    tmp["radar_score"] = pd.to_numeric(tmp["radar_score"], errors="coerce")

    domain_mean = (
        tmp.groupby(["athlete", "session_date", "domain"], as_index=False)["radar_score"]
        .mean()
    )
    pivot = domain_mean.pivot_table(
        index=["athlete", "session_date"],
        columns="domain",
        values="radar_score",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None

    rename = {}
    if "reactive_strength" in pivot.columns:
        rename["reactive_strength"] = "elastic_support_score"
    if "endurance" in pivot.columns:
        rename["endurance"] = "engine_support_score"

    pivot = pivot.rename(columns=rename)
    keep = ["athlete", "session_date"] + [c for c in ["elastic_support_score", "engine_support_score"] if c in pivot.columns]
    if len(keep) > 2:
        out = out.merge(pivot[keep], on=["athlete", "session_date"], how="left", suffixes=("", "_new"))
        for c in ["elastic_support_score", "engine_support_score"]:
            newc = f"{c}_new"
            if newc in out.columns:
                out[c] = out[newc].combine_first(out[c])
                out = out.drop(columns=[newc])
    return out


def mean_available(df: pd.DataFrame, cols: List[str]) -> pd.Series:
    present = [c for c in cols if c in df.columns]
    if not present:
        return pd.Series([math.nan] * len(df), index=df.index)
    return df[present].mean(axis=1, skipna=True)


def compute_indices(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # 利用可能な acceleration 系だけで平均
    acc_cols = ["radar_5m", "radar_10m", "radar_20m", "radar_30m"]
    mv_cols = ["radar_fly5", "radar_fly10", "radar_20_30_seg"]

    out["acceleration_index"] = mean_available(out, acc_cols)
    out["max_velocity_index"] = mean_available(out, mv_cols)

    both = out["acceleration_index"].notna() & out["max_velocity_index"].notna()
    out["speed_reserve_index_basic"] = math.nan
    out.loc[both, "speed_reserve_index_basic"] = (
        out.loc[both, "max_velocity_index"] - out.loc[both, "acceleration_index"]
    )

    out["split_balance_index"] = math.nan
    valid = out["v_20_30"].notna() & out["v_0_5"].notna() & (out["v_20_30"] != 0)
    out.loc[valid, "split_balance_index"] = (
        (out.loc[valid, "v_20_30"] - out.loc[valid, "v_0_5"]) / out.loc[valid, "v_20_30"]
    )

    return out


def classify_row(row: pd.Series) -> str:
    acc = row.get("acceleration_index")
    mv = row.get("max_velocity_index")

    if pd.notna(acc) and pd.isna(mv):
        return "Partial Profile (Acceleration only)"
    if pd.isna(acc) and pd.notna(mv):
        return "Partial Profile (Max velocity only)"
    if pd.isna(acc) and pd.isna(mv):
        return "Insufficient Data"

    if acc < 50 and mv < 50:
        return "Underdeveloped Sprint Type"
    if acc >= mv + 8:
        return "Acceleration Type"
    if mv >= acc + 8:
        return "Max Velocity Type"
    return "Balanced Sprint Type"


def run_validation(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    flags = []
    notes = []

    for _, row in out.iterrows():
        row_flags: List[str] = []

        available_tests = [
            c for c in ["time_5m", "time_10m", "time_20m", "time_30m", "fly5_time", "fly10_time"]
            if pd.notna(row.get(c))
        ]
        if len(available_tests) < 2:
            row_flags.append("INSUFFICIENT_INPUT")

        if pd.notna(row.get("time_10m")) and pd.notna(row.get("time_20m")):
            if row["time_10m"] >= row["time_20m"]:
                row_flags.append("TIME_ORDER_ERROR")
        if pd.notna(row.get("time_20m")) and pd.notna(row.get("time_30m")):
            if row["time_20m"] >= row["time_30m"]:
                row_flags.append("TIME_ORDER_ERROR")
        if pd.notna(row.get("time_5m")) and pd.notna(row.get("time_10m")):
            if row["time_5m"] >= row["time_10m"]:
                row_flags.append("TIME_ORDER_ERROR")

        for key in ["split_5_10", "split_10_20", "split_20_30", "fly5_time", "fly10_time"]:
            v = row.get(key)
            if pd.notna(v) and v <= 0:
                row_flags.append("NON_POSITIVE_SPLIT")
                break

        if pd.notna(row.get("v_fly10")) and pd.notna(row.get("v_20_30")) and row["v_fly10"] != 0:
            mismatch = abs(row["v_fly10"] - row["v_20_30"]) / row["v_fly10"]
            if mismatch > 0.10:
                row_flags.append("FLY_SEGMENT_MISMATCH")

        missing_core = []
        for key in ["time_5m", "time_30m", "fly5_time", "fly10_time"]:
            if pd.isna(row.get(key)):
                missing_core.append(key)
        if missing_core:
            row_flags.append("PARTIAL_INPUT")

        uniq = sorted(set(row_flags))
        if not uniq:
            flags.append("OK")
            notes.append("")
        elif len(uniq) == 1:
            flags.append(uniq[0])
            notes.append(uniq[0])
        else:
            flags.append("MULTI_FLAG")
            notes.append(";".join(uniq))

    out["validation_flag"] = flags
    out["validation_notes"] = notes
    return out


def finalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["sprint_profile_type"] = out.apply(classify_row, axis=1)
    for c in OUTPUT_COLUMNS:
        if c not in out.columns:
            out[c] = math.nan
    return out[OUTPUT_COLUMNS].copy()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Sprint Profile Scores を生成します。")
    p.add_argument("--test-scores", default="data/analysis/test_scores.csv")
    p.add_argument("--benchmarks", default="data/reference/benchmark_values.csv")
    p.add_argument("--output", default="data/analysis/sprint_profile_scores.csv")
    return p


def main() -> None:
    args = build_parser().parse_args()

    test_scores = load_test_scores(Path(args.test_scores))
    benchmarks = load_benchmarks(Path(args.benchmarks))
    benchmark_lookup = build_benchmark_lookup(benchmarks)

    info(f"Loaded test scores: {len(test_scores)} rows")
    info("Available sprint-related tests:")
    sprint_names = sorted([
        t for t in test_scores["test"].dropna().unique().tolist()
        if "sprint" in str(t).lower() or "fly" in str(t).lower()
    ])
    print(sprint_names)

    sprint_df = filter_sprint_tests(test_scores)
    if sprint_df.empty:
        raise ValueError("対象となる sprint test が見つかりません。DEFAULT_TEST_MAPPING を確認してください。")

    values_wide = pivot_values(sprint_df)
    radar_wide = pivot_radar_scores(sprint_df)

    merged = values_wide.merge(radar_wide, on=["athlete", "session_date"], how="left")
    merged = ensure_base_columns(merged)
    merged = compute_splits(merged)
    merged = compute_velocities(merged)
    merged = compute_segment_radar(merged, benchmark_lookup)
    merged = merge_support_scores(merged, test_scores)
    merged = compute_indices(merged)
    merged = run_validation(merged)
    result = finalize_columns(merged)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")

    info(f"Built sprint profile rows: {len(result)}")
    for k, v in result["validation_flag"].value_counts().to_dict().items():
        if k != "OK":
            warn(f"{k}: {v} row(s)")
    info(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
