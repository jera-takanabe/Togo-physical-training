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
Status: Next

目的:
- 各測定項目が、どのドメインに紐づくべきかを見直す
- 1つの測定値が複数能力を含む場合の扱いを整理する

成果物:
- `docs/specs/analysis_validity_review.md`

作業予定メモ:
- 2.1 で見つかった旧ドメイン名と現行6軸の不整合を引き継ぐ
- 各テスト項目について、以下の対応を確認する
  - test
  - current domain
  - subdomain
  - axis
  - representative metric として妥当か
- `test_scores.csv` の `domain` 列が、axis なのか subdomain なのかを明確化する
- `domain_scores.csv` を将来的に `subdomain_scores` と `axis_scores` に分けるか検討する

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
Status: Next

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

### 2.5 ベンチマーク値・引用根拠の整理
Status: Next

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