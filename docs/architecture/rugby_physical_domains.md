# Rugby Physical Domains Design

Project: Togo Physical Training Purpose:
ラグビー育成に最適化したフィジカル能力ドメイン定義

------------------------------------------------------------------------

## 1. Overview

このドキュメントはラグビー選手育成におけるフィジカル能力を
**能力ドメイン（Physical Domains）として整理する設計書**である。

測定種目そのものではなく、

-   どの能力を伸ばすべきか
-   能力のバランスは適切か
-   トレーニング優先順位は何か

を判断するための基盤として使用する。

------------------------------------------------------------------------

## 2. Domain Philosophy

測定種目ではなく **能力ドメイン** を評価単位とする。

例

20m sprint → 加速能力\
CMJ → 下肢爆発力\
Pro Agility → COD能力

つまり

    測定 → 能力 → トレーニング

という構造で分析を行う。

------------------------------------------------------------------------

## 3. Core Physical Domains

ラグビー育成で重要なドメイン

  Domain              Description
  ------------------- ----------------
  acceleration        短距離加速能力
  top_speed           最高速度
  cod                 方向転換能力
  lower_body_power    下肢爆発力
  reactive_strength   SSC能力
  upper_body_power    上半身パワー
  speed_endurance     スピード持久力
  work_capacity       全体運動耐性

------------------------------------------------------------------------

## 4. Domain Definitions

### Acceleration

短距離で素早く加速する能力

重要度 ★★★★★

主な用途

-   ラインブレイク
-   ディフェンス突破
-   タックル回避

主な測定

-   10m sprint
-   20m sprint

------------------------------------------------------------------------

### Top Speed

最高速度能力

重要度 ★★★

ラグビーでは加速ほど重要ではないが、 ブレイク後の独走で重要。

測定

-   flying sprint

------------------------------------------------------------------------

### COD (Change of Direction)

方向転換能力

重要度 ★★★★★

ラグビーでは最重要能力の一つ

測定

-   Pro Agility
-   5-10-5
-   T test

------------------------------------------------------------------------

### Lower Body Power

下肢爆発力

重要度 ★★★★★

測定

-   CMJ
-   SJ
-   Standing Long Jump

------------------------------------------------------------------------

### Reactive Strength

SSC能力

重要度 ★★★★★

地面反発を利用する能力

測定

-   RSI
-   pogo jump
-   drop jump

------------------------------------------------------------------------

### Upper Body Power

上半身パワー

重要度 ★★★★

用途

-   タックル
-   パス
-   コンタクト

測定

-   medicine ball throw

------------------------------------------------------------------------

### Speed Endurance

スピードを繰り返す能力

重要度 ★★★★

測定

-   repeated sprint

------------------------------------------------------------------------

### Work Capacity

全体的運動耐性

重要度 ★★★

測定

-   YoYo test
-   shuttle runs

------------------------------------------------------------------------

## 5. Test → Domain Mapping

  Test                  Domain
  --------------------- ------------------
  10m sprint            acceleration
  20m sprint            acceleration
  CMJ                   lower_body_power
  SJ                    lower_body_power
  Standing Long Jump    lower_body_power
  Pro Agility           cod
  5-10-5                cod
  medicine ball throw   upper_body_power

------------------------------------------------------------------------

## 6. Domain Priority for Youth Rugby

12歳育成では以下を優先

1 acceleration 2 cod 3 reactive_strength 4 lower_body_power 5
upper_body_power 6 speed_endurance

理由

-   加速と方向転換がゲームで最も頻出
-   SSC能力がスピード系能力の基盤

------------------------------------------------------------------------

## 7. Domain Balance Model

理想的な能力バランス

    Acceleration      ★★★★★
    COD               ★★★★★
    ReactiveStrength  ★★★★★
    LowerBodyPower    ★★★★
    UpperBodyPower    ★★★★
    SpeedEndurance    ★★★
    TopSpeed          ★★★
    WorkCapacity      ★★★

------------------------------------------------------------------------

## 8. Integration with Analysis Layer

analysisレイヤーでは

    event_scores
    ↓
    domain_profiles
    ↓
    trend_analysis
    ↓
    development_priorities

という流れで能力を評価する。

------------------------------------------------------------------------

## 9. Training Translation

能力ドメインはトレーニング提案に直接つながる。

例

reactive_strength 低い

推奨

-   pogo jumps
-   ankle hops
-   low drop jumps

acceleration 低い

推奨

-   resisted sprint
-   hill sprint
-   sled sprint

------------------------------------------------------------------------

## 10. Expected Outcome

このドメイン設計により

測定データは

    記録
    ↓
    能力評価
    ↓
    課題抽出
    ↓
    トレーニング提案

という育成サイクルに変換される。
