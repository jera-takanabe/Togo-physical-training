#!/usr/bin/env python3
"""
generate_growth_trend_chart.py

Purpose:
- Read analysis outputs
- Create trend charts for rugby physical score and domain scores
- Save charts to docs/dashboards/

Inputs:
- data/analysis/rugby_physical_score.csv
- data/analysis/domain_scores.csv

Outputs:
- docs/dashboards/rugby_physical_score_trend.png
- docs/dashboards/domain_scores_trend.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
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
OUTPUT_DIR = BASE_DIR / "docs" / "dashboards"

RUGBY_SCORE_PATH = ANALYSIS_DIR / "rugby_physical_score.csv"
DOMAIN_SCORES_PATH = ANALYSIS_DIR / "domain_scores.csv"

RUGBY_SCORE_OUT = OUTPUT_DIR / "rugby_physical_score_trend.png"
DOMAIN_SCORES_OUT = OUTPUT_DIR / "domain_scores_trend.png"

for font_name in ["Noto Sans JP", "Yu Gothic", "Meiryo", "MS Gothic"]:
    try:
        matplotlib.rcParams["font.family"] = font_name
        break
    except Exception:
        pass
matplotlib.rcParams["axes.unicode_minus"] = False


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def prepare_time_series(df: pd.DataFrame, date_col: str = "session_date") -> pd.DataFrame:
    if date_col not in df.columns:
        raise ValueError(f"Missing required column: {date_col}")

    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    out = out.dropna(subset=[date_col]).sort_values(date_col)
    return out


def plot_rugby_score_trend(df: pd.DataFrame, labels: dict[str, str]) -> None:
    title = labels.get("rugby_physical_score", "Rugby Physical Score")
    y_label = labels.get("score", "Score")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["session_date"], df["rugby_physical_score"], marker="o", linewidth=2)
    ax.set_title(f"{title} Trend")
    ax.set_xlabel(labels.get("session_date", "Session Date"))
    ax.set_ylabel(y_label)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    for x, y in zip(df["session_date"], df["rugby_physical_score"]):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(RUGBY_SCORE_OUT, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_domain_scores_trend(df: pd.DataFrame, labels: dict[str, str]) -> None:
    domain_cols = [
        ("acceleration_score", "acceleration"),
        ("cod_score", "cod"),
        ("reactive_strength_score", "reactive_strength"),
        ("explosive_power_score", "explosive_power"),
        ("upper_body_power_score", "upper_body_power"),
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    plotted_any = False

    for col, key in domain_cols:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce")
        if series.notna().sum() == 0:
            continue

        ax.plot(
            df["session_date"],
            series,
            marker="o",
            linewidth=2,
            label=map_value(key, labels),
        )
        plotted_any = True

    if not plotted_any:
        raise ValueError("No plottable domain score columns found.")

    ax.set_title(f"{labels.get('domain_scores', 'Domain Scores')} Trend")
    ax.set_xlabel(labels.get("session_date", "Session Date"))
    ax.set_ylabel(labels.get("score", "Score"))
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(DOMAIN_SCORES_OUT, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    labels = load_labels()

    rugby_df = prepare_time_series(read_csv(RUGBY_SCORE_PATH))
    domain_df = prepare_time_series(read_csv(DOMAIN_SCORES_PATH))

    plot_rugby_score_trend(rugby_df, labels)
    plot_domain_scores_trend(domain_df, labels)

    print(f"Created: {RUGBY_SCORE_OUT}")
    print(f"Created: {DOMAIN_SCORES_OUT}")


if __name__ == "__main__":
    main()
