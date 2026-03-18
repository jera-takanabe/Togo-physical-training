# Elastic Profile Analysis 仕様書 v1.0

## 1. 目的

本仕様は、ジャンプ系テストとスプリント系テストの関係から、 選手の
**弾性能力・パワー能力・スプリント転移特性** を評価する Elastic Profile
Analysis を定義する。

本分析の目的は次の通り。

-   スプリント能力の背景を分解する
-   パワー不足か、弾性不足か、技術先行型かを判別する
-   限られた時間内で、最も効率のよいトレーニング優先順位を決める
-   将来の最高到達点を引き上げるための育成判断材料を作る

------------------------------------------------------------------------

# 2. 背景

スプリント能力は、単なる走技術だけでなく、
次のような身体能力の影響を強く受ける。

-   垂直方向の爆発力
-   水平方向の爆発力
-   反発力 / stiffness
-   接地時間の短さ
-   力発揮方向

本プロジェクトでは、低設備環境でも継続的に測定しやすい次の4指標を中心に扱う。

-   CMJ
-   RSI
-   Standing Long Jump
-   10m Sprint

------------------------------------------------------------------------

# 3. 入力データ

## 3.1 必須入力

`data/analysis/test_scores.csv`

対象 test:

-   `cmj`
-   `rsi`
-   `standing_long_jump`
-   `10m_sprint`

使用列:

-   `athlete`
-   `session_date`
-   `test`
-   `raw_value`
-   `unit`
-   `radar_score`

------------------------------------------------------------------------

# 4. 基本指標

## 4.1 Elastic Index

``` text
elastic_index = radar_score(rsi)
```

意味: - 反発力 - stiffness - 短接地能力 - reactive strength

------------------------------------------------------------------------

## 4.2 Vertical Power Index

``` text
vertical_power_index = radar_score(cmj)
```

意味: - 垂直方向の爆発力 - 下肢パワー - SSC の活用

------------------------------------------------------------------------

## 4.3 Horizontal Power Index

``` text
horizontal_power_index = radar_score(standing_long_jump)
```

意味: - 水平方向の力発揮 - 加速局面への転移しやすさ

------------------------------------------------------------------------

## 4.4 Sprint Index

``` text
sprint_index = radar_score(10m_sprint)
```

意味: - 初期加速能力 - スプリント技術を含む総合指標

------------------------------------------------------------------------

# 5. 派生指標

## 5.1 Power Index

``` text
power_index =
mean(
  vertical_power_index,
  horizontal_power_index
)
```

意味: - 一般的な爆発力レベル - スプリントの土台となる出力能力

------------------------------------------------------------------------

## 5.2 Sprint Transfer Index

``` text
sprint_transfer_index =
sprint_index - power_index
```

解釈: - 正の値が大きい - パワーの割にスプリントが高い - 技術先行型 -
伸びしろが大きい可能性 - 0付近 -
スプリントとパワーのバランスが取れている - 負の値が大きい -
パワーの割にスプリントへ転移できていない - 走技術 /
力の使い方の改善余地が大きい

------------------------------------------------------------------------

## 5.3 Elastic Transfer Index

``` text
elastic_transfer_index =
sprint_index - elastic_index
```

解釈: - 正の値が大きい - 弾性能力の割にスプリントが高い - 技術先行 /
弾性不足の可能性 - 負の値が大きい -
弾性能力は高いのにスプリントへ転移していない - acceleration mechanics
の改善余地

------------------------------------------------------------------------

## 5.4 Power--Elastic Balance

``` text
power_elastic_balance =
power_index - elastic_index
```

解釈: - 正の値が大きい - パワー優位 - 負の値が大きい - 弾性優位 -
0付近 - バランス型

------------------------------------------------------------------------

# 6. タイプ分類

## 6.1 Skill-Driven Sprinter

条件例:

``` text
sprint_transfer_index >= 20
and power_index < 50
```

特徴: - スプリント能力が高い - しかしジャンプ系の土台能力がまだ低い -
技術で走れている可能性が高い - 将来的な伸びしろが大きい

推奨: - 水平パワー強化 - RSI強化 - スプリントは維持しつつ土台作り

------------------------------------------------------------------------

## 6.2 Elastic Deficit Type

条件例:

``` text
elastic_index < 50
and sprint_index >= 60
```

特徴: - 走力に対して反発力が不足 - 接地改善で伸びやすい

推奨: - pogo - drop jump - low amplitude plyometrics

------------------------------------------------------------------------

## 6.3 Power Deficit Type

条件例:

``` text
power_index < 50
and sprint_index >= 60
```

特徴: - スプリントの土台となるパワー不足 - 将来的な出力向上余地が大きい

推奨: - standing long jump 系 - bounding - med ball throw - jump squat
系（将来）

------------------------------------------------------------------------

## 6.4 Transfer Deficit Type

条件例:

``` text
power_index >= 60
and sprint_index < 60
```

特徴: - パワーはあるが走力へ転移していない - 技術改善優先

推奨: - acceleration mechanics - wall drill - start drill

------------------------------------------------------------------------

## 6.5 Balanced Development Type

条件例:

``` text
abs(sprint_transfer_index) < 10
and abs(power_elastic_balance) < 10
```

特徴: - 全体のバランスが良い - 次のボトルネックを Sprint Profile や COD
から探す

------------------------------------------------------------------------

# 7. 出力ファイル

## 7.1 elastic_profile_scores.csv

推奨パス:

``` text
data/analysis/elastic_profile_scores.csv
```

推奨列:

  列名                     説明
  ------------------------ ------------------------
  athlete                  選手
  session_date             測定日
  cmj_raw                  CMJ raw
  rsi_raw                  RSI raw
  slj_raw                  standing long jump raw
  sprint10_raw             10m sprint raw
  vertical_power_index     CMJ radar
  elastic_index            RSI radar
  horizontal_power_index   SLJ radar
  sprint_index             10m radar
  power_index              平均パワー
  sprint_transfer_index    sprint - power
  elastic_transfer_index   sprint - elastic
  power_elastic_balance    power - elastic
  elastic_profile_type     タイプ分類
  training_priority_1      優先課題1
  training_priority_2      優先課題2
  notes                    補足

------------------------------------------------------------------------

# 8. type 判定ロジック（優先順）

判定は上から順に行う。

1.  Skill-Driven Sprinter
2.  Power Deficit Type
3.  Elastic Deficit Type
4.  Transfer Deficit Type
5.  Balanced Development Type
6.  Unclassified

------------------------------------------------------------------------

# 9. トレーニング優先順位の自動付与

## Skill-Driven Sprinter

-   training_priority_1 = "水平パワー強化"
-   training_priority_2 = "RSI強化"

## Power Deficit Type

-   training_priority_1 = "Broad Jump / Bounding"
-   training_priority_2 = "下肢爆発力"

## Elastic Deficit Type

-   training_priority_1 = "Drop Jump / Pogo"
-   training_priority_2 = "接地改善"

## Transfer Deficit Type

-   training_priority_1 = "加速技術"
-   training_priority_2 = "力の方向づけ"

## Balanced Development Type

-   training_priority_1 = "総合維持"
-   training_priority_2 = "次のボトルネック確認"

------------------------------------------------------------------------

# 10. 可視化案

## 10.1 Elastic Triangle

3軸で表示

``` text
Power
Elastic
Sprint
```

または

``` text
CMJ
RSI
10m
```

------------------------------------------------------------------------

## 10.2 Transfer Bar

-   sprint_transfer_index
-   elastic_transfer_index
-   power_elastic_balance

------------------------------------------------------------------------

## 10.3 Trend View

時系列で追う

-   power_index
-   elastic_index
-   sprint_index
-   sprint_transfer_index

------------------------------------------------------------------------

# 11. 解釈原則

本分析は、単一測定で断定するためのものではなく、
**継続測定により「伸ばすべき能力」を見つけるためのもの**とする。

特に U12 では、

-   成長
-   技術習得
-   測定誤差

の影響が大きいため、トレンド解釈を優先する。

------------------------------------------------------------------------

# 12. 今回の選手データへの暫定解釈例

例:

-   10m_sprint radar = 100
-   cmj radar = 32
-   rsi radar = 48
-   standing_long_jump radar = 20

この場合、

``` text
power_index = 26
sprint_transfer_index = 74
```

となり、典型的な

``` text
Skill-Driven Sprinter
```

と解釈できる。

つまり、 - 走技術で速い - まだ身体能力の土台が十分でない -
正しく鍛えると伸び幅が大きい

という状態を示す。

------------------------------------------------------------------------

# 13. 設計判断の明示

## 外部知見に沿う部分

-   ジャンプ系能力とスプリント能力は関連が強い
-   RSI は短接地スプリント能力と関係が深い
-   standing long jump は acceleration の proxy として有用

## 本プロジェクト独自ルール

-   elastic_index / power_index / sprint_transfer_index の定義
-   タイプ分類しきい値
-   training_priority の自動付与
-   CSV 列構成

これらは、U12育成・低設備・長期トレンド重視という条件に合わせた
実務設計ルールである。
