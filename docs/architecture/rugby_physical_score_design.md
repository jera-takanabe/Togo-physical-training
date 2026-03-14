# Rugby Physical Score Design
**Project:** Togo Physical Training  
**Purpose:** 12歳ラグビー選手のための総合フィジカル評価モデル

---

## 1. Overview

このドキュメントは、測定データと benchmark データを使って  
**Rugby Physical Score** を算出する設計書である。

目的は次の3つ。

1. 個別テスト結果を分かりやすいスコアに変換する  
2. 能力ドメインごとの強み・弱みを可視化する  
3. トレーニング優先順位を抽出しやすくする  

---

## 2. Input Data

想定入力ファイル

```text
data/processed/sprint_sessions.csv
data/processed/cod_sessions.csv
data/processed/jump_sessions.csv
data/processed/horizontal_sessions.csv
data/processed/throw_sessions.csv
data/reference/benchmark_values.csv
```

必要テスト

- 10m sprint
- 20m sprint
- CMJ
- Standing Long Jump
- Pro Agility (5-10-5)
- RSI
- Medicine Ball Throw

---

## 3. Model Structure

評価構造は以下。

```text
test result
↓
benchmark comparison
↓
test score (0-100)
↓
domain score
↓
rugby physical score
```

---

## 4. Test Score

各テストは benchmark を使って 0-100 に正規化する。

### 4.1 lower is better
対象:
- 10m sprint
- 20m sprint
- Pro Agility

基準:
- general_youth_p50 = 50
- youth_athlete_p50 = 70
- elite_u18_p50 = 85
- world_elite_p50 = 100

### 4.2 higher is better
対象:
- CMJ
- Standing Long Jump
- RSI
- Medicine Ball Throw

基準:
- general_youth_p50 = 50
- youth_athlete_p50 = 70
- elite_u18_p50 = 85
- world_elite_p50 = 100

### 4.3 interpolation

各 benchmark の間は線形補間する。

例:
- sprint は値が小さいほど高得点
- jump は値が大きいほど高得点

スコア範囲:
- 0 未満にはしない
- 100 を超えたら 100 に丸める

---

## 5. Domain Definitions

### 5.1 Acceleration
使用テスト:
- 10m sprint
- 20m sprint

算出:
```text
Acceleration = (10m score × 0.6) + (20m score × 0.4)
```

### 5.2 Change of Direction
使用テスト:
- Pro Agility

算出:
```text
COD = Pro Agility score
```

### 5.3 Explosive Power
使用テスト:
- CMJ
- Standing Long Jump

算出:
```text
ExplosivePower = (CMJ score × 0.6) + (SLJ score × 0.4)
```

### 5.4 Reactive Strength
使用テスト:
- RSI

算出:
```text
ReactiveStrength = RSI score
```

### 5.5 Upper Body Power
使用テスト:
- Medicine Ball Throw

算出:
```text
UpperBodyPower = MB Throw score
```

---

## 6. Rugby Physical Score

ラグビー12歳育成を想定した重み付け。

| Domain | Weight |
|---|---:|
| Acceleration | 0.30 |
| Change of Direction | 0.25 |
| Reactive Strength | 0.20 |
| Explosive Power | 0.15 |
| Upper Body Power | 0.10 |

算出式

```text
RugbyPhysicalScore =
  Acceleration × 0.30 +
  COD × 0.25 +
  ReactiveStrength × 0.20 +
  ExplosivePower × 0.15 +
  UpperBodyPower × 0.10
```

---

## 7. Score Bands

| Score | Label |
|---|---|
| 90-100 | Elite |
| 80-89 | Competitive |
| 70-79 | Advanced |
| 60-69 | Developing |
| 50-59 | Foundation |
| 0-49 | Early Stage |

---

## 8. Output Files

### 8.1 test_scores.csv
```text
data/analysis/test_scores.csv
```

例カラム:
- athlete
- session_date
- test_name
- raw_value
- score
- benchmark_band
- gap_to_next_level

### 8.2 domain_scores.csv
```text
data/analysis/domain_scores.csv
```

例カラム:
- athlete
- session_date
- acceleration_score
- cod_score
- reactive_strength_score
- explosive_power_score
- upper_body_power_score

### 8.3 rugby_physical_score.csv
```text
data/analysis/rugby_physical_score.csv
```

例カラム:
- athlete
- session_date
- rugby_physical_score
- score_band
- strongest_domain
- weakest_domain
- priority_1
- priority_2

---

## 9. Interpretation Rules

### 9.1 strongest_domain
最大スコアのドメイン

### 9.2 weakest_domain
最小スコアのドメイン

### 9.3 priority extraction
原則:
- weakest 2 domains を優先課題とする
- ただし Acceleration/COD/ReactiveStrength は優先度補正あり

優先補正:
- Acceleration: +5
- COD: +5
- ReactiveStrength: +3

---

## 10. Dashboard Display

例

```text
Rugby Physical Score: 74 (Advanced)

Acceleration        82
COD                 75
ReactiveStrength    68
ExplosivePower      72
UpperBodyPower      65

Priority 1: Reactive Strength
Priority 2: Upper Body Power
```

子ども向け表示例

```text
Acceleration        ★★★★☆
COD                 ★★★★☆
ReactiveStrength    ★★★☆☆
ExplosivePower      ★★★★☆
UpperBodyPower      ★★★☆☆
```

---

## 11. Design Principles

1. 自分比を最優先  
2. benchmark は比較の補助  
3. スコアは意思決定のための道具  
4. 高得点でも停滞なら課題扱い  
5. 低得点でも成長率が高ければポジティブ評価を付与  

---

## 12. Future Extensions

将来的に追加できるもの

- readiness 補正
- 成長率スコア
- 半年後予測スコア
- 年齢補正 / 発育補正
- ポジション別重み付け

---

## 13. Recommended Repository Location

```text
docs/architecture/rugby_physical_score_design.md
```
