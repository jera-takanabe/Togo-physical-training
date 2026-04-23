# Yo-Yo IR1 Measurement Protocol v1.0

---

## ■ 基本情報

* version: v1.0
* last_updated: 2026-04-16
* scope: Yo-Yo Intermittent Recovery Level 1
* purpose: 高強度反復持久力評価

---

## ■ 1. テスト概要

* 20m往復走
* ビープ音に同期
* 折り返し後10秒休息
* 限界まで継続

---

## ■ 2. 成功条件

* ビープまでにライン到達
* 2回連続失敗で終了

---

## ■ 3. 記録ルール

👉 **1回目の失敗の直前を記録**

---

## ■ 4. 測定項目

* 総距離（m）
* レベル
* 速度

---

## ■ 5. 無効判定

* 意図的停止
* 明らかな未到達
* 判定不明

---

## ■ 6. CSV

```csv
test_type, distance, level, speed, valid, invalid_reason, protocol_version
```

```csv
yoyo_ir1, 280, 13.1, 14.0, true, , v1.0
```

---

## ■ 7. invalid_reason

```text
early_stop
missed_line
unclear
```

---

## ■ 8. 目的

* 試合強度の持久力評価
