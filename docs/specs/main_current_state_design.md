# mainブランチ現状設計書（現状記述版 v1.1）

---

## 0. 本資料の基本情報

| 項目 | 内容 |
|------|------|
| 対象ブランチ | main |
| 対象リポジトリ | jera-takanabe/Togo-physical-training |
| 作成目的 | 現状の固定化 |
| 更新方針 | 原則更新しない（スナップショット） |

---

## 1. 本資料の位置づけ

本資料は、**mainブランチ時点の状態をそのまま記述するスナップショット設計書**である。

目的：

- 現在の構造を固定する
- 将来の再設計の比較基準とする
- 「何があったか」を失わない

本資料では以下を厳守する：

- 設計改善を書かない
- 理想を書かない
- 不整合もそのまま書く

---

## 2. スコープ

### 2.1 対象

- ディレクトリ構成
- データ構造
- スクリプト構成
- パイプライン
- 設計資料
- ダッシュボード出力

### 2.2 非対象

以下は意図的に扱わない：

- 改善提案
- リファクタリング方針
- 新設計
- 最適化

---

## 3. 参照資料

本資料は以下を前提とする。

- README.md
- docs/index.md
- docs/architecture/*
- docs/analytics/*
- docs/protocols/*
- scripts/*
- data/*
- .github/workflows/pipeline.yml

---

## 4. リポジトリの目的

READMEにおいて定義されている目的：

- 測定結果の継続保存
- 年齢別目標の管理
- 強み・課題の可視化
- トレーニングへの反映

長期目標：

- 100m：10.5秒
- Vertical Jump：100cm
- Standing Long Jump：350cm

---

## 5. 全体構成

| 区分 | 内容 |
|------|------|
| 入力 | data/raw |
| 集計 | data/processed |
| 参照 | data/reference |
| ドキュメント | docs |
| スクリプト | scripts |
| 出力 | docs/dashboards |
| 自動化 | GitHub Actions |

処理フロー：

測定 → 集計 → スコア → 可視化

---

## 6. ディレクトリ構成

### 6.1 ルート

```text
.github/workflows
archive
config
data
docs
scripts
README.md
```

---

### 6.2 docs

```text
docs/
├── analytics
├── architecture
├── athletes/togo
├── dashboards
├── growth_models
├── philosophy
├── protocols
├── references
├── training_blocks
├── glossary.md
└── index.md
```

---

### 6.3 data

```text
data/
├── raw
├── processed
├── reference
├── test_results.csv
└── growth_tracking.csv
```

---

### 6.4 scripts

```text
scripts/
├── analyze_tests.py
├── build_latest_summary.py
├── build_sessions.py
├── calc_rugby_physical_score.py
├── generate_growth_trend_chart.py
├── generate_radar_chart.py
├── generate_target_radar_v2.py
├── run_pipeline.py
├── update_dashboard.py
├── update_personal_bests.py
├── validate_data.py
└── utils/
```

---

## 7. データモデル

### raw

- 試技データ
- セッション情報

### processed

- セッション単位データ
- パーソナルベスト

### reference

- benchmark
- target
- test定義

---

## 8. 設定

```text
config/
├── athlete_profile.yaml
└── language.yaml
```

- current_stage: JH1
- language: jp

---

## 9. パイプライン

実行順序：

1. validate
2. session生成
3. PB更新
4. スコア算出
5. サマリー生成
6. レーダー生成
7. トレンド生成
8. ターゲット比較

---

## 10. GitHub Actions

- Python 3.11
- pandas
- pipeline実行
- 自動commit

対象：

- data/processed
- docs/dashboards

---

## 11. ダッシュボード

出力：

- latest_summary.md
- radar_chart.png
- score_trend
- target比較

---

## 12. 選手情報

対象：

- 小6ラグビー選手

構成：

- profile
- physical_map
- roadmap

---

## 13. 評価モデル

構造：

test → score → domain → total

ドメイン（5）：

- Acceleration
- COD
- Reactive Strength
- Explosive Power
- Upper Body Power

---

## 14. 設計資料の状態

| 種類 | 状態 |
|------|------|
| スコア設計 | 実装あり |
| ドメイン設計 | 8ドメイン定義あり |
| analysisレイヤー | 構想のみ |
| analytics | 個別分析 |

---

## 15. 現状の差異

- 5ドメイン vs 8ドメイン
- README vs 実装
- analysis層未実装

---

## 16. 利用方法

### 読み手

- 自分（設計者）
- 将来の自分
- 再設計時の基準

### 使い方

- 差分比較
- リファクタ前確認
- 設計判断の根拠

---

## 17. 更新方針（重要）

本資料は以下のルールで扱う：

- ❌ 追記しない
- ❌ 修正しない
- ❌ 改善を書かない
- ⭕ 新しい状態は別資料で作る

---

## 18. 結論

本リポジトリは以下の複合体である：

1. 測定記録
2. 分析パイプライン
3. 設計資料群

---

## 19. 次に作るべき資料

- 俯瞰資料（overview）
- 再設計仕様（v2）
- ドメイン再定義

---