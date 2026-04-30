# Benchmark Design Policy

## 1. 目的

本資料は、`data/reference/benchmark_values.csv` に記録する benchmark 値の設計方針を定義する。

これまでの benchmark は、以下の4段階で管理していた。

- `general_youth_p50`
- `youth_athlete_p50`
- `elite_u18_p50`
- `world_elite_p50`

この構造は初期設計としては扱いやすいが、以下の点が曖昧である。

- 年齢・発達段階
- 性別
- 母集団
- 競技経験レベル
- 測定条件
- percentile の意味
- ラグビー特化値なのか、基礎フィジカル値なのか

benchmark 値は、後続のスコア、弱点判定、優先順位、トレーニングメニューに大きく影響する。

そのため、本資料では、benchmark を単なる出典一覧ではなく、後続プロセスに耐えられる設計要素として整理する。

---

## 2. benchmark が後続プロセスへ与える影響

本システムでは、測定値は以下の流れで使われる。

    raw measurement
        ↓
    benchmark score
        ↓
    test score
        ↓
    subdomain / axis score
        ↓
    weakness detection
        ↓
    training priority
        ↓
    training menu
        ↓
    effect review

したがって、benchmark の設計が曖昧だと、以下の問題が発生する。

- 実際には標準的な値なのに、弱点として判定される
- 実際には不足している能力なのに、十分と判定される
- 年齢的に妥当な発達を、過小評価または過大評価する
- ラグビーで重要な能力と、単なる同年代比較が混ざる
- トレーニング優先順位が誤る
- トレーニング効果の検証が不安定になる

特に、10m sprint、CMJ、standing long jump などの基礎フィジカル指標は、トレーニングメニューへ直接影響する。

そのため、benchmark は可能な限り早い段階で設計方針を明確にする。

---

## 3. 現在の benchmark_values.csv の問題

現在の `benchmark_values.csv` は以下の形式である。

    test,unit,general_youth_p50,youth_athlete_p50,elite_u18_p50,world_elite_p50

この形式には、以下の問題がある。

### 3.1 年齢ステージが曖昧

`general_youth_p50` が、何歳を対象にした値なのかが明確ではない。

例:

- U12 なのか
- U14 なのか
- 11〜13歳の平均なのか
- 小学生高学年なのか
- 中学1年なのか

特に成長期では、1〜2年の違いで大きく値が変わるため、年齢ステージの曖昧さはスコア解釈に大きく影響する。

---

### 3.2 母集団が曖昧

`general_youth_p50` や `youth_athlete_p50` の母集団が明確ではない。

例:

- 一般男子全体
- 運動部所属者
- 競技スポーツ経験者
- サッカー / 陸上 / ラグビーなどの競技者
- 学校体力テストの平均
- 地域・国別データ

母集団が異なると、同じ p50 でも意味が変わる。

---

### 3.3 percentile の意味が曖昧

現在の列名には `p50` が含まれているが、全ての値が実際の percentile に基づいているとは限らない。

特に以下は注意が必要である。

- `elite_u18_p50`
- `world_elite_p50`

これらは percentile というより、参照値または目標値に近い可能性がある。

そのため、今後は percentile と reference value を区別する必要がある。

---

### 3.4 ラグビー特化値と基礎フィジカル値が混ざる

10m sprint や CMJ は、ラグビー特有の能力ではなく、基礎フィジカル能力である。

一方、ラグビーではそれらの能力の重要度が高い。

この2つを benchmark 値の中で混ぜると、以下の問題が起こる。

- 同年代比較なのか、ラグビー適性評価なのかが分からない
- 競技重要度と能力水準が混ざる
- トレーニング優先順位の理由が説明しづらくなる

したがって、基礎フィジカル benchmark とラグビー重要度は分離する。

---

### 3.5 出典・測定条件・信頼度がない

現在の `benchmark_values.csv` には、以下の情報がない。

- 出典
- source type
- 対象年齢
- 性別
- 競技
- 測定条件
- 測定機器
- 信頼度
- review status

そのため、現在の値は、厳密な標準化値ではなく、暫定的な合成・推定 benchmark として扱う。

---

## 4. 基本方針

### 4.1 基礎フィジカル benchmark とラグビー重要度を分ける

benchmark は、まず基礎フィジカル能力の水準を評価するために使う。

例:

- 10m sprint が同年代の中でどの程度か
- CMJ が同年代・同発達段階でどの程度か
- standing long jump が同年代の中でどの程度か

一方、ラグビーでその能力がどれだけ重要かは、別レイヤーで扱う。

    raw measurement
        ↓
    age/stage benchmark
        ↓
    axis score
        ↓
    rugby importance
        ↓
    training priority

この分離により、以下を区別できる。

- 基礎能力として低いのか
- ラグビー上の重要度が高いのか
- 今トレーニング優先度を上げるべきなのか

---

### 4.2 年齢・発達段階を優先する

U12〜U18では、年齢と発達段階の影響が非常に大きい。

そのため、benchmark は以下のような stage 別に整理することを検討する。

- U12
- U14
- U16
- U18
- 18+

特に U12 / U14 では、暦年齢だけでなく、成長スパートや成熟度の影響も大きい。

将来的には、以下の情報も補助的に扱う。

- 身長
- 体重
- PHV 前後
- 成熟度
- 競技歴

ただし、初期段階では複雑化を避けるため、まずは stage 別 benchmark を優先する。

---

### 4.3 percentile を使う

benchmark は、可能な限り percentile として扱う。

候補は以下である。

- `p50`: 同年代の中央値
- `p75`: 上位25%程度
- `p90`: 上位10%程度
- `p95`: 上位5%程度
- `elite_reference`: 年代別または競技別エリート参考値

ただし、全ての test で percentile データが手に入るとは限らない。

その場合は、以下を区別する。

- 実測 percentile
- 文献由来の平均値
- エリート集団の平均値
- 推定値
- プロジェクト内の仮置き値

---

### 4.4 ラグビー文脈は上位レイヤーで扱う

ラグビーで重要な能力かどうかは、benchmark 値そのものではなく、上位レイヤーで扱う。

例:

- Speed はラグビーで重要
- COD はラグビーで重要
- Elastic はスプリントや切り返しに重要
- Upper はコンタクトやボールキャリーに重要
- Endurance は試合後半や反復高強度運動に重要

この重要度は、以下で使う。

- axis weighting
- weakness priority
- training priority
- weekly training menu
- decision log

これにより、benchmark は「同年代・同発達段階との比較」、rugby layer は「競技上の重要度」として役割を分けられる。

---

## 5. 推奨ステージ

benchmark は、暦年齢だけでなく、育成年代の大まかな発達段階を反映できるように stage 別に管理する。

推奨する stage は以下である。

| stage | 主な対象 | 用途 |
|---|---|---|
| U12 | 小学校高学年〜中学入学前後 | 基礎運動能力の現在地確認 |
| U14 | 中学1〜2年相当 | 成長期初期〜中期の発達確認 |
| U16 | 中学3年〜高校1年相当 | 競技者としての基礎能力確認 |
| U18 | 高校2〜3年相当 | ユース上位層・高校年代の目標確認 |
| 18+ | 大学・成人・プロ | 長期的な最高到達点の参照 |

---

### 5.1 U12

U12 は、基礎運動能力の現在地を確認するための stage とする。

主な用途:

- 同年代男子と比較した現在地を知る
- 基礎的なスプリント、ジャンプ、方向転換、持久力の偏りを確認する
- 将来の専門的トレーニングに入る前の土台を確認する

注意点:

- 成熟差が大きいため、数値だけで優劣を断定しない
- 体格、成長スパート、運動経験の影響を考慮する
- トレーニング目標は「勝つための即時最適化」よりも「将来伸びる土台作り」を優先する

---

### 5.2 U14

U14 は、中学初期〜中期における発達段階を確認する stage とする。

主な用途:

- 中学年代での成長変化を確認する
- U12 からの伸びを評価する
- 部活動や競技練習の増加に対して、基礎フィジカルが追いついているか確認する

注意点:

- PHV 前後の個人差が非常に大きい
- 急激な成長による動作のぎこちなさや怪我リスクを考慮する
- 数値向上だけでなく、動作品質や疲労状態も合わせて見る

---

### 5.3 U16

U16 は、競技者としての基礎フィジカルが本格的に問われ始める stage とする。

主な用途:

- 高校年代に向けた競技基盤を確認する
- Speed / Power / COD / Elastic などの不足を明確にする
- トレーニングの専門性を少しずつ高める

注意点:

- 競技経験、体格差、成熟度差によって数値差が大きい
- 成熟が早い選手の値を、そのまま全員の目標にしない
- 怪我リスクとパフォーマンス向上を両立する必要がある

---

### 5.4 U18

U18 は、ユース上位層や高校年代の目標確認に使う stage とする。

主な用途:

- 高校上位層・ユースアカデミー水準との比較
- 長期目標の中間地点として使う
- 18+ や成人競技者への接続を確認する

注意点:

- U18 の値は、U12 / U14 の短期目標として直接使わない
- 早期に U18 水準を求めると、過負荷や怪我につながる可能性がある
- 現在地確認よりも、長期的な到達目標として扱う

---

### 5.5 18+

18+ は、成人・大学・プロレベルの参照 stage とする。

主な用途:

- 長期的な最高到達点をイメージする
- 将来的な競技レベルの上限参照として使う
- world / professional reference として扱う

注意点:

- U12 / U14 の評価に直接使わない
- 成長期の選手に対して、短期目標として設定しない
- あくまで長期的な方向性を示す参考値とする

---

## 6. 推奨percentile

benchmark は、可能な限り percentile または reference level として整理する。

推奨する指標は以下である。

| 指標 | 意味 | 主な用途 |
|---|---|---|
| p50 | 同年代・同stageの中央値 | 現在地の標準確認 |
| p75 | 上位25%程度 | 良好な基礎能力の目安 |
| p90 | 上位10%程度 | 競技者として強みになり得る水準 |
| p95 | 上位5%程度 | 高い競技能力の目安 |
| elite_reference | 年代別または競技別エリート参考値 | 長期目標・上位層比較 |

---

### 6.1 p50

p50 は、同年代・同stageの中央値として扱う。

用途:

- 現在値が同年代の標準付近か確認する
- 大きな弱点がないか確認する
- 成長に伴う自然な発達を追う

注意点:

- p50 を超えているから十分とは限らない
- ラグビーで重要な能力は、p50 以上でも強化対象になり得る
- p50 は「競技で勝つ基準」ではなく「現在地の基準」として扱う

---

### 6.2 p75

p75 は、同年代の中で良好な基礎能力を持つ水準として扱う。

用途:

- 基礎能力として良好か確認する
- 次の短期目標として使いやすい
- U12 / U14 では現実的な到達目標になりやすい

注意点:

- p75 はエリート基準ではない
- 競技重要度が高い軸では、p75 到達後も強化を継続することがある

---

### 6.3 p90

p90 は、同年代の上位10%程度の水準として扱う。

用途:

- 競技者として強みになり得る能力を確認する
- 中期目標として使う
- Speed / COD / Power などの重要能力の目標値として使う

注意点:

- 全項目で p90 を目指す必要はない
- 怪我リスクや疲労状態を見ずに p90 を追いすぎない
- 成熟が早い選手の影響を受けやすい可能性がある

---

### 6.4 p95

p95 は、同年代の上位5%程度の非常に高い水準として扱う。

用途:

- 特定能力の強み確認
- 長期的な到達目標
- エリート候補水準の参考

注意点:

- U12 / U14 では短期目標にしない
- 成熟度・体格・競技歴の影響を強く受ける
- p95 未満だから悪い、とは判断しない

---

### 6.5 elite_reference

elite_reference は、年代別または競技別のエリート参考値として扱う。

用途:

- 上位層との距離感を把握する
- 長期目標の参考にする
- 高校年代・成人レベルへの接続を考える

注意点:

- percentile ではない場合がある
- 母集団や測定条件が異なる場合は、直接比較しない
- U12 / U14 の短期トレーニング目標としては使わない

---

## 7. スコア変換への影響

benchmark 設計を変更すると、スコア変換ロジックにも影響する。

現在の `calc_rugby_physical_score.py` では、以下の4点を使って raw 値を 0〜100 点に変換している。

| 現在の列 | 現在のスコア上の扱い |
|---|---:|
| `general_youth_p50` | 50 |
| `youth_athlete_p50` | 70 |
| `elite_u18_p50` | 85 |
| `world_elite_p50` | 100 |

この方式は初期実装としては分かりやすいが、以下の問題がある。

- 年齢 stage が固定されていない
- p50 と reference value が混在している
- `world_elite_p50` が本当に p50 なのか不明
- U12 選手に対して U18 / adult elite の値が強く影響する
- 短期目標と長期参照値が同じスコア軸に入っている

---

### 7.1 現行スコアの扱い

現行スコアは、厳密な標準化スコアではなく、暫定 benchmark に基づく区分線形スコアとして扱う。

したがって、現行スコアの意味は以下である。

- 同年代・同stageの正確な percentile ではない
- 成長段階を厳密に補正した値ではない
- 複数資料を合成した暫定目安に対する相対スコアである
- 弱点把握やモチベーションには使えるが、厳密な能力判定には使わない

---

### 7.2 stage × percentile 型にした場合

将来的に stage × percentile 型へ変更する場合、benchmark は以下のような構造になる。

| test | stage | p50 | p75 | p90 | p95 | elite_reference |
|---|---|---:|---:|---:|---:|---:|
| 10m_sprint | U12 | TBD | TBD | TBD | TBD | TBD |
| 10m_sprint | U14 | TBD | TBD | TBD | TBD | TBD |
| 10m_sprint | U16 | TBD | TBD | TBD | TBD | TBD |
| 10m_sprint | U18 | TBD | TBD | TBD | TBD | TBD |
| 10m_sprint | 18+ | TBD | TBD | TBD | TBD | TBD |

この場合、スコア変換では、対象選手の stage に対応する benchmark 行を使う。

例:

- U12 選手には U12 の benchmark を使う
- U14 選手には U14 の benchmark を使う
- U18 選手には U18 の benchmark を使う
- 18+ の値は、短期評価ではなく長期参照に使う

---

### 7.3 推奨スコア対応

stage × percentile 型では、以下のようなスコア対応を検討する。

| benchmark | score |
|---|---:|
| p50 | 50 |
| p75 | 70 |
| p90 | 85 |
| p95 | 95 |
| elite_reference | 100 |

この対応により、現在の 50 / 70 / 85 / 100 に近い構造を維持しつつ、基準の意味を明確化できる。

ただし、`elite_reference` は percentile ではない場合があるため、必ず `source_type` と `confidence` を併記する。

---

### 7.4 U12 / U14 での注意

U12 / U14 では、p90 や p95 を短期目標にしない。

理由:

- 成熟差の影響が大きい
- 体格差が大きい
- 高強度トレーニングを急ぐと怪我リスクがある
- 将来の伸びしろを潰す可能性がある

したがって、U12 / U14 では、スコアを以下のように扱う。

| score range | 解釈 |
|---|---|
| 0〜49 | 同stage内で不足傾向。基礎づくりを優先 |
| 50〜69 | 標準〜やや良好。継続的に伸ばす |
| 70〜84 | 良好。強みに育てる候補 |
| 85以上 | 非常に高い。維持・怪我予防・他能力とのバランスを重視 |

---

### 7.5 長期参照値の扱い

18+ や elite_reference は、U12 / U14 の短期評価に直接使わない。

用途は以下に限定する。

- 長期的な最高到達点のイメージ
- 高校年代以降の参考値
- 現在地と将来目標の距離感を把握する
- モチベーション用の参照

短期トレーニングメニューは、原則として現在の stage benchmark に基づいて設計する。

---

## 8. トレーニングメニューへの影響

benchmark は、単にスコアを出すためだけではなく、トレーニングメニュー設計にも影響する。

特に以下の流れに影響する。

    benchmark score
        ↓
    weakness detection
        ↓
    training priority
        ↓
    training menu
        ↓
    effect review

そのため、benchmark の設計では、短期目標・中期目標・長期参照値を混同しないことが重要である。

---

### 8.1 短期目標

短期目標は、現在の stage に基づいて設定する。

U12 / U14 では、原則として以下を短期目標にする。

- p50 未満の項目は、まず p50 付近を目指す
- p50 付近の項目は、p75 を目指す
- p75 付近の項目は、安定維持または p90 へ向けて中期的に伸ばす
- p90 以上の項目は、さらに追い込むよりも維持・怪我予防・他能力とのバランスを優先する

短期目標では、U18 や 18+ の elite_reference を直接使わない。

理由:

- 成熟度の違いが大きい
- 体格差が大きい
- 過負荷につながる可能性がある
- トレーニング内容が年齢に合わなくなる可能性がある

---

### 8.2 中期目標

中期目標は、現在の stage の上位 percentile または次の stage を参考にする。

例:

- U12 選手の場合:
  - 現在stageの p75 / p90
  - 将来の U14 p50 / p75
- U14 選手の場合:
  - 現在stageの p75 / p90
  - 将来の U16 p50 / p75

中期目標は、半年〜1年程度の成長確認や、次年度に向けた準備に使う。

ただし、成長期では急激な身長・体重変化があるため、数値だけでなく以下も確認する。

- 疲労
- 怪我リスク
- 動作品質
- 体重変化
- モチベーション
- 学校・部活・ラグビー活動の負荷

---

### 8.3 長期参照値

長期参照値は、将来的な最高到達点のイメージとして使う。

対象:

- U18 elite_reference
- 18+ elite_reference
- professional / world reference

用途:

- 将来の方向性を確認する
- 高校年代以降の目標感を持つ
- 現在地との差を理解する
- モチベーションを高める

注意点:

- U12 / U14 の短期メニューには直接使わない
- 長期参照値との差を、そのまま現在の不足量として扱わない
- 成長段階を無視して成人値に近づけようとしない

---

### 8.4 ラグビー重要度との接続

benchmark は、基礎フィジカルの現在地を示す。

一方で、トレーニング優先順位を決めるには、ラグビーでの重要度を重ねる必要がある。

例:

| axis | benchmark上の状態 | rugby importance | training priority |
|---|---|---|---|
| Speed | p50未満 | 高 | 高 |
| COD | p75付近 | 高 | 中〜高 |
| Upper | p50未満 | 中 | 中 |
| Endurance | p75以上 | 中〜高 | 維持 |
| Elastic | p50未満 | 高 | 高 |

このように、benchmark score だけでなく、rugby importance を重ねて priority を決める。

---

### 8.5 トレーニングメニューへの変換方針

トレーニングメニューは、単に低いscoreを上げるためだけに作らない。

以下を合わせて判断する。

- benchmark score
- rugby importance
- readiness
- fatigue
- injury risk
- growth stage
- body weight / body composition
- current rugby schedule
- athlete motivation

例:

- Speed が低く、膝の痛みがある場合:
  - 高強度スプリントを増やすのではなく、低負荷のドリル、姿勢改善、基礎筋力、体重管理を優先する
- Elastic が低く、疲労が強い場合:
  - pogo や drop jump を増やすのではなく、接地ドリルや低強度ジャンプから始める
- Endurance が低い場合:
  - 長距離走ではなく、ラグビーに近い間欠的持久力や低衝撃の有酸素運動を検討する

---

### 8.6 効果検証への影響

benchmark 設計は、トレーニング効果の見方にも影響する。

効果検証では、以下を分けて見る。

- raw value の変化
- stage benchmark に対する位置
- axis score の変化
- readiness / fatigue の変化
- 体重・体組成の変化
- 動作品質の変化

特に成長期では、raw value が改善しても、同stage benchmark 上の位置が変わらないことがある。

逆に、raw value が大きく変わらなくても、体重増加や疲労状態を考慮すると意味のある変化である場合もある。

そのため、トレーニング効果は score だけで判断しない。

---

## 9. 今後のCSV設計案

将来的には、現在の `benchmark_values.csv` を、stage と percentile を明示できる構造へ再設計する。

現在の形式は以下である。

    test,unit,general_youth_p50,youth_athlete_p50,elite_u18_p50,world_elite_p50

この形式は初期実装としては扱いやすいが、以下を表現しにくい。

- stage
- percentile
- reference value
- source type
- confidence
- measurement protocol
- review status

---

### 9.1 推奨する基本構造

将来的には、以下のような縦持ち構造を検討する。

| column | meaning |
|---|---|
| `test` | 測定項目 |
| `unit` | 単位 |
| `stage` | U12 / U14 / U16 / U18 / 18+ |
| `sex` | male / female / mixed / unknown |
| `population` | general / athlete / academy / elite / professional |
| `metric_type` | percentile / reference / estimate |
| `metric` | p50 / p75 / p90 / p95 / elite_reference |
| `value` | benchmark 値 |
| `direction` | higher / lower |
| `source_type` | primary_source / secondary_source / synthesized_estimate / project_placeholder |
| `confidence` | high / medium / low |
| `review_status` | reviewed / needs_review / provisional / replace_candidate |
| `measurement_protocol` | 測定条件 |
| `source_note` | 出典や補足 |
| `review_note` | レビュー上の注意 |

この構造にすると、同じ `test` でも stage や percentile ごとに複数行を持てる。

例:

| test | unit | stage | metric | value | direction |
|---|---|---|---|---:|---|
| 10m_sprint | s | U12 | p50 | TBD | lower |
| 10m_sprint | s | U12 | p75 | TBD | lower |
| 10m_sprint | s | U12 | p90 | TBD | lower |
| 10m_sprint | s | U14 | p50 | TBD | lower |
| 10m_sprint | s | U14 | p75 | TBD | lower |

---

### 9.2 縦持ち構造の利点

縦持ち構造には、以下の利点がある。

- stage を明示できる
- percentile と reference value を区別できる
- 1つの test に複数の source を紐づけやすい
- 新しい stage や percentile を追加しやすい
- 出典レビュー状態を行単位で管理できる
- スコア計算時に、対象選手の stage に応じた benchmark を選択できる

---

### 9.3 現行形式との関係

現行形式は、当面は維持してもよい。

理由:

- 既存スクリプトが現在の列構造に依存している
- すぐに変更すると pipeline が壊れる可能性がある
- まずは benchmark 設計方針と出典レビューを固める方が優先

そのため、移行期間中は以下の2層構造を検討する。

| file | role |
|---|---|
| `benchmark_values.csv` | 現行 pipeline 用の暫定 benchmark |
| `benchmark_stage_percentile_values.csv` | 将来設計用の stage × percentile benchmark |

---

### 9.4 将来ファイル案

将来的には、以下のファイル構成を検討する。

| file | purpose |
|---|---|
| `data/reference/benchmark_values.csv` | 現行pipeline互換のbenchmark |
| `data/reference/benchmark_stage_percentile_values.csv` | stage × percentile 型benchmark |
| `docs/references/benchmark_source_review.md` | 各benchmark値の出典レビュー |
| `docs/references/benchmark_design_policy.md` | benchmark設計方針 |
| `docs/references/rugby_importance_policy.md` | ラグビー重要度・優先度設計 |

---

### 9.5 最小移行案

いきなりスクリプトを全面変更せず、以下の順で進める。

1. 現行 `benchmark_values.csv` は維持する
2. `benchmark_design_policy.md` で設計方針を明文化する
3. `benchmark_source_review.md` で現在値の信頼度を管理する
4. 新規に `benchmark_stage_percentile_values.csv` を作成する
5. まずは `10m_sprint` のみで stage × percentile 型を試作する
6. 問題なければ他の test に拡張する
7. 既存 pipeline に影響しない形で新スコア計算を試す
8. 十分に検証してから `calc_rugby_physical_score.py` に反映する

この方針により、現行システムを壊さずに benchmark 設計を改善できる。

---

## 10. 移行方針

benchmark 設計の見直しは、スコア計算、レーダーチャート、トレーニング優先順位に影響する。

そのため、既存 pipeline を壊さないように段階的に移行する。

---

### 10.1 移行原則

移行時は以下を原則とする。

- 既存の `benchmark_values.csv` はすぐに壊さない
- 現行 dashboard / radar_chart / rugby_physical_score が動く状態を維持する
- 新しい benchmark 設計は、別ファイルで試作する
- まず1項目だけで検証する
- 計算結果の差分を確認してから対象を広げる
- スコアの意味が変わる場合は、必ずドキュメントに記録する

---

### 10.2 移行ステップ

推奨する移行ステップは以下である。

1. `benchmark_design_policy.md` を作成し、設計方針を明文化する
2. `benchmark_source_review.md` で現在値の信頼度を整理する
3. `benchmark_stage_percentile_values.csv` を新規作成する
4. まず `10m_sprint` の stage × percentile benchmark を試作する
5. 既存 `benchmark_values.csv` と新 benchmark の差を確認する
6. 新スコア計算ロジックを別スクリプトまたは別関数で試作する
7. 出力を既存 `test_scores.csv` とは別ファイルに出す
8. 差分をレビューする
9. 問題がなければ他の test に拡張する
10. 十分に確認できた段階で、既存 pipeline への統合を検討する

---

### 10.3 試作用ファイル案

移行期間中は、以下のような試作用ファイルを使う。

| file | purpose |
|---|---|
| `data/reference/benchmark_stage_percentile_values.csv` | 新しい stage × percentile benchmark |
| `data/analysis/test_scores_stage_based.csv` | 新 benchmark による test score |
| `data/analysis/axis_scores_stage_based.csv` | 新 benchmark による axis score |
| `docs/references/benchmark_design_policy.md` | benchmark設計方針 |
| `docs/references/benchmark_source_review.md` | benchmark出典レビュー |

これにより、現行 pipeline の成果物を壊さずに比較できる。

---

### 10.4 既存スコアとの比較観点

新 benchmark を試作した場合、以下を比較する。

- raw value は同じか
- 現行 score と stage based score の差
- score band の変化
- 弱点判定の変化
- training priority の変化
- radar chart の見え方の変化
- 親・本人が見たときの納得感
- トレーニングメニューへの影響

特に、score が変わった結果、トレーニング優先順位が変わる場合は必ず記録する。

---

### 10.5 当面の採用方針

当面は、以下の方針とする。

- 現行 `benchmark_values.csv` は pipeline 互換のため維持する
- 現行 score は暫定 benchmark score として扱う
- 新しい stage × percentile benchmark は試作扱いとする
- いきなり dashboard や radar chart に反映しない
- まずは `10m_sprint` で設計・値・スコア変換の妥当性を確認する
- 妥当性が確認できたら、20m sprint、CMJ、standing long jump へ広げる

---

### 10.6 backlog との関係

この移行方針は、以下の backlog 項目に関係する。

- 2.4 スコア算出根拠の明確化
- 2.5 ベンチマーク値・引用根拠の整理
- 1.1 トレーニング設計
- 1.3 decisionログ
- 4.1 InBody統合

特に 2.4 は、benchmark 設計が固まるまで `Blocked` として扱う。

---

## 11. 現時点の結論

現時点では、benchmark 設計について以下の方針を採用する。

- benchmark は、まず基礎フィジカルの年齢・発達段階別比較として設計する
- ラグビー重要度は、benchmark値ではなく上位レイヤーで扱う
- U12 / U14 では短期目標と長期参照値を分ける
- p50 / p75 / p90 / p95 / elite_reference を区別する
- 現行 `benchmark_values.csv` は暫定互換ファイルとして維持する
- 新しい stage × percentile benchmark は、別ファイルで試作する
- 最初の試作対象は `10m_sprint` とする

この方針により、現行システムを壊さずに、より説明可能でトレーニング判断に使いやすい benchmark 設計へ移行する。

---
