#!/usr/bin/env python3
"""
calc_rugby_physical_score.py

Purpose:
- Read processed session files and benchmark values
- Convert test results to 0-100 scores
- Build domain scores
- Build rugby physical score summary

Notes:
- rugby_ball_throw is intentionally excluded from score calculation.
- medicine_ball_throw_2kg is included when present in processed throw sessions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
REFERENCE = ROOT / "data" / "reference"
ANALYSIS = ROOT / "data" / "analysis"

BENCHMARK_PATH = REFERENCE / "benchmark_values.csv"

TEST_CONFIG = {
    "10m_sprint": {"direction": "lower", "domain": "acceleration"},
    "20m_sprint": {"direction": "lower", "domain": "acceleration"},
    "pro_agility_5_10_5": {"direction": "lower", "domain": "cod"},
    "cmj": {"direction": "higher", "domain": "explosive_power"},
    "standing_long_jump": {"direction": "higher", "domain": "explosive_power"},
    "rsi": {"direction": "higher", "domain": "reactive_strength"},
    "medicine_ball_throw_2kg": {"direction": "higher", "domain": "upper_body_power"},
}

DOMAIN_WEIGHTS = {
    "acceleration": 0.30,
    "cod": 0.25,
    "reactive_strength": 0.20,
    "explosive_power": 0.15,
    "upper_body_power": 0.10,
}

PRIORITY_BONUS = {
    "acceleration": 5.0,
    "cod": 5.0,
    "reactive_strength": 3.0,
    "explosive_power": 0.0,
    "upper_body_power": 0.0,
}


def ensure_dirs() -> None:
    ANALYSIS.mkdir(parents=True, exist_ok=True)


def load_benchmarks() -> pd.DataFrame:
    df = pd.read_csv(BENCHMARK_PATH)
    required = {
        "test",
        "unit",
        "general_youth_p50",
        "youth_athlete_p50",
        "elite_u18_p50",
        "world_elite_p50",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"benchmark_values.csv missing columns: {sorted(missing)}")
    return df


def interpolate_score(value: float, g: float, a: float, e: float, w: float, direction: str) -> float:
    def clamp(x: float) -> float:
        return max(0.0, min(100.0, x))

    if direction == "lower":
        if value >= g:
            if g == a:
                return 50.0
            score = 50.0 - (value - g) * 20.0 / abs(a - g)
            return clamp(score)
        if value <= w:
            return 100.0

        segments = [
            (g, a, 50.0, 70.0),
            (a, e, 70.0, 85.0),
            (e, w, 85.0, 100.0),
        ]
        for left_val, right_val, left_score, right_score in segments:
            if left_val >= value >= right_val:
                ratio = (left_val - value) / (left_val - right_val)
                return clamp(left_score + ratio * (right_score - left_score))
        return clamp(100.0)

    if value <= g:
        if a == g:
            return 50.0
        score = 50.0 - (g - value) * 20.0 / abs(a - g)
        return clamp(score)
    if value >= w:
        return 100.0

    segments = [
        (g, a, 50.0, 70.0),
        (a, e, 70.0, 85.0),
        (e, w, 85.0, 100.0),
    ]
    for left_val, right_val, left_score, right_score in segments:
        if left_val <= value <= right_val:
            ratio = (value - left_val) / (right_val - left_val)
            return clamp(left_score + ratio * (right_score - left_score))
    return clamp(100.0)


def score_band(score: float) -> str:
    if score >= 90:
        return "Elite"
    if score >= 80:
        return "Competitive"
    if score >= 70:
        return "Advanced"
    if score >= 60:
        return "Developing"
    if score >= 50:
        return "Foundation"
    return "Early Stage"


def next_level_gap(value: float, benchmark_row: pd.Series, direction: str) -> Optional[float]:
    levels = [
        ("general", benchmark_row["general_youth_p50"]),
        ("athlete", benchmark_row["youth_athlete_p50"]),
        ("elite", benchmark_row["elite_u18_p50"]),
        ("world", benchmark_row["world_elite_p50"]),
    ]

    if direction == "lower":
        for _, target in reversed(levels):
            if value > target:
                return round(value - target, 4)
        return 0.0

    for _, target in levels:
        if value < target:
            return round(target - value, 4)
    return 0.0


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def extract_test_results_from_processed() -> pd.DataFrame:
    rows = []

    sprint = _safe_read_csv(PROCESSED / "sprint_sessions.csv")
    if not sprint.empty:
        for _, r in sprint.iterrows():
            athlete = r["athlete"]
            session_date = r["date"]
            if pd.notna(r.get("best_split_10m_s")):
                rows.append({
                    "athlete": athlete,
                    "session_date": session_date,
                    "test": "10m_sprint",
                    "raw_value": float(r["best_split_10m_s"]),
                    "unit": "s",
                })
            if pd.notna(r.get("best_split_20m_s")):
                rows.append({
                    "athlete": athlete,
                    "session_date": session_date,
                    "test": "20m_sprint",
                    "raw_value": float(r["best_split_20m_s"]),
                    "unit": "s",
                })

    cod = _safe_read_csv(PROCESSED / "cod_sessions.csv")
    if not cod.empty:
        cod = cod[cod["test_type"].astype(str).str.lower() == "pro_agility"].copy()
        cod["best_total_time_s"] = pd.to_numeric(cod["best_total_time_s"], errors="coerce")
        cod = cod.dropna(subset=["best_total_time_s"])
        if not cod.empty:
            idx = cod.groupby(["athlete", "date"])["best_total_time_s"].idxmin()
            for _, r in cod.loc[idx].iterrows():
                rows.append({
                    "athlete": r["athlete"],
                    "session_date": r["date"],
                    "test": "pro_agility_5_10_5",
                    "raw_value": float(r["best_total_time_s"]),
                    "unit": "s",
                })

    jump = _safe_read_csv(PROCESSED / "jump_sessions.csv")
    if not jump.empty:
        for _, r in jump.iterrows():
            test_type = str(r["test_type"]).upper()
            athlete = r["athlete"]
            session_date = r["date"]

            if test_type == "CMJ" and pd.notna(r.get("best_jump_height_cm")):
                rows.append({
                    "athlete": athlete,
                    "session_date": session_date,
                    "test": "cmj",
                    "raw_value": float(r["best_jump_height_cm"]),
                    "unit": "cm",
                })

            if test_type == "DJ" and pd.notna(r.get("best_rsi")):
                rows.append({
                    "athlete": athlete,
                    "session_date": session_date,
                    "test": "rsi",
                    "raw_value": float(r["best_rsi"]),
                    "unit": "ratio",
                })

    horizontal = _safe_read_csv(PROCESSED / "horizontal_sessions.csv")
    if not horizontal.empty:
        slj = horizontal[horizontal["test_type"].astype(str).str.lower() == "standing_long_jump"].copy()
        for _, r in slj.iterrows():
            if pd.notna(r.get("best_distance_cm")):
                rows.append({
                    "athlete": r["athlete"],
                    "session_date": r["date"],
                    "test": "standing_long_jump",
                    "raw_value": round(float(r["best_distance_cm"]) / 100.0, 4),
                    "unit": "m",
                })

    throw = _safe_read_csv(PROCESSED / "throw_sessions.csv")
    if not throw.empty:
        throw = throw[throw["test_type"].astype(str).str.lower() == "medicine_ball_throw_2kg"].copy()
        for _, r in throw.iterrows():
            if pd.notna(r.get("best_distance_m")):
                rows.append({
                    "athlete": r["athlete"],
                    "session_date": r["date"],
                    "test": "medicine_ball_throw_2kg",
                    "raw_value": float(r["best_distance_m"]),
                    "unit": "m",
                })

    return pd.DataFrame(rows)


def calculate_test_scores(test_results: pd.DataFrame, benchmarks: pd.DataFrame) -> pd.DataFrame:
    benchmark_map: Dict[str, pd.Series] = {row["test"]: row for _, row in benchmarks.iterrows()}

    out_rows = []
    for _, row in test_results.iterrows():
        test = row["test"]
        if test not in benchmark_map or test not in TEST_CONFIG:
            continue

        b = benchmark_map[test]
        direction = TEST_CONFIG[test]["direction"]

        score = interpolate_score(
            value=float(row["raw_value"]),
            g=float(b["general_youth_p50"]),
            a=float(b["youth_athlete_p50"]),
            e=float(b["elite_u18_p50"]),
            w=float(b["world_elite_p50"]),
            direction=direction,
        )

        out_rows.append({
            "athlete": row["athlete"],
            "session_date": row["session_date"],
            "test": test,
            "raw_value": row["raw_value"],
            "unit": row["unit"],
            "score": round(score, 2),
            "score_band": score_band(score),
            "domain": TEST_CONFIG[test]["domain"],
            "gap_to_next_level": next_level_gap(float(row["raw_value"]), b, direction),
        })

    return pd.DataFrame(out_rows)


def calculate_domain_scores(test_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (athlete, session_date), group in test_scores.groupby(["athlete", "session_date"]):
        score_map = {r["test"]: float(r["score"]) for _, r in group.iterrows()}

        acceleration = score_map.get("10m_sprint", 0.0) * 0.6 + score_map.get("20m_sprint", 0.0) * 0.4
        cod = score_map.get("pro_agility_5_10_5", 0.0)
        explosive = score_map.get("cmj", 0.0) * 0.6 + score_map.get("standing_long_jump", 0.0) * 0.4
        reactive = score_map.get("rsi", 0.0)
        upper = score_map.get("medicine_ball_throw_2kg")

        rows.append({
            "athlete": athlete,
            "session_date": session_date,
            "acceleration_score": round(acceleration, 2),
            "cod_score": round(cod, 2),
            "reactive_strength_score": round(reactive, 2),
            "explosive_power_score": round(explosive, 2),
            "upper_body_power_score": round(upper, 2) if upper is not None else None,
        })

    return pd.DataFrame(rows)


def calculate_rugby_physical_score(domain_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in domain_scores.iterrows():
        domains = {
            "acceleration": row["acceleration_score"],
            "cod": row["cod_score"],
            "reactive_strength": row["reactive_strength_score"],
            "explosive_power": row["explosive_power_score"],
            "upper_body_power": row["upper_body_power_score"],
        }

        available_domains = {
            name: float(score)
            for name, score in domains.items()
            if pd.notna(score)
        }

        available_weights = {
            name: DOMAIN_WEIGHTS[name]
            for name in available_domains.keys()
            if name in DOMAIN_WEIGHTS
        }

        weight_sum = sum(available_weights.values())
        if weight_sum == 0:
            total = 0.0
        else:
            total = sum(
                available_domains[name] * (available_weights[name] / weight_sum)
                for name in available_domains.keys()
            )

        weakest_sorted = sorted(
            (
                (name, score - PRIORITY_BONUS.get(name, 0.0))
                for name, score in available_domains.items()
            ),
            key=lambda x: x[1]
        )

        strongest = max(available_domains.items(), key=lambda x: x[1])[0]
        weakest = min(available_domains.items(), key=lambda x: x[1])[0]

        rows.append({
            "athlete": row["athlete"],
            "session_date": row["session_date"],
            "rugby_physical_score": round(total, 2),
            "score_band": score_band(total),
            "strongest_domain": strongest,
            "weakest_domain": weakest,
            "priority_1": weakest_sorted[0][0],
            "priority_2": weakest_sorted[1][0] if len(weakest_sorted) > 1 else weakest_sorted[0][0],
        })
    return pd.DataFrame(rows)


def main() -> None:
    ensure_dirs()
    benchmarks = load_benchmarks()
    test_results = extract_test_results_from_processed()

    if test_results.empty:
        raise ValueError("No test results extracted from processed files.")

    test_scores = calculate_test_scores(test_results, benchmarks)
    domain_scores = calculate_domain_scores(test_scores)
    rugby_score = calculate_rugby_physical_score(domain_scores)

    test_scores.to_csv(ANALYSIS / "test_scores.csv", index=False)
    domain_scores.to_csv(ANALYSIS / "domain_scores.csv", index=False)
    rugby_score.to_csv(ANALYSIS / "rugby_physical_score.csv", index=False)

    print("Created:")
    print(f"- {ANALYSIS / 'test_scores.csv'}")
    print(f"- {ANALYSIS / 'domain_scores.csv'}")
    print(f"- {ANALYSIS / 'rugby_physical_score.csv'}")


if __name__ == "__main__":
    main()
