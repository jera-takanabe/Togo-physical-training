# Sprint Profile Analysis 仕様書 v1.0

## 1. 目的

本仕様は、既存のスプリント測定データから\
**加速型か、最大速度型か、あるいは両方が弱いのか** を判別するための\
Sprint Profile Analysis の設計を定義する。

本分析は、単なる 20m や 30m の総合タイムではなく、

-   立ち上がりの速さ
-   中間加速の伸び
-   最大速度局面
-   スピード持久の簡易的な余裕度

を分けて解釈することを目的とする。

------------------------------------------------------------------------

# 2. 背景と考え方

スプリント能力は単一の能力ではなく、少なくとも

-   初期加速
-   加速維持
-   最大速度

の複数要素から成る。

既存研究では、10m タイムは加速能力の良い反映であり、\
30m 走では 20--30m 区間が最大速度能力の推定に使えるとされている。\
また、若年選手では年齢とともに加速距離や最大速度局面が変化するため、\
分割区間で見ることに意味がある。

本プロジェクトでは、特殊機材を使わずに動画解析から取得できる

-   5m
-   10m
-   20m
-   30m
-   Fly5
-   Fly10

を用いて、実用的な Sprint Profile を構成する。

------------------------------------------------------------------------

# 3. 入力データ

## 3.1 必須入力

  項目         単位   説明
  ------------ ------ -------------------
  time_5m      s      0--5m 累積タイム
  time_10m     s      0--10m 累積タイム
  time_20m     s      0--20m 累積タイム
  time_30m     s      0--30m 累積タイム
  fly5_time    s      Fly5 タイム
  fly10_time   s      Fly10 タイム

## 3.2 任意入力

  項目                単位   説明
  ------------------- ------ ---------------
  yoyo_distance_m     m      YoYo IR1 距離
  rsa_best_time       s      RSA ベスト
  rsa_mean_time       s      RSA 平均
  athlete_height_cm   cm     身長
  athlete_weight_kg   kg     体重

任意入力は、Sprint Profile の補助解釈に使う。

------------------------------------------------------------------------

# 4. 基本 split 計算

累積タイムから区間タイムを算出する。

## 4.1 区間タイム

``` text
split_0_5   = time_5m
split_5_10  = time_10m - time_5m
split_10_20 = time_20m - time_10m
split_20_30 = time_30m - time_20m
```

## 4.2 区間平均速度

``` text
v_0_5   = 5  / split_0_5
v_5_10  = 5  / split_5_10
v_10_20 = 10 / split_10_20
v_20_30 = 10 / split_20_30
v_fly5  = 5  / fly5_time
v_fly10 = 10 / fly10_time
```

単位はすべて m/s とする。

------------------------------------------------------------------------

# 5. 主要指標

## 5.1 Acceleration Index

立ち上がりの加速能力を表す主指標。

``` text
acceleration_index =
mean(
  radar_score(5m),
  radar_score(10m),
  radar_score(20m)
)
```

補助的には、速度増加量も見る。

``` text
delta_v_0_10 = v_5_10 - v_0_5
delta_v_10_20 = v_10_20 - v_5_10
```

意味: - 高いほど初期加速が良い - 5m はスタート技術の影響も強く受ける -
10m / 20m を併用して安定化する

------------------------------------------------------------------------

## 5.2 Max Velocity Index

最大速度局面の能力を表す指標。

``` text
max_velocity_index =
mean(
  radar_score(fly5),
  radar_score(fly10),
  radar_score(20_30_segment)
)
```

ここで

``` text
radar_score(20_30_segment)
```

は 20--30m 区間平均速度を別 benchmark でスコア化したものとする。

意味: - 高いほどトップスピード能力が高い - Fly10 を主指標、Fly5
を補助指標として扱う - 20--30m 区間は動画 split から算出できる簡易 MSS
代理指標

------------------------------------------------------------------------

## 5.3 Speed Reserve Index（実務版）

本来の ASR（Anaerobic Speed Reserve）は MSS と MAS
の差で扱うことが多い。\
本プロジェクトではまず、簡易版の「スプリント余裕度」を定義する。

### 方式A: Endurance 情報なし版

``` text
speed_reserve_index_basic =
max_velocity_index - acceleration_index
```

解釈: - 正の値が大きい → 最高速は高いが、立ち上がりが相対的に弱い -
0付近 → 加速と最高速のバランスが良い - 負の値が大きい →
初速優位だが、トップスピードが伸び切らない

### 方式B: Endurance 情報あり版（推奨）

YoYo または RSA がある場合は補助指標を追加する。

``` text
engine_modifier =
mean(
  radar_score(yoyo_distance_m),
  radar_score_inverse(rsa_mean_time)
)
```

``` text
speed_reserve_index =
max_velocity_index - engine_modifier
```

解釈: - 最高速に対して、反復や有酸素系の余裕がどれくらいあるかを見る -
まず v1.0 では参考指標とし、主判定には使わない

------------------------------------------------------------------------

## 5.4 Split Balance Index

区間の伸び方を見るバランス指標。

``` text
split_balance_index =
(v_20_30 - v_0_5) / v_20_30
```

解釈: - 値が大きい → 立ち上がりより後半伸びるタイプ - 値が小さい →
初速寄り - 異常に大きい / 小さい → 計測誤差や start / fly
判定ルールの再確認候補

------------------------------------------------------------------------

# 6. タイプ分類ロジック

## 6.1 基本タイプ

### Acceleration Type

条件例

``` text
acceleration_index >= max_velocity_index + 8
```

特徴: - 5m / 10m に強い - 試合での短距離反応に向く -
最高速の伸びが課題になりやすい

------------------------------------------------------------------------

### Max Velocity Type

条件例

``` text
max_velocity_index >= acceleration_index + 8
```

特徴: - Fly 系や 20--30m 区間に強い - 助走があると速い -
初速改善で総合スプリント能力が大きく伸びる余地がある

------------------------------------------------------------------------

### Balanced Sprint Type

条件例

``` text
abs(acceleration_index - max_velocity_index) < 8
```

特徴: - 加速と最高速のバランスが良い - 次の改善ポイントは Endurance /
RSA や Elastic 系から探しやすい

------------------------------------------------------------------------

### Underdeveloped Sprint Type

条件例

``` text
acceleration_index < 50 and max_velocity_index < 50
```

特徴: - 全体的に基礎段階 - 技術改善・筋力・反発力の土台づくりを優先する

------------------------------------------------------------------------

## 6.2 補助タイプ

### Elastic Sprinter

条件例

``` text
elastic_domain_score >= 70
and max_velocity_index >= 65
```

特徴: - RSI や Bounding が高く、接地反発に強みがある

### Power Sprinter

条件例

``` text
power_domain_score >= 70
and acceleration_index >= 65
```

特徴: - CMJ / SJ / Broad jump が高く、押し出す能力が強い

------------------------------------------------------------------------

# 7. 出力指標一覧

## 7.1 sprint_profile_scores.csv

  列名                        説明
  --------------------------- ----------------------
  athlete_id                  選手ID
  session_date                測定日
  split_0_5                   0--5m 区間タイム
  split_5_10                  5--10m 区間タイム
  split_10_20                 10--20m 区間タイム
  split_20_30                 20--30m 区間タイム
  v_0_5                       0--5m 平均速度
  v_5_10                      5--10m 平均速度
  v_10_20                     10--20m 平均速度
  v_20_30                     20--30m 平均速度
  v_fly5                      Fly5 平均速度
  v_fly10                     Fly10 平均速度
  acceleration_index          加速指標
  max_velocity_index          最大速度指標
  speed_reserve_index_basic   実務版 speed reserve
  split_balance_index         区間バランス
  sprint_profile_type         タイプ分類

------------------------------------------------------------------------

## 7.2 sprint_profile_summary.csv

  列名                  説明
  --------------------- -----------------------
  athlete_id            選手ID
  session_date          測定日
  sprint_profile_type   主要タイプ
  primary_strength      主な強み
  primary_limit         主な制約
  training_focus_1      優先トレーニング1
  training_focus_2      優先トレーニング2
  validation_flag       再測定 / 要確認フラグ

------------------------------------------------------------------------

# 8. 可視化案

## 8.1 Sprint Velocity Stair

横軸: 区間\
縦軸: 平均速度

``` text
0-5m | 5-10m | 10-20m | 20-30m | Fly5 | Fly10
```

狙い: - どこで伸びるか - どこで失速 / 頭打ちになるか

------------------------------------------------------------------------

## 8.2 Sprint Profile Radar

4軸を推奨する。

``` text
Acceleration
Max Velocity
Elastic Support
Engine Support
```

ここで - Acceleration = acceleration_index - Max Velocity =
max_velocity_index - Elastic Support = elastic domain score - Engine
Support = endurance domain score

------------------------------------------------------------------------

## 8.3 Trend View

時系列で次を追う。

-   acceleration_index
-   max_velocity_index
-   split_balance_index

狙い: - 技術改善か - 最高速改善か - バランス改善か

------------------------------------------------------------------------

# 9. 異常値チェック

以下の条件では validation_flag を立てる。

## 9.1 累積タイム矛盾

``` text
time_5m >= time_10m
time_10m >= time_20m
time_20m >= time_30m
```

上記はすべて異常。

------------------------------------------------------------------------

## 9.2 Fly と 20--30m の不整合

``` text
abs(v_fly10 - v_20_30) / v_fly10 > 0.10
```

意味: - Fly10 と 20--30m が
10%以上ずれる場合、助走距離・ライン判定・動画切り出しを再確認する

------------------------------------------------------------------------

## 9.3 12歳として非現実的な高値

年齢 benchmark を大幅に超える場合は\
「才能の可能性」ではなく、まず測定妥当性を確認する。

------------------------------------------------------------------------

# 10. 実装ステップ

## Phase 1

-   split 計算
-   速度計算
-   acceleration_index
-   max_velocity_index
-   type 分類

## Phase 2

-   speed_reserve_index
-   summary 自動生成
-   trend chart

## Phase 3

-   benchmark 年齢補正
-   予測モデル
-   トレーニング提案自動化

------------------------------------------------------------------------

# 11. 解釈の原則

本分析は、単発の順位付けではなく\
**「どう速いか」「どこを伸ばすか」を示すためのもの**とする。

特に U12 では、

-   成長
-   技術習得
-   測定誤差

の影響が大きいため、\
1回の測定だけで断定せず、時系列トレンドを重視する。

------------------------------------------------------------------------

# 12. 根拠と設計判断

## 12.1 外部知見に基づく部分

-   10m タイムは加速能力の有効な反映である
-   20--30m 区間または flying split は最大速度能力の推定に有用である
-   若年選手では加速距離や最大速度局面が年齢とともに変化する
-   MSS と ASR の概念は競技プロフィールやトレーニング処方に有用である

## 12.2 本プロジェクト独自の設計判断

-   acceleration_index / max_velocity_index の具体式
-   speed_reserve_index_basic の簡易式
-   タイプ分類しきい値（±8）
-   validation_flag の閾値
-   出力 CSV 構造

これらは、低設備・動画解析・ジュニア育成用途に合わせた\
**実務設計ルール**として定義する。
