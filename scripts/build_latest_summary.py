from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs" / "dashboards"

SPRINT_SESSION = PROCESSED_DIR / "sprint_sessions.csv"
COD_SESSION = PROCESSED_DIR / "cod_sessions.csv"
JUMP_SESSION = PROCESSED_DIR / "jump_sessions.csv"
HORIZONTAL_SESSION = PROCESSED_DIR / "horizontal_sessions.csv"
THROW_SESSION = PROCESSED_DIR / "throw_sessions.csv"
PERSONAL_BESTS = PROCESSED_DIR / "personal_bests.csv"

LATEST_SUMMARY = DOCS_DIR / "latest_summary.md"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def latest_date_from_frames(*frames: pd.DataFrame):
    dates = []
    for df in frames:
        if not df.empty and "date" in df.columns:
            dates.extend(df["date"].dropna().astype(str).tolist())
    if not dates:
        return None
    return max(dates)


def format_value(value, digits=2):
    if pd.isna(value):
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def add_table(lines: list[str], title: str, df: pd.DataFrame, columns: list[str]):
    if df.empty:
        return

    lines.append(f"## {title}")
    lines.append("")
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("|" + "|".join(["---"] * len(columns)) + "|")

    for _, row in df.iterrows():
        values = [format_value(row.get(col)) for col in columns]
        lines.append("| " + " | ".join(values) + " |")

    lines.append("")


def build_summary():
    sprint_df = load_csv(SPRINT_SESSION)
    cod_df = load_csv(COD_SESSION)
    jump_df = load_csv(JUMP_SESSION)
    horizontal_df = load_csv(HORIZONTAL_SESSION)
    throw_df = load_csv(THROW_SESSION)
    pbs_df = load_csv(PERSONAL_BESTS)

    latest_date = latest_date_from_frames(
        sprint_df, cod_df, jump_df, horizontal_df, throw_df
    )

    if latest_date is None:
        content = "# Latest Summary\n\nデータがありません。\n"
    else:
        lines = []
        lines.append("# Latest Summary")
        lines.append("")
        lines.append(f"- Latest Test Date: **{latest_date}**")
        lines.append("")

        latest_sprint = sprint_df[sprint_df["date"] == latest_date].copy() if not sprint_df.empty else pd.DataFrame()
        latest_cod = cod_df[cod_df["date"] == latest_date].copy() if not cod_df.empty else pd.DataFrame()
        latest_jump = jump_df[jump_df["date"] == latest_date].copy() if not jump_df.empty else pd.DataFrame()
        latest_horizontal = horizontal_df[horizontal_df["date"] == latest_date].copy() if not horizontal_df.empty else pd.DataFrame()
        latest_throw = throw_df[throw_df["date"] == latest_date].copy() if not throw_df.empty else pd.DataFrame()

        if not latest_sprint.empty:
            latest_sprint = latest_sprint.sort_values(["athlete", "test_type"])
            add_table(
                lines,
                "Sprint Sessions",
                latest_sprint,
                [
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
                ],
            )

        if not latest_cod.empty:
            latest_cod = latest_cod.sort_values(["athlete", "test_type", "side"])
            add_table(
                lines,
                "COD Sessions",
                latest_cod,
                [
                    "test_type",
                    "side",
                    "trials",
                    "best_segment_1_s",
                    "best_segment_2_s",
                    "best_segment_3_s",
                    "best_total_time_s",
                    "quality_flag",
                ],
            )

        if not latest_jump.empty:
            latest_jump = latest_jump.sort_values(["athlete", "test_type"])
            add_table(
                lines,
                "Jump Sessions",
                latest_jump,
                [
                    "test_type",
                    "trials",
                    "best_jump_height_cm",
                    "avg_jump_height_cm",
                    "std_jump_height_cm",
                    "best_contact_time_ms",
                    "best_flight_time_ms",
                    "best_rsi",
                    "quality_flag",
                ],
            )

        if not latest_horizontal.empty:
            latest_horizontal = latest_horizontal.sort_values(["athlete", "test_type", "side"])
            add_table(
                lines,
                "Horizontal Sessions",
                latest_horizontal,
                [
                    "test_type",
                    "side",
                    "trials",
                    "best_distance_cm",
                    "avg_distance_cm",
                    "std_distance_cm",
                    "quality_flag",
                ],
            )

        if not latest_throw.empty:
            latest_throw = latest_throw.sort_values(["athlete", "test_type"])
            add_table(
                lines,
                "Throw Sessions",
                latest_throw,
                [
                    "test_type",
                    "trials",
                    "best_distance_m",
                    "avg_distance_m",
                    "std_distance_m",
                    "quality_flag",
                ],
            )

        if not pbs_df.empty:
            pbs_df = pbs_df.sort_values(["test_type", "metric_name", "side"], na_position="last")
            add_table(
                lines,
                "Current Personal Bests",
                pbs_df,
                [
                    "test_type",
                    "side",
                    "metric_name",
                    "best_value",
                    "unit",
                    "date",
                ],
            )

        content = "\n".join(lines) + "\n"

    LATEST_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    LATEST_SUMMARY.write_text(content, encoding="utf-8")
    print(f"Created: {LATEST_SUMMARY}")


if __name__ == "__main__":
    build_summary()