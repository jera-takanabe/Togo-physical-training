# Data Dictionary
Togo Physical Training Repository

このファイルは、本リポジトリで扱う測定データの定義、運用ルール、スキーマをまとめたものです。  
本リポジトリでは、測定データを **trial-level（試技単位）** で raw に保存し、そこから processed データを自動生成します。

---

# 1. Design Principles

## 1.1 Data Layers

本リポジトリでは、データを次の3層で管理する。

### raw
- 試技単位の元データ
- 1行 = 1試技
- 測定条件やコンディションも含めて保存する
- 再集計・再分析可能な形で保持する

### processed
- raw から自動生成される集計データ
- session 単位の best / avg / std を保持する
- personal best や dashboard 用データを保持する

### reference
- データ定義
- テスト種目辞書
- スケール定義
- 運用ルール
- 年齢別目標や基準値

---

## 1.2 Session and Trial

### session_id
同一測定イベントを識別するID。  
同日に複数種目を測定しても、同じ測定イベントであれば同じ `session_id` を付与する。

例:
- `2026-03-08_test1`
- `2026-04-12_test1`

### trial
同一種目内の試技番号。

例:
- CMJ 1回目 → `trial = 1`
- CMJ 2回目 → `trial = 2`
- 30m走 1本目 → `trial = 1`

---

## 1.3 Athlete Identifier

### athlete
選手名または識別子。  
現時点では `togo` を使用する。

---

# 2. Raw Data Files

## 2.0 Measurement Sessions

対象ファイル:
- `data/raw/measurement_sessions.csv`

測定セッション共通情報を保持する台帳。  
同じ `session_id` に属する sprint / cod / jump / horizontal / throw の raw データは、このセッション情報に紐づく。

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベント識別子 |
| date | 測定日 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| location | 測定場所 | 例: `academy_field`, `school_ground` |
| surface | 路面 | 例: `track`, `grass`, `asphalt`, `gym` |
| shoes | シューズ | 例: `spike`, `trainer`, `スニーカー` |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| body_weight_kg | 体重 | 単位は kg |
| height_cm | 身長 | 単位は cm |
| practice_load | 練習負荷 | 主観または簡易負荷指標 |
| weather | 天候 | 例: `sunny`, `cloudy`, `rainy`, `晴れ` |
| temperature_c | 気温 | 単位は ℃ |
| wind | 風 | 風速または風のメモ |
| notes | 備考 | 任意メモ |

---

## 2.1 Sprint Tests

対象ファイル:
- `data/raw/sprint_tests_raw.csv`

直線スプリント系の測定データ。

対象種目:
- 30m走
- Fly5
- Fly10

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベント識別子 |
| date | 測定日 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| test_type | テスト種別 | `sprint_30m`, `fly_5m`, `fly_10m` |
| trial | 試技番号 | 1, 2, 3 ... |
| valid | 集計対象フラグ | `true` なら集計対象、`false` なら記録のみで集計から除外 |
| device | 測定ツール | 例: `Kinovea` |
| video_file | 動画ファイル | 元動画ファイル名 |
| fps | フレームレート | 動画FPS。例: `240` |
| start_rule | スタート判定 | どの瞬間をスタートとしたか |
| finish_rule | ゴール判定 | どの瞬間をゴールとしたか |
| split_5m_s | 5m通過時間 | 単位は秒 |
| split_10m_s | 10m通過時間 | 単位は秒 |
| split_20m_s | 20m通過時間 | 単位は秒 |
| split_30m_s | 30m通過時間 | 単位は秒 |
| fly_5m_s | Fly5タイム | 助走付き5m区間タイム。単位は秒 |
| fly_10m_s | Fly10タイム | 助走付き10m区間タイム。単位は秒 |
| total_time_s | 総タイム | テスト全体のタイム。単位は秒 |
| camera_position | カメラ位置 | 例: `side_15m` |
| surface | 路面 | 例: `track`, `grass`, `asphalt`, `gym` |
| shoes | シューズ | 使用シューズ |
| wind | 風 | 風速または風のメモ |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| memo | メモ | 任意メモ |

### Sprint Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| sprint_30m | 30m走 | 10m, 20m, 30mの通過タイムと全体タイムを記録する |
| fly_5m | Fly5 | 助走付き5m区間タイム |
| fly_10m | Fly10 | 助走付き10m区間タイム |

---

## 2.2 COD Tests

対象ファイル:
- `data/raw/cod_tests_raw.csv`

方向転換（COD）系の測定データ。

対象種目:
- Pro Agility（= 5-10-5）

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベント識別子 |
| date | 測定日 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| test_type | テスト種別 | `pro_agility` など |
| trial | 試技番号 | 1, 2, 3 ... |
| side | 左右 | `left` / `right`。左右区別なしは空欄 |
| valid | 集計対象フラグ | `true` なら集計対象、`false` なら記録のみで集計から除外 |
| device | 測定ツール | 例: `Kinovea` |
| video_file | 動画ファイル | 元動画ファイル名 |
| fps | フレームレート | 動画FPS |
| start_rule | スタート判定 | どの瞬間をスタートとしたか |
| finish_rule | ゴール判定 | どの瞬間をゴールとしたか |
| segment_1_s | 区間1タイム | 必要に応じて記録。単位は秒 |
| segment_2_s | 区間2タイム | 必要に応じて記録。単位は秒 |
| segment_3_s | 区間3タイム | 必要に応じて記録。単位は秒 |
| total_time_s | 総タイム | テスト全体のタイム。単位は秒 |
| camera_position | カメラ位置 | 例: `side_15m` |
| surface | 路面 | 例: `track`, `grass`, `asphalt`, `gym` |
| shoes | シューズ | 使用シューズ |
| wind | 風 | 風速または風のメモ |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| memo | メモ | 任意メモ |

### COD Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| pro_agility | Pro Agility | 5-10-5 shuttle と同義で扱うCODテスト |

### side

| 値 | 意味 |
|---|---|
| left | 左方向 / 左脚側 |
| right | 右方向 / 右脚側 |
| 空欄 | 左右区別なし |

---

## 2.3 Jump Tests

対象ファイル:
- `data/raw/jump_tests_raw.csv`

垂直方向ジャンプ系の測定データ。

対象種目:
- CMJ
- SJ
- DJ

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベント識別子 |
| date | 測定日 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| test_type | テスト種別 | `CMJ`, `SJ`, `DJ` |
| trial | 試技番号 | 1, 2, 3 ... |
| valid | 集計対象フラグ | `true` なら集計対象、`false` なら記録のみで集計から除外 |
| device | 測定ツール | 例: `MyJumpLab` |
| video_file | 動画ファイル | 元動画ファイル名 |
| fps | フレームレート | 動画FPS |
| jump_height_cm | ジャンプ高 | 単位は cm |
| contact_time_ms | 接地時間 | 単位は ms。主に DJ で使用 |
| flight_time_ms | 滞空時間 | 単位は ms |
| rsi | RSI | Reactive Strength Index |
| surface | 路面 | 例: `track`, `gym`, `asphalt` |
| shoes | シューズ | 使用シューズ |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| memo | メモ | 任意メモ |

### Jump Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| CMJ | カウンタームーブメントジャンプ | 反動ありの垂直ジャンプ |
| SJ | スクワットジャンプ | 静止姿勢からの垂直ジャンプ |
| DJ | ドロップジャンプ | 接地反応と跳躍をみるジャンプ |

---

## 2.4 Horizontal Tests

対象ファイル:
- `data/raw/horizontal_tests_raw.csv`

水平方向の跳躍系・バウンディング系の測定データ。

対象種目:
- 立ち幅跳び
- 10バウンディング
- 5HOP

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベント識別子 |
| date | 測定日 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| test_type | テスト種別 | `standing_long_jump`, `bounding_10`, `hop_5` |
| trial | 試技番号 | 1, 2, 3 ... |
| side | 左右 | `left` / `right`。不要な種目は空欄 |
| valid | 集計対象フラグ | `true` なら集計対象、`false` なら記録のみで集計から除外 |
| device | 測定ツール | 記録方法。空欄でも可 |
| video_file | 動画ファイル | 元動画ファイル名。空欄可 |
| fps | フレームレート | 動画がある場合のFPS。空欄可 |
| distance_cm | 距離 | 単位は cm |
| surface | 路面 | 例: `track`, `grass`, `asphalt`, `gym` |
| shoes | シューズ | 使用シューズ |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| memo | メモ | 任意メモ |

### Horizontal Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| standing_long_jump | 立ち幅跳び | 両脚での水平ジャンプ |
| bounding_10 | 10バウンディング | 10歩の連続バウンド距離 |
| hop_5 | 5HOP | 片脚5歩ホップ距離 |

### side

| 値 | 意味 |
|---|---|
| left | 左脚 / 左方向 |
| right | 右脚 / 右方向 |
| 空欄 | 左右区別なし |

---

## 2.5 Throw Tests

対象ファイル:
- `data/raw/throw_tests_raw.csv`

投てき系の測定データ。

対象種目:
- ラグビーボール投げ

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベント識別子 |
| date | 測定日 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| test_type | テスト種別 | `rugby_ball_throw` |
| trial | 試技番号 | 1, 2, 3 ... |
| valid | 集計対象フラグ | `true` なら集計対象、`false` なら記録のみで集計から除外 |
| device | 測定ツール | 測定方法。空欄可 |
| video_file | 動画ファイル | 元動画ファイル名。空欄可 |
| distance_m | 距離 | 単位は m |
| surface | 路面 | 例: `track`, `grass`, `asphalt`, `gym` |
| shoes | シューズ | 使用シューズ |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| memo | メモ | 任意メモ |

### Throw Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| rugby_ball_throw | ラグビーボール投げ | 上半身・全身のパワー指標として使う投てきテスト |

---

## 2.6 Readiness / Growth

対象ファイル:
- `data/raw/readiness/daily_readiness.csv`

コンディション・成長管理用データ。  
競技パフォーマンスの背景情報として扱う。

### Columns

| column | 日本語 | 説明 |
|---|---|---|
| date | 日付 | `YYYY-MM-DD` |
| athlete | 選手ID | 例: `togo` |
| sleep_hours | 睡眠時間 | 前日の睡眠時間 |
| fatigue | 疲労度 | 主観疲労。1〜5 |
| pain | 痛み | 痛みの程度。0〜5 |
| body_weight_kg | 体重 | 単位は kg |
| height_cm | 身長 | 単位は cm |
| practice_load | 練習負荷 | 主観または簡易負荷指標 |
| notes | メモ | 任意メモ |

---

# 3. Processed Data Files

## 3.1 Sprint Sessions
- `data/processed/sprint_sessions.csv`

`sprint_tests_raw.csv` から `valid=true` の行のみを対象に集計した session 単位データ。

主な出力:
- `trials`
- `best_split_10m_s`
- `avg_split_10m_s`
- `std_split_10m_s`
- `best_total_time_s`

time 系なので、best は **最小値**。

---

## 3.2 COD Sessions
- `data/processed/cod_sessions.csv`

`cod_tests_raw.csv` から `valid=true` の行のみを対象に、`side` 別で集計した session 単位データ。

主な出力:
- `side`
- `trials`
- `best_total_time_s`
- `avg_total_time_s`
- `std_total_time_s`

time 系なので、best は **最小値**。

---

## 3.3 Jump Sessions
- `data/processed/jump_sessions.csv`

`jump_tests_raw.csv` から `valid=true` の行のみを対象に集計した session 単位データ。

主な出力:
- `best_jump_height_cm`（最大）
- `avg_jump_height_cm`
- `std_jump_height_cm`
- `best_contact_time_ms`（最小）
- `best_flight_time_ms`（最大）
- `best_rsi`（最大）

---

## 3.4 Horizontal Sessions
- `data/processed/horizontal_sessions.csv`

`horizontal_tests_raw.csv` から `valid=true` の行のみを対象に、必要に応じて `side` 別で集計した session 単位データ。

主な出力:
- `best_distance_cm`
- `avg_distance_cm`
- `std_distance_cm`

distance 系なので、best は **最大値**。

---

## 3.5 Throw Sessions
- `data/processed/throw_sessions.csv`

`throw_tests_raw.csv` から `valid=true` の行のみを対象に集計した session 単位データ。

主な出力:
- `best_distance_m`
- `avg_distance_m`
- `std_distance_m`

distance 系なので、best は **最大値**。

---

## 3.6 Personal Bests
- `data/processed/personal_bests.csv`

カテゴリ別 session データから生成される自己ベスト一覧。

主な列:
- `athlete`
- `test_type`
- `metric_name`
- `best_value`
- `unit`
- `date`
- `session_id`
- `side`

---

# 4. Scales

## 4.1 Fatigue Scale

| 値 | 定義 |
|---|---|
| 1 | 非常に良い |
| 2 | 良い |
| 3 | 普通 |
| 4 | 疲労あり |
| 5 | 非常に疲労 |

## 4.2 Pain Scale

| 値 | 定義 |
|---|---|
| 0 | 痛みなし |
| 1 | 軽い痛み |
| 2 | 少し気になる |
| 3 | 中程度の痛み |
| 4 | 強い痛み |
| 5 | テスト中止レベル |

---

# 5. Validation Policy

## 5.1 Error
次の条件は validation error とし、pipeline を停止する。

- 必須ファイルが存在しない
- 必須列が不足している
- `session_id` が `measurement_sessions.csv` に存在しない
- `test_type` が `test_definitions.csv` に存在しない
- 数値列に不正値が入っている
- `valid` が `true / false` 以外
- `pro_agility` / `hop_5` で `side` が不正

## 5.2 Warning
次の条件は warning とし、pipeline は継続する。

- 規定の有効試技数に不足がある
- 規定より多い試技数がある
- 参考記録を除外した結果、有効試技数が不足する

---

# 6. Trial Count Policy

現時点の規定有効試技数は次の通り。

| test_type | 規定 |
|---|---|
| sprint_30m | 2 |
| CMJ | 3 |
| SJ | 3 |
| DJ | 3 |
| standing_long_jump | 3 |
| bounding_10 | 2 |
| rugby_ball_throw | 3 |
| pro_agility | 左右それぞれ 1 |
| hop_5 | 左右それぞれ 2 |

---

# 7. Current Measurement Policy

現時点の基本運用ルール:

- raw データは試技単位で保存する
- processed データは raw から自動生成する
- session 単位では best / avg / std を保持する
- `valid=false` の行は記録として残すが集計から除外する
- スプリント系とCOD系は Kinovea を使用する
- ジャンプ系は My Jump Lab を使用する
- 距離系テストは測定値を raw に保存する
- コンディション系データは readiness / growth として別管理する

---

# 8. Current Test Menu

## Sprint
- 30m走（10m, 20m, 30m, Fly5, Fly10）

## COD
- Pro Agility（= 5-10-5）

## Jump
- CMJ
- SJ
- DJ

## Horizontal
- 立ち幅跳び
- 10バウンディング
- 5HOP

## Throw
- ラグビーボール投げ

## Readiness / Growth
- 睡眠
- 疲労
- 痛み
- 身長
- 体重
- 練習負荷

---

# 9. Future Extension Policy

今後、測定項目が増えることを前提とする。

追加候補:
- 505
- T-test
- L-drill
- インターバル / 回復系テスト
- 反復スプリント
- 持久系
- 心肺系
- 試合パフォーマンス指標
- コーチ評価
- 成長スパート監視
- 回復指標

拡張時の基本方針:

1. raw は試技または日単位の元データを保持する
2. processed は raw から自動生成する
3. reference に定義を追加する
4. 既存スキーマを壊さず、新ファイル追加で拡張する
5. `measurement_sessions.csv` を将来的な正規化の親テーブルとして活用する