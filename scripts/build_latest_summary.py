from pathlib import Path

import pandas as pd

from utils.i18n import load_labels, map_value, translate_column


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
ANALYSIS_DIR = BASE_DIR / "data" / "analysis"
OUTPUT_PATH = BASE_DIR / "docs" / "dashboards" / "latest_summary.md"
TARGET_GAP_PATH = BASE_DIR / "docs" / "dashboards" / "target_gap_summary.md"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def latest_rows(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    if df.empty or date_col not in df.columns:
        return df
    latest_date = df[date_col].dropna().astype(str).max()
    return df[df[date_col].astype(str) == latest_date].copy()


def latest_rows_session(df: pd.DataFrame, date_col: str = "session_date") -> pd.DataFrame:
    if df.empty or date_col not in df.columns:
        return df
    latest_date = df[date_col].dropna().astype(str).max()
    return df[df[date_col].astype(str) == latest_date].copy()


def dash(v):
    if pd.isna(v):
        return "-"
    return v


def format_df(df: pd.DataFrame, labels: dict[str, str]) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()

    for col in out.columns:
        if pd.api.types.is_float_dtype(out[col]):
            out[col] = out[col].map(lambda x: "-" if pd.isna(x) else f"{x:.2f}")
        else:
            out[col] = out[col].map(dash)

    for col in out.columns:
        if col in {"domain", "strongest_domain", "weakest_domain", "priority_1", "priority_2", "score_band"}:
            out[col] = out[col].map(lambda x: map_value(x, labels) if x != "-" else x)

    out.columns = [translate_column(c, labels) for c in out.columns]
    return out


def _escape_md(value) -> str:
    return str(value).replace("\n", " ")


def to_md_table(df: pd.DataFrame, labels: dict[str, str]) -> str:
    if df.empty:
        return f"{labels.get('no_data', '_No data_')}\n"

    df = format_df(df, labels)
    headers = [_escape_md(c) for c in df.columns]
    rows = [[_escape_md(v) for v in row] for row in df.astype(str).values.tolist()]

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def read_target_gap_summary() -> str:
    if not TARGET_GAP_PATH.exists():
        return ""
    text = TARGET_GAP_PATH.read_text(encoding="utf-8").strip()
    if not text:
        return ""
    return text + "\n\n"


def build_summary() -> str:
    labels = load_labels()

    sprint = latest_rows(read_csv(PROCESSED_DIR / "sprint_sessions.csv"))
    cod = latest_rows(read_csv(PROCESSED_DIR / "cod_sessions.csv"))
    jump = latest_rows(read_csv(PROCESSED_DIR / "jump_sessions.csv"))
    horizontal = latest_rows(read_csv(PROCESSED_DIR / "horizontal_sessions.csv"))
    throw = latest_rows(read_csv(PROCESSED_DIR / "throw_sessions.csv"))
    pb = read_csv(PROCESSED_DIR / "personal_bests.csv")

    test_scores = latest_rows_session(read_csv(ANALYSIS_DIR / "test_scores.csv"))
    domain_scores = latest_rows_session(read_csv(ANALYSIS_DIR / "domain_scores.csv"))
    rugby_score = latest_rows_session(read_csv(ANALYSIS_DIR / "rugby_physical_score.csv"))

    latest_dates = []
    for df, col in [
        (sprint, "date"),
        (cod, "date"),
        (jump, "date"),
        (horizontal, "date"),
        (throw, "date"),
        (test_scores, "session_date"),
        (domain_scores, "session_date"),
        (rugby_score, "session_date"),
    ]:
        if not df.empty and col in df.columns:
            latest_dates.extend(df[col].dropna().astype(str).tolist())

    latest_date = max(latest_dates) if latest_dates else "-"

    lines = []
    lines.append(f"# {labels.get('latest_summary', 'Latest Summary')}")
    lines.append("")
    lines.append(f"- {labels.get('latest_test_date', 'Latest Test Date')}: **{latest_date}**")
    lines.append("")
    lines.append("![Radar Chart](radar_chart.png)")
    lines.append("")
    lines.append("![Target Radar v2](target_radar_v2.png)")
    lines.append("")
    lines.append("![Rugby Physical Score Trend](rugby_physical_score_trend.png)")
    lines.append("")
    lines.append("![Domain Scores Trend](domain_scores_trend.png)")
    lines.append("")

    gap_text = read_target_gap_summary()
    if gap_text:
        lines.append(gap_text.rstrip())
        lines.append("")

    if not rugby_score.empty:
        row = rugby_score.iloc[0]
        lines.append(f"## {labels.get('rugby_physical_score', 'Rugby Physical Score')}")
        lines.append("")
        lines.append(f"- {labels.get('score', 'Score')}: **{row['rugby_physical_score']:.2f}**")
        lines.append(f"- {labels.get('band', 'Band')}: **{map_value(row['score_band'], labels)}**")
        lines.append(f"- {labels.get('strongest_domain', 'Strongest Domain')}: **{map_value(row['strongest_domain'], labels)}**")
        lines.append(f"- {labels.get('weakest_domain', 'Weakest Domain')}: **{map_value(row['weakest_domain'], labels)}**")
        lines.append(f"- {labels.get('priority_1', 'Priority 1')}: **{map_value(row['priority_1'], labels)}**")
        lines.append(f"- {labels.get('priority_2', 'Priority 2')}: **{map_value(row['priority_2'], labels)}**")
        lines.append("")

    if not domain_scores.empty:
        preferred = [
            "athlete", "session_date", "acceleration_score", "cod_score",
            "reactive_strength_score", "explosive_power_score", "upper_body_power_score",
        ]
        existing = [c for c in preferred if c in domain_scores.columns]
        lines.append(f"## {labels.get('domain_scores', 'Domain Scores')}")
        lines.append("")
        lines.append(to_md_table(domain_scores[existing], labels))
        lines.append("")

    if not test_scores.empty:
        preferred = [
            "athlete", "session_date", "test", "raw_value", "unit",
            "score", "score_band", "domain", "gap_to_next_level",
        ]
        existing = [c for c in preferred if c in test_scores.columns]
        lines.append(f"## {labels.get('test_scores', 'Test Scores')}")
        lines.append("")
        lines.append(to_md_table(test_scores[existing], labels))
        lines.append("")

    section_map = [
        ("sprint_sessions", sprint, ["test_type", "trials", "best_split_5m_s", "best_split_10m_s", "best_split_20m_s", "best_split_30m_s", "best_fly_5m_s", "best_fly_10m_s", "best_total_time_s", "quality_flag"]),
        ("cod_sessions", cod, ["test_type", "side", "trials", "best_segment_1_s", "best_segment_2_s", "best_segment_3_s", "best_total_time_s", "quality_flag"]),
        ("jump_sessions", jump, ["test_type", "trials", "best_jump_height_cm", "avg_jump_height_cm", "std_jump_height_cm", "best_contact_time_ms", "best_flight_time_ms", "best_rsi", "quality_flag"]),
        ("horizontal_sessions", horizontal, ["test_type", "side", "trials", "best_distance_cm", "avg_distance_cm", "std_distance_cm", "quality_flag"]),
        ("throw_sessions", throw, ["test_type", "trials", "best_distance_m", "avg_distance_m", "std_distance_m", "quality_flag"]),
        ("personal_bests", pb, list(pb.columns)),
    ]

    for section_key, df, preferred in section_map:
        lines.append(f"## {labels.get(section_key, section_key)}")
        lines.append("")
        if not df.empty:
            existing = [c for c in preferred if c in df.columns]
            lines.append(to_md_table(df[existing], labels))
        else:
            lines.append(f"{labels.get('no_data', '_No data_')}\n")

    return "\n".join(lines).rstrip() + "\n"


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = build_summary()
    OUTPUT_PATH.write_text(summary, encoding="utf-8")
    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
