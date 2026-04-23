# RSA Measurement Protocol v1.0

---

## ■ 基本情報

* version: v1.0
* last_updated: 2026-04-16
* scope: 反復スプリント能力（RSA）
* purpose: 疲労下でのスプリント維持能力評価

---

## ■ 1. テスト設計

* 距離：20m
* 本数：6本
* 休息：20秒
* 強度：全力

---

## ■ 2. 共通ルール

### スタート

* 静止スタート
* 後足離地で判定

---

### フィニッシュ

* 胸で通過

---

### 無効判定

* 明らかな力抜き
* スタート遅延
* 減速ゴール

---

## ■ 3. 測定項目

* 各本タイム（6本）
* 平均タイム
* ベストタイム
* ディクレメント（低下率）

---

## ■ 4. CSV

```csv
test_type, rep, time, unit, valid, invalid_reason, protocol_version
```

```csv
rsa, 1, 3.45, sec, true, , v1.0
rsa, 6, 3.78, sec, true, , v1.0
```

---

## ■ 5. invalid_reason

```text
low_effort
late_start
deceleration
```

---

## ■ 6. 目的

* スプリント持続能力の可視化
