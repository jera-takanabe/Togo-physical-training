# ドキュメント構造（俯瞰）

---

## 1. 本資料の目的

本資料は、プロジェクト内のドキュメントの関係性を整理するための入口資料である。

目的は以下とする。

- どの資料を見ればよいか分かるようにする
- 俯瞰資料から詳細資料への関係を明確にする
- 測定 → 分析 → 判断 → 実行 → 再測定 のサイクルを迷わず回せるようにする

---

## 2. 全体サイクル

このプロジェクトは、以下のサイクルで運用する。

```text
目的・方針
↓
現状把握
↓
測定
↓
分析
↓
判断
↓
実行
↓
観察
↓
再測定
↓
次の判断
```

重要なのは、実行で終わりではなく、再測定によって次の判断につなげることである。

---

## 3. ドキュメント群の役割

### 3.1 俯瞰・入口

| 資料 | 役割 |
|---|---|
| overview.md | システム全体の流れを把握する |
| document_map.md | ドキュメントの関係性を把握する |
| target_vision_memo.md | どこを目指すかを整理する |

---

### 3.2 現状固定

| 資料 | 役割 |
|---|---|
| main_current_state_design.md | mainブランチ時点の現状を固定する |
| u_12_ラグビーs_c分析システム_俯瞰資料_v_1.md | 旧来の俯瞰・検討内容を残す |

現状固定資料は、原則として頻繁に更新しない。

---

### 3.3 設計・計画

| 資料 | 役割 |
|---|---|
| gap_analysis.md | 現状と目指す姿の差分を整理する |
| improvement_plan.md | 改善の進め方を整理する |
| training_decision_rule.md | 測定・観察からトレーニング判断へつなげるルール |
| decision_log_design.md | 判断履歴をどう残すかの設計 |

---

### 3.4 測定・記録ルール

| 資料 | 役割 |
|---|---|
| data_recording_rule.md | rawデータの記録ルール |
| weekly_checklist.md | 週次観察の観点 |
| sprint_measurement_protocol.md | スプリント測定手順 |
| jump_measurement_protocol.md | ジャンプ測定手順 |
| rsa_measurement_protocol.md | RSA測定手順 |
| yo-yo_ir1_protocol.md | Yo-Yo IR1測定手順 |
| cmj.md / sj.md / rsi.md / sprint_10m_30m.md | 既存の種目別手順 |

---

### 3.5 分析資料

| 資料 | 役割 |
|---|---|
| sprint_analysis.md | スプリント分析 |
| jump_analysis.md | ジャンプ分析 |
| asymmetry_analysis.md | 左右差分析 |

---

### 3.6 判断ログ

| 資料 | 役割 |
|---|---|
| decision_log_*.md | 実際に何を判断したかを残す |

decision_log は、測定結果または観察結果をもとにした正式な判断記録である。

---

### 3.7 日次・週次メモ

| 資料 | 役割 |
|---|---|
| daily_notes.md | 日々の気づきを軽く残す |
| weekly_checklist/* | 週次観察の作業メモ |

日次・週次メモは decision_log の材料であり、最終判断ではない。

---

### 3.8 ダッシュボード

| 資料 | 役割 |
|---|---|
| latest_summary.md | 最新測定結果のサマリー |
| radar_chart.png | レーダーチャート |
| target_radar_v2.png | 目標比較 |
| trend系画像 | 推移確認 |

---

## 4. 俯瞰から詳細への関係

```text
overview.md
├── target_vision_memo.md
├── main_current_state_design.md
├── gap_analysis.md
├── improvement_plan.md
└── document_map.md

training_decision_rule.md
├── decision_log_design.md
└── decision_log_*.md

data_recording_rule.md
├── 各 raw CSV
└── measurement_sessions.csv

weekly_checklist.md
├── daily_notes.md
└── decision_log_*.md

dashboards/
└── latest_summary.md
```

---

## 5. 実運用で使う順序

### 5.1 測定前

1. `document_map.md` で資料の位置づけを確認する
2. `data_recording_rule.md` を確認する
3. 必要に応じて各 measurement protocol を確認する

---

### 5.2 測定後

1. rawデータを記録する
2. pipelineを実行する
3. `latest_summary.md` を確認する
4. 必要に応じて decision_log を作成する

---

### 5.3 トレーニング運用中

1. `daily_notes.md` に軽く記録する
2. `weekly_checklist.md` の観点で週次確認する
3. `decision_log_*.md` に判断を残す

---

### 5.4 設計を見直すとき

1. `overview.md` を見る
2. `target_vision_memo.md` を見る
3. `gap_analysis.md` を更新する
4. `improvement_plan.md` を更新する

---

## 6. 現在の配置と将来の整理方針

現時点では、既存の `docs/specs`, `docs/protocols`, `docs/logs`, `docs/analytics`, `docs/dashboards` を維持する。

将来的には、必要に応じて以下のような役割別構成に整理する。

```text
docs/
├── 00_overview
├── 01_current_state
├── 02_specs
├── 03_protocols
├── 04_analysis
├── 05_decision
├── 06_logs
├── 07_dashboards
└── 99_archive
```

ただし、現時点では物理的な移動を急がない。  
まずは本資料で関係性を明確にし、必要になった段階で段階的に移動する。

---

## 7. 迷ったとき

迷った場合は、以下の順に確認する。

1. `document_map.md`
2. `overview.md`
3. `target_vision_memo.md`
4. `gap_analysis.md`
5. `improvement_plan.md`

---

## 8. 原則

- 完璧に整理しようとしない
- 分からなくなったら俯瞰に戻る
- 設計と運用を混ぜすぎない
- 測定・記録・判断の流れを止めない
- 物理的なファイル移動は段階的に行う

---