# Club HashCash ゲームデータ分析
## Winstonダッシュボード・スクリーンショットより（2026年3月28日時点）

---

## 1. ネットワーク現況

| 指標 | 値 |
|---|---|
| 施設数 | 411/730 (オンライン/最大) |
| ネットワークハッシュレート | 182.689 GH/s |
| ネットワーク消費電力 | 408.4 kW |
| エミッション/ブロック | 2.50 hCASH |
| エミッション/日 | 214,925 hCASH (~85,970 blocks/day) |
| 次の半減期まで | 6日5時間56分 (537,077 blocks) |
| 現在ブロック | 81,495,250 |
| hCASH価格 | $0.0798 / 0.009016 AVAX |

### トークン供給状況
| 指標 | 値 |
|---|---|
| 総供給（発行済み） | 3,050,400 / 21,000,000 |
| バーン済み | 4,018,688 hCASH |
| トレジャリー | 1,807,404 hCASH |
| 残りマイニング可能 | 16,981,313 |
| 流通量 | 1,242,995 (供給 - トレジャリー) |
| 流動性 | Pharaoh V2: 291,142 / V3 CL: 72,932 |

**重要な発見**: バーン量(4.01M)が総供給(3.05M)を超えている。つまりゲーム内でhCASHを消費する活動（施設購入、マイナー購入、電気代等）がエミッションを上回るペースで行われている。

---

## 2. 施設ティア

| レベル | グリッド | スロット数 | 最大電力 | 電気代/kWh | コスト | オンライン数 | ハッシュシェア |
|---|---|---|---|---|---|---|---|
| Lv.1 | 2×2 | 4 | 400W | 8.96 (現在8.89) | 2 AVAX | 135/400 | 4.0% |
| Lv.2 | 2×3 | 6 | 1,000W | 7.16 (現在7.11) | 500 hCASH | 181/228 | 33.1% |
| Lv.3 | 3×3 | 9 | 2,000W | 6.27 (現在6.23) | 3,000 hCASH | 74/79 | 31.4% |
| Lv.4 | 3×4 | 12 | 6,000W | 7.16 (現在7.11) | 10,500 hCASH | 21/23 | 31.6% |

**分析ポイント**:
- Lv1はオンライン率が低い（135/400 = 34%）→ 放置施設が多い
- Lv2-4は高稼働率（79-91%）
- Lv1は全スロットの17%しか使っていない（277/1600）
- Lv4はたった21施設で31.6%のハッシュシェア → 鯨プレイヤー集中

---

## 3. 公式ハードウェアベンダー（5社）

1. **Red Dragon Technologies** (rdhash.com) - GPU・リグ中心、v2.0アップグレード提供
2. **HashTech** (hashtech.tech) - ASIC特化、Beast系列
3. **Plasma Systems** (plasmasystems.io) - 高効率GPU、Plasma Base/XL/XXL/Absolute
4. **Lightning GPU** (lightninggpu.com) - GPUライン、G1/G2/G3 + リグ組立
5. **Jvidia** (jvidia.xyz) - 最新GPU、JX420/JX450/JX500

---

## 4. 全マイナーリスト（効率順・スクショから読み取り）

### Tier S - 超高効率（1.0+ MH/W）
| # | 名前 | タイプ | MH/s | W | MH/W | 価格(hCASH) | 備考 |
|---|---|---|---|---|---|---|---|
| 45 | RedDragon Octa-TiX | Custom Rig | 400 | 200 | 2.000 | 10,000 | 8× TiX + 2,000組立 |
| 52 | Stormcore Superconductor | Specialized | 1,000 | 0 | ∞ | 25,000 | 電力ゼロ |
| 27 | Moats Miner | Specialized | 100 | 100 | 1.000 | 5,000 | |
| 46 | Campfire Miner | Specialized | 200 | 200 | 1.000 | 1,300 | |

### Tier A - 高効率（0.5-0.99 MH/W）
| # | 名前 | タイプ | MH/s | W | MH/W | 価格(hCASH) | 備考 |
|---|---|---|---|---|---|---|---|
| 43 | Lightning G3 Tri-Rig | Custom Rig | 150 | ~200 | 0.750 | 5,000 | |
| 40 | The Grotto Miner | Specialized | 150 | 200 | 0.750 | ? | |
| 35 | Quad Socket CPU v2.0 | Custom Rig | 120 | 200 | 0.600 | 2,500 | |
| 47 | Jvidia JX420 | GPU | 200 | ~500 | ~0.560 | ~3,300 | |
| 30 | Lightning G3 | GPU | 50 | 100 | 0.500 | 1,500 | |
| 31 | Galactic Hash C | Specialized | 300 | 600 | 0.500 | 10,000 | |
| 42 | Plasma Absolute | Unknown | 400 | 800 | 0.500 | 10,000 | |
| 48 | Jvidia JX450 | GPU | 400 | ~800 | ~0.500 | 5,000 | |

### Tier B - 中効率（0.2-0.49 MH/W）
| # | 名前 | タイプ | MH/s | W | MH/W | 価格(hCASH) |
|---|---|---|---|---|---|---|
| 32 | RedDragon TiX | GPU | 45 | 100 | 0.450 | 1,000 |
| 34 | Ennee Socket CPU | Custom Rig | 50 | 200 | ~0.450 | 1,700 |
| 49 | Jvidia JX500 | GPU | 500 | 1,200 | 0.417 | 7,000 |
| 44 | HashTech BeastRack | Custom Rig | 800 | 2,000 | 0.400 | 15,000 |
| 36 | Lightning G1 Quad-Rig | Custom Rig | 80 | 200 | 0.400 | 1,500 |
| 37 | Lightning G2 Quad-Rig | Custom Rig | 140 | 400 | 0.350 | 4,500 |
| 33 | HashTech Beast2 ASIC | ASIC | 350 | 1,000 | 0.350 | ? |
| 29 | CPU Miner v2.0 | CPU | 30 | 100 | 0.300 | 500 |
| 25 | HashTech Mini Beast | ASIC | 150 | 500 | 0.300 | 5,000 |
| 26 | Plasma XXL | GPU | 60 | ~200 | ~0.300 | 5,000 |
| 14 | Plasma Base | GPU | 25 | ~100 | 0.250 | 750 |
| 15 | Plasma XL | GPU | 45 | 200 | 0.225 | 1,000 |
| 23 | Windflash Red | Wind/Plasma | 125 | 600 | 0.208 | 1,500 |
| 24 | Windflash Blue | Wind/Plasma | 250 | 1,200 | 0.208 | 6,000 |
| 6 | Quad Socket CPU | Custom Rig | 40 | 200 | 0.200 | 1,700 |
| 11 | Lightning G1 | GPU | 20 | 100 | 0.200 | 750 |
| 17 | HashTech Beast ASIC | ASIC | 200 | 1,000 | 0.200 | 3,500 |

### Tier C - 低効率（<0.2 MH/W）= 旧世代マイナー
| # | 名前 | タイプ | MH/s | W | MH/W | 価格(hCASH) |
|---|---|---|---|---|---|---|
| 19-22 | RedDragon各種 v2.0 | Custom Rig | 45-110 | 300-600 | 0.138-0.175 | 2,500-3,750 |
| 12 | Lightning G2 | GPU | 35 | ~200 | 0.175 | 1,000 |
| 2 | DragonTech RedDragon | GPU | 14 | 100 | 0.140 | 750 |
| 13 | Miner #13 | Unknown | 250 | 2,000 | 0.125 | 5,000 |
| 7 | RedDragon Tri-Rig | Custom Rig | 45 | 400 | 0.113 | 2,750 |
| 1 | Home Brew CPU Miner | CPU | 10 | 100 | 0.100 | 200 |
| 8 | RedDragon Ti Duo-Rig | Custom Rig | 70 | 700 | 0.100 | 2,000 |
| 4 | RedDragon Quadro | CPU Rig | 70 | 600 | ~0.007 | 2,000 |
| 16 | USB Miner | USB | 1 | ~10 | 0.010 | 300 |
| 18 | Quad USB Array | USB Rig | 0 | 100 | 0.000 | 50 |

### 特殊アイテム（0 MH/s / ユーティリティ系）
| # | 名前 | タイプ | 価格(hCASH) | 備考 |
|---|---|---|---|---|
| 9 | Jnnt | Device | ? | 0 MH/s, 0W |
| 10 | Jnead | Device | ? | 0 MH/s, 0W |
| 38 | Jiga Jiant | Device | 10,000 | 150 MH/s, 0W! |
| 39 | Jiga Jnead | Device | 10,000 | 150 MH/s, 0W! |
| 41 | Bundle of Sticks | Device | 100 | 0 MH/s, 0W |
| 50 | Mini Torch | ? | 300 | 0 MH/s, 0W |
| 51 | Book of Matches | ? | 300 | 0 MH/s, 0W |
| 53 | Burnt Sticks | Device | ? | 0 MH/s, 0W |
| 28 | ne pas ouvrir | Specialized | 5,000 | 0 MH/s, 0W |

**注目**: Jiga JiantとJiga Jneadは0Wで150 MH/sを出す。これはStormcore Superconductor(0Wで1000MH/s)と同じく「電力を消費しない」特殊カテゴリ。

---

## 5. 重要な構造的パターン

### A. Custom Rig（組立リグ）の仕組み
既にゲーム内に「ベースマイナーを組み合わせてリグを作る」メカニズムが存在:
- HashTech BeastRack = 4× HashTech "The Beast" ASIC + 1,000 assembly fee
- RedDragon Octa-TiX = 8× RedDragon TiX + 2,000 assembly fee

→ **これは「Second Hash」のコアメカニズムに直結する既存パターン**

### B. v2.0アップグレードの存在
複数のマイナーにv2.0バージョンが存在:
- CPU Miner → CPU Miner v2.0 (0.100→0.300 MH/W、3倍改善)
- RedDragon Tri-Rig → v2.0 (0.113→0.150 MH/W)
- RedDragon Quadro → v2.0 (電力600W→400Wに削減)

→ **「旧型→改良型」の進化パスが既にある**

### C. 効率ギャップの深刻さ
- 最高効率: RedDragon Octa-TiX = 2.000 MH/W
- 最低効率: USB Miner = 0.010 MH/W
- **200倍の差**がある
- Tier Cの旧マイナーは実質的に「死んでいる」

### D. Lv1施設の放棄問題
- 400施設中135しかオンラインでない（34%）
- Lv1は全ネットワークハッシュの4%しか貢献していない
- 多くの初期プレイヤーが離脱している可能性大

### E. 特殊アイテムの示唆
- Bundle of Sticks, Mini Torch, Book of Matches → 焚き火/燃焼系のテーマ？
- Burnt Sticks → 何かを「燃やした」結果のアイテム？
- Campfire Miner（効率1.0）→ これらの燃焼系アイテムと関連？
- **バーン（燃焼）メカニズムがゲームのテーマに組み込まれている可能性**
