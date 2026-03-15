from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
LANGUAGE_PATH = BASE_DIR / "config" / "language.yaml"
LABELS_PATH = BASE_DIR / "data" / "reference" / "i18n_labels.csv"


def get_language() -> str:
    if not LANGUAGE_PATH.exists():
        return "ja"

    for line in LANGUAGE_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("language:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            return value or "ja"
    return "ja"


def load_labels() -> dict[str, str]:
    lang = get_language()
    df = pd.read_csv(LABELS_PATH)
    if lang not in df.columns:
        lang = "ja"
    return dict(zip(df["key"], df[lang]))


def t(key: str, default: str | None = None) -> str:
    labels = load_labels()
    if key in labels:
        return str(labels[key])
    return default if default is not None else key


def map_value(value: str, labels: dict[str, str]) -> str:
    key = str(value).strip().lower().replace(" ", "_")
    return labels.get(key, str(value))


def translate_column(column_name: str, labels: dict[str, str]) -> str:
    key = str(column_name).strip().lower().replace(" ", "_")
    return labels.get(key, column_name)
