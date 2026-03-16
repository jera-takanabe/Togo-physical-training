#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from utils.i18n import load_labels, map_value
except Exception:
    def load_labels():
        return {}
    def map_value(value, labels):
        return str(value)


BASE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "data" / "analysis"
REFERENCE_DIR = BASE_DIR / "data" / "reference"
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "docs" / "dashboards"

TEST_SCORES_PATH = ANALYSIS_DIR / "test_scores.csv"
TARGET_PATH = REFERENCE_DIR / "target_by_stage.csv"
PROFILE_PATH = CONFIG_DIR / "athlete_profile.yaml"
BENCHMARK_PATH = REFERENCE_DIR / "benchmark_values.csv"

OUTPUT_RADAR = OUTPUT_DIR / "target_radar_v2.png"
OUTPUT_GAP = OUTPUT_DIR / "target_gap_summary.md"

AXES = [
    ("acceleration_score", "acceleration"),
    ("cod_score", "cod"),
    ("reactive_strength_score", "reactive_strength"),
    ("explosive_power_score", "explosive_power"),
    ("upper_body_power_score", "upper_body_power"),
]

RAW_LABELS = {
    "10m_sprint": ("10m", "s"),
    "pro_agility_5_10_5": ("COD", "s"),
    "rsi": ("RSI", ""),
    "cmj": ("CMJ", "cm"),
    "medicine_ball_throw_2kg": ("MBT 2kg", "m"),
}

GAP_AXES = [
    ("10m_s", "10m_sprint", "acceleration", "lower", None),
    ("COD_s", "pro_agility_5_10_5", "cod", "lower", None),
    ("RSI", "rsi", "reactive_strength", "higher", None),
    ("CMJ_cm", "cmj", "explosive_power", "higher", None),
    ("MBT_m", "medicine_ball_throw_2kg", "upper_body_power", "higher", None),
]

TEST_TO_DOMAIN = {
    "10m_sprint": ("acceleration_score", 0.6),
    "20m_sprint": ("acceleration_score", 0.4),
    "pro_agility_5_10_5": ("cod_score", 1.0),
    "rsi": ("reactive_strength_score", 1.0),
    "cmj": ("explosive_power_score", 0.6),
    "standing_long_jump": ("explosive_power_score", 0.4),
    "medicine_ball_throw_2kg": ("upper_body_power_score", 1.0),
}

for font_name in ["Noto Sans JP", "Yu Gothic", "Meiryo", "MS Gothic"]:
    try:
        matplotlib.rcParams["font.family"] = font_name
        break
    except Exception:
        pass
matplotlib.rcParams["axes.unicode_minus"] = False


def latest_rows_session(df: pd.DataFrame, date_col: str = "session_date") -> pd.DataFrame:
    if df.empty or date_col not in df.columns:
        return df
    latest_date = df[date_col].dropna().astype(str).max()
    return df[df[date_col].astype(str) == latest_date].copy()


def get_current_stage() -> str:
    if PROFILE_PATH.exists():
        text = PROFILE_PATH.read_text(encoding="utf-8")
        m = re.search(r"^\s*current_stage\s*:\s*([A-Za-z0-9_+-]+)\s*$", text, flags=re.MULTILINE)
        if m:
            return m.group(1).strip()
    return "JH1"


def interpolate_score(value: float, g: float, a: float, e: float, w: float, direction: str) -> float:
    def clamp(x: float) -> float:
        return max(0.0, min(100.0, x))

    if direction == "lower":
        if value >= g:
            if g == a:
                return 50.0
            return clamp(50.0 - (value - g) * 20.0 / abs(a - g))
        if value <= w:
            return 100.0
        segments = [(g, a, 50.0, 70.0), (a, e, 70.0, 85.0), (e, w, 85.0, 100.0)]
        for lv, rv, ls, rs in segments:
            if lv >= value >= rv:
                ratio = (lv - value) / (lv - rv)
                return clamp(ls + ratio * (rs - ls))
        return 100.0

    if value <= g:
        if a == g:
            return 50.0
        return clamp(50.0 - (g - value) * 20.0 / abs(a - g))
    if value >= w:
        return 100.0
    segments = [(g, a, 50.0, 70.0), (a, e, 70.0, 85.0), (e, w, 85.0, 100.0)]
    for lv, rv, ls, rs in segments:
        if lv <= value <= rv:
            ratio = (value - lv) / (rv - lv)
            return clamp(ls + ratio * (rs - ls))
    return 100.0


def interpolate_radar_score(value: float, floor: float, world: float, direction: str) -> float:
    def clamp(x: float) -> float:
        return max(0.0, min(100.0, x))

    if pd.isna(value) or pd.isna(floor) or pd.isna(world):
        return 0.0

    if direction == "higher":
        if world == floor:
            return 100.0
        score = 100.0 * (value - floor) / (world - floor)
        return clamp(score)

    if direction == "lower":
        if floor == world:
            return 100.0
        score = 100.0 * (floor - value) / (floor - world)
        return clamp(score)

    raise ValueError(f"Unknown direction: {direction}")

def load_current_test_scores() -> pd.DataFrame:
    df = pd.read_csv(TEST_SCORES_PATH)
    df = latest_rows_session(df)
    if df.empty:
        raise ValueError("No latest test_scores rows found.")
    return df

def load_current_domain_scores() -> pd.DataFrame:
    path = ANALYSIS_DIR / "domain_scores.csv"
    df = pd.read_csv(path)
    df = latest_rows_session(df)
    if df.empty:
        raise ValueError("No latest domain_scores rows found.")
    return df

def load_targets(stage: str) -> pd.DataFrame:
    df = pd.read_csv(TARGET_PATH)
    out = df[df["Stage"].astype(str) == stage].copy()
    if out.empty:
        raise ValueError(f"No target rows found for stage={stage}")
    return out


def build_current_score_map(domain_scores: pd.DataFrame) -> dict[str, float]:
    row = domain_scores.iloc[0]
    return {
        "acceleration_score": float(row.get("acceleration_score", 0.0)),
        "cod_score": float(row.get("cod_score", 0.0)),
        "reactive_strength_score": float(row.get("reactive_strength_score", 0.0)),
        "explosive_power_score": float(row.get("explosive_power_score", 0.0)),
        "upper_body_power_score": float(row.get("upper_body_power_score", 0.0)),
    }

def build_current_raw_map(test_scores: pd.DataFrame) -> dict[str, float]:
    return {str(r["test"]): float(r["raw_value"]) for _, r in test_scores.iterrows()}


def build_target_score_map(level_row: pd.Series, benchmark_values: pd.DataFrame) -> dict[str, float]:
    bench_map = {str(r["test"]): r for _, r in benchmark_values.iterrows()}

    domain_totals: dict[str, float] = {
        "acceleration_score": 0.0,
        "cod_score": 0.0,
        "reactive_strength_score": 0.0,
        "explosive_power_score": 0.0,
        "upper_body_power_score": 0.0,
    }

    domain_weights: dict[str, float] = {
        "acceleration_score": 0.0,
        "cod_score": 0.0,
        "reactive_strength_score": 0.0,
        "explosive_power_score": 0.0,
        "upper_body_power_score": 0.0,
    }

    for target_col, test_name, _, direction, _ in [
        ("10m_s", "10m_sprint", "acceleration", "lower", None),
        ("COD_s", "pro_agility_5_10_5", "cod", "lower", None),
        ("RSI", "rsi", "reactive_strength", "higher", None),
        ("CMJ_cm", "cmj", "explosive_power", "higher", None),
        ("MBT_m", "medicine_ball_throw_2kg", "upper_body_power", "higher", None),
    ]:
        if pd.isna(level_row.get(target_col)):
            continue
        if test_name not in bench_map:
            continue

        b = bench_map[test_name]
        radar_score = interpolate_radar_score(
            value=float(level_row[target_col]),
            floor=float(b["floor_anchor"]),
            world=float(b["world_elite_p50"]),
            direction=str(b["direction"]),
        )

        domain_key, weight = TEST_TO_DOMAIN[test_name]
        domain_totals[domain_key] += radar_score * weight
        domain_weights[domain_key] += weight

    out = {}
    for domain_key in domain_totals.keys():
        if domain_weights[domain_key] > 0:
            out[domain_key] = domain_totals[domain_key] / domain_weights[domain_key]

    return out

def create_radar(current_scores: dict[str, float], target_maps: dict[str, dict[str, float]], labels: dict[str, str], stage: str) -> None:
    axis_names = [map_value(domain_key, labels) for _, domain_key in AXES]
    current_values = [float(current_scores.get(score_col, 0.0)) for score_col, _ in AXES]

    angles = np.linspace(0, 2 * np.pi, len(axis_names), endpoint=False).tolist()
    angles += angles[:1]

    fig = plt.figure(figsize=(8.5, 8.5))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(axis_names, fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=10)

    world_values = [100.0] * len(axis_names)
    world_values += world_values[:1]
    ax.plot(angles, world_values, linewidth=1.5, linestyle="--", alpha=0.7, label="World")

    current_plot = current_values + current_values[:1]
    ax.plot(angles, current_plot, linewidth=2, label="Current")
    ax.fill(angles, current_plot, alpha=0.18)

    style_map = {"Benchmark": "-.", "Competitive": "--", "Elite": ":"}
    for level_name, score_map in target_maps.items():
        vals = [float(score_map.get(score_col, 0.0)) for score_col, _ in AXES]
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=2, linestyle=style_map.get(level_name, "--"), label=level_name)

    ax.set_title(f"Target Radar ({stage})", pad=20, fontsize=14)
    ax.legend(loc="upper right", bbox_to_anchor=(1.30, 1.12))
    fig.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_RADAR, dpi=150, bbox_inches="tight")
    plt.close(fig)

def format_gap(current: float, target: float, lower_better: bool) -> str:
    if lower_better:
        gap = current - target
        if gap > 0.005:
            return f"差 {gap:.2f}"
        if gap < -0.005:
            return f"超過 {abs(gap):.2f}"
        return "達成"
    gap = target - current
    if gap > 0.005:
        return f"差 {gap:.2f}"
    if gap < -0.005:
        return f"超過 {abs(gap):.2f}"
    return "達成"


def create_gap_summary(test_scores: pd.DataFrame, targets: pd.DataFrame, stage: str) -> None:
    elite = targets[targets["Level"].astype(str) == "Elite"]
    if elite.empty:
        return
    elite = elite.iloc[0]
    current_raw = build_current_raw_map(test_scores)

    lines = [f"## Target Gap Summary ({stage})", "", "### Elite 目標との差", ""]
    for target_col, test_name, _, direction, _ in GAP_AXES:
        label, unit = RAW_LABELS[test_name]
        current = current_raw.get(test_name, float("nan"))
        target = float(elite.get(target_col, float("nan")))
        if pd.isna(current) or pd.isna(target):
            lines.append(f"- {label}: -")
            continue
        gap_text = format_gap(float(current), float(target), direction == "lower")
        unit_text = unit
        lines.append(f"- {label}: 現在 {current:.2f}{unit_text} / Elite目標 {target:.2f}{unit_text} / {gap_text}{unit_text}")

    OUTPUT_GAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    labels = load_labels()
    stage = get_current_stage()
    test_scores = load_current_test_scores()
    domain_scores = load_current_domain_scores()
    benchmark_values = pd.read_csv(BENCHMARK_PATH)
    targets = load_targets(stage)

    current_score_map = build_current_score_map(domain_scores)
    target_maps = {}
    for _, row in targets.iterrows():
        target_maps[str(row["Level"])] = build_target_score_map(row, benchmark_values)

    create_radar(current_score_map, target_maps, labels, stage)
    create_gap_summary(test_scores, targets, stage)
    print(f"Created: {OUTPUT_RADAR}")
    print(f"Created: {OUTPUT_GAP}")


if __name__ == "__main__":
    main()
