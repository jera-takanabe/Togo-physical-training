# やりたいことリスト（バックログ）

※本資料は随時更新する（変更前提）
※優先順位は固定しない（状況に応じて変更）

---

## 1. 運用・意思決定

### 1.1 トレーニング設計
- priority → トレーニングメニュー変換
- 種目 / 回数 / セット設計
- 成長に応じた負荷調整

### 1.2 運用ルール
- 週次サイクル（測定 → 判断 → 実行）
- dashboard確認タイミング
- トレーニング頻度設計

### 1.3 decisionログ
- なぜそのトレーニングを選んだか
- 仮説と結果の記録
- 次回への改善

---

## 2. 分析の妥当性

### 2.1 6軸構成の妥当性確認
Status: Done

目的:
- U12 / 中学ラグビー選手のフィジカル評価として、現在の6軸が妥当か確認する
- 各軸が重複しすぎていないか、逆に抜けている能力がないか確認する

作業メモ:
- 現在の6軸定義の親ドキュメントは `docs/architecture/u12_scoring_overview.md` とする
- `docs/specs/u12_rugby_sc_test_battery_v1.md` は現在の main ブランチには存在しない
- `docs/architecture/u12_scoring_overview.md` に以下の軽微な不整合あり
  - `## 9. Related Documents（関連ドキュメント）` の見出しが重複している
  - 存在しない `../specs/u12_rugby_sc_test_battery_v1.md` へのリンクが残っている
- Speed軸は妥当と判断
  - Speed は `acceleration + max_velocity` の複合軸として扱う
  - U12 / 中学ラグビーでは acceleration の重要度が高い
  - max_velocity はブレイク後の独走能力や将来的な走力評価のために保持する
  - 旧資料では `top_speed`、現行overviewでは `max_velocity` と表記されているため、今後は `max_velocity` に統一する
- Power軸は妥当と判断
  - 現行6軸では Upper 軸が別に存在するため、Power は主に下半身の爆発的出力として扱う
  - 代表指標は CMJ / SJ / Standing Long Jump
  - 旧資料では `lower_body_power`、`Lower Body Power`、`Explosive Power` と表記されている
  - 現行設計では `Power` に統一する
  - Upper Body Power は現行設計では `Upper` 軸として扱う
- Elastic軸は妥当と判断
  - Elastic は Power とは別に扱うべき軸
  - Power は主に下半身の爆発的出力を表す
  - Elastic は SSC能力、地面反発を利用する能力、短い接地で反発を使う能力を表す
  - 代表指標は RSI / pogo jump / drop jump
  - 旧資料では `reactive_strength`、`Reactive Strength`、`ReactiveStrength` と表記されている
  - 現行設計では `Elastic` / `elastic` に統一する
- COD軸は妥当と判断
  - COD は Speed とは別に扱うべき軸
  - Speed は直線方向の加速・最高速度を表す
  - COD は減速、姿勢制御、切り返し、再加速を含む能力を表す
  - 代表指標は Pro Agility / 5-10-5
  - 現行overviewと旧資料の間に大きな矛盾はない
  - 説明文では、CODを単なる方向転換ではなく、減速・切り返し・再加速を含む能力として明記する
- Upper軸は妥当と判断
  - Upper は Power とは別に扱うべき軸
  - Power は主に下半身の爆発的出力を表す
  - Upper は上半身出力・上半身パワーを表す
  - 代表指標は Medicine Ball Throw / MB Throw
  - 旧資料では `upper_body_power`、`Upper Body Power`、`UpperBodyPower` と表記されている
  - 現行設計では `Upper` / `upper` に統一する
- Endurance軸は妥当と判断
  - Endurance は単なる長距離持久力ではなく、ラグビーに必要な間欠的持久力・反復スプリント能力・回復力を表す軸として扱う
  - 代表指標は Yo-Yo IR1 / RSA
  - 旧資料では `speed_endurance`、`Speed Endurance`、`スピード持久力` と表記されている
  - 現行設計では `Endurance` / `endurance` に統一する
  - `docs/specs/endurance_score_design.md` では、Yo-Yo IR1 と RSA を Endurance ドメインに組み込む設計が既に書かれており、現行6軸との整合性は高い
暫定結論:
- 現在の6軸構成は、U12 / 中学ラグビー選手のフィジカル評価軸として妥当と判断
- 6軸は現行のまま維持する
  - Speed
  - Power
  - Elastic
  - COD
  - Upper
  - Endurance
- Speed は `acceleration + max_velocity` の複合軸として扱う
- その他5軸は、現時点では1軸 = 1サブドメインとして扱う
- ただし、旧資料との間で用語の揺れが残っているため、今後ドキュメント整理が必要

用語整理メモ:
- `top_speed` は現行設計では `max_velocity` に統一する
- `lower_body_power` / `Explosive Power` は現行設計では `Power` に統一する
- `reactive_strength` / `Reactive Strength` / `ReactiveStrength` は現行設計では `Elastic` に統一する
- `upper_body_power` / `Upper Body Power` / `UpperBodyPower` は現行設計では `Upper` に統一する
- `speed_endurance` / `Speed Endurance` / `SpeedEndurance` は現行設計では `Endurance` に統一する
実データ確認メモ:
- `data/reference/benchmark_values.csv` には現時点で `domain` / `axis` / `subdomain` / `direction` / `floor_anchor` 列がない
- `data/analysis/test_scores.csv` の `domain` 列は、現行6軸ではなく旧ドメイン / サブドメイン名が混在している
  - `acceleration`
  - `cod`
  - `explosive_power`
  - `reactive_strength`
  - `upper_body_power`
  - `endurance`
- `data/analysis/domain_scores.csv` は6列だが、現行6軸名ではなく旧ドメイン名で出力されている
  - `acceleration_score`
  - `cod_score`
  - `reactive_strength_score`
  - `explosive_power_score`
  - `upper_body_power_score`
  - `endurance_score`
- 現行6軸に合わせるなら、将来的には以下のような出力名へ整理する必要がある
  - `speed_score`
  - `power_score`
  - `elastic_score`
  - `cod_score`
  - `upper_score`
  - `endurance_score`
- 特に Speed は `acceleration + max_velocity` の複合軸と定義されているが、現状の出力には `acceleration_score` のみで、`max_velocity_score` / `speed_score` が存在しない
スクリプト確認メモ:
- `scripts/calc_rugby_physical_score.py` 内で旧ドメイン名が明示的に定義されている
  - `acceleration`
  - `cod`
  - `reactive_strength`
  - `explosive_power`
  - `upper_body_power`
  - `endurance`
- `test_scores.csv` の `domain` 列は、`calc_rugby_physical_score.py` のテスト定義から出力されている可能性が高い
- `domain_scores.csv` の列名も同スクリプト内で直接定義されている
  - `acceleration_score`
  - `cod_score`
  - `reactive_strength_score`
  - `explosive_power_score`
  - `upper_body_power_score`
  - `endurance_score`
- `rugby_physical_score` の計算も旧ドメイン名を前提にしている
- 現行overviewでは `Speed = acceleration + max_velocity` と定義しているため、今すぐ `acceleration_score` を `speed_score` に単純リネームするのは避ける
- 今後は `subdomain_scores` と `axis_scores` を分ける設計を検討する

最終判断:
- 現在の6軸構成は、U12 / 中学ラグビー選手のフィジカル評価軸として妥当と判断
- 現行6軸を維持する
  - Speed
  - Power
  - Elastic
  - COD
  - Upper
  - Endurance
- Speed は `acceleration + max_velocity` の複合軸として扱う
- その他5軸は、現時点では1軸 = 1サブドメインとして扱う

残課題:
- ドキュメント上の用語揺れを整理する
  - `top_speed` → `max_velocity`
  - `lower_body_power` / `Explosive Power` → `Power`
  - `reactive_strength` / `Reactive Strength` → `Elastic`
  - `upper_body_power` / `Upper Body Power` → `Upper`
  - `speed_endurance` / `Speed Endurance` → `Endurance`
- `data/analysis/domain_scores.csv` は現行6軸名ではなく、旧ドメイン名で出力されている
- `scripts/calc_rugby_physical_score.py` も旧ドメイン名を前提にしている
- 実データ・スクリプト側の整合性確認は、2.2 / 2.4 で扱う

### 2.2 各テスト項目とドメイン対応の妥当性確認
Status: Done

目的:
- 各測定項目が、どのドメインに紐づくべきかを見直す
- 1つの測定値が複数能力を含む場合の扱いを整理する

成果物:
- `docs/specs/analysis_validity_review.md`

作業メモ:
- `data/analysis/test_scores.csv` に出ている現在の test → domain 対応を確認した
- 現在の対応は以下
  - `10m_sprint` → `acceleration`
  - `20m_sprint` → `acceleration`
  - `cmj` → `explosive_power`
  - `standing_long_jump` → `explosive_power`
  - `rsi` → `reactive_strength`
  - `pro_agility_5_10_5` → `cod`
  - `medicine_ball_throw_2kg` → `upper_body_power`
  - `yoyo_ir1` → `endurance`
  - `rsa_avg_time` → `endurance`
  - `rsa_decline` → `endurance`
- 現行6軸への対応は大きく破綻していない
- 問題は、割り当てそのものよりも、旧domain名と現行axis/subdomain名の不一致である
- `test_scores.csv` の `domain` 列は、現行設計では `axis` ではなく `subdomain` に近い
- `analysis_validity_review.md` に、test → current domain → subdomain → axis の対応表を追加した
- 複数能力を含むテストについて、現段階では1つのテストを複数axisへ配点せず、主axisを1つに決めて扱う方針とした
- 理由:
  - システムが複雑になりすぎることを避ける
  - スコアの説明可能性を保つ
  - 測定数が少ない段階では、細かい配点よりも継続測定と傾向把握を優先する
  - 1つのテストを複数axisに配点すると、総合スコアで二重計上になる可能性がある

次工程へ送る課題:
- スコア算出ロジックへの反映は 2.4 で扱う
- `test_scores.csv` の `domain` 列を `subdomain` として扱うか検討する
- 現行6軸に対応する `axis` 列を追加するか検討する
- `domain_scores.csv` を `subdomain_scores.csv` と `axis_scores.csv` に分けるか検討する
- 複数能力を含むテストの扱いを、今後スコア算出ロジックへ反映するか検討する

### 2.3 レーダーチャート不整合の修正

Status: Done

#### 対応内容

- レーダーチャートが5軸で表示されていた問題を修正
- 仕様上の6軸に合わせて表示されることを確認
  - Speed
  - Power
  - Elastic
  - COD
  - Upper
  - Endurance
- `latest_summary.md` 上のレーダーチャート出力も確認済み

#### 完了条件

- 6軸レーダーとして表示される
- GitHub Pages / dashboard 上でも6軸として確認できる
- 今後の課題は「軸の妥当性」「スコア算出根拠」「ベンチマーク根拠」の検証に移す

### 2.4 スコア算出根拠の明確化
Status: Blocked

目的:
- raw値から radar_score / domain_score / rugby_physical_score に変換される根拠を明確にする
- なぜその点数になるのかを追跡可能にする

確認対象:
- `data/reference/benchmark_values.csv`
- `data/analysis/test_scores.csv`
- `data/analysis/domain_scores.csv`
- `data/analysis/rugby_physical_score.csv`
- `scripts/calc_rugby_physical_score.py`

確認観点:
- floor_anchor = 0 の扱い
- world_elite_p50 = 100 の扱い
- タイム系と距離・高さ系の direction
- 補間計算の妥当性
- ベンチマークが不足している項目の扱い

作業メモ:
- スコア計算ロジックは `interpolate_score()` により説明可能
- ただし、計算の前提となる `benchmark_values.csv` の基準値の妥当性が未確認
- benchmark値の出典・測定条件・信頼度が不明なままでは、スコアの妥当性は確定できない
- そのため、2.4 の途中で 2.5「ベンチマーク値・引用根拠の整理」を先に確認する

Blocked reason:
- `benchmark_values.csv` の出典・測定条件・信頼度が未確認のため

### 2.5 ベンチマーク値・引用根拠の整理
Status: In Progress

目的:
- benchmark_values.csv に入っている値の根拠を明確化する
- どの値が実測、推定、仮置き、文献由来かを区別する

確認対象:
- general_youth_p50
- youth_athlete_p50
- elite_u18_p50
- world_elite_p50
- floor_anchor

必要な整理:
- 出典
- 対象年齢
- 対象競技
- 性別
- 測定条件
- このプロジェクトで採用した理由
- 信頼度

作業メモ:
- 2.4「スコア算出根拠の明確化」を進める前提として、`benchmark_values.csv` の基準値の根拠確認を先に行う
- 現時点では、各benchmark値が以下のどれに該当するか未整理
  - 1次ソース由来
  - 2次資料由来
  - 推定値
  - 仮置き
  - プロジェクト内での暫定値
- benchmark値の出典・測定条件・信頼度を整理しない限り、スコアの妥当性は確定できない

確認メモ:
- `data/reference/benchmark_values.csv` には10個のbenchmark項目がある
  - `10m_sprint`
  - `20m_sprint`
  - `cmj`
  - `standing_long_jump`
  - `pro_agility_5_10_5`
  - `rsi`
  - `medicine_ball_throw_2kg`
  - `yoyo_ir1`
  - `rsa_avg_time`
  - `rsa_decline`
- 現在の列は以下のみ
  - `test`
  - `unit`
  - `general_youth_p50`
  - `youth_athlete_p50`
  - `elite_u18_p50`
  - `world_elite_p50`
- 現在の `benchmark_values.csv` には、出典・測定条件・信頼度を示す列がない
- `docs/references/rugby_benchmark_dataset_documentation.md` には、複数のスポーツ科学資料を合成したbenchmarkである旨が書かれている
- ただし、具体的な論文名・著者・年・URL・DOI・対象年齢・測定条件は記録されていない
- 現時点では、benchmark値は「一次ソースに紐づいた確定値」ではなく、「複数資料をもとにした暫定的な合成・推定benchmark」として扱う
- したがって、現在のスコアは厳密な標準化スコアではなく、育成・比較・モチベーション用の暫定スコアとして扱う

追加検討する列:
- `source_type`
- `source_note`
- `age_range`
- `sex`
- `sport_context`
- `measurement_protocol`
- `confidence`
- `review_status`
- `primary_source`
- `secondary_source`
- `source_url_or_doi`

拡張方針:
- `benchmark_values.csv` に出典情報をすべて詰め込むのではなく、計算に必要な値と最低限の根拠メタ情報を持たせる
- 詳細な出典・レビュー内容は、別ドキュメントで管理する
- 候補ドキュメント:
  - `docs/references/benchmark_source_review.md`

`benchmark_values.csv` に追加する最小候補列:
- `source_type`
- `source_note`
- `confidence`
- `review_status`
- `review_note`

現時点の暫定扱い:
- 全benchmark値は、一次ソース確認が完了するまでは以下として扱う
  - `source_type`: `synthesized_estimate`
  - `confidence`: `low`
  - `review_status`: `needs_review`
- 理由:
  - 具体的な一次ソースが未記録
  - 対象年齢・性別・競技・測定条件が未整理
  - 現在の値は厳密な標準化値ではなく、育成・比較・モチベーション用の暫定値であるため

成果物:
- `docs/references/benchmark_source_review.md`
- `docs/references/benchmark_design_policy.md`

追加作業メモ:
- `docs/references/benchmark_source_review.md` を作成した
- 現在の benchmark 値は全て `needs_review` として扱う
- 現時点では、全 benchmark 値の `confidence` は `low` とする
- 今後、test ごとに一次ソース候補を確認し、必要に応じて benchmark 値を修正する

方針変更メモ:
- benchmark値は後続の弱点判定・優先順位・トレーニングメニュー設計に大きく影響するため、単なる出典確認ではなく、benchmark設計そのものを早期に見直す
- 10m_sprint などの基礎フィジカル指標は、最初からラグビー専用benchmarkに限定しない
- benchmark はまず、年齢・発達段階・性別・競技経験レベルに基づく基礎フィジカル基準として整理する
- ラグビー文脈は benchmark値そのものではなく、上位レイヤーの重要度・優先順位・トレーニング判断で扱う
- 将来的には `U12 / U14 / U16 / U18 / 18+` の stage 別 benchmark を検討する
- 可能であれば `p50 / p75 / p90 / p95 / elite_reference` のような percentile 設計を検討する
- 現在の `general_youth_p50 / youth_athlete_p50 / elite_u18_p50 / world_elite_p50` は暫定構造として扱い、stage × percentile 型へ再設計する可能性がある
- この方針はトレーニングメニュー設計にも影響するため、個別benchmark値の出典確認より先に設計方針を明文化する
- `docs/references/benchmark_design_policy.md` を作成した
- benchmark は、まず基礎フィジカルの年齢・発達段階別比較として設計する方針とした
- ラグビー重要度は、benchmark値ではなく上位レイヤーで扱う方針とした
- `U12 / U14 / U16 / U18 / 18+` の stage 別 benchmark を検討する
- `p50 / p75 / p90 / p95 / elite_reference` を区別する
- 現行 `benchmark_values.csv` は暫定互換ファイルとして維持する
- 新しい stage × percentile benchmark は、別ファイルで試作する
- 最初の試作対象は `10m_sprint` とする

試作メモ:
- `data/reference/benchmark_stage_percentile_values.csv` を作成した
- まずは `10m_sprint` のみで stage × percentile 型 benchmark を試作した
- stage は以下
  - `U12`
  - `U14`
  - `U16`
  - `U18`
  - `18+`
- metric は以下
  - `p50`
  - `p75`
  - `p90`
  - `p95`
  - `elite_reference`
- 現時点では値は全て `TBD`
- 現行 pipeline ではまだ使用しない

---

## 3. システム強化

### 3.1 アプリ化
- GUI入力（RAWデータ / decisionログ）
- CSV → DB化
- データ入力の簡易化

### 3.2 マルチアスリート対応
- athlete_id設計
- 複数選手の管理
- 比較機能

---

## 4. データ拡張

### 4.1 InBody統合
- 体重 / 体脂肪 / 筋量の管理
- パフォーマンスとの関係分析
- 減量 / 増量戦略への反映

---

## 5. 統合ビジョン

### 5.1 マンダラート統合
- フィジカル
- 技術
- メンタル
- 生活
- 学習

---

## 6. 優先順位の考え方

以下を基準に判断する：

1. パフォーマンスに直結するか
2. すぐ実行できるか
3. 現在のシステムを壊さないか

---

## 7. 進め方

1. 1つ選ぶ  
2. 小さく分解する  
3. 1つだけ実行する  
4. 結果を確認する  
5. 記録する  

---