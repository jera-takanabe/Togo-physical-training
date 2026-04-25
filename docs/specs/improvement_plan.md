# 改善計画（v2）

---

## 0. 前提

- 本計画は暫定であり、途中で変更される前提とする
- 運用（測定・記録・分析・判断）を止めないことを最優先とする
- 1回の変更は最小単位で実施する
- 物理的なファイル移動や大規模再設計は急がない
- 設計変更は `document_map.md` と整合させる

---

## 1. 現在の重点ギャップ

| No | ギャップ | 状態 | 優先度 |
|----|----------|------|--------|
| G1 | スプリント評価 | surface差により比較不可 | 最重要 |
| G2 | 動作改善 | サイクル・姿勢・切り替えに課題 | 高 |
| G3 | トレーニング体系化 | 実施内容が週ごとに揺れやすい | 高 |
| G4 | RSA / Yo-Yo の評価体系統合 | raw記録済みだがスコア未統合 | 中 |
| G5 | ドメイン定義 | 5軸・6軸・8軸が混在 | 中 |
| G6 | 指標表現 | 指標が多く本人に伝わりにくい | 中 |
| G7 | ラグビーパフォーマンス接続 | 将来課題 | 保留 |

---

## 2. マイルストーン

### M1：設計の再整理

目的：
- 資料の関係性を明確にする
- 迷ったときに戻れる状態を作る

対象：
- `document_map.md`
- `overview.md`
- `training_decision_rule.md`
- `gap_analysis.md`
- `improvement_plan.md`

状態：
- 実施中 / ほぼ完了

---

### M2：測定・分析運用の安定化

目的：
- raw記録からpipeline実行までを安定させる
- 測定条件を含めて比較可能な状態を作る

対象：
- raw CSV
- measurement_sessions
- measurement protocols
- latest_summary

重点：
- sprint / COD は同一surfaceで次回以降比較
- Yo-Yo / RSI / jump は比較可能データとして扱う

---

### M3：判断・トレーニング接続の安定化

目的：
- 測定・観察から次のトレーニング判断に迷わず進める

対象：
- decision_log
- daily_notes
- weekly_checklist
- training_decision_rule

重点：
- 優先課題は最大2つ
- 条件差がある測定値は比較しない
- 観察と数値を両方使う

---

### M4：評価体系の再設計

目的：
- 「何を見ればよいか」を明確にする

対象：
- ドメイン定義
- スコア構造
- RSA / Yo-Yo の位置づけ
- radar / dashboard 表現

重点：
- ドメイン数の整理
- Endurance の扱い
- 本人に伝わる表現

---

### M5：ラグビーパフォーマンス接続（将来）

目的：
- フィジカル指標と実戦パフォーマンスを接続する

対象：
- 試合観察
- オフザボール
- 個人スキル
- ゲーム内評価

状態：
- 保留

---

## 3. フェーズ分割

### Phase 1：設計整理

対象：
- docs構造
- document_map
- overview
- decision_rule
- gap_analysis
- improvement_plan

ゴール：
- 設計で迷わない

---

### Phase 2：測定運用安定化

対象：
- raw記録
- protocol整備
- pipeline確認
- surface / shoes / device の統一

ゴール：
- 次回測定で比較可能なデータを取る

---

### Phase 3：判断運用安定化

対象：
- decision_log
- daily_notes
- weekly_checklist
- training_decision_rule

ゴール：
- 測定後・週次観察後に判断を更新できる

---

### Phase 4：評価体系整理

対象：
- ドメイン
- スコア
- RSA / Yo-Yo
- dashboard

ゴール：
- 何を見ればよいか明確にする

---

### Phase 5：競技接続

対象：
- ラグビー実戦
- スキル
- オフザボール
- 試合内評価

ゴール：
- フィジカル改善と競技パフォーマンスを接続する

---

## 4. 直近の作業候補

### 最優先

1. 設計コア資料の整合確認
   - `document_map.md`
   - `overview.md`
   - `training_decision_rule.md`
   - `gap_analysis.md`
   - `improvement_plan.md`

2. 4月測定結果の扱いを整理
   - sprint / COD は比較対象外
   - Yo-Yo / RSI / jump は比較可能
   - decision_log に反映

3. 次回測定の条件固定
   - surface
   - shoes
   - device
   - session_id

---

### 次点

4. RSA / Yo-Yo の評価体系への組み込み検討
5. ドメイン定義の整理
6. dashboardの表現改善

---

### 保留

7. ラグビー実戦パフォーマンス接続
8. AI判断履歴の学習化
9. DB化

---

## 5. 作業単位ルール

1回の作業では以下を守る。

- 変更対象は1つ
- 影響範囲を限定する
- 動作確認する
- 意図を記録する
- コミット単位を小さくする

例：

- 1資料だけ更新
- 1CSVだけ修正
- 1プロトコルだけ整備
- 1decisionだけ追加
- 1スクリプトだけ修正

---

## 6. チャット分割

### チャット1：全体管理

扱う内容：
- 計画更新
- 優先順位
- 次にやる作業の決定

---

### チャット2：設計整理

扱う内容：
- document_map
- overview
- specs
- gap_analysis
- improvement_plan

---

### チャット3：測定・記録

扱う内容：
- raw CSV
- measurement_sessions
- protocols
- pipeline実行前チェック

---

### チャット4：分析・評価

扱う内容：
- latest_summary
- test_scores
- domain_scores
- score設計
- dashboard

---

### チャット5：判断・トレーニング

扱う内容：
- decision_log
- daily_notes
- weekly_checklist
- training_decision_rule

---

### チャット6：実装作業

扱う内容：
- Git操作
- ファイル移動
- スクリプト修正
- コマンド実行

---

## 7. 計画変更ルール

- 途中変更は許可する
- 方針変更は `decision_log` または `gap_analysis` に残す
- 構造変更は `document_map.md` に反映する
- 測定条件の変更は `measurement_sessions.csv` と decision_log に残す
- 未完のタスクは保留として残す

---

## 8. 現時点の判断

現時点では、設計資料の関係整理を優先する。

物理的なフォルダ移動はまだ行わない。  
まずは各資料の役割を明確にし、運用を止めずに改善を継続する。

---