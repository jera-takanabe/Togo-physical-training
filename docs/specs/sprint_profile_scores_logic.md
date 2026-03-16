# sprint_profile_scores.csv 生成ロジック仕様 v1.0

## 1. 目的

本仕様は、Sprint Profile Analysis の中核出力である

`sprint_profile_scores.csv`

を生成するためのロジックを定義する。

このファイルは、各測定セッションにおけるスプリント split、区間速度、
加速指標、最大速度指標、タイプ分類を一元化した分析結果テーブルである。

------------------------------------------------------------------------

# 2. 入力ファイル

本ロジックは、原則として以下の入力を参照する。

## 2.1 必須入力

### `data/analysis/test_scores.csv`

少なくとも以下のテスト結果が必要。

-   5m sprint
-   10m sprint
-   20m sprint
-   30m sprint
-   Fly5
-   Fly10

### `data/reference/benchmark_values.csv`

少なくとも以下の benchmark が必要。

-   5m sprint
-   10m sprint
-   20m sprint
-   Fly5
-   Fly10
-   20--30m segment（新規追加推奨）

------------------------------------------------------------------------

## 2.2 任意入力

### `data/analysis/domain_scores.csv`

補助指標に使用する。

-   Elastic
-   Endurance

### `data/raw/athlete_profile.csv`

補助的な体格情報に使用する。

-   height
-   weight

### `data/analysis/rsa_scores.csv` または同等ファイル

補助的な engine 指標に使用する。

------------------------------------------------------------------------

# 3. 前提条件

## 3.1 測定単位

-   time: 秒
-   distance: m
-   velocity: m/s

## 3.2 データ粒度

1行 = 1選手 × 1測定日

現時点では単一選手運用を前提とするが、 将来の複数選手対応を見据えて
`athlete_id` を含める。

------------------------------------------------------------------------

# 4. 出力ファイル

## 4.1 ファイル名

`data/analysis/sprint_profile_scores.csv`

## 4.2 出力列

  列名                        型       説明
  --------------------------- -------- -----------------------------
  athlete_id                  string   選手ID
  session_date                date     測定日
  time_5m                     float    0--5m 累積
  time_10m                    float    0--10m 累積
  time_20m                    float    0--20m 累積
  time_30m                    float    0--30m 累積
  fly5_time                   float    Fly5
  fly10_time                  float    Fly10
  split_0_5                   float    0--5m 区間
  split_5_10                  float    5--10m 区間
  split_10_20                 float    10--20m 区間
  split_20_30                 float    20--30m 区間
  v_0_5                       float    0--5m 平均速度
  v_5_10                      float    5--10m 平均速度
  v_10_20                     float    10--20m 平均速度
  v_20_30                     float    20--30m 平均速度
  v_fly5                      float    Fly5 平均速度
  v_fly10                     float    Fly10 平均速度
  radar_5m                    float    5m radar_score
  radar_10m                   float    10m radar_score
  radar_20m                   float    20m radar_score
  radar_fly5                  float    Fly5 radar_score
  radar_fly10                 float    Fly10 radar_score
  radar_20_30_seg             float    20--30m segment radar_score
  acceleration_index          float    加速指標
  max_velocity_index          float    最大速度指標
  speed_reserve_index_basic   float    実務版 speed reserve
  split_balance_index         float    split バランス
  elastic_support_score       float    Elastic 補助指標
  engine_support_score        float    Endurance 補助指標
  sprint_profile_type         string   タイプ分類
  validation_flag             string   異常値フラグ
  validation_notes            string   詳細メモ

------------------------------------------------------------------------

# 5. 入力データの抽出ルール

## 5.1 test_scores.csv の想定構造

以下のような縦持ちデータを想定する。

  athlete_id   session_date   test_name   value   radar_score
  ------------ -------------- ----------- ------- -------------

この構造から `test_name` を列展開して横持ちに変換する。

対象 test_name 例:

-   sprint_5m
-   sprint_10m
-   sprint_20m
-   sprint_30m
-   fly_5m
-   fly_10m

※ 実際の test_name は既存命名に合わせてマッピングテーブルで吸収する。

------------------------------------------------------------------------

# 6. 計算ロジック

## 6.1 split 計算

``` text
split_0_5   = time_5m
split_5_10  = time_10m - time_5m
split_10_20 = time_20m - time_10m
split_20_30 = time_30m - time_20m
```

------------------------------------------------------------------------

## 6.2 区間平均速度

``` text
v_0_5   = 5  / split_0_5
v_5_10  = 5  / split_5_10
v_10_20 = 10 / split_10_20
v_20_30 = 10 / split_20_30
v_fly5  = 5  / fly5_time
v_fly10 = 10 / fly10_time
```

------------------------------------------------------------------------

## 6.3 20--30m segment の radar_score

### 方式

20--30m 区間の平均速度を benchmark に対してスコア化する。

推奨方法:

1.  `benchmark_values.csv` に `sprint_20_30_segment_velocity` を追加
2.  `floor_anchor`, `competitive`, `elite`, `world_elite_p50` を設定
3.  他のテストと同じ正規化を行う

``` text
radar_20_30_seg =
100 × (v_20_30 - floor_anchor)
      / (world_elite_p50 - floor_anchor)
```

### 注意

時間指標ではなく **速度指標** として benchmark を持つこと。 理由: -
split は距離固定であり、速度で扱うほうが Fly と整合しやすい - 20--30m
は最大速度局面の簡易 proxy として扱うため

------------------------------------------------------------------------

## 6.4 acceleration_index

``` text
acceleration_index =
mean(
  radar_5m,
  radar_10m,
  radar_20m
)
```

補足: - 5m はスタート技術の影響が強い - 10m は主指標 - 20m
は加速持続の確認

------------------------------------------------------------------------

## 6.5 max_velocity_index

``` text
max_velocity_index =
mean(
  radar_fly5,
  radar_fly10,
  radar_20_30_seg
)
```

補足: - Fly10 を主指標 - Fly5 は補助 - 20--30m は動画 split からの簡易
MSS proxy

------------------------------------------------------------------------

## 6.6 speed_reserve_index_basic

``` text
speed_reserve_index_basic =
max_velocity_index - acceleration_index
```

解釈: - 正: 最大速度寄り - 0付近: バランス型 - 負: 加速寄り

------------------------------------------------------------------------

## 6.7 split_balance_index

``` text
split_balance_index =
(v_20_30 - v_0_5) / v_20_30
```

解釈: - 大きい: 後半伸びる - 小さい: 初速寄り

------------------------------------------------------------------------

## 6.8 elastic_support_score

`domain_scores.csv` から取得する。

``` text
elastic_support_score = domain_score("Elastic")
```

ない場合は空欄でもよい。

------------------------------------------------------------------------

## 6.9 engine_support_score

優先順位:

1.  `domain_scores.csv` に Endurance がある場合はそれを使う
2.  なければ YoYo / RSA から簡易平均を作る
3.  どちらも無ければ空欄

------------------------------------------------------------------------

# 7. タイプ分類ロジック

## 7.1 基本分類

### Underdeveloped Sprint Type

``` text
if acceleration_index < 50 and max_velocity_index < 50
```

------------------------------------------------------------------------

### Acceleration Type

``` text
elif acceleration_index >= max_velocity_index + 8
```

------------------------------------------------------------------------

### Max Velocity Type

``` text
elif max_velocity_index >= acceleration_index + 8
```

------------------------------------------------------------------------

### Balanced Sprint Type

``` text
else
```

------------------------------------------------------------------------

## 7.2 補助ラベル（将来拡張）

Elastic / Power / Engine の高値がある場合に サブラベルを付ける。

例:

-   Acceleration Type + Power Support
-   Balanced Type + Elastic Support

v1.0 では `sprint_profile_type` は単一値でよい。

------------------------------------------------------------------------

# 8. validation_flag ロジック

## 8.1 OK

異常なし

``` text
OK
```

------------------------------------------------------------------------

## 8.2 TIME_ORDER_ERROR

累積タイムの順序異常

``` text
time_5m >= time_10m
or time_10m >= time_20m
or time_20m >= time_30m
```

------------------------------------------------------------------------

## 8.3 NON_POSITIVE_SPLIT

split が 0 以下

``` text
split_5_10 <= 0
or split_10_20 <= 0
or split_20_30 <= 0
or fly5_time <= 0
or fly10_time <= 0
```

------------------------------------------------------------------------

## 8.4 FLY_SEGMENT_MISMATCH

Fly10 と 20--30m の速度差が大きい

``` text
abs(v_fly10 - v_20_30) / v_fly10 > 0.10
```

------------------------------------------------------------------------

## 8.5 OUTLIER_YOUTH_CHECK

年齢相応 benchmark を大幅に逸脱

ルール例:

-   既存 U12 benchmark を 15%以上上回る
-   連続セッションで再現しない

※ v1.0 では暫定フラグでよい

------------------------------------------------------------------------

## 8.6 MULTI_FLAG

複数異常がある場合

``` text
MULTI_FLAG
```

`validation_notes` に詳細をセミコロン区切りで記録する。

例:

``` text
TIME_ORDER_ERROR;FLY_SEGMENT_MISMATCH
```

------------------------------------------------------------------------

# 9. 疑似コード

``` python
load test_scores
pivot sprint tests by athlete_id, session_date

for each row:
    compute splits
    compute velocities
    compute radar_20_30_seg
    compute acceleration_index
    compute max_velocity_index
    compute speed_reserve_index_basic
    compute split_balance_index

    merge elastic_support_score
    merge engine_support_score

    run validation rules
    classify sprint_profile_type

save sprint_profile_scores.csv
```

------------------------------------------------------------------------

# 10. マッピングテーブル設計

既存 test_name と Sprint Profile 用の内部キーを分ける。

例:

  original_test_name   profile_key
  -------------------- -------------
  5m                   time_5m
  10m                  time_10m
  20m                  time_20m
  30m                  time_30m
  Fly5                 fly5_time
  Fly10                fly10_time

これにより、既存 CSV 命名変更に強くなる。

------------------------------------------------------------------------

# 11. 参考実装方針

推奨スクリプト:

``` text
scripts/build_sprint_profile_scores.py
```

推奨責務: - sprint 入力の抽出 - split / velocity 計算 - validation -
type classification - CSV 出力

他スクリプトに責務を分散しすぎないこと。 Sprint Profile
は1つの独立分析レイヤーとして扱う。

------------------------------------------------------------------------

# 12. 出力例

  ------------------------------------------------------------------------------------------------------------------
  athlete_id   session_date     acceleration_index   max_velocity_index sprint_profile_type   validation_flag
  ------------ -------------- -------------------- -------------------- --------------------- ----------------------
  togo         2026-03-08                     78.4                 64.1 Acceleration Type     OK

  togo         2026-04-12                     74.2                 75.8 Balanced Sprint Type  FLY_SEGMENT_MISMATCH
  ------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 13. 将来拡張

## Phase 2

-   `sprint_profile_summary.csv` 自動生成
-   強み / 課題 / 推奨トレーニングの自動出力
-   時系列チャート

## Phase 3

-   年齢補正 benchmark
-   position profile との統合
-   RSA / YoYo との結合による拡張 speed reserve

------------------------------------------------------------------------

# 14. 設計判断の明示

## 外部知見に沿う部分

-   分割区間で acceleration と top speed を分けて考える
-   flying split と後半 split を最大速度 proxy に使う
-   ユースでは時系列解釈が重要

## 本プロジェクト独自ルール

-   acceleration_index / max_velocity_index の具体式
-   ±8 のタイプ分類閾値
-   validation_flag 閾値
-   CSV 列構造
-   20--30m を速度 benchmark で管理する方式

これらは、動画解析ベース・低設備・U12育成用途に合わせた
**実務設計上のルール**である。
