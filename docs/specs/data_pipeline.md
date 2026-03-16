# データパイプライン仕様（Data Pipeline）

本プロジェクトはデータパイプライン型の分析構造で設計されている。

------------------------------------------------------------------------

# パイプライン構造

Raw Data ↓ Test Scores ↓ Domain Scores ↓ Rugby Physical Score ↓
Dashboards

------------------------------------------------------------------------

# Raw Data

data/raw/

ここには測定データを保存する。

例

-   sprint_tests_raw.csv
-   jump_tests_raw.csv
-   cod_tests_raw.csv

------------------------------------------------------------------------

# Test Scores

data/analysis/test_scores.csv

各測定結果を radar_score に変換する。

------------------------------------------------------------------------

# Domain Scores

data/analysis/domain_scores.csv

ドメイン単位の能力評価。

------------------------------------------------------------------------

# Rugby Physical Score

data/analysis/rugby_physical_score.csv

総合フィジカル能力指数。

------------------------------------------------------------------------

# Dashboards

docs/dashboards/

ここに分析結果の可視化を出力する。

例

-   radar_chart.png
-   target_radar.png
-   trend_chart.png
