# Second Hash — AI画像生成プロンプトセット v3.0（V1確定版）

## 確定スタイル: SH-R1 V1に基づく

SH-R1 V1の生成結果から以下のスタイルを全製品の基準とする:

### 確定ビジュアル要素
- **視点**: アイソメトリックではなく、やや低めのパースペクティブ（斜め前方から見上げる角度）
- **背景**: ダークコンクリート/金属床面、スタジオ撮影風、微かな反射
- **筐体**: ブラッシュドスチール/シルバーメタル、目立つ溶接ビード（ボックス角に沿って走る）
- **ヒートシンク**: コッパー（銅色）ヒートシンクが上部に複数配置、サイズ・形状が異なる（大小混在）
- **ヒートパイプ**: コッパー色のパイプが筐体表面を這う
- **ファン**: 大型側面マウント、アンバー/コッパー色のLEDリング光
- **ドナー表示**: 元ベンダーのラベル/プレートが一部残留（例: "HASHTECH"）
- **LCD表示**: ハッシュレートをデジタル表示するLCDパネル
- **ケーブル**: リボンケーブル、電源コネクタが上部から露出（整理はされているがむき出し）
- **透明パネル**: サイドに透明パネル、内部の緑基板・チップが見える
- **ライティング**: ドラマチックなリムライト、コッパーの暖色反射
- **質感**: フォトリアリスティック3D、金属の傷・使用感あり

---

## 共通スタイルプリフィックス v3（V1実績に基づく）

**注意**: SH-R1 V1の画像をスタイルリファレンスとしてGPTに添付し、以下のプリフィックスと共に使用すること。

```
Photorealistic 3D render of a mining hardware device, dark concrete floor background with subtle reflections, dramatic studio lighting with warm copper/amber rim light, brushed steel and copper metallic aesthetic with visible weld seams, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square aspect ratio. The device should look like refabricated mining hardware — rebuilt from salvaged parts with visible craftsmanship.
```

---

## マイナー製品 — 3モデル

### SH-R1 "Reclaim" （エントリーレベル・CPU再構築）✅ 確定済み

**V1画像で確定**。以下は生成時に使用したプロンプトの参考記録:

```
[SH-R1 V1の画像をリファレンスとして添付]

Photorealistic 3D render of a small compact mining hardware device, dark concrete floor background with subtle reflections, dramatic studio lighting with warm copper/amber rim light, brushed steel and copper metallic aesthetic, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square.

A compact rectangular mining box made of brushed stainless steel panels joined by visible weld beads along every edge. The top surface has multiple copper heatsinks of different sizes and shapes — some with fine fins, some blocky — connected by copper heat pipes running across the surface. A large cooling fan is mounted on the left side with a glowing amber/copper LED ring. The right side has a transparent panel revealing a green PCB with rows of chips inside. A small LCD display shows hashrate numbers. A weathered label plate from a donor vendor (e.g. "HASHTECH") is still attached to the front face. Ribbon cables and a yellow power connector emerge from the top. The aesthetic says "precision-rebuilt from salvaged mining hardware" — high quality refurbishment, not junk.
```

**スペック表示**: LCD上に "40 MH" と表示

---

### SH-R2 "Reforge" （ミッドレンジ・GPU再構築）

**コンセプト**: R1と同じスタイルで、サイズが1.5倍。GPUカード×2の搭載を示唆する構造。ファン×2。

```
[SH-R1 V1の画像をリファレンスとして添付]

Generate the next product in this exact same art style and rendering quality.

Photorealistic 3D render of a medium-sized mining hardware device, dark concrete floor background with subtle reflections, dramatic studio lighting with warm copper/amber rim light, brushed steel and copper metallic aesthetic with visible weld seams, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square.

A medium rectangular mining unit, roughly 1.5x the size of the SH-R1 Reclaim. The brushed stainless steel body has prominent weld beads along all joints. TWO large cooling fans are mounted — one on the left side, one on the right — both with glowing amber/copper LED rings, but slightly different fan blade designs (one straight, one curved) indicating they were harvested from different donor hardware. The top surface has a larger array of mixed copper heatsinks connected by copper heat pipes, plus a secondary aluminum heatsink (silver) from a different donor — the color mismatch is intentional. A transparent side panel reveals TWO green PCBs stacked inside, with visible reworked solder points in amber color. A small LCD display shows "120 MH". Two different donor vendor label plates are visible — one reads "REDDRAGON" (partially scratched), another has remnants of a "LIGHTNING" sticker. Thick braided power cables emerge from the top with two power connectors. The aesthetic is the same "precision-rebuilt" style as SH-R1 but clearly a step up in size and power.
```

**ポイント**: R1と同じスタイル。2ファン（異なるブレード）。2枚の基板。2つのドナーラベル（RedDragon + Lightning）。LCD "120 MH"。

---

### SH-X1 "Overhaul" （フラッグシップ・マルチソース再構築）

**コンセプト**: R1/R2の筐体スタイルをベースに、オープンフレーム構造に拡大。3ベンダー部品統合の最大モデル。

```
[SH-R1 V1の画像をリファレンスとして添付]

Generate the flagship product in this exact same art style and rendering quality, but significantly larger and more impressive.

Photorealistic 3D render of a large open-frame mining rig, dark concrete floor background with subtle reflections, dramatic studio lighting with warm copper/amber rim light, brushed steel and copper metallic aesthetic with visible weld seams, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square.

A large open-frame mining rig built on a dark brushed steel frame with polished copper support joints and struts. Three distinct compute modules are mounted inside the frame — each clearly salvaged from a different vendor: the left module has RED-tinted cooling elements and a scratched "REDDRAGON" plate, the center module has GREEN PCB sections with a "JVIDIA" label remnant, and the right module has BLUE cooling fins suggesting Plasma Systems origin. All three modules are unified by an elaborate copper heat pipe network that weaves between them, feeding into a large shared copper-fin heatsink array on top of the frame. Three fans of different sizes are arranged across the top, all with amber/copper LED rings. A prominent LCD diagnostic panel on the front frame shows "300 MH" in amber digits. Heavy braided power cables in copper-colored sleeves connect everything to a central power distribution board at the bottom. The copper "SH" emblem is prominently welded onto the top frame rail. Multiple ribbon cables and connectors are visible. The aesthetic is "masterwork rebuild from premium salvage" — three dead vendors' best parts given new unified life. This should look as impressive and detailed as a high-end gaming PC build.
```

**ポイント**: オープンフレーム。3ベンダーカラー（赤・緑・青）の部品。コッパー統一パイプ。LCD "300 MH"。SHエンブレム。R1と同じ質感・ライティング。

---

## ブーストモジュール — 3タイプ

### SH-B1 "Patch" （電力効率ブースト: -15% Power）

**コンセプト**: R1と同じスタイルの超小型デバイス。取り付けクリップ付き。

```
[SH-R1 V1の画像をリファレンスとして添付]

Generate a very small add-on module in this exact same art style — same lighting, same materials, same rendering quality, but much smaller device.

Photorealistic 3D render of a tiny add-on hardware module, dark concrete floor background with subtle reflections, dramatic studio lighting with warm copper/amber rim light and soft green accent light, brushed steel and copper metallic aesthetic, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square.

A very small rectangular module about the size of a matchbox, made of the same brushed stainless steel as the SH-R1 with visible micro weld beads. The top surface has exposed copper voltage regulator chips and tiny copper traces. Green LED accent dots glow on two corners — the green color indicates power optimization function. Two copper spring-loaded clips on opposite edges serve as attachment mechanism to mount on a host miner. A small section of green solder-masked PCB is visible through a tiny window. Fine copper wire traces run in neat patterns. A tiny "SH" is stamped in copper on the end. The device sits on the dark concrete floor looking precise and delicate — like a watchmaker's creation from salvaged electronics.
```

**ポイント**: 超小型。グリーンLEDアクセント。コッパークリップ。R1と同じ金属質感。

---

### SH-B2 "Splice" （ハッシュレートブースト: +10% Hashrate）

```
[SH-R1 V1の画像をリファレンスとして添付]

Generate a small add-on module in this exact same art style — same lighting, same materials, same rendering quality.

Photorealistic 3D render of a small add-on hardware module, dark concrete floor background with subtle reflections, dramatic studio lighting with warm copper/amber rim light and soft teal/cyan accent light, brushed steel and copper metallic aesthetic, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square.

A small rectangular module slightly larger than a matchbox, made of brushed stainless steel with visible micro weld beads. The centerpiece is a visible compute die — a small metallic square chip — sitting under a tiny copper heatsink with micro cooling fins. Teal/cyan LED accents glow at the edges, indicating active hash computation. Fine copper wire bonding traces radiate from the die to edge connectors. A dark PCB carrier board is visible with exposed copper routing traces. The module has attachment rails on the bottom edge for mounting to a host miner. A "SH" stamp in copper near one connector. The aesthetic is "surgical GPU die transplant" — a compute die carefully extracted from a dead GPU, reballed, and mounted on this custom carrier board.
```

**ポイント**: 演算ダイが見える。ティール/シアンLED。ワイヤーボンディング。R1と同じ質感。

---

### SH-B3 "Overclock" （デュアルブースト: +8% Hash / -10% Power）

```
[SH-R1 V1の画像をリファレンスとして添付]

Generate the premium boost module in this exact same art style — same lighting, same materials, same rendering quality. This is the most refined module.

Photorealistic 3D render of a small premium add-on hardware module, dark concrete floor background with subtle reflections, dramatic studio lighting with warm golden/copper rim light, brushed steel and copper metallic aesthetic, high detail, slightly low-angle perspective view, clean composition, no text overlays, 1:1 square.

The largest of the boost modules — about the size of a deck of playing cards — and clearly the premium piece. Made of brushed stainless steel with clean weld beads. The design visually shows TWO functions: one half has GREEN-tinted circuitry and components (power optimization, matching the Patch module), the other half has TEAL-tinted circuitry (hash acceleration, matching the Splice module), separated by a central copper divider strip. A small 30mm cooling fan with a gold-copper LED ring sits on top of a polished copper heatsink spanning both sections. Gold-plated edge connectors extend from both sides. A diagnostic LED strip along the front shows alternating amber and green indicators. The "SH" logo is more prominently engraved in copper — this is the flagship module. The aesthetic is "dual-purpose fusion" — visually communicating two boost types fused into one premium package.
```

**ポイント**: モジュール中最大。2セクション（グリーン+ティール）。ファン付き。ゴールドコネクタ。

---

## ブランドロゴ/アイコン

### Second Hash ロゴマーク

```
Minimalist logo design on dark background, a geometric monogram combining the letters "S" and "H" interlinked with circuit board trace motifs, copper/amber metallic color (#D4924A) with gradient to darker copper (#B87333), clean vector style suitable for small icon use, industrial and technical aesthetic, slight worn/weathered metallic texture suggesting heritage and craftsmanship, no additional text besides the stylized "SH" letters
```

---

## 生成ワークフロー

### 推奨手順
1. **SH-R1 V1を常にリファレンス添付** — 全製品でスタイル統一の基準
2. 各プロンプトの冒頭に「Generate in this exact same art style」を明記
3. サイズの違い（R1 < R2 < X1、B1 < B2 < B3）を意識
4. 生成後、ドナーラベル表示やLCD数値が不正確な場合は「Change the LCD to show '120 MH'」等で修正指示

### 生成順序（推奨）
1. ~~SH-R1 "Reclaim"~~ ✅ 確定
2. **SH-R2 "Reforge"** ← 次
3. SH-X1 "Overhaul"
4. SH-B1 "Patch"
5. SH-B2 "Splice"
6. SH-B3 "Overclock"
7. SH ロゴマーク

### ツール設定
- **GPT-4o**: SH-R1画像を添付 + プロンプト。最推奨
- **Midjourney**: `--ar 1:1 --style raw --s 250 --q 2` + `--sref [R1画像URL]`
- 比率: 1:1（正方形）
- 背景除去: 必要に応じて生成後に処理

### 画像ファイル命名規則
```
SH-R1_Reclaim.png
SH-R2_Reforge.png
SH-X1_Overhaul.png
SH-B1_Patch.png
SH-B2_Splice.png
SH-B3_Overclock.png
SH_Logo.png
```
