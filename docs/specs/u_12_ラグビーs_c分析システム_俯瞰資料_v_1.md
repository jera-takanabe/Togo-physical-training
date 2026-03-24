# U12ラグビーS&C分析システム 俯瞰資料 v1

---

## 1. 本資料の目的

本資料は、U12ラグビー向けフィジカル分析システムにおける

- 全体構造の整理
- レーダー設計と分析設計の関係整理
- 現状の確定事項と未解決論点の明確化

を目的とする。

---

## 2. 全体アーキテクチャ（俯瞰）

```mermaid
flowchart TD
    A[Raw Measurements] --> B[Test Scores]
    B --> C[Internal Analysis Domains]
    C --> D[6-axis Radar]
    C --> E[Overall Score]

    F[Medical / Injury Screening] -. separate .-> D
    G[Growth Context] -. interpretive layer .-> D
```

### 解釈

- Performance（スコア化対象）と
- Medical / Growth（解釈レイヤー）

は分離されている

---

## 3. レーダー設計（正本）

### 6軸（確定）

- Speed
- Power
- Elastic
- COD
- Upper
- Endurance

👉 spec（u12\_rugby\_sc\_test\_battery\_v1.md）を正本とする

---

## 4. 内部分析構造

### サブドメイン（推奨構造）

- acceleration
- top\_speed
- cod
- lower\_body\_power
- reactive\_strength
- upper\_body\_power
- speed\_endurance

👉 analysis\_layer\_design.md をベースに採用

---

## 5. レーダーと分析の関係

```mermaid
flowchart LR
    S1[Speed] --> A1[acceleration]
    S1 --> A2[top_speed]

    S2[Power] --> B1[lower_body_power]

    S3[Elastic] --> C1[reactive_strength]

    S4[COD] --> D1[cod]

    S5[Upper] --> E1[upper_body_power]

    S6[Endurance] --> F1[speed_endurance]
```

### 重要原則

- レーダー＝表示構造（6軸）
- サブドメイン＝分析構造（7軸）

👉 両者は一致させる必要はない

---

## 6. 測定項目との対応

| 6軸        | サブドメイン             | 主な測定                   |
| --------- | ------------------ | ---------------------- |
| Speed     | acceleration       | 5m, 10m, 20m           |
| Speed     | top\_speed         | 30m, Fly               |
| Power     | lower\_body\_power | CMJ, SJ, SLJ, Bounding |
| Elastic   | reactive\_strength | RSI, Drop Jump         |
| COD       | cod                | Pro Agility            |
| Upper     | upper\_body\_power | Medicine Ball Throw    |
| Endurance | speed\_endurance   | RSA, YoYo              |

---

## 7. データ構造（論点含む）

### 現状の候補

#### パターンA（単層）

- domain\_scores = 6軸

#### パターンB（二層）※推奨

- internal\_domain\_scores = 7サブドメイン
- domain\_scores = 6軸（レーダー用）

---

## 8. 確定事項

- 6軸レーダーは固定
- 内部は6軸より細かく持つ
- Speed / Power / Endurance は内部で分解が必要
- Elastic / COD / Upper は比較的単純

---

## 9. 未解決論点

### ① domain\_scores の構造

- 6軸で持つか
- 7サブドメインで持つか
- 二層にするか

### ② Power の分解

- vertical / horizontal を分けるか

### ③ Endurance の分解

- YoYo と RSA を分けるか

### ④ work\_capacity の扱い

- 無視するか
- 将来拡張か

---

## 10. 資料間の関係構造

```mermaid
flowchart TD
    SPEC[u12_rugby_sc_test_battery_v1.md]
    ARCH[rugby_physical_domains.md]
    ANALYSIS[analysis_layer_design.md]

    SPEC --> RADAR[6-axis Radar]
    ARCH --> DOMAINS[Physical Domains]
    ANALYSIS --> SUBDOMAINS[Analysis Domains]

    SUBDOMAINS --> DOMAIN_SCORES
    RADAR --> DOMAIN_SCORES

    DOMAIN_SCORES --> DASHBOARD
```

### 解釈

- SPEC = 正本（何を評価するか）
- ARCH = 理論モデル（能力とは何か）
- ANALYSIS = 実装モデル（どう計算するか）

👉 domain\_scores がすべてを接続するコア

---

## 11. 今後の進め方

### 優先順位

1. domain\_scores 再設計
2. 測定→サブドメイン配分
3. profile（sprint / elastic）の役割確定
4. ドキュメント統一

---

## 12. 一言でまとめると

👉 レーダーは世界観 👉 サブドメインは分析 👉 domain\_scoresは翻訳層

---

