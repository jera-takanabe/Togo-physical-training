# Enduranceスコア設計（暫定）

---

## 1. 目的

Yo-Yo IR1 と RSA を Endurance ドメインに組み込み、持久力・反復能力を評価できるようにする。

---

## 2. 使用指標

### Yo-Yo IR1

使用値：

- distance_m

理由：

- 記録が単純
- 比較しやすい
- 成長推移を見やすい

---

### RSA

使用値：

- average_time_sec
- decline_rate

理由：

- average_time_sec：反復全体の走力
- decline_rate：後半の落ち幅

---

## 3. Enduranceドメインの構成

Endurance は以下の2要素で構成する。

| 要素 | 指標 | 役割 |
|---|---|---|
| Aerobic / intermittent endurance | Yo-Yo IR1 distance_m | 間欠的持久力 |
| Repeated sprint ability | RSA average_time_sec / decline_rate | 反復スプリント能力 |

---

## 4. 暫定重み

| 指標 | 重み |
|---|---|
| Yo-Yo IR1 distance_m | 50% |
| RSA average_time_sec | 30% |
| RSA decline_rate | 20% |

---

## 5. 実装方針

- `data/raw/yoyo_tests_raw.csv` から Yo-Yo 距離を取得する
- `data/raw/rsa_tests_raw.csv` から RSA 各本タイムを取得する
- RSA はセッション単位で平均タイムと落ち幅を算出する
- Endurance ドメインとして `domain_scores.csv` に反映する

---

## 6. 保留事項

- Yo-Yo の benchmark 値
- RSA average_time_sec の benchmark 値
- RSA decline_rate の benchmark 値
- 既存5ドメインとの統合方法
- radar_chart への Endurance 追加

---