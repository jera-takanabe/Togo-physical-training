# Data Dictionary
Togo Physical Training Repository

このファイルは測定データCSVの項目定義をまとめたものです。

---

# 1 Jump Tests (jumps_raw.csv)

ジャンプ系測定データ  
主に My Jump Lab で解析

|列名|日本語|説明|
|---|---|---|
session_id | セッションID | 同一測定イベント識別子 |
date | 測定日 | YYYY-MM-DD |
athlete | 選手ID | 選手名またはID |
test_type | テスト種別 | SJ / CMJ / DJ / RSI 等 |
trial | 試技番号 | 1,2,3... |
device | 測定ツール | MyJumpLab |
video_file | 動画ファイル | 元動画 |
fps | フレームレート | 動画FPS |
jump_height_cm | ジャンプ高さ | cm |
contact_time_ms | 接地時間 | ms |
flight_time_ms | 滞空時間 | ms |
rsi | Reactive Strength Index | jump_height / contact_time |
surface | 路面 | track / grass / gym |
shoes | シューズ | spike / trainer |
sleep_hours | 睡眠時間 | 前日の睡眠 |
fatigue | 疲労度 | 1〜5 |
pain | 痛み | 0〜5 |
memo | メモ | 任意 |

---

# Jump Test Type

|test_type|説明|
|---|---|
SJ | Squat Jump |
CMJ | Countermovement Jump |
DJ | Drop Jump |
RSI | Reactive Strength Index |
SLJ | Standing Long Jump |
Hop_L | 左片脚ホップ |
Hop_R | 右片脚ホップ |

---

# 2 Sprint Tests (sprints_raw.csv)

スプリント系測定データ  
主に Kinovea で解析

|列名|日本語|説明|
|---|---|---|
session_id | セッションID | 同一測定イベント |
date | 測定日 | YYYY-MM-DD |
athlete | 選手ID | 選手名 |
test_type | テスト種別 | sprint_10m 等 |
trial | 試技番号 | 試技 |
device | 測定ツール | Kinovea |
video_file | 動画ファイル | 元動画 |
fps | フレームレート | 動画FPS |
start_rule | スタート判定 | rear_foot_off 等 |
finish_rule | ゴール判定 | chest_line 等 |
split_5m_s | 5mタイム | 秒 |
split_10m_s | 10mタイム | 秒 |
split_20m_s | 20mタイム | 秒 |
split_30m_s | 30mタイム | 秒 |
total_time_s | 総タイム | 秒 |
camera_position | カメラ位置 | side_15m 等 |
surface | 路面 | track / grass |
shoes | シューズ | spike |
wind | 風 | m/s |
memo | メモ | 任意 |

---

# Sprint Test Type

|test_type|説明|
|---|---|
sprint_10m | 10mスプリント |
sprint_20m | 20mスプリント |
sprint_30m | 30mスプリント |
flying_10m | 助走付き10m |
pro_agility | プロアジリティ |
505_left | 505左 |
505_right | 505右 |

---

# Fatigue Scale

|値|意味|
|---|---|
1 | 非常に良い |
2 | 良い |
3 | 普通 |
4 | 疲労 |
5 | 非常に疲労 |

---

# Pain Scale

|値|意味|
|---|---|
0 | 痛みなし |
1 | 軽い |
2 | 気になる |
3 | 中程度 |
4 | 強い |
5 | テスト中止 |