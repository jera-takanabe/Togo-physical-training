# データ記録ルール（暫定）

---

## 1. 基本方針

- 測定したデータは必ず raw に保存する
- 既存構造を壊さない
- 不明な場合は新しいファイルを作る

---

## 2. 種目ごとの保存先

| 種目 | 保存先 |
|------|--------|
| Sprint | data/raw/sprint_tests_raw.csv |
| Jump | data/raw/jump_tests_raw.csv |
| COD | data/raw/cod_tests_raw.csv |
| Horizontal | data/raw/horizontal_tests_raw.csv |
| Throw (MBT) | data/raw/throw_tests_raw.csv |
| RSA | data/raw/rsa_tests_raw.csv |
| YO-YO | data/raw/yoyo_tests_raw.csv |

---

## 3. 記録単位

- 1試技 = 1行
- trial番号を付与
- valid=true/falseを必ず記録

---

## 4. セッション

- セッションは「1回の評価としてまとめる測定単位」とする
- 日付ではなく評価単位で管理する
- 複数日にまたがっても同一 session_id を使用可能

例：
- 3/8 sprint、3/9 jump → 同一セッション
- 一部再測定も同一セッションに含める

session_idの命名ルール：
- YYYY-MM_testN

### ■ セッション統一ルール（重要）

同一 session_id にまとめる条件：

- 同一の評価目的で実施した測定
- 同一の分析として扱う測定
- 同一のレポート（dashboard）に反映する測定

例：
- sprint / jump / Yo-Yo / RSA をまとめて評価する場合
→ 同一 session_id を使用する

分ける条件：

- 別のタイミングで評価する場合
- コンディションや環境が大きく異なる場合
- 別レポートとして扱う場合

補足：

- session_id は「分析単位」であり「測定日」ではない
- date は実施日として別に保持する

---

## 5. 必須項目

- date
- athlete
- test_type
- trial
- valid

---

## 6. 原則

- 仮データは必ず削除または置き換える
- 実測データを優先する
- 後から分析できる形で残す

---

## 7. 保留事項

- RSAの集計方法
- YOYOのレベル管理
- fatigueの定義

---
