# Second Hash — プロジェクト概要

## ハッカソン情報

- **イベント**: Club HashCash Hashathon
- **トラック**: Hardware Supplier — "Launch a full miner brand for Club HashCash, including a lineup, website, and social presence ready for ecosystem integration."
- **賞金**: 1st $1,000 USDC / 2nd $200 USDC
- **応募開始**: 2026年4月1日
- **IP注記**: 優勝者のブランド・アートワークはゲームに統合される可能性あり
- **審査基準**: Relevance, Execution, Impact, Creativity, Usability

## ブランドコンセプト

**Second Hash** = Club HashCash初の「再製造（リファブリケーション）」ベンダー

### ポジショニング
既存5ベンダー（RedDragon, HashTech, Plasma, Lightning, Jvidia）は全て「新品ハードウェアメーカー」。Second Hashは唯一の「再製造ベンダー」として、ゲーム内に放置された旧世代マイナーNFTを回収・再構築し、新たなマイナーやブーストモジュールを生み出す。

### エコシステム貢献（コアバリュー）
1. **NFTバーン圧力**: 旧マイナーNFTをTrade-inで回収・バーン → 死んだNFTの清掃
2. **hCASHバーン圧力**: 再構築に手数料としてhCASH消費 → デフレ加速
3. **休眠プレイヤー復帰**: 放置されたLv1施設（66%が非稼働）の所有者にマイナーリサイクルという帰還動機を提供
4. **効率格差の緩和**: 200倍の効率ギャップ（USB: 0.010 vs Octa-TiX: 2.000 MH/W）の間を埋める

### ブランドアイデンティティ
- **カラー**: ダークアンバー/コッパー (#D4924A, #B87333) — 全既存ベンダーと非重複
- **テーマ**: 「修復と再構築」— 修理痕、溶接跡、異なるベンダー部品の混在
- **タグライン**: "Every hash deserves a second chance."
- **フォント**: Space Mono（テクニカル）+ Inter（本文）

---

## 製品ラインナップ

### マイナー（3モデル）

| モデル | コンセプト | MH/s | W | MH/W | 組立費(hCASH) | 素材 |
|---|---|---|---|---|---|---|
| SH-R1 "Reclaim" | CPU再構築 | 40 | 150 | 0.267 | 800 | 3× CPU系 or 8× USB系 |
| SH-R2 "Reforge" | GPU再構築 | 120 | 400 | 0.300 | 1,500 | 2× 旧GPU系 |
| SH-X1 "Overhaul" | マルチソース再構築 | 300 | 600 | 0.500 | 3,000 | 3× 異なるベンダーGPU+リグ |

**効率ポジション**: Tier B上位〜Tier A下位（0.267-0.500 MH/W）。旧マイナーよりは大幅に良いが、最新ハードウェア（Octa-TiX: 2.0）は脅かさない。

### ブーストモジュール（3タイプ）

| モデル | 効果 | 素材 | 組立費(hCASH) | 特殊ルール |
|---|---|---|---|---|
| SH-B1 "Patch" | 消費電力 -15% | 2× USB or 1× CPU系 | 300 | 取り外し時にバーン |
| SH-B2 "Splice" | ハッシュレート +10% | 1× GPU系 | 600 | 取り外し時にバーン |
| SH-B3 "Overclock" | +8% Hash / -10% Power | 1× GPU + 1× CPU | 1,000 | 取り外し時にバーン |

**メカニクス**: Craft → Attach → Boost → Remove（バーン）。非可逆的な取り外しで、戦略的な意思決定と持続的なデフレ圧力を生む。

### Trade-inレシピ（素材マイナー対象）

**最優先素材（Tier C: 効率 < 0.2 MH/W の実質稼働不能マイナー）:**
- Home Brew CPU Miner (0.100 MH/W)
- USB Miner (0.010 MH/W)
- Quad USB Array (0.000 MH/W)
- RedDragon Quadro (0.007 MH/W)
- RedDragon v1.0系各種 (0.100-0.175 MH/W)
- Lightning G2 単体 (0.175 MH/W)
- DragonTech RedDragon (0.140 MH/W)

---

## 提出物

| 成果物 | 形式 | 状態 |
|---|---|---|
| ブランドWebサイト | HTML (index.html) | ✅ 完成 |
| マイナーアートワーク | AI画像生成 | 🔄 プロンプト完成、生成待ち |
| 企画書 / ホワイトペーパー | TBD | ⏳ 未着手（画像確定後） |
| ソーシャルプレゼンス | X/Twitter | ⏳ 未着手 |

---

## 参考リンク

### ゲーム関連
- ゲーム本体: https://hashcash.club
- Winstonダッシュボード: https://hcash.winstonhq.com/hardware
- マーケットプレイス: https://hashcash.club/marketplace
- Player Guide: https://team1.blog/

### 既存ベンダーサイト（デザイン参考）
- Red Dragon Technologies: https://rdhash.com
- HashTech: https://hashtech.tech
- Plasma Systems: https://plasmasystems.io
- Lightning GPU: https://lightninggpu.com
- Jvidia: https://jvidia.xyz

### ネットワーク統計（2026年3月28日時点）
- 施設: 411/730 オンライン
- ハッシュレート: 182.689 GH/s
- hCASH価格: $0.0798
- バーン量: 4,018,688 > 供給量: 3,050,400
- 次の半減期: 約6日後
