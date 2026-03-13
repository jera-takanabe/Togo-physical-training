from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

JUMPS_SESSION = BASE_DIR / "data" / "processed" / "jumps_session.csv"
SPRINTS_SESSION = BASE_DIR / "data" / "processed" / "sprints_session.csv"
PERSONAL_BESTS = BASE_DIR / "data" / "processed" / "personal_bests.csv"


def build_jump_pbs():
    if not JUMPS_SESSION.exists():
        return []

    df = pd.read_csv(JUMPS_SESSION)
    rows = []

    jump_metrics = [
        ("best_jump_height_cm", "cm", "max"),
        ("best_contact_time_ms", "ms", "min"),
        ("best_flight_time_ms", "ms", "max"),
        ("best_rsi", "", "max"),
    ]

    for _, row in df.iterrows():
        for metric_name, unit, rule in jump_metrics:
            value = row.get(metric_name)
            if pd.notna(value):
                rows.append({
                    "athlete": row["athlete"],
                    "test_type": row["test_type"],
                    "metric_name": metric_name,
                    "value": value,
                    "unit": unit,
                    "date": row["date"],
                    "session_id": row["session_id"],
                    "rule": rule,
                })

    if not rows:
        return []

    metric_df = pd.DataFrame(rows)
    pb_rows = []

    for (athlete, test_type, metric_name, unit, rule), group in metric_df.groupby(
        ["athlete", "test_type", "metric_name", "unit", "rule"], dropna=False
    ):
        if rule == "max":
            best_idx = group["value"].idxmax()
        else:
            best_idx = group["value"].idxmin()

        best_row = group.loc[best_idx]
        pb_rows.append({
            "athlete": athlete,
            "test_type": test_type,
            "metric_name": metric_name,
            "best_value": best_row["value"],
            "unit": unit,
            "date": best_row["date"],
            "session_id": best_row["session_id"],
        })

    return pb_rows


def build_sprint_pbs():
    if not SPRINTS_SESSION.exists():
        return []

    df = pd.read_csv(SPRINTS_SESSION)
    rows = []

    sprint_metrics = [
        ("best_5m_s", "s", "min"),
        ("best_10m_s", "s", "min"),
        ("best_20m_s", "s", "min"),
        ("best_30m_s", "s", "min"),
        ("best_total_time_s", "s", "min"),
    ]

    for _, row in df.iterrows():
        for metric_name, unit, rule in sprint_metrics:
            value = row.get(metric_name)
            if pd.notna(value):
                rows.append({
                    "athlete": row["athlete"],
                    "test_type": row["test_type"],
                    "metric_name": metric_name,
                    "value": value,
                    "unit": unit,
                    "date": row["date"],
                    "session_id": row["session_id"],
                    "rule": rule,
                })

    if not rows:
        return []

    metric_df = pd.DataFrame(rows)
    pb_rows = []

    for (athlete, test_type, metric_name, unit, rule), group in metric_df.groupby(
        ["athlete", "test_type", "metric_name", "unit", "rule"], dropna=False
    ):
        best_idx = group["value"].idxmin()
        best_row = group.loc[best_idx]
        pb_rows.append({
            "athlete": athlete,
            "test_type": test_type,
            "metric_name": metric_name,
            "best_value": best_row["value"],
            "unit": unit,
            "date": best_row["date"],
            "session_id": best_row["session_id"],
        })

    return pb_rows


def main():
    pb_rows = []
    pb_rows.extend(build_jump_pbs())
    pb_rows.extend(build_sprint_pbs())

    if not pb_rows:
        print("No PB data created")
        return

    out_df = pd.DataFrame(pb_rows)
    out_df = out_df.sort_values(["athlete", "test_type", "metric_name"]).reset_index(drop=True)

    PERSONAL_BESTS.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(PERSONAL_BESTS, index=False)
    print(f"Created: {PERSONAL_BESTS}")


if __name__ == "__main__":
    main()