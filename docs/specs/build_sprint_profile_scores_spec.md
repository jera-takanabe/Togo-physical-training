# build_sprint_profile_scores.py 設計仕様 v1.0

## 1. 目的

本仕様は、Sprint Profile Analysis を実装するための 集計スクリプト

`build_sprint_profile_scores.py`

の責務、入出力、処理手順、関数構成を定義する。

このスクリプトの役割は、既存の測定データから Sprint Profile
用の分析テーブル

`data/analysis/sprint_profile_scores.csv`

を生成することである。

------------------------------------------------------------------------

# 2. スクリプト配置

推奨配置

``` text
scripts/build_sprint_profile_scores.py
```

------------------------------------------------------------------------

# 3. 入力

## 3.1 必須入力

### `data/analysis/test_scores.csv`

想定列

  列名           説明
  -------------- ----------
  athlete_id     選手ID
  session_date   測定日
  test_name      テスト名
  value          測定値
  radar_score    スコア

必要な test_name

-   5m
-   10m
-   20m
-   30m
-   Fly5
-   Fly10

### `data/reference/benchmark_values.csv`

必要 benchmark

-   5m
-   10m
-   20m
-   Fly5
-   Fly10
-   sprint_20_30_segment_velocity

------------------------------------------------------------------------

## 3.2 任意入力

### `data/analysis/domain_scores.csv`

補助ドメイン

-   Elastic
-   Endurance

### `data/raw/athlete_profile.csv`

補助情報

-   height
-   weight

### `data/analysis/rsa_scores.csv`

Endurance 補助指標

------------------------------------------------------------------------

# 4. 出力

## 4.1 主出力

``` text
data/analysis/sprint_profile_scores.csv
```

## 4.2 副出力（任意）

``` text
data/analysis/sprint_profile_summary.csv
```

v1.0 では主出力のみ必須。

------------------------------------------------------------------------

# 5. 処理フロー

``` text
test_scores.csv 読み込み
↓
Sprint対象テスト抽出
↓
横持ち変換
↓
split計算
↓
区間速度計算
↓
20–30m segment radar_score 計算
↓
acceleration_index / max_velocity_index 計算
↓
補助ドメイン結合
↓
validation判定
↓
タイプ分類
↓
CSV保存
```

------------------------------------------------------------------------

# 6. 関数構成（推奨）

## 6.1 `load_test_scores(path)`

役割: - test_scores.csv 読み込み - 必須列存在確認 - 型変換

戻り値: - DataFrame

------------------------------------------------------------------------

## 6.2 `filter_sprint_tests(df, mapping)`

役割: - Sprint Profile で必要な test_name のみ抽出 -
内部キーへマッピング

内部キー:

-   time_5m
-   time_10m
-   time_20m
-   time_30m
-   fly5_time
-   fly10_time

戻り値: - 縦持ち DataFrame

------------------------------------------------------------------------

## 6.3 `pivot_sprint_tests(df)`

役割: - athlete_id, session_date 単位で横持ちへ変換

戻り値: - 1行1セッションの DataFrame

------------------------------------------------------------------------

## 6.4 `validate_required_columns(df)`

役割: - 必須キーの欠損確認 - 不足時はエラーまたは warning

確認対象:

-   time_5m
-   time_10m
-   time_20m
-   time_30m
-   fly5_time
-   fly10_time

------------------------------------------------------------------------

## 6.5 `compute_splits(df)`

計算:

``` text
split_0_5   = time_5m
split_5_10  = time_10m - time_5m
split_10_20 = time_20m - time_10m
split_20_30 = time_30m - time_20m
```

戻り値: - split列追加済み DataFrame

------------------------------------------------------------------------

## 6.6 `compute_velocities(df)`

計算:

``` text
v_0_5   = 5  / split_0_5
v_5_10  = 5  / split_5_10
v_10_20 = 10 / split_10_20
v_20_30 = 10 / split_20_30
v_fly5  = 5  / fly5_time
v_fly10 = 10 / fly10_time
```

戻り値: - velocity列追加済み DataFrame

------------------------------------------------------------------------

## 6.7 `load_benchmarks(path)`

役割: - benchmark_values.csv 読み込み - 必須 benchmark の存在確認

特に確認:

-   sprint_20_30_segment_velocity

戻り値: - benchmark辞書 または DataFrame

------------------------------------------------------------------------

## 6.8 `calc_radar_score(value, floor_anchor, world_elite_p50, inverse=False)`

役割: - 単一値を radar_score 化

式:

``` text
score =
100 × (value - floor_anchor) / (world_elite_p50 - floor_anchor)
```

制限:

``` text
0〜100 に clamp
```

補足: - sprint time は原則 inverse 指標として扱う必要がある -
既存実装に合わせて time 系と velocity 系の関数を分けてもよい

------------------------------------------------------------------------

## 6.9 `compute_segment_radar(df, benchmarks)`

役割: - 20--30m 区間速度を radar_score 化

追加列: - radar_20_30_seg

------------------------------------------------------------------------

## 6.10 `merge_existing_radar_scores(df, test_scores_pivot)`

役割: - 5m / 10m / 20m / Fly5 / Fly10 の radar_score を結合

追加列: - radar_5m - radar_10m - radar_20m - radar_fly5 - radar_fly10

------------------------------------------------------------------------

## 6.11 `compute_indices(df)`

計算:

``` text
acceleration_index =
mean(radar_5m, radar_10m, radar_20m)
```

``` text
max_velocity_index =
mean(radar_fly5, radar_fly10, radar_20_30_seg)
```

``` text
speed_reserve_index_basic =
max_velocity_index - acceleration_index
```

``` text
split_balance_index =
(v_20_30 - v_0_5) / v_20_30
```

------------------------------------------------------------------------

## 6.12 `merge_support_scores(df, domain_scores)`

役割: - Elastic / Endurance を補助指標として結合

追加列: - elastic_support_score - engine_support_score

------------------------------------------------------------------------

## 6.13 `run_validation(df)`

役割: - validation_flag - validation_notes

判定対象:

-   TIME_ORDER_ERROR
-   NON_POSITIVE_SPLIT
-   FLY_SEGMENT_MISMATCH
-   OUTLIER_YOUTH_CHECK

------------------------------------------------------------------------

## 6.14 `classify_sprint_profile(df)`

ルール:

-   Underdeveloped Sprint Type
-   Acceleration Type
-   Max Velocity Type
-   Balanced Sprint Type

------------------------------------------------------------------------

## 6.15 `save_output(df, path)`

役割: - 列順を整える - CSV保存

------------------------------------------------------------------------

# 7. エラーハンドリング方針

## 7.1 ハードエラー

以下は処理停止とする。

-   test_scores.csv が存在しない
-   必須列不足
-   benchmark_values.csv が存在しない
-   sprint_20_30_segment_velocity benchmark が無い

------------------------------------------------------------------------

## 7.2 ソフトエラー

以下は warning とし、対象行のみ flag を立てる。

-   一部テスト欠損
-   Fly mismatch
-   異常に高い youth 値
-   split負値

------------------------------------------------------------------------

# 8. CLI仕様（推奨）

実行例

``` bash
python scripts/build_sprint_profile_scores.py
```

拡張例

``` bash
python scripts/build_sprint_profile_scores.py \
  --test-scores data/analysis/test_scores.csv \
  --benchmarks data/reference/benchmark_values.csv \
  --domain-scores data/analysis/domain_scores.csv \
  --output data/analysis/sprint_profile_scores.csv
```

------------------------------------------------------------------------

# 9. ログ出力（推奨）

標準出力に次を表示する。

-   入力件数
-   出力件数
-   欠損件数
-   validation件数
-   主な warning

例:

``` text
[INFO] Loaded sprint test scores: 6 rows
[INFO] Built sprint profile rows: 1
[WARN] FLY_SEGMENT_MISMATCH: 1 row
[INFO] Saved: data/analysis/sprint_profile_scores.csv
```

------------------------------------------------------------------------

# 10. テストケース

## 正常系

-   すべての sprint 値が存在
-   split 正常
-   Fly と 20--30m が整合
-   classification 成功

------------------------------------------------------------------------

## 異常系1

-   time_10m \< time_5m

期待: - TIME_ORDER_ERROR

------------------------------------------------------------------------

## 異常系2

-   fly10_time \<= 0

期待: - NON_POSITIVE_SPLIT

------------------------------------------------------------------------

## 異常系3

-   v_fly10 と v_20_30 の差が 10%以上

期待: - FLY_SEGMENT_MISMATCH

------------------------------------------------------------------------

## 異常系4

-   必須 benchmark 欠損

期待: - 処理停止

------------------------------------------------------------------------

# 11. 列順（推奨）

``` text
athlete_id
session_date
time_5m
time_10m
time_20m
time_30m
fly5_time
fly10_time
split_0_5
split_5_10
split_10_20
split_20_30
v_0_5
v_5_10
v_10_20
v_20_30
v_fly5
v_fly10
radar_5m
radar_10m
radar_20m
radar_fly5
radar_fly10
radar_20_30_seg
acceleration_index
max_velocity_index
speed_reserve_index_basic
split_balance_index
elastic_support_score
engine_support_score
sprint_profile_type
validation_flag
validation_notes
```

------------------------------------------------------------------------

# 12. 実装上の注意

## 12.1 既存スコアとの整合

5m / 10m / 20m / Fly5 / Fly10 の radar_score は、 既存の
`test_scores.csv` を信頼し、再計算しない方針を推奨する。

理由: - スコアリングロジックの一元化 - 将来 benchmark 更新時の整合性維持

------------------------------------------------------------------------

## 12.2 20--30m のみ新規計算

20--30m segment は既存 test_scores に存在しない可能性が高いため、 Sprint
Profile 側で新規計算する。

------------------------------------------------------------------------

## 12.3 単一選手前提だが複数選手対応可能にする

現時点では息子さん1人の育成ツールだが、 将来的な複数選手対応を見越して
athlete_id を必須保持する。

------------------------------------------------------------------------

# 13. 将来拡張

## Phase 2

-   sprint_profile_summary.csv 生成
-   推奨トレーニング出力
-   前回比較差分

## Phase 3

-   Plot 出力
-   MSS 推定
-   ASR 拡張
-   position profile 連携

------------------------------------------------------------------------

# 14. 設計判断の明示

## 外部知見に沿う部分

-   split から acceleration / max velocity を分けてみる
-   Fly と後半 split を max velocity proxy に使う
-   ユースでは時系列解釈が重要

## 本プロジェクト独自ルール

-   関数分割方針
-   validation_flag 条件
-   CLI引数
-   出力列順
-   20--30m segment を Sprint Profile 専用で計算する運用

これらは、低設備・動画解析・U12育成用途に合わせた
実装設計上のルールである。
