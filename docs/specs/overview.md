# 全体俯瞰資料（軽量版）

---

## 1. このシステムの目的

- 測定データを記録する
- 成長を可視化する
- トレーニング判断に活かす
- 改善サイクルを回し続ける

---

## 2. 全体構造（重要）

このシステムは以下のサイクルで動く
このサイクルをセッションとする
session_id は測定日ではなく、測定セット（分析単位）を表す

```
測定（raw）
↓
集計（processed）
↓
スコア（analysis）
↓
可視化（dashboard）
↓
判断（decision）
↓
実行（training）
↓
再測定
↓
次の判断
```

👉 実行で終わらず、必ず再測定に戻る

---

## 3. データの流れ

### ① 測定（input）

- data/raw/*
- 各種テストデータ（sprint / jump / RSA / YOYO / MBT）

---

### ② 集計（processing）

- scripts/build_sessions.py
- scripts/update_personal_bests.py

👉 試技 → セッション / PB

---

### ③ 評価（analysis）

- scripts/calc_rugby_physical_score.py

👉 テスト → スコア → ドメイン → 総合

---

### ④ 可視化（output）

- docs/dashboards/*
- latest_summary.md
- radar_chart.png

---

### ⑤ 判断（decision）

- decision_log_*.md

👉 何を伸ばすか決める

---

### ⑥ 実行（training）

👉 トレーニング実施

---

### ⑦ 観察（logs）

- daily_notes.md
- weekly_checklist

👉 変化の兆しを記録

---

## 4. 現在の主な構成要素

### データ

- raw：測定データ
- processed：集計データ
- analysis：スコア
- reference：基準値

---

### スクリプト

- パイプライン：run_pipeline.py
- 集計系
- スコア系
- 可視化系

---

### ドキュメント

- specs：設計
- protocols：測定方法
- analysis：分析
- decision：判断
- logs：観察
- dashboards：出力

---

## 5. 現在の課題位置

### 🔴 判断 → 実行

- 数値はあるが、トレーニングに完全には接続されていない

---

### 🟡 評価体系

- ドメイン定義が不統一
- RSA / YOYO 未統合

---

### 🟡 表現

- 指標が多く分かりにくい

---

## 6. 改善の方向

### Phase 1（完了）

- 構造理解
- ドキュメント整理

---

### Phase 2（次）

- 評価体系整理
- ドメイン統一

---

### Phase 3

- トレーニング接続の強化

---

## 7. この資料の役割

- 全体のサイクルを理解するための入口
- 迷ったときに戻る場所
- 詳細は各ドキュメントに委ねる

---
