from pathlib import Path
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.rcParams["font.family"] = "Noto Sans JP"
matplotlib.rcParams["axes.unicode_minus"] = False

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
OUTPUT_PATH = OUTPUT_DIR / "radar_chart.png"


DOMAIN_COLUMNS = [
    ("acceleration_score", "acceleration"),
    ("cod_score", "cod"),
    ("reactive_strength_score", "reactive_strength"),
    ("explosive_power_score", "explosive_power"),
    ("upper_body_power_score", "upper_body_power"),
]


def latest_rows_session(df: pd.DataFrame, date_col: str = "session_date") -> pd.DataFrame:
    if df.empty or date_col not in df.columns:
        return df
    latest_date = df[date_col].dropna().astype(str).max()
    return df[df[date_col].astype(str) == latest_date].copy()


def main():
    labels = load_labels()
    domain_path = ANALYSIS_DIR / "domain_scores.csv"
    if not domain_path.exists():
        raise FileNotFoundError(domain_path)

    df = pd.read_csv(domain_path)
    df = latest_rows_session(df)
    if df.empty:
        raise ValueError("No domain score rows found.")

    row = df.iloc[0]

    domain_keys = [d for _, d in DOMAIN_COLUMNS]
    values = []
    display_labels = []
    for col, domain_key in DOMAIN_COLUMNS:
        value = row.get(col, float("nan"))
        if pd.isna(value):
            value = 0.0
        values.append(float(value))
        display_labels.append(map_value(domain_key, labels))

    n = len(display_labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    display_labels += display_labels[:1]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(display_labels[:-1], fontsize=12)

    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=10)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    title = f"{labels.get('rugby_physical_score', 'Rugby Physical Score')} Radar"
    session_date = row.get("session_date", "")
    if session_date:
        title += f" ({session_date})"
    ax.set_title(title, pad=20, fontsize=14)

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
