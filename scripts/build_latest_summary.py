from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
ANALYSIS_DIR = BASE_DIR / "data" / "analysis"
OUTPUT_PATH = BASE_DIR / "docs" / "dashboards" / "latest_summary.md"


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


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_float_dtype(out[col]):
            out[col] = out[col].map(lambda x: "-" if pd.isna(x) else f"{x:.2f}")
        else:
            out[col] = out[col].map(dash)
    return out


def _escape_md(value) -> str:
    text = str(value)
    text = text.replace("\n", " ")
    return text


def to_md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data_\n"

    df = format_df(df)
    headers = [_escape_md(c) for c in df.columns]
    rows = [[_escape_md(v) for v in row] for row in df.astype(str).values.tolist()]

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def build_summary() -> str:
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
    lines.append("# Latest Summary")
    lines.append("")
    lines.append(f"- Latest Test Date: **{latest_date}**")
    lines.append("")

    if not rugby_score.empty:
        row = rugby_score.iloc[0]
        lines.append("## Rugby Physical Score")
        lines.append("")
        lines.append(f"- Score: **{row['rugby_physical_score']:.2f}**")
        lines.append(f"- Band: **{row['score_band']}**")
        lines.append(f"- Strongest Domain: **{row['strongest_domain']}**")
        lines.append(f"- Weakest Domain: **{row['weakest_domain']}**")
        lines.append(f"- Priority 1: **{row['priority_1']}**")
        lines.append(f"- Priority 2: **{row['priority_2']}**")
        lines.append("")

    if not domain_scores.empty:
        ds = domain_scores.copy()
        preferred = [
            "athlete",
            "session_date",
            "acceleration_score",
            "cod_score",
            "reactive_strength_score",
            "explosive_power_score",
            "upper_body_power_score",
        ]
        existing = [c for c in preferred if c in ds.columns]
        lines.append("## Domain Scores")
        lines.append("")
        lines.append(to_md_table(ds[existing]))
        lines.append("")

    if not test_scores.empty:
        ts = test_scores.copy()
        preferred = [
            "athlete",
            "session_date",
            "test",
            "raw_value",
            "unit",
            "score",
            "score_band",
            "domain",
            "gap_to_next_level",
        ]
        existing = [c for c in preferred if c in ts.columns]
        lines.append("## Test Scores")
        lines.append("")
        lines.append(to_md_table(ts[existing]))
        lines.append("")

    lines.append("## Sprint Sessions")
    lines.append("")
    if not sprint.empty:
        preferred = [
            "test_type",
            "trials",
            "best_split_5m_s",
            "best_split_10m_s",
            "best_split_20m_s",
            "best_split_30m_s",
            "best_fly_5m_s",
            "best_fly_10m_s",
            "best_total_time_s",
            "quality_flag",
        ]
        existing = [c for c in preferred if c in sprint.columns]
        lines.append(to_md_table(sprint[existing]))
    else:
        lines.append("_No data_\n")

    lines.append("## COD Sessions")
    lines.append("")
    if not cod.empty:
        preferred = [
            "test_type",
            "side",
            "trials",
            "best_segment_1_s",
            "best_segment_2_s",
            "best_segment_3_s",
            "best_total_time_s",
            "quality_flag",
        ]
        existing = [c for c in preferred if c in cod.columns]
        lines.append(to_md_table(cod[existing]))
    else:
        lines.append("_No data_\n")

    lines.append("## Jump Sessions")
    lines.append("")
    if not jump.empty:
        preferred = [
            "test_type",
            "trials",
            "best_jump_height_cm",
            "avg_jump_height_cm",
            "std_jump_height_cm",
            "best_contact_time_ms",
            "best_flight_time_ms",
            "best_rsi",
            "quality_flag",
        ]
        existing = [c for c in preferred if c in jump.columns]
        lines.append(to_md_table(jump[existing]))
    else:
        lines.append("_No data_\n")

    lines.append("## Horizontal Sessions")
    lines.append("")
    if not horizontal.empty:
        preferred = [
            "test_type",
            "side",
            "trials",
            "best_distance_cm",
            "avg_distance_cm",
            "std_distance_cm",
            "quality_flag",
        ]
        existing = [c for c in preferred if c in horizontal.columns]
        lines.append(to_md_table(horizontal[existing]))
    else:
        lines.append("_No data_\n")

    lines.append("## Throw Sessions")
    lines.append("")
    if not throw.empty:
        preferred = [
            "test_type",
            "trials",
            "best_distance_m",
            "avg_distance_m",
            "std_distance_m",
            "quality_flag",
        ]
        existing = [c for c in preferred if c in throw.columns]
        lines.append(to_md_table(throw[existing]))
    else:
        lines.append("_No data_\n")

    if not pb.empty:
        lines.append("## Personal Bests")
        lines.append("")
        lines.append(to_md_table(pb))

    return "\n".join(lines).rstrip() + "\n"


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = build_summary()
    OUTPUT_PATH.write_text(summary, encoding="utf-8")
    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
