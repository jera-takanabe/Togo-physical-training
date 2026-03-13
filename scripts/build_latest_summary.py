from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

JUMPS_SESSION = BASE_DIR / "data" / "processed" / "jumps_session.csv"
SPRINTS_SESSION = BASE_DIR / "data" / "processed" / "sprints_session.csv"
PERSONAL_BESTS = BASE_DIR / "data" / "processed" / "personal_bests.csv"

LATEST_SUMMARY = BASE_DIR / "docs" / "dashboards" / "latest_summary.md"


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


def build_summary():
    jumps_df = load_csv(JUMPS_SESSION)
    sprints_df = load_csv(SPRINTS_SESSION)
    pbs_df = load_csv(PERSONAL_BESTS)

    latest_date = latest_date_from_frames(jumps_df, sprints_df)
    if latest_date is None:
        content = "# Latest Summary\n\nデータがありません。\n"
    else:
        latest_jumps = jumps_df[jumps_df["date"] == latest_date].copy() if not jumps_df.empty else pd.DataFrame()
        latest_sprints = sprints_df[sprints_df["date"] == latest_date].copy() if not sprints_df.empty else pd.DataFrame()

        lines = []
        lines.append("# Latest Summary")
        lines.append("")
        lines.append(f"- Latest Test Date: **{latest_date}**")
        lines.append("")

        if not latest_jumps.empty:
            lines.append("## Jump Sessions")
            lines.append("")
            lines.append("| test_type | trials | best_jump_height_cm | avg_jump_height_cm | best_rsi | quality_flag |")
            lines.append("|---|---:|---:|---:|---:|---|")
            for _, row in latest_jumps.sort_values(["athlete", "test_type"]).iterrows():
                lines.append(
                    f"| {row['test_type']} | {format_value(row['trials'], 0)} | "
                    f"{format_value(row.get('best_jump_height_cm'))} | "
                    f"{format_value(row.get('avg_jump_height_cm'))} | "
                    f"{format_value(row.get('best_rsi'))} | "
                    f"{format_value(row.get('quality_flag'), 0)} |"
                )
            lines.append("")

        if not latest_sprints.empty:
            lines.append("## Sprint Sessions")
            lines.append("")
            lines.append("| test_type | trials | best_10m_s | best_20m_s | best_30m_s | best_total_time_s | quality_flag |")
            lines.append("|---|---:|---:|---:|---:|---:|---|")
            for _, row in latest_sprints.sort_values(["athlete", "test_type"]).iterrows():
                lines.append(
                    f"| {row['test_type']} | {format_value(row['trials'], 0)} | "
                    f"{format_value(row.get('best_10m_s'))} | "
                    f"{format_value(row.get('best_20m_s'))} | "
                    f"{format_value(row.get('best_30m_s'))} | "
                    f"{format_value(row.get('best_total_time_s'))} | "
                    f"{format_value(row.get('quality_flag'), 0)} |"
                )
            lines.append("")

        if not pbs_df.empty:
            lines.append("## Current Personal Bests")
            lines.append("")
            lines.append("| test_type | metric_name | best_value | unit | date |")
            lines.append("|---|---|---:|---|---|")
            for _, row in pbs_df.sort_values(["test_type", "metric_name"]).iterrows():
                lines.append(
                    f"| {row['test_type']} | {row['metric_name']} | "
                    f"{format_value(row['best_value'])} | {row['unit']} | {row['date']} |"
                )
            lines.append("")

        content = "\n".join(lines) + "\n"

    LATEST_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    LATEST_SUMMARY.write_text(content, encoding="utf-8")
    print(f"Created: {LATEST_SUMMARY}")


if __name__ == "__main__":
    build_summary()