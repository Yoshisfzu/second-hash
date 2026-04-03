# Second Hash — 製品ロードマップ Phase 2 / Phase 3

---

## 現行カバー範囲（Phase 1）

### 対象素材: Tier C（効率 < 0.2 MH/W）— 実質稼働不能マイナー
| # | マイナー | MH/W | Phase 1 用途 |
|---|---|---|---|
| 1 | Home Brew CPU Miner | 0.100 | R1素材 / B1素材 / B3素材 |
| 2 | DragonTech RedDragon | 0.140 | R2素材 / B2素材 |
| 4 | RedDragon Quadro | 0.007 | R1素材 |
| 7 | RedDragon Tri-Rig | 0.113 | R2素材 |
| 8 | RedDragon Ti Duo-Rig | 0.100 | R2素材 |
| 11 | Lightning G1 | 0.200 | B2素材（ボーダーライン）|
| 12 | Lightning G2 | 0.175 | R2素材 / B2素材 |
| 13 | Miner #13 | 0.125 | R2素材 |
| 16 | USB Miner | 0.010 | R1素材 / B1素材 |
| 18 | Quad USB Array | 0.000 | R1素材 / B1素材 |
| 19-22 | RedDragon v2.0系 | 0.138-0.175 | R2素材 / X1素材 |

### Phase 1 製品の効率帯: 0.267 〜 0.500 MH/W

---

## 未対応マイナー分析

### グループA: Low Tier B（0.200〜0.250 MH/W）— 老朽化した標準機
| # | マイナー | タイプ | MH/s | W | MH/W | 価格 |
|---|---|---|---|---|---|---|
| 6 | Quad Socket CPU | Custom Rig | 40 | 200 | 0.200 | 1,700 |
| 14 | Plasma Base | GPU | 25 | 100 | 0.250 | 750 |
| 15 | Plasma XL | GPU | 45 | 200 | 0.225 | 1,000 |
| 17 | HashTech Beast ASIC | ASIC | 200 | 1,000 | 0.200 | 3,500 |
| 23 | Windflash Red | Wind/Plasma | 125 | 600 | 0.208 | 1,500 |
| 24 | Windflash Blue | Wind/Plasma | 250 | 1,200 | 0.208 | 6,000 |

**特徴**: 半減期を重ねるごとに収益性が急速に悪化。現時点ではギリギリ稼働可能だが、次の1〜2回の半減期で実質退役。

### グループB: Mid Tier B（0.300〜0.350 MH/W）— 中堅世代
| # | マイナー | タイプ | MH/s | W | MH/W | 価格 |
|---|---|---|---|---|---|---|
| 25 | HashTech Mini Beast | ASIC | 150 | 500 | 0.300 | 5,000 |
| 26 | Plasma XXL | GPU | 60 | 200 | 0.300 | 5,000 |
| 29 | CPU Miner v2.0 | CPU | 30 | 100 | 0.300 | 500 |
| 33 | HashTech Beast2 ASIC | ASIC | 350 | 1,000 | 0.350 | ? |
| 37 | Lightning G2 Quad-Rig | Custom Rig | 140 | 400 | 0.350 | 4,500 |

**特徴**: まだ十分に稼働しているが、効率面で上位機種に大きく劣る。電力コストの高いLv1-2施設では赤字に近い。

### グループC: High Tier B（0.400〜0.450 MH/W）— 後期世代
| # | マイナー | タイプ | MH/s | W | MH/W | 価格 |
|---|---|---|---|---|---|---|
| 32 | RedDragon TiX | GPU | 45 | 100 | 0.450 | 1,000 |
| 34 | Ennee Socket CPU | Custom Rig | 50 | 200 | 0.450 | 1,700 |
| 36 | Lightning G1 Quad-Rig | Custom Rig | 80 | 200 | 0.400 | 1,500 |
| 44 | HashTech BeastRack | Custom Rig | 800 | 2,000 | 0.400 | 15,000 |
| 49 | Jvidia JX500 | GPU | 500 | 1,200 | 0.417 | 7,000 |

**特徴**: 現時点では競争力あり。ただし上位マイナー（Tier A: 0.5+）との差は大きく、2〜3回の半減期後にはTrade-in候補に。

### グループD: Tier A（0.500〜0.999 MH/W）— 現役上位機
| # | マイナー | タイプ | MH/s | W | MH/W | 価格 |
|---|---|---|---|---|---|---|
| 30 | Lightning G3 | GPU | 50 | 100 | 0.500 | 1,500 |
| 31 | Galactic Hash C | Specialized | 300 | 600 | 0.500 | 10,000 |
| 35 | Quad Socket CPU v2.0 | Custom Rig | 120 | 200 | 0.600 | 2,500 |
| 40 | The Grotto Miner | Specialized | 150 | 200 | 0.750 | ? |
| 42 | Plasma Absolute | Unknown | 400 | 800 | 0.500 | 10,000 |
| 43 | Lightning G3 Tri-Rig | Custom Rig | 150 | 200 | 0.750 | 5,000 |
| 47 | Jvidia JX420 | GPU | 200 | 500 | 0.560 | 3,300 |
| 48 | Jvidia JX450 | GPU | 400 | 800 | 0.500 | 5,000 |

**特徴**: 現在の主力機。Trade-in対象になるのは遠い将来。Phase 3の長期ビジョンとして位置付け。

### 対象外: Tier S（1.0+ MH/W）+ 特殊アイテム
Octa-TiX, Stormcore, Moats, Campfire等のTier S機、およびJnnt/Jnead/Jiga系/Bundle of Sticks等の特殊アイテムはTrade-in対象外。

---

## Phase 2 製品プラン — 「中堅世代の再構築」

**コンセプト**: 半減期の進行で収益性が悪化したTier B（0.2〜0.45 MH/W）マイナーを回収し、Tier A相当（0.600〜0.850 MH/W）の高効率マイナーに再構築する。

**リリース想定**: 3〜4回目の半減期以降（Tier Bマイナーの退役が本格化するタイミング）

### Phase 2 マイナー

#### SH-R3 "Refit"
| 項目 | 値 |
|---|---|
| コンセプト | ASIC再構築 — HashTech系ASICの高密度チップを再配線 |
| MH/s | 250 |
| W | 400 |
| MH/W | 0.625 |
| 組立費 | 2,500 hCASH |
| 素材レシピA | 1× HashTech Beast ASIC (#17) + 2× CPU Miner v2.0 (#29) |
| 素材レシピB | 1× HashTech Mini Beast (#25) + 1× Quad Socket CPU (#6) |
| ビジュアル方向性 | ASICチップ露出型、HashTechパネルの切断痕、SH銅フレーム |

#### SH-R4 "Fuse"
| 項目 | 値 |
|---|---|
| コンセプト | GPU統合 — Plasma/Lightning系GPUコアの融合リグ |
| MH/s | 400 |
| W | 600 |
| MH/W | 0.667 |
| 組立費 | 4,000 hCASH |
| 素材レシピA | 2× Plasma XL (#15) + 1× Lightning G1 Quad-Rig (#36) |
| 素材レシピB | 1× Plasma XXL (#26) + 1× Lightning G2 Quad-Rig (#37) |
| 素材レシピC | 3× Plasma Base (#14) + 2× Windflash Red (#23) |
| ビジュアル方向性 | デュアルGPUリグ、Plasma青+Lightning黄の混在パーツ、大型冷却 |

#### SH-X2 "Apex"
| 項目 | 値 |
|---|---|
| コンセプト | 全ベンダー統合 — Tier Bの最良パーツを選別して最高出力に |
| MH/s | 700 |
| W | 850 |
| MH/W | 0.824 |
| 組立費 | 6,000 hCASH |
| 素材レシピ | 1× RedDragon TiX (#32) + 1× HashTech Beast2 ASIC (#33) + 1× Ennee Socket CPU (#34) |
| ビジュアル方向性 | X1の進化版、4ベンダーロゴ混在、ブルー+アンバーのデュアルLED |

### Phase 2 ブーストモジュール

#### SH-B4 "Surge"
| 項目 | 値 |
|---|---|
| コンセプト | 高出力ハッシュブースト — 中堅GPUダイを活用 |
| 効果 | +20% Hashrate |
| 素材 | 1× Windflash Red (#23) or 1× Ennee Socket CPU (#34) |
| 組立費 | 1,500 hCASH |
| ビジュアル方向性 | B2の大型版、グリーンLED強調、大型ヒートシンク |

#### SH-B5 "Regulate"
| 項目 | 値 |
|---|---|
| コンセプト | 高効率パワーモジュール — ASIC電源回路の流用 |
| 効果 | -25% Power Draw |
| 素材 | 1× CPU Miner v2.0 (#29) + 1× Plasma Base (#14) |
| 組立費 | 2,000 hCASH |
| ビジュアル方向性 | B1の大型版、アンバーLED、コイル/コンデンサ露出 |

### Phase 2 効率マップ

```
効率 (MH/W)
  |
0.8|                                    [X2 Apex]
  |                          [R4 Fuse]
0.6|                [R3 Refit]
  |   ─────── Phase 1 ゾーン ────────
0.5|          [X1 Overhaul]
  |
0.3|    [R2 Reforge]
  |  [R1 Reclaim]
0.2|
  | ── Tier C 素材 ──|── Tier B 素材 ──|── Tier A 現役 ──
  └──────────────────────────────────────────────────────
        Phase 1 回収        Phase 2 回収      Phase 3 回収
```

---

## Phase 3 ビジョン — 「現役上位機の次世代化」（長期構想）

**コンセプト**: 半減期が十分に進行し、現在のTier A（0.5〜0.75 MH/W）すら退役候補になった段階で、これらをTier S相当（1.0+ MH/W）に再構築する。

**リリース想定**: 6〜8回目の半減期以降

### Phase 3 コンセプト製品（詳細設計は将来）

#### SH-X3 "Zenith"
| 項目 | 値 |
|---|---|
| コンセプト | Tier A統合 — 退役した上位機を究極の1台に |
| 想定 MH/W | 1.000〜1.200 |
| 想定素材 | Tier Aマイナー 2〜3台 |
| 組立費 | 8,000〜10,000 hCASH |
| ポジション | Octa-TiX/Stormcoreに次ぐ第3のTier S機 |

#### SH-B6 "Transcend"
| 項目 | 値 |
|---|---|
| コンセプト | 究極のデュアルブースト |
| 想定効果 | +15% Hash / -20% Power |
| 想定素材 | Tier Aマイナー 1〜2台 |
| 組立費 | 3,000〜5,000 hCASH |

---

## 全Phase比較サマリー

| Phase | 素材ティア | 素材効率帯 | 製品効率帯 | 製品 | 状態 |
|---|---|---|---|---|---|
| 1 | Tier C | < 0.200 MH/W | 0.267〜0.500 | R1, R2, X1, B1-B3 | 現行（提出対象）|
| 2 | Tier B | 0.200〜0.450 | 0.625〜0.824 | R3, R4, X2, B4-B5 | ロードマップ |
| 3 | Tier A | 0.500〜0.750 | 1.000〜1.200 | X3, B6 | 長期ビジョン |

### エコシステムへの影響

- **Phase 1**: 死んだNFTの清掃 → ネットワーク衛生の改善
- **Phase 2**: 中堅退役機の吸収 → 半減期ごとの自然な需要サイクル
- **Phase 3**: 上位機のリサイクル → 長期的なエコシステム持続性の証明

この3段階ロードマップにより、Second Hashは「ゲームの半減期サイクルと連動して自然に需要が拡大するベンダー」として位置付けられる。他の5ベンダーが新品販売で成長するのに対し、Second Hashは退役マイナーの増加で成長する — 根本的に異なるビジネスモデル。

---

## 特殊アイテム系（対象外）

以下のアイテムはSecond Hashの対象外とする:
- **Tier S機** (#27 Moats, #45 Octa-TiX, #46 Campfire, #52 Stormcore): 現在も将来も最高効率であり再構築の必要なし
- **0W特殊機** (#38 Jiga Jiant, #39 Jiga Jnead): 電力消費ゼロの特殊メカニクスで独立
- **ユーティリティ系** (#9 Jnnt, #10 Jnead, #28 ne pas ouvrir, #41 Bundle of Sticks, #50 Mini Torch, #51 Book of Matches, #53 Burnt Sticks): マイニング能力を持たない特殊アイテム
