# Sprint Measurement Protocol v1.0

---

## ■ 基本情報

* version: v1.0
* last_updated: 2026-04-16
* scope: 10m / 20m / 30m / Fly-5 / Fly-10
* purpose: スプリント能力の正確な分解評価

---

## ■ 1. 共通ルール

### 1.1 スタート

* 静止スタート（統一）
* 判定：**後足が完全に離れた瞬間**

---

### 1.2 フィニッシュ

* 判定：**胸（体幹）がライン通過**

---

### 1.3 無効判定

* フライング
* 減速してのゴール
* ライン判定不明
* スリップ・接触

---

## ■ 2. 測定項目

* 0–10m
* 0–20m
* 0–30m
* 20–25m（Fly-5）
* 20–30m（Fly-10）

---

## ■ 3. 測定条件

### カメラ

* 240fps
* 側面（中央付近）

### マーカー

* 0 / 10 / 20 / 25 / 30m

---

## ■ 4. 試技

* 2〜3本
* ベスト採用

---

## ■ 5. CSV

```csv
test_type, distance, time, unit, valid, invalid_reason, protocol_version
```

```csv
sprint, 10, 1.62, sec, true, , v1.0
sprint, 30, 5.39, sec, true, , v1.0
```

---

## ■ 6. invalid_reason

```text
false_start
deceleration
unclear_line
slip
```

---

## ■ 7. 目的

* 加速・最大速度の分解評価
