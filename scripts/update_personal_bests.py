from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

SPRINT_SESSION = PROCESSED_DIR / "sprint_sessions.csv"
COD_SESSION = PROCESSED_DIR / "cod_sessions.csv"
JUMP_SESSION = PROCESSED_DIR / "jump_sessions.csv"
HORIZONTAL_SESSION = PROCESSED_DIR / "horizontal_sessions.csv"
THROW_SESSION = PROCESSED_DIR / "throw_sessions.csv"

PERSONAL_BESTS = PROCESSED_DIR / "personal_bests.csv"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def add_pb_candidates(df: pd.DataFrame, metrics: list[tuple[str, str, str]], rows: list[dict], include_side: bool = False):
    """
    metrics: [(column_name, unit, rule)]
    rule: 'max' or 'min'
    """
    if df.empty:
        return

    for _, row in df.iterrows():
        for metric_name, unit, rule in metrics:
            value = row.get(metric_name)
            if pd.notna(value):
                pb_row = {
                    "athlete": row.get("athlete"),
                    "test_type": row.get("test_type"),
                    "metric_name": metric_name,
                    "best_value": value,
                    "unit": unit,
                    "date": row.get("date"),
                    "session_id": row.get("session_id"),
                    "rule": rule,
                }
                if include_side:
                    pb_row["side"] = row.get("side")
                else:
                    pb_row["side"] = None
                rows.append(pb_row)


def select_best_rows(candidate_df: pd.DataFrame) -> pd.DataFrame:
    if candidate_df.empty:
        return pd.DataFrame()

    pb_rows = []

    group_cols = ["athlete", "test_type", "metric_name", "unit", "rule", "side"]

    for keys, group in candidate_df.groupby(group_cols, dropna=False):
        rule = keys[4]
        if rule == "max":
            best_idx = group["best_value"].idxmax()
        else:
            best_idx = group["best_value"].idxmin()

        best_row = group.loc[best_idx]
        pb_rows.append({
            "athlete": best_row["athlete"],
            "test_type": best_row["test_type"],
            "metric_name": best_row["metric_name"],
            "best_value": best_row["best_value"],
            "unit": best_row["unit"],
            "date": best_row["date"],
            "session_id": best_row["session_id"],
            "side": best_row["side"],
        })

    out_df = pd.DataFrame(pb_rows)
    return out_df.sort_values(["athlete", "test_type", "metric_name", "side"], na_position="last").reset_index(drop=True)


def main():
    candidate_rows = []

    # Sprint
    sprint_df = load_csv(SPRINT_SESSION)
    sprint_metrics = [
        ("best_split_5m_s", "s", "min"),
        ("best_split_10m_s", "s", "min"),
        ("best_split_20m_s", "s", "min"),
        ("best_split_30m_s", "s", "min"),
        ("best_fly_5m_s", "s", "min"),
        ("best_fly_10m_s", "s", "min"),
        ("best_total_time_s", "s", "min"),
    ]
    add_pb_candidates(sprint_df, sprint_metrics, candidate_rows, include_side=False)

    # COD
    cod_df = load_csv(COD_SESSION)
    cod_metrics = [
        ("best_segment_1_s", "s", "min"),
        ("best_segment_2_s", "s", "min"),
        ("best_segment_3_s", "s", "min"),
        ("best_total_time_s", "s", "min"),
    ]
    add_pb_candidates(cod_df, cod_metrics, candidate_rows, include_side=True)

    # Jump
    jump_df = load_csv(JUMP_SESSION)
    jump_metrics = [
        ("best_jump_height_cm", "cm", "max"),
        ("best_contact_time_ms", "ms", "min"),
        ("best_flight_time_ms", "ms", "max"),
        ("best_rsi", "", "max"),
    ]
    add_pb_candidates(jump_df, jump_metrics, candidate_rows, include_side=False)

    # Horizontal
    horizontal_df = load_csv(HORIZONTAL_SESSION)
    horizontal_metrics = [
        ("best_distance_cm", "cm", "max"),
    ]
    add_pb_candidates(horizontal_df, horizontal_metrics, candidate_rows, include_side=True)

    # Throw
    throw_df = load_csv(THROW_SESSION)
    throw_metrics = [
        ("best_distance_m", "m", "max"),
    ]
    add_pb_candidates(throw_df, throw_metrics, candidate_rows, include_side=False)

    candidate_df = pd.DataFrame(candidate_rows)

    if candidate_df.empty:
        print("No PB data created")
        return

    out_df = select_best_rows(candidate_df)
    PERSONAL_BESTS.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(PERSONAL_BESTS, index=False)
    print(f"Created: {PERSONAL_BESTS}")


if __name__ == "__main__":
    main()