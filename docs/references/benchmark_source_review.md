# Benchmark Source Review

## 1. 目的

本資料は、`data/reference/benchmark_values.csv` に記録されている benchmark 値について、出典・測定条件・信頼度を確認するためのレビュー資料である。

現在の benchmark 値は、一次ソースに紐づいた確定値ではなく、複数資料をもとにした暫定的な合成・推定 benchmark として扱う。

そのため、本資料では各 test について以下を整理する。

- 現在の benchmark 値
- 想定している対象
- 出典候補
- 測定条件
- 信頼度
- 採用判断
- 今後の確認事項

---

## 2. 現在の benchmark_values.csv

| test | unit | general_youth_p50 | youth_athlete_p50 | elite_u18_p50 | world_elite_p50 | current_status |
|---|---|---:|---:|---:|---:|---|
| `10m_sprint` | s | 2.0 | 1.85 | 1.75 | 1.65 | needs_review |
| `20m_sprint` | s | 4.2 | 4.0 | 3.85 | 3.6 | needs_review |
| `cmj` | cm | 28.0 | 35.0 | 45.0 | 55.0 | needs_review |
| `standing_long_jump` | m | 1.7 | 2.0 | 2.3 | 2.6 | needs_review |
| `pro_agility_5_10_5` | s | 6.6 | 6.2 | 5.8 | 5.3 | needs_review |
| `rsi` | ratio | 1.2 | 1.6 | 2.0 | 2.6 | needs_review |
| `medicine_ball_throw_2kg` | m | 3.5 | 4.5 | 5.5 | 6.5 | needs_review |
| `yoyo_ir1` | m | 1000 | 1500 | 2000 | 2400 | needs_review |
| `rsa_avg_time` | s | 5.5 | 5.0 | 4.5 | 4.0 | needs_review |
| `rsa_decline` | ratio | 0.15 | 0.10 | 0.07 | 0.05 | needs_review |

---

## 3. レビュー方針

### 3.1 source_type

| source_type | 意味 |
|---|---|
| `primary_source` | 論文・公式データなど、直接確認可能な一次ソース |
| `secondary_source` | 書籍・記事・まとめ資料など、一次ソースを要約した資料 |
| `synthesized_estimate` | 複数資料や経験的判断を合成した推定値 |
| `project_placeholder` | プロジェクト内で仮置きした値 |
| `unknown` | 根拠不明 |

現時点では、全 benchmark 値を `synthesized_estimate` または `unknown` として扱う。

---

### 3.2 confidence

| confidence | 意味 |
|---|---|
| `high` | 対象年齢・性別・競技・測定条件が近く、出典も明確 |
| `medium` | 出典はあるが、対象や測定条件に一部ずれがある |
| `low` | 出典や条件が不明、または推定要素が大きい |

現時点では、全 benchmark 値を `low` として扱う。

---

### 3.3 review_status

| review_status | 意味 |
|---|---|
| `reviewed` | 根拠確認済み |
| `needs_review` | 根拠確認が必要 |
| `provisional` | 暫定採用 |
| `replace_candidate` | 将来的に置換候補 |
| `do_not_use` | スコア計算に使わない方がよい |

現時点では、全 benchmark 値を `needs_review` として扱う。

---

## 4. test別レビュー

### 4.1 10m_sprint

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 2.0 | s |
| youth_athlete_p50 | 1.85 | s |
| elite_u18_p50 | 1.75 | s |
| world_elite_p50 | 1.65 | s |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- 対象年齢が 11〜13歳に近いか
- ラグビー選手、または近い競技のデータか
- 10m の測定開始条件が一致しているか
  - 静止スタート
  - 光電管
  - 手動計測
  - 動画解析
- タイムの開始・終了定義が一致しているか

#### 採用判断

現時点では暫定値として扱う。

#### ソース選定方針

`10m_sprint` は、ラグビー固有のスキルではなく、基礎スプリント能力として扱う。

そのため、benchmark source はラグビー選手のデータに限定しない。

優先する source は以下である。

1. 年齢 / stage が明確である
2. 男子データである
3. 10m sprint または 0–10m split が含まれる
4. percentile または年齢別 reference value がある
5. 測定条件が明記されている
6. 対象集団が `general` / `athlete` / `elite` のどれに近いか判断できる

サッカー選手データは、基礎スプリント能力の athlete benchmark として利用候補にする。

ただし、一般男子基準ではなく、`population = athlete` として扱う。

#### ソース候補

| candidate | 対象 | 使えそうな用途 | 注意点 | status |
|---|---|---|---|---|
| Nikolaidis et al. (2016), male football players aged 9–35 years | 男子サッカー選手 9〜35歳 | 0–10m split の age reference 候補。U12〜18+ の athlete benchmark 候補 | サッカー選手データであり general ではない。percentile として使えるか表確認が必要 | candidate |
| Nowak et al. / Normative and limit values of speed, endurance and power tests in young football players | 男子サッカー選手 12〜16歳 | 10m sprint の percentile 候補。U14 / U16 の athlete benchmark 候補 | U12 / U18 / 18+ には不足。サッカーアカデミー系の可能性がある | candidate |
| Development of juvenile sprint performance in boys | 男子 U12 / U14 / U16 / U18 / U20 | stage 区分の参考。U12〜U18 の発達傾向の確認候補 | 10m sprint 値や percentile の詳細確認が必要 | candidate |

#### 現時点の判断

現時点では、`10m_sprint` の benchmark 値はまだ確定しない。

まずは `benchmark_stage_percentile_values.csv` の値を `TBD` のままとし、各 source の対象年齢・測定条件・percentile 定義を確認する。

特に、以下を分けて扱う。

- `population = general`
- `population = athlete`
- `population = academy`
- `population = elite`

`10m_sprint` の最初の試作では、一般男子基準と athlete 基準を混同しない。

#### 候補ソースの暫定評価

現時点では、以下のように扱う。

| candidate | source_type | population | stage coverage | percentile availability | provisional role |
|---|---|---|---|---|---|
| Nikolaidis et al. (2016) | primary_source | athlete | U12〜18+ 相当を広く含む | 0–10m split の percentile table あり | `10m_sprint` の athlete benchmark 候補 |
| Nowak et al. (2025) | primary_source | athlete / academy | 主に U14 / U16 | 10m sprint の percentile table あり | U14 / U16 の athlete benchmark 候補 |
| Development of juvenile sprint performance in boys | primary_source | general / athlete 要確認 | U12 / U14 / U16 / U18 / U20 | percentile ではなく mean / SD / min / max 中心の可能性 | stage設計・発達傾向の参考候補 |

#### 採用前に確認すること

- 各 source の測定開始条件
- 測定機器
- 0–10m split と 10m sprint の定義差
- 対象者の競技レベル
- 各 stage に対応する年齢範囲
- percentile が実測値か、モデル推定値か
- `population = general` として使えるデータが別途必要か

---

### 4.2 20m_sprint

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 4.2 | s |
| youth_athlete_p50 | 4.0 | s |
| elite_u18_p50 | 3.85 | s |
| world_elite_p50 | 3.6 | s |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- 20m sprint の対象年齢別データがあるか
- 10m sprint との整合が取れているか
- 測定方法が一致しているか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.3 cmj

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 28.0 | cm |
| youth_athlete_p50 | 35.0 | cm |
| elite_u18_p50 | 45.0 | cm |
| world_elite_p50 | 55.0 | cm |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- CMJ の測定機器が一致しているか
  - force plate
  - jump mat
  - smartphone app
  - video
- arm swing あり / なしが一致しているか
- 対象年齢・性別・競技が近いか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.4 standing_long_jump

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 1.7 | m |
| youth_athlete_p50 | 2.0 | m |
| elite_u18_p50 | 2.3 | m |
| world_elite_p50 | 2.6 | m |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- 年齢別の立ち幅跳びデータがあるか
- 学校体力テストとの比較が可能か
- 測定方法が一致しているか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.5 pro_agility_5_10_5

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 6.6 | s |
| youth_athlete_p50 | 6.2 | s |
| elite_u18_p50 | 5.8 | s |
| world_elite_p50 | 5.3 | s |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- Pro Agility / 5-10-5 の年齢別データがあるか
- 測定距離が yard か meter か
- 手動計測か光電管か
- 切り返しラインの判定条件が一致しているか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.6 rsi

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 1.2 | ratio |
| youth_athlete_p50 | 1.6 | ratio |
| elite_u18_p50 | 2.0 | ratio |
| world_elite_p50 | 2.6 | ratio |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- RSI の算出方法が一致しているか
  - drop jump RSI
  - RSI modified
  - pogo RSI
- jump height と contact time の取得方法
- 対象年齢・競技が近いか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.7 medicine_ball_throw_2kg

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 3.5 | m |
| youth_athlete_p50 | 4.5 | m |
| elite_u18_p50 | 5.5 | m |
| world_elite_p50 | 6.5 | m |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- メディシンボール重量が 2kg で一致しているか
- 座位 / 立位 / kneeling など測定姿勢が一致しているか
- 投げ方が一致しているか
- 対象年齢・競技が近いか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.8 yoyo_ir1

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 1000 | m |
| youth_athlete_p50 | 1500 | m |
| elite_u18_p50 | 2000 | m |
| world_elite_p50 | 2400 | m |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- Yo-Yo IR1 の年齢別・競技別データがあるか
- Yo-Yo IR1 と Yo-Yo endurance test を混同していないか
- 記録方式が一致しているか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.9 rsa_avg_time

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 5.5 | s |
| youth_athlete_p50 | 5.0 | s |
| elite_u18_p50 | 4.5 | s |
| world_elite_p50 | 4.0 | s |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- RSA のプロトコルが一致しているか
  - 距離
  - 本数
  - レスト
  - スタート条件
- 平均タイムの算出方法が一致しているか

#### 採用判断

現時点では暫定値として扱う。

---

### 4.10 rsa_decline

#### 現在値

| level | value | unit |
|---|---:|---|
| general_youth_p50 | 0.15 | ratio |
| youth_athlete_p50 | 0.10 | ratio |
| elite_u18_p50 | 0.07 | ratio |
| world_elite_p50 | 0.05 | ratio |

#### 現時点の扱い

- source_type: `synthesized_estimate`
- confidence: `low`
- review_status: `needs_review`

#### 確認したい観点

- decline rate の定義が一致しているか
- best time 比なのか、平均比なのか
- 疲労指数の算出式が一致しているか

#### 採用判断

現時点では暫定値として扱う。

---

## 5. 今後の進め方

1. まず各 test の現在値を暫定 benchmark として明示する
2. その後、test ごとに一次ソース候補を探す
3. 対象年齢・性別・競技・測定条件の一致度を確認する
4. 必要に応じて benchmark 値を修正する
5. 修正した場合は、`benchmark_values.csv` と本資料の両方を更新する