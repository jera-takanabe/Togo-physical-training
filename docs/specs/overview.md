# 全体俯瞰資料（軽量版）

---

## 1. このシステムの目的

- 測定データを記録する
- 成長を可視化する
- トレーニング判断に活かす

---

## 2. 全体構造

```
測定（raw）
↓
集計（processed）
↓
スコア（domain / total）
↓
可視化（dashboard）
↓
判断（トレーニング）
```

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

### ③ 評価（scoring）

- scripts/calc_rugby_physical_score.py

👉 テスト → スコア → ドメイン → 総合

---

### ④ 可視化（output）

- docs/dashboards/*
- latest_summary.md
- radar_chart.png

---

### ⑤ 活用（use）

- トレーニング判断
- 課題抽出
- 成長確認

---

## 4. 現在の主な構成要素

### データ

- raw：測定データ
- processed：集計データ
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
- dashboards：出力

---

## 5. 現在の課題位置

### 🔴 測定 → トレーニング

- 数値はあるが判断につながっていない

---

### 🟡 評価体系

- ドメイン定義が不統一
- RSA / YOYO 未統合

---

### 🟡 表現

- 指標が多く分かりにくい

---

## 6. 改善の方向

### Phase 1（今）

- 構造理解
- 軽微整理

---

### Phase 2

- 評価体系整理

---

### Phase 3

- トレーニング接続

---

## 7. この資料の役割

- 全体の位置関係を把握するための資料
- 詳細設計は各specsに委ねる

---
