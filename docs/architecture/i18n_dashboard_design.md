# i18n Complete Set

## Files included

- `config/language.yaml`
- `data/reference/i18n_labels.csv`
- `scripts/utils/i18n.py`
- `scripts/build_latest_summary_i18n.py`
- `docs/architecture/i18n_dashboard_design.md`

## Installation

```bash
mkdir -p config
mkdir -p data/reference
mkdir -p scripts/utils

cp config/language.yaml <repo>/config/language.yaml
cp data/reference/i18n_labels.csv <repo>/data/reference/i18n_labels.csv
cp scripts/utils/i18n.py <repo>/scripts/utils/i18n.py
cp scripts/build_latest_summary_i18n.py <repo>/scripts/build_latest_summary.py
```

## Switch language

Japanese:

```yaml
language: ja
```

English:

```yaml
language: en
```

## Policy

- Raw / processed / analysis column names stay in English
- Dashboard only is localized
- Add new rows to `i18n_labels.csv` when needed
