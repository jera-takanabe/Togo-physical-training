# U12 Rugby S&C Scoring Overview

## 1. Purpose（目的）
本ドキュメントは、U12ラグビーにおけるS&C（Strength & Conditioning）評価システムの全体構造を定義する。

## 2. Scope（スコープ）
本システムが扱う範囲（測定・スコアリング・可視化）と、対象外を明確にする。

## 3. System Structure（システム構造）
本システムを構成する主要要素の関係を示す。

- test_scores（各テストのスコア）
- domain_scores（ドメインスコア）
- radar_chart（6軸レーダー）
- rugby_physical_score（総合スコア）

## 4. Domain Model（ドメインモデル）

### 4.1 Axis（6軸）
- Speed
- Power
- Elastic
- COD
- Upper
- Endurance

### 4.2 Subdomain（7サブドメイン）
- acceleration
- max_velocity
- power
- elastic
- cod
- upper
- endurance

### 4.3 Axis と Subdomain の関係
- Speed = acceleration + max_velocity
- その他は1対1対応

## 5. Data Flow（データフロー）

```text
raw measurement
    ↓
test_scores
    ↓
domain_scores（subdomain）
    ↓
domain_scores（axis）
    ↓
radar_chart / rugby_physical_score
```

## 6. Score Layers（スコアレイヤー）

本システムでは、スコアを以下のレイヤーで管理する。

- test level（テスト単位）
- subdomain level（サブドメイン）
- axis level（レーダー軸）

## 7. Missing Data Handling（欠測データの扱い）

欠測データは、以下の3種類のスコアとして扱う。

- observed（実測値）
- carried（前回値補完）
- display（表示用スコア）

詳細は `domain_score_concept.md` を参照。

## 8. Design Principles（設計原則）

- 二層構造（subdomain / axis）
- 実測値と補完値の分離
- 欠測を0として扱わない
- スコアと信頼性（coverage / confidence）を分離

## 9. Related Documents（関連ドキュメント）

## 9. Related Documents（関連ドキュメント）

- [Domain Score Concept](../specs/domain_score_concept.md)
- [Domain Score Schema](../specs/domain_score_schema.md)
- [Domain Score Calculation](../specs/domain_score_calculation.md)
- [U12 Rugby S&C Test Battery](../specs/u12_rugby_sc_test_battery_v1.md)