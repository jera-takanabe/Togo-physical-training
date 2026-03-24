# ドキュメント構造（俯瞰）

---

## 1. 全体構造

```
目的（target_vision）
↓
課題（gap_analysis）
↓
計画（improvement_plan）
↓
実行（decision / training）
↓
観察（weekly_checklist）
↓
改善（次のdecision）
```

---

## 2. ドキュメント一覧と役割

### ■ 方向

- target_vision_memo.md  
👉 どこを目指すか

---

### ■ 問題

- gap_analysis.md  
👉 何が足りないか

---

### ■ 計画

- improvement_plan.md  
👉 どう進めるか

---

### ■ 構造理解

- overview.md  
👉 全体の流れ

---

### ■ 判断ルール

- training_decision_rule.md  
👉 どう判断するか

---

### ■ 判断履歴

- decision_log_*.md  
👉 実際にどう判断したか

---

### ■ 観察

- weekly_checklist.md  
👉 何が変わったか

---

### ■ データルール

- data_recording_rule.md  
👉 どう記録するか

---

### ■ 将来拡張

- decision_log_design.md  
👉 学習システム構想

---

## 3. 俯瞰 → 詳細の関係

```
overview
├ target_vision
├ gap_analysis
├ improvement_plan
└ training_decision_rule

training_decision_rule
└ decision_log

decision_log
└ weekly_checklist
```

---

## 4. 実運用で使う順序（重要）

① overviewを見る  
② decision_ruleで判断  
③ decision_logに記録  
④ weekly_checklistで観察  
⑤ 次のdecisionへ  

---

## 5. 迷ったとき

👉 overview.md を見る

---

## 6. 原則

- 完璧に理解しなくてよい
- 分からなくなったら俯瞰に戻る
- 小さく回す

---