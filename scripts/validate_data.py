from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

REFERENCE_DIR = BASE_DIR / "data" / "reference"
RAW_DIR = BASE_DIR / "data" / "raw"

TEST_DEFINITIONS = REFERENCE_DIR / "test_definitions.csv"
MEASUREMENT_SESSIONS = RAW_DIR / "measurement_sessions.csv"

RAW_FILES = {
    "sprint": RAW_DIR / "sprint_tests_raw.csv",
    "cod": RAW_DIR / "cod_tests_raw.csv",
    "jump": RAW_DIR / "jump_tests_raw.csv",
    "horizontal": RAW_DIR / "horizontal_tests_raw.csv",
    "throw": RAW_DIR / "throw_tests_raw.csv",
}

EXPECTED_COLUMNS = {
    "sprint": [
        "session_id", "date", "athlete", "test_type", "trial", "valid", "device", "video_file",
        "fps", "start_rule", "finish_rule", "split_5m_s", "split_10m_s", "split_20m_s",
        "split_30m_s", "fly_5m_s", "fly_10m_s", "total_time_s", "camera_position",
        "surface", "shoes", "wind", "sleep_hours", "fatigue", "pain", "memo"
    ],
    "cod": [
        "session_id", "date", "athlete", "test_type", "trial", "side", "valid", "device",
        "video_file", "fps", "start_rule", "finish_rule", "segment_1_s", "segment_2_s",
        "segment_3_s", "total_time_s", "camera_position", "surface", "shoes", "wind",
        "sleep_hours", "fatigue", "pain", "memo"
    ],
    "jump": [
        "session_id", "date", "athlete", "test_type", "trial", "valid", "device", "video_file",
        "fps", "jump_height_cm", "contact_time_ms", "flight_time_ms", "rsi", "surface",
        "shoes", "sleep_hours", "fatigue", "pain", "memo"
    ],
    "horizontal": [
        "session_id", "date", "athlete", "test_type", "trial", "side", "valid", "device",
        "video_file", "fps", "distance_cm", "surface", "shoes", "sleep_hours",
        "fatigue", "pain", "memo"
    ],
    "throw": [
        "session_id", "date", "athlete", "test_type", "trial", "valid", "device", "video_file",
        "distance_m", "surface", "shoes", "sleep_hours", "fatigue", "pain", "memo"
    ],
}

NUMERIC_COLUMNS = {
    "sprint": [
        "trial", "fps", "split_5m_s", "split_10m_s", "split_20m_s", "split_30m_s",
        "fly_5m_s", "fly_10m_s", "total_time_s", "sleep_hours", "fatigue", "pain"
    ],
    "cod": [
        "trial", "fps", "segment_1_s", "segment_2_s", "segment_3_s", "total_time_s",
        "sleep_hours", "fatigue", "pain"
    ],
    "jump": [
        "trial", "fps", "jump_height_cm", "contact_time_ms", "flight_time_ms", "rsi",
        "sleep_hours", "fatigue", "pain"
    ],
    "horizontal": [
        "trial", "fps", "distance_cm", "sleep_hours", "fatigue", "pain"
    ],
    "throw": [
        "trial", "distance_m", "sleep_hours", "fatigue", "pain"
    ],
}


def load_csv(path: Path, label: str, errors: list[str]) -> pd.DataFrame | None:
    if not path.exists():
        errors.append(f"[ERROR] Missing file: {label} -> {path}")
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        errors.append(f"[ERROR] Failed to read {label}: {e}")
        return None


def check_expected_columns(df: pd.DataFrame, expected: list[str], label: str, errors: list[str], warnings: list[str]):
    actual = list(df.columns)
    missing = [c for c in expected if c not in actual]
    extra = [c for c in actual if c not in expected]

    if missing:
        errors.append(f"[ERROR] {label}: missing columns -> {missing}")
    if extra:
        warnings.append(f"[WARN] {label}: unexpected columns -> {extra}")


def check_numeric_columns(df: pd.DataFrame, numeric_columns: list[str], label: str, errors: list[str]):
    for col in numeric_columns:
        if col not in df.columns:
            continue
        coerced = pd.to_numeric(df[col], errors="coerce")
        invalid_mask = df[col].notna() & (df[col].astype(str).str.strip() != "") & coerced.isna()
        if invalid_mask.any():
            bad_rows = list(df.index[invalid_mask] + 2)
            errors.append(f"[ERROR] {label}: non-numeric values in '{col}' at rows {bad_rows}")


def check_session_ids(df: pd.DataFrame, valid_session_ids: set[str], label: str, errors: list[str]):
    if "session_id" not in df.columns:
        return
    values = set(df["session_id"].dropna().astype(str))
    unknown = sorted(v for v in values if v not in valid_session_ids)
    if unknown:
        errors.append(f"[ERROR] {label}: unknown session_id -> {unknown}")


def check_test_types(df: pd.DataFrame, valid_test_types: set[str], label: str, errors: list[str]):
    if "test_type" not in df.columns:
        return
    values = set(df["test_type"].dropna().astype(str))
    unknown = sorted(v for v in values if v not in valid_test_types)
    if unknown:
        errors.append(f"[ERROR] {label}: unknown test_type -> {unknown}")


def check_side_rules(df: pd.DataFrame, label: str, errors: list[str]):
    if "test_type" not in df.columns or "side" not in df.columns:
        return

    requires_side = {"pro_agility", "hop_5"}

    for idx, row in df.iterrows():
        test_type = str(row.get("test_type", "")).strip()
        side = str(row.get("side", "")).strip()

        if test_type in requires_side and side not in {"left", "right"}:
            errors.append(
                f"[ERROR] {label}: row {idx + 2} test_type='{test_type}' requires side=left/right"
            )


def check_valid_column(df: pd.DataFrame, label: str, errors: list[str]):
    if "valid" not in df.columns:
        return

    normalized = df["valid"].fillna("").astype(str).str.strip().str.lower()
    invalid_mask = ~normalized.isin(["true", "false"])
    if invalid_mask.any():
        bad_rows = list(df.index[invalid_mask] + 2)
        bad_values = sorted(set(df.loc[invalid_mask, "valid"].astype(str)))
        errors.append(
            f"[ERROR] {label}: invalid values in 'valid' at rows {bad_rows} -> {bad_values}"
        )


def check_trial_counts(df: pd.DataFrame, label: str, warnings: list[str]):
    if df.empty or "test_type" not in df.columns or "trial" not in df.columns:
        return

    if "valid" in df.columns:
        normalized = df["valid"].fillna("").astype(str).str.strip().str.lower()
        df = df[normalized == "true"].copy()

    if df.empty:
        return

    expected_counts = {
        "sprint_30m": 2,
        "CMJ": 3,
        "SJ": 3,
        "DJ": 3,
        "standing_long_jump": 3,
        "bounding_10": 2,
        "rugby_ball_throw": 3,
    }

    side_required_counts = {
        "pro_agility": 1,
        "hop_5": 2,
    }

    for test_type, expected in expected_counts.items():
        subset = df[df["test_type"] == test_type]
        if subset.empty:
            continue

        grouped = subset.groupby(["session_id", "date", "athlete", "test_type"], dropna=False).size()

        for keys, actual in grouped.items():
            if actual != expected:
                warnings.append(
                    f"[WARN] {label}: {test_type} expected {expected} valid trials but found {actual} "
                    f"for session_id={keys[0]}"
                )

    if "side" in df.columns:
        for test_type, expected in side_required_counts.items():
            subset = df[df["test_type"] == test_type]
            if subset.empty:
                continue

            grouped = subset.groupby(["session_id", "date", "athlete", "test_type", "side"], dropna=False).size()

            for keys, actual in grouped.items():
                side = keys[4]
                if actual != expected:
                    warnings.append(
                        f"[WARN] {label}: {test_type} expected {expected} valid trials for side={side} "
                        f"but found {actual} for session_id={keys[0]}"
                    )


def validate():
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    sessions_df = load_csv(MEASUREMENT_SESSIONS, "measurement_sessions", errors)
    defs_df = load_csv(TEST_DEFINITIONS, "test_definitions", errors)

    if sessions_df is None or defs_df is None:
        for msg in errors:
            print(msg)
        sys.exit(1)

    valid_session_ids = set(sessions_df["session_id"].dropna().astype(str))
    valid_test_types = set(defs_df["test_type"].dropna().astype(str))

    infos.append(f"[INFO] measurement_sessions loaded: {len(sessions_df)} rows")
    infos.append(f"[INFO] test_definitions loaded: {len(defs_df)} rows")

    for label, path in RAW_FILES.items():
        df = load_csv(path, label, errors)
        if df is None:
            continue

        infos.append(f"[INFO] {label} loaded: {len(df)} rows")

        check_expected_columns(df, EXPECTED_COLUMNS[label], label, errors, warnings)
        check_numeric_columns(df, NUMERIC_COLUMNS[label], label, errors)
        check_session_ids(df, valid_session_ids, label, errors)
        check_test_types(df, valid_test_types, label, errors)
        check_side_rules(df, label, errors)
        check_valid_column(df, label, errors)
        check_trial_counts(df, label, warnings)

    for msg in infos:
        print(msg)

    for msg in warnings:
        print(msg)

    if errors:
        for msg in errors:
            print(msg)
        sys.exit(1)

    if warnings:
        print("[OK] validation passed with warnings")
    else:
        print("[OK] validation passed")


if __name__ == "__main__":
    validate()