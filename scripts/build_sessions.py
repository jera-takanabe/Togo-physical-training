from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

SPRINT_RAW = RAW_DIR / "sprint_tests_raw.csv"
COD_RAW = RAW_DIR / "cod_tests_raw.csv"
JUMP_RAW = RAW_DIR / "jump_tests_raw.csv"
HORIZONTAL_RAW = RAW_DIR / "horizontal_tests_raw.csv"
THROW_RAW = RAW_DIR / "throw_tests_raw.csv"

SPRINT_SESSION = PROCESSED_DIR / "sprint_sessions.csv"
COD_SESSION = PROCESSED_DIR / "cod_sessions.csv"
JUMP_SESSION = PROCESSED_DIR / "jump_sessions.csv"
HORIZONTAL_SESSION = PROCESSED_DIR / "horizontal_sessions.csv"
THROW_SESSION = PROCESSED_DIR / "throw_sessions.csv"
RSA_RAW = RAW_DIR / "rsa_tests_raw.csv"
YOYO_RAW = RAW_DIR / "yoyo_tests_raw.csv"

RSA_SESSION = PROCESSED_DIR / "rsa_sessions.csv"
YOYO_SESSION = PROCESSED_DIR / "yoyo_sessions.csv"

def safe_std(series: pd.Series):
    series = series.dropna()
    if len(series) <= 1:
        return None
    return series.std(ddof=0)


def load_csv(path: Path):
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def save_df(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Created: {path}")


def filter_valid_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "valid" not in df.columns:
        return df
    normalized = df["valid"].fillna("").astype(str).str.strip().str.lower()
    return df[normalized == "true"].copy()


def build_sprint_sessions():
    df = load_csv(SPRINT_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {SPRINT_RAW} is empty or not found")
        return

    group_cols = ["session_id", "date", "athlete", "test_type"]
    rows = []

    metric_cols = [
        "split_5m_s", "split_10m_s", "split_20m_s", "split_30m_s",
        "fly_5m_s", "fly_10m_s", "total_time_s"
    ]

    for keys, group in df.groupby(group_cols, dropna=False):
        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "trials": len(group),
            "quality_flag": "ok",
            "memo": "",
        }

        for col in metric_cols:
            s = pd.to_numeric(group[col], errors="coerce") if col in group.columns else pd.Series(dtype=float)
            row[f"best_{col}"] = s.min(skipna=True) if not s.dropna().empty else None
            row[f"avg_{col}"] = s.mean(skipna=True) if not s.dropna().empty else None
            row[f"std_{col}"] = safe_std(s)

        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete", "test_type"]).reset_index(drop=True)
    save_df(out_df, SPRINT_SESSION)


def build_cod_sessions():
    df = load_csv(COD_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {COD_RAW} is empty or not found")
        return

    group_cols = ["session_id", "date", "athlete", "test_type", "side"]
    rows = []

    metric_cols = ["segment_1_s", "segment_2_s", "segment_3_s", "total_time_s"]

    for keys, group in df.groupby(group_cols, dropna=False):
        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "side": keys[4],
            "trials": len(group),
            "quality_flag": "ok",
            "memo": "",
        }

        for col in metric_cols:
            s = pd.to_numeric(group[col], errors="coerce") if col in group.columns else pd.Series(dtype=float)
            row[f"best_{col}"] = s.min(skipna=True) if not s.dropna().empty else None
            row[f"avg_{col}"] = s.mean(skipna=True) if not s.dropna().empty else None
            row[f"std_{col}"] = safe_std(s)

        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete", "test_type", "side"]).reset_index(drop=True)
    save_df(out_df, COD_SESSION)


def build_jump_sessions():
    df = load_csv(JUMP_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {JUMP_RAW} is empty or not found")
        return

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
            "best_jump_height_cm": jump_height.max(skipna=True) if not jump_height.dropna().empty else None,
            "avg_jump_height_cm": jump_height.mean(skipna=True) if not jump_height.dropna().empty else None,
            "std_jump_height_cm": safe_std(jump_height),
            "best_contact_time_ms": contact_time.min(skipna=True) if not contact_time.dropna().empty else None,
            "avg_contact_time_ms": contact_time.mean(skipna=True) if not contact_time.dropna().empty else None,
            "std_contact_time_ms": safe_std(contact_time),
            "best_flight_time_ms": flight_time.max(skipna=True) if not flight_time.dropna().empty else None,
            "avg_flight_time_ms": flight_time.mean(skipna=True) if not flight_time.dropna().empty else None,
            "std_flight_time_ms": safe_std(flight_time),
            "best_rsi": rsi.max(skipna=True) if not rsi.dropna().empty else None,
            "avg_rsi": rsi.mean(skipna=True) if not rsi.dropna().empty else None,
            "std_rsi": safe_std(rsi),
            "quality_flag": "ok",
            "memo": "",
        }
        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete", "test_type"]).reset_index(drop=True)
    save_df(out_df, JUMP_SESSION)


def build_horizontal_sessions():
    df = load_csv(HORIZONTAL_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {HORIZONTAL_RAW} is empty or not found")
        return

    group_cols = ["session_id", "date", "athlete", "test_type", "side"]
    rows = []

    for keys, group in df.groupby(group_cols, dropna=False):
        distance = pd.to_numeric(group["distance_cm"], errors="coerce")

        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "side": keys[4],
            "trials": len(group),
            "best_distance_cm": distance.max(skipna=True) if not distance.dropna().empty else None,
            "avg_distance_cm": distance.mean(skipna=True) if not distance.dropna().empty else None,
            "std_distance_cm": safe_std(distance),
            "quality_flag": "ok",
            "memo": "",
        }
        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete", "test_type", "side"]).reset_index(drop=True)
    save_df(out_df, HORIZONTAL_SESSION)


def build_throw_sessions():
    df = load_csv(THROW_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {THROW_RAW} is empty or not found")
        return

    group_cols = ["session_id", "date", "athlete", "test_type"]
    rows = []

    for keys, group in df.groupby(group_cols, dropna=False):
        distance = pd.to_numeric(group["distance_m"], errors="coerce")

        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "trials": len(group),
            "best_distance_m": distance.max(skipna=True) if not distance.dropna().empty else None,
            "avg_distance_m": distance.mean(skipna=True) if not distance.dropna().empty else None,
            "std_distance_m": safe_std(distance),
            "quality_flag": "ok",
            "memo": "",
        }
        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete", "test_type"]).reset_index(drop=True)
    save_df(out_df, THROW_SESSION)

def build_rsa_sessions():
    df = load_csv(RSA_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {RSA_RAW} is empty or not found")
        return

    group_cols = ["session_id", "date", "athlete", "test_type"]
    rows = []

    for keys, group in df.groupby(group_cols, dropna=False):
        times = pd.to_numeric(group["time_sec"], errors="coerce")

        if times.dropna().empty:
            continue

        avg_time = times.mean()
        best_time = times.min()
        worst_time = times.max()

        decline = (worst_time - best_time) / best_time if best_time > 0 else None

        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "trials": len(group),
            "avg_time": avg_time,
            "best_time": best_time,
            "worst_time": worst_time,
            "decline_ratio": decline,
            "quality_flag": "ok",
            "memo": "",
        }

        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete"]).reset_index(drop=True)
    save_df(out_df, RSA_SESSION)

def build_yoyo_sessions():
    df = load_csv(YOYO_RAW)
    df = filter_valid_rows(df)

    if df.empty:
        print(f"Skip: {YOYO_RAW} is empty or not found")
        return

    group_cols = ["session_id", "date", "athlete", "test_type"]
    rows = []

    for keys, group in df.groupby(group_cols, dropna=False):
        distance = pd.to_numeric(group["distance_m"], errors="coerce")

        if distance.dropna().empty:
            continue

        row = {
            "session_id": keys[0],
            "date": keys[1],
            "athlete": keys[2],
            "test_type": keys[3],
            "trials": len(group),
            "best_distance_m": distance.max(),
            "quality_flag": "ok",
            "memo": "",
        }

        rows.append(row)

    out_df = pd.DataFrame(rows).sort_values(["date", "athlete"]).reset_index(drop=True)
    save_df(out_df, YOYO_SESSION)

def main():
    build_sprint_sessions()
    build_cod_sessions()
    build_jump_sessions()
    build_horizontal_sessions()
    build_throw_sessions()
    build_rsa_sessions()
    build_yoyo_sessions()

if __name__ == "__main__":
    main()