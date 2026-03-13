from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

JUMPS_RAW = BASE_DIR / "data" / "raw" / "myjump" / "jumps_raw.csv"
SPRINTS_RAW = BASE_DIR / "data" / "raw" / "kinovea" / "sprints_raw.csv"

JUMPS_SESSION = BASE_DIR / "data" / "processed" / "jumps_session.csv"
SPRINTS_SESSION = BASE_DIR / "data" / "processed" / "sprints_session.csv"


def safe_std(series: pd.Series):
    series = series.dropna()
    if len(series) <= 1:
        return None
    return series.std(ddof=0)


def build_jumps_session():
    if not JUMPS_RAW.exists():
        print(f"Skip: {JUMPS_RAW} not found")
        return

    df = pd.read_csv(JUMPS_RAW)

    group_cols = ["session_id", "date", "athlete", "test_type"]

    rows = []
    for keys, group in df.groupby(group_cols, dropna=False):
        jump_height = pd.to_numeric(group["jump_height_cm"], errors="coerce")
        contact_time = pd.to_numeric(group["contact_time_ms"], errors="coerce")
        flight_time = pd.to_numeric(group["flight_time_ms"], errors="coerce")
        rsi = pd.to_numeric(group["rsi"], errors="coerce")

        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "trials": len(group),
            "best_jump_height_cm": jump_height.max(skipna=True),
            "avg_jump_height_cm": jump_height.mean(skipna=True),
            "std_jump_height_cm": safe_std(jump_height),
            "best_contact_time_ms": contact_time.min(skipna=True) if contact_time.notna().any() else None,
            "avg_contact_time_ms": contact_time.mean(skipna=True),
            "best_flight_time_ms": flight_time.max(skipna=True),
            "avg_flight_time_ms": flight_time.mean(skipna=True),
            "best_rsi": rsi.max(skipna=True),
            "avg_rsi": rsi.mean(skipna=True),
            "quality_flag": "ok",
            "memo": "",
        }
        rows.append(row)

    out_df = pd.DataFrame(rows)
    out_df = out_df.sort_values(["date", "athlete", "test_type"]).reset_index(drop=True)

    JUMPS_SESSION.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(JUMPS_SESSION, index=False)
    print(f"Created: {JUMPS_SESSION}")


def build_sprints_session():
    if not SPRINTS_RAW.exists():
        print(f"Skip: {SPRINTS_RAW} not found")
        return

    df = pd.read_csv(SPRINTS_RAW)

    group_cols = ["session_id", "date", "athlete", "test_type"]

    rows = []
    for keys, group in df.groupby(group_cols, dropna=False):
        split_5m = pd.to_numeric(group["split_5m_s"], errors="coerce")
        split_10m = pd.to_numeric(group["split_10m_s"], errors="coerce")
        split_20m = pd.to_numeric(group["split_20m_s"], errors="coerce")
        split_30m = pd.to_numeric(group["split_30m_s"], errors="coerce")
        total_time = pd.to_numeric(group["total_time_s"], errors="coerce")

        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "trials": len(group),
            "best_5m_s": split_5m.min(skipna=True) if split_5m.notna().any() else None,
            "avg_5m_s": split_5m.mean(skipna=True),
            "best_10m_s": split_10m.min(skipna=True) if split_10m.notna().any() else None,
            "avg_10m_s": split_10m.mean(skipna=True),
            "best_20m_s": split_20m.min(skipna=True) if split_20m.notna().any() else None,
            "avg_20m_s": split_20m.mean(skipna=True),
            "best_30m_s": split_30m.min(skipna=True) if split_30m.notna().any() else None,
            "avg_30m_s": split_30m.mean(skipna=True),
            "best_total_time_s": total_time.min(skipna=True) if total_time.notna().any() else None,
            "avg_total_time_s": total_time.mean(skipna=True),
            "quality_flag": "ok",
            "memo": "",
        }
        rows.append(row)

    out_df = pd.DataFrame(rows)
    out_df = out_df.sort_values(["date", "athlete", "test_type"]).reset_index(drop=True)

    SPRINTS_SESSION.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(SPRINTS_SESSION, index=False)
    print(f"Created: {SPRINTS_SESSION}")


def main():
    build_jumps_session()
    build_sprints_session()


if __name__ == "__main__":
    main()