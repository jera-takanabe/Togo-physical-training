# Analysis Layer Design

Project: Togo Physical Training Purpose:
12歳ラグビー選手のフィジカル能力を最大化するための分析基盤

------------------------------------------------------------------------

## 1. Overview

本プロジェクトはラグビー選手（12歳）のフィジカル測定データを継続的に記録・分析し、
トレーニング意思決定を支援する分析ツールを構築することを目的とする。

現在のパイプライン

raw (trialデータ) ↓ processed (session集計) ↓ summary (ダッシュボード)

analysisレイヤー追加後

raw ↓ processed ↓ analysis ↓ dashboard

analysisレイヤーでは以下を実現する

-   パフォーマンス評価
-   成長トレンド分析
-   能力バランス分析
-   トレーニング優先順位抽出
-   年齢別ベンチマーク比較

------------------------------------------------------------------------

## 2. Goals

analysisレイヤーの目的

1.  選手の成長を定量的に把握
2.  能力の強みと弱みを特定
3.  トレーニング優先順位を抽出
4.  同年代ベンチマーク比較
5.  コーチング意思決定支援

最終目的

測定記録ツール → 分析ツール → 育成意思決定システム

------------------------------------------------------------------------

## 3. Data Structure

data/

raw/ processed/

analysis/ - event_scores.csv - domain_profiles.csv -
trend_analysis.csv - fatigue_flags.csv - development_priorities.csv -
benchmark_comparisons.csv - benchmark_summary.csv

reference/ - benchmark_catalog.csv - benchmark_values.csv

------------------------------------------------------------------------

## 4. Analysis Pipeline

validate_data ↓ build_sessions ↓ update_personal_bests ↓
build_analysis_scores ↓ build_domain_profiles ↓ build_trend_analysis ↓
detect_fatigue_flags ↓ build_benchmark_comparisons ↓
build_development_priorities ↓ build_latest_summary

------------------------------------------------------------------------

## 5. Event Scores

file

data/analysis/event_scores.csv

columns

athlete session_date test_type metric_name metric_value unit pb_value
pb_delta prev_value prev_delta ma3 trend_30d stability status

status

improving plateau declining

------------------------------------------------------------------------

## 6. Domain Profiles

file

data/analysis/domain_profiles.csv

domain

acceleration top_speed cod lower_body_power reactive_strength
upper_body_power speed_endurance

example

athlete,session_date,domain,score,status,evidence
togo,2026-03-08,acceleration,72,improving,"20m sprint改善"
togo,2026-03-08,reactive_strength,48,plateau,"jump停滞"

------------------------------------------------------------------------

## 7. Trend Analysis

file

data/analysis/trend_analysis.csv

metrics

rolling_mean rolling_std pb_rate progress_rate recent_change

------------------------------------------------------------------------

## 8. Fatigue Detection

file

data/analysis/fatigue_flags.csv

flags

low_readiness_performance_drop sleep_deficit_flag fatigue_suspected

------------------------------------------------------------------------

## 9. Benchmark Layer

ベンチマークは3層

1 同年代一般 2 競技上位 3 国内 / 世界トップ

------------------------------------------------------------------------

### benchmark_catalog

data/reference/benchmark_catalog.csv

columns

benchmark_id benchmark_name category population age_band country source

------------------------------------------------------------------------

### benchmark_values

data/reference/benchmark_values.csv

columns

test_type p10 p25 p50 p75 p90 elite

------------------------------------------------------------------------

### benchmark_comparisons

data/analysis/benchmark_comparisons.csv

columns

athlete session_date test_type athlete_value benchmark_id
percentile_estimate gap_to_p50 gap_to_p75 gap_to_elite status_label
motivational_label

motivational_label examples

平均到達 平均超え 上位25% 競技上位接近 成長率良好

------------------------------------------------------------------------

## 10. Development Priorities

file

data/analysis/development_priorities.csv

columns

priority_rank domain issue_type evidence recommendation
expected_transfer review_after_days

example

1 reactive_strength plateau jump停滞 pogo_jump acceleration 21 2 cod
unstable trialばらつき deceleration_drill change_of_direction 14

------------------------------------------------------------------------

## 11. Dashboard Outputs

docs/dashboards/

latest_summary.md latest_analysis.md latest_priority_plan.md

summary構成

1 今日の総評 2 伸びている能力 3 停滞している能力 4 ベンチマーク比較 5
今週の優先課題 6 推奨トレーニング

------------------------------------------------------------------------

## 12. Implementation Roadmap

Phase1

event_scores trend_analysis domain_profiles

Phase2

fatigue_flags benchmark_comparisons

Phase3

development_priorities training_recommendations

------------------------------------------------------------------------

## 13. Design Principles

1 自分比較を重視

過去の自分 \> 他者比較

2 能力ドメインで評価

測定種目ではなく能力ドメイン

3 モチベーション設計

同年代 競技上位 世界トップ

------------------------------------------------------------------------

## 14. Expected Outcome

測定記録ツール ↓ 分析ツール ↓ 育成意思決定システム
