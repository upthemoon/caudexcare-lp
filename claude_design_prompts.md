# Claude Design 用プロンプト集（CaudexCare LP・SVG/CSS版）

Claude Design は SVG/HTML/CSS 特化のため、すべての素材を SVG・CSS で作成します。
19世紀ボタニカル銅版画スタイル（Curtis's Botanical Magazine 系）で統一。

**配色トーン:**
- 苔色 `#3F5E3F` / 深苔 `#2A4329`
- 葉緑 `#7BA76C` / 新芽 `#B4D3A5`
- 素焼き `#C18D6E` / クリーム `#FBF8F1`
- 墨 `#2D2A24` / インクサブ `#6F695E`

**使い方:**
- 各プロンプトを **https://claude.ai/design** に貼って生成
- 出来た SVG コードをコピーして、Ryo が私（Claude Code）に貼り付け
- 私が `index.html` に組み込みます

---

## 🎨 1. Hero 植物図鑑フレーム（最優先・B案：差し込み枠付き）

**配置**: ファーストビュー右側のクリーム色エリア（既存 .hero-art-frame を置き換え）
**サイズ**: 400×500px 想定（CSS で max-width 制御）
**コード**: HTML + 内蔵 CSS + 内蔵 SVG

### 背景
Claude Design は複雑な植物イラスト本体は SVG で描けない（ガイドラインで禁止）。なので **フレームだけを作って、中央にイラストの差し込みスロットを用意する** B案で進める。後で PD銅版画 or 自分の写真 or AI生成画像を `<img>` で差し込む。

### プロンプト

```
19世紀の植物図鑑ページ風の「装飾フレーム」を HTML/CSS/SVG で作成してください。
中央にイラスト差し込み用の <img> スロットを設けます。

レイアウト構造:
- 縦長 4:5 のカード（width: 100%, aspect-ratio: 4/5）
- 古紙色背景 #FBF8F1 + 微細な紙テクスチャ（SVG filter feTurbulence で）
- 角は 8px ラウンド
- 外側に1px の薄いボーダー #E0D9CB
- 控えめなドロップシャドウ

上部装飾:
- 上部に小さなセクション (高さ 60px)
- 中央寄せで「PLATE No. 001」セリフ体・letter-spacing 0.3em・色 #6F695E・size 11px
- その下に細い装飾罫（左右に小さな葉のシンボル付き、中央に細線）

中央スロット (上下 60〜420px の領域):
- <img id="hero-plant-img" src="" alt="" /> を配置
- src は空（後で差し替え）
- src が空の場合に表示する placeholder スタイル:
  - 中央に薄い色 #B4D3A5 の手描き風植物シルエット SVG（簡易な多肉のシルエット程度でOK）
  - その下に「Botanical Plate」セリフ斜体 14px #6F695E
- src が指定された場合は画像のみ表示（object-fit: contain, padding 20px）

下部装飾:
- 上記中央スロットの下に再度装飾罫
- その下に学名表示エリア:
  - 「Dioscorea elephantipes」セリフ体イタリック 18px #2A4329
  - 改行して「亀甲竜 — カイメイリュウ」セリフ体 11px #6F695E
- 下部に小さく "From the Caudex Collection" セリフ斜体 10px #6F695E

スタイル指定:
- フォント: 'Noto Serif JP' をベース、なければ system serif
- カラー値はすべて上記指定の HEX のまま
- 内蔵 CSS は <style scoped> 形式でラップ
- 画像差し替え時に学名テキストも JS で書き換えられるよう data 属性 or id を付ける

出力形式:
- 単一 HTML スニペット
- <div class="botanical-plate"> ... </div> の形でラップ
- 内部に必要な <style> と <svg>（古紙ノイズ filter, 装飾葉, 簡易プレースホルダー植物）を全部含める
- 既存の親コンテナ（.hero-art）にそのまま差し込んで動くこと
```

差し込みパターン（あとで Ryo が選ぶ）:
- **PD 銅版画**: Wikimedia から Köhler's Medicinal Plants / Curtis's Botanical Magazine の銅版画を DL → `plate_001.jpg` として置く
- **自分の株写真**: 背景白で撮影 → 同上ファイル名で配置
- **AI 生成（将来）**: Midjourney 等で生成 → 同上

---

## 🎨 2. 装飾 SVG パーツセット（snippets）

**配置**: 既存の `<svg width="0" height="0">` ブロックを差し替え
**コード**: 1つの `<svg>` 内に複数 `<symbol>` を含める

### プロンプト

```
植物図鑑風の装飾SVGパーツ集（symbol セット）を作成してください。
すべて currentColor 塗りで、CSS から色変更できるようにします。

含める symbol（id 指定）:
1. #leaf-oval — 楕円型の葉、葉脈付き
2. #leaf-heart — ハート型の葉、亀甲竜の葉に似たもの
3. #leaf-blade — 細い剣型の葉、多肉系
4. #leaf-fern — 羽状の葉（シダのような）
5. #vine-curl — 巻き蔓、らせん状
6. #vine-bough — 横長の枝に葉が数枚ついた装飾
7. #sprout-double — 双葉（双子葉植物）
8. #sprout-bud — 蕾と新芽
9. #cactus-mini — 小さなサボテンのシルエット
10. #caudex-mini — 小さなコーデックスのシルエット
11. #divider-branch — 横長の細い枝、セクション区切り用
12. #ornament-corner — コーナー装飾、植物のからみ

スタイル:
- 全部 viewBox を統一（葉系: 0 0 64 64、蔓系: 0 0 120 40、その他適切に）
- stroke: currentColor、stroke-width: 1.5
- 一部 fill: currentColor でアクセント
- 線の手彫り感（微妙な太さ変化・微妙な歪み）
- 過度なディテールは避け、シルエットで伝わる強さを重視

出力形式:
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="leaf-oval" viewBox="0 0 64 64">...</symbol>
    ...12個全部
  </defs>
</svg>

の形で1ブロックにまとめる。
```

---

## 🎨 3. OG 画像テンプレート（HTML/CSS）

**配置**: 別ファイル `og_template.html` を作って、ブラウザで開いて 1200×630 でスクショ → `og.jpg` として保存
**サイズ**: 1200×630px の固定 div

### プロンプト

```
SNSシェア用 OG画像を 1200×630px の固定サイズで HTML/CSS 一枚絵として作成してください。
ブラウザで開いて、スクリーンショットで PNG/JPG として書き出して使います。

レイアウト:
- 横長1200x630px固定
- body のサイズも 1200x630 にして overflow:hidden
- 背景: クリーム色 #FBF8F1 + 微細な紙テクスチャ（CSS の SVG ノイズフィルタで再現）

左半分 (0〜600px):
- 上部 60px の余白
- 苔色 #3F5E3F の小さなテキスト「CAUDEX CARE」セリフ体・letter-spacing 0.3em・サイズ 20px
- 中央に大きく「水やりタイミング、もう忘れない。」
  - Noto Serif JP 700, 色 #2A4329, サイズ 64px, line-height 1.4
- 下部に控えめなテキスト
  - 「多肉植物・コーデックスの管理アプリ」 #6F695E, 28px
  - 「App Store ・ iPhone/iPad対応」#7BA76C, 18px, letter-spacing 0.2em

右半分 (600〜1200px):
- インライン SVG でパキポディウム・グラキリス（または亀甲竜）の銅版画風線画
- viewBox を縦長に
- stroke: #2A4329, fill: none, stroke-width 1.5
- 塊根のハッチング陰影あり
- 下部に小さく「Pachypodium gracilius」セリフ体イタリック・#6F695E・16px

全体に古紙のテクスチャを SVG filter（feTurbulence）で薄く重ねる。

出力: 単一 HTML ファイル（CSS は <style> 内）
```

---

## 🎨 4. 古紙テクスチャ CSS（SVG filter ベース）

**配置**: `index.html` の `body` 背景に追加

### プロンプト

```
CSS と SVG filter だけで再現する「古紙テクスチャ」を作成してください。
画像ファイル（PNG）は使わず、すべて CSS / インライン SVG で完結。

要件:
- ベース色 #FBF8F1（クリーム）
- 微細な繊維のムラ（feTurbulence ノイズ、baseFrequency 0.9 程度）
- ごく薄い茶色斑点（複数の box-shadow か radial-gradient で再現）
- ローディング軽量
- body 全体にタイル状ではなくシームレスに

出力:
1. <svg> ブロック（インライン、SVG filter 定義）
2. body { background: ..., filter: url(#paperNoise); } のCSS
3. 既存の body 背景に追加する形（既存の radial-gradient は残す）

コメント付きで貼り付け箇所を明示してください。
```

---

## 📋 反映フロー

各プロンプトの SVG/HTML が出来たら、Ryo は **コードをコピーして私（Claude Code）に貼り付けてください**。
私が `index.html` の該当箇所に組み込みます（プレースホルダー差し替え or 既存要素置換）。

**優先順位**: 1 → 2 → 3 → 4

1 だけでも LP の印象が劇的に変わります。

---

## 💡 補足

- Claude Design は SVG/HTML/CSS の生成・調整に特化（画像ファイル生成は不可）
- 「想像と違う」「線が太い」「もっと細く」など微調整も Claude Design で完結
- ボツ案を取っておきたい場合は `~/caudexcare-lp/_rejected/` に避難
