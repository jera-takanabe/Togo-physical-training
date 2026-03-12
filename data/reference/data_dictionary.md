# Data Dictionary
Togo Physical Training Repository

このファイルは測定データCSVの項目定義をまとめたものです。

---

# 1. Jump Tests

対象ファイル:
- `data/raw/myjump/jumps_raw.csv`

ジャンプ系測定データ。主に My Jump Lab で解析する。

| 列名 | 日本語名 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベントを識別するID。同日に複数種目を測る場合も同じIDを付与する。例: `2026-03-08_test1` |
| date | 測定日 | 測定日。形式は `YYYY-MM-DD` |
| athlete | 選手ID | 選手名または識別子。例: `togo` |
| test_type | テスト種別 | ジャンプ種別。例: `CMJ`, `SJ`, `DJ`, `RSI` |
| trial | 試技番号 | その種目内の試技番号。1, 2, 3 ... |
| device | 測定ツール | 使用した解析ツール。基本は `MyJumpLab` |
| video_file | 動画ファイル名 | 元動画ファイル名 |
| fps | フレームレート | 動画のフレームレート。例: `240` |
| jump_height_cm | ジャンプ高 | ジャンプ高。単位は cm |
| contact_time_ms | 接地時間 | 接地時間。単位は ms。RSI系で主に使用 |
| flight_time_ms | 滞空時間 | 滞空時間。単位は ms |
| rsi | RSI | Reactive Strength Index |
| surface | 路面 | 実施路面。例: `track`, `grass`, `gym` |
| shoes | シューズ | 使用シューズ。例: `spike`, `trainer` |
| sleep_hours | 睡眠時間 | 前日の睡眠時間。単位は時間 |
| fatigue | 疲労度 | 主観疲労。1〜5で評価 |
| pain | 痛み | 痛みの程度。0〜5で評価 |
| memo | メモ | 任意メモ |

## 1.1 Jump Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| SJ | スクワットジャンプ | 反動を使わず静止姿勢から跳ぶジャンプ |
| CMJ | カウンタームーブメントジャンプ | 反動ありの垂直ジャンプ |
| DJ | ドロップジャンプ | 台から降りて接地後すばやく跳ぶジャンプ |
| RSI | リアクティブストレングス指標 | 主に Drop Jump の跳躍高と接地時間から算出 |
| SLJ | 立ち幅跳び | 水平方向の爆発力を見るジャンプ |
| Hop_L | 左片脚ホップ | 左脚の片脚ホップ |
| Hop_R | 右片脚ホップ | 右脚の片脚ホップ |

---

# 2. Sprint Tests

対象ファイル:
- `data/raw/kinovea/sprints_raw.csv`

スプリント系測定データ。主に Kinovea で解析する。

| 列名 | 日本語名 | 説明 |
|---|---|---|
| session_id | セッションID | 同一測定イベントを識別するID。例: `2026-03-08_test1` |
| date | 測定日 | 測定日。形式は `YYYY-MM-DD` |
| athlete | 選手ID | 選手名または識別子。例: `togo` |
| test_type | テスト種別 | スプリント種別。例: `sprint_10m`, `sprint_30m` |
| trial | 試技番号 | その種目内の試技番号。1, 2, 3 ... |
| device | 測定ツール | 使用した解析ツール。基本は `Kinovea` |
| video_file | 動画ファイル名 | 元動画ファイル名 |
| fps | フレームレート | 動画のフレームレート |
| start_rule | スタート判定ルール | どの瞬間をスタートとするか。例: `rear_foot_off` |
| finish_rule | ゴール判定ルール | どの瞬間をゴールとするか。例: `chest_line` |
| split_5m_s | 5m通過時間 | 5m地点の通過時間。単位は秒 |
| split_10m_s | 10m通過時間 | 10m地点の通過時間。単位は秒 |
| split_20m_s | 20m通過時間 | 20m地点の通過時間。単位は秒 |
| split_30m_s | 30m通過時間 | 30m地点の通過時間。単位は秒 |
| total_time_s | 総タイム | 全区間のタイム。単位は秒 |
| camera_position | カメラ位置 | 撮影位置。例: `side_15m` |
| surface | 路面 | 実施路面。例: `track`, `grass` |
| shoes | シューズ | 使用シューズ |
| wind | 風 | 風の影響や風速メモ。必要に応じて記録 |
| memo | メモ | 任意メモ |

## 2.1 Sprint Test Type

| test_type | 日本語名 | 説明 |
|---|---|---|
| sprint_10m | 10mスプリント | 10mの加速評価 |
| sprint_20m | 20mスプリント | 20mまでの加速評価 |
| sprint_30m | 30mスプリント | 30mまでの加速〜初期最高速度評価 |
| flying_10m | 助走付き10m | 最高速度局面の評価 |
| pro_agility | プロアジリティ | 切り返し能力評価 |
| 505_left | 505左 | 左方向の505テスト |
| 505_right | 505右 | 右方向の505テスト |

---

# 3. Fatigue Scale

| 値 | 定義 |
|---|---|
| 1 | 非常に良い |
| 2 | 良い |
| 3 | 普通 |
| 4 | 疲労あり |
| 5 | 非常に疲労 |

---

# 4. Pain Scale

| 値 | 定義 |
|---|---|
| 0 | 痛みなし |
| 1 | 軽い痛み |
| 2 | 少し気になる |
| 3 | 中程度の痛み |
| 4 | 強い痛み |
| 5 | テスト中止レベル |

---

# 5. Current Measurement Policy

現時点の基本運用ルール:

- CMJ は 3回試技で実施する
- 代表値としてはベストを重視する
- 将来的には `raw` から `processed` を自動生成し、best / avg / std を保持する
- ジャンプ系は My Jump Lab、スプリント系は Kinovea を使用する