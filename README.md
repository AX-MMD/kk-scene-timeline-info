[DeepL翻訳 日本語](https://github.com/AX-MMD/kk-scene-timeline-info#コイカツシーンtimeline情報)

# KK Scene Timeline Info

**KKSceneTimelineInfo** is a console executable designed to add timeline information to a scene's file name. It provides configurable options to customize how file names are updated, including adding author names, replacing tags, and handling subfolders.

## Features
- Add timeline information to file names.
- Add `SFX` tag to the file name of scenes that include sounds (experimental).
- Add custom tags to the file name.
- Optional: Prepend the file name with an `[author name]`.
- Optional: Handle subfolders as scene collections with aggregated information.

## Limitations
- I haven't found a way to detect when preset Studio animations are used, so if a scene does not animate in Timeline and only uses presets, it will be treated as static.

## Installation
- Download `KKSceneTimelineInfo.zip` from the [release page](https://github.com/AX-MMD/kk-scene-timeline-info/releases/)
- Extract wherever you want, but keep all the files together.

## Usage
- Drag and drop a scene file or folder on `KKSceneTimelineInfo.bat`
A scene will be designated as:
* `(static)` if the Timeline is not used at all (see limitation with preset animations).
* `(dynamic;MmSS)` if the Timeline is used, but not to move characters (ex. camera, SFX, VFX) .
* `(MMmSS)` if the Timeline is used to animate characters.

## Configuration
The script behaviour can be customized using the `config.toml` file. Below are the available options:

- **`display_only`**:  
  If `true`, the script will only display the changes without applying them.  
  Default: `false`

- **`author`**:  
  Specify an author name to add to file names.  
  If left empty, it will not add an author name.  
  If removed completely or commented out, it will use the parent folder's name.  
  Default: `""`

- **`replace_author`**:  
  If `false`, the script will not update the author in file names.  
  Default: `true`

- **`replace_tags`**:  
  If `true`, all tags (except `SFX`) will be replaced (instead of updated) with the content of `add_tags`.  
  To force remove the `SFX` tag, add `NoSFX` to `add_tags`.  
  Default: `false`

- **`add_tags`**:  
  A list of tags to add or replace. Example: `add_tags=["animation", "creampie"]`.  
  Default: `[]`

- **`no_subfolder`**:  
  If `false`, subfolders will be treated as scene collections, and each subfolder will be assigned the author name and the total duration.

  .
  
  .
  
  .

  .
# コイカツシーン[Timeline]情報 

**KKSceneTimelineInfo** は、シーンのファイル名にタイムライン情報を追加するために設計されたコンソール実行ファイルです。作者名の追加、タグの置き換え、サブフォルダの扱いなど、ファイル名の更新方法をカスタマイズするための設定可能なオプションを提供します。

## 機能
- ファイル名にタイムライン情報を追加
- サウンドを含むシーンのファイル名に`SFX`タグを追加（実験的）。
- ファイル名にカスタムタグを追加。
- オプション： ファイル名の前に`[作者名]`を付ける。
- オプション：情報を集約したシーンコレクションとしてサブフォルダーを扱う。

## 制限事項
- プリセットスタジオのアニメーションが使用されていることを検出する方法が見つかりませんでした。そのため、シーンがタイムラインでアニメーションせず、プリセットだけが使用されている場合、静的なものとして扱われます。

## インストール
- リリースページから `KKSceneTimelineInfo.zip` をダウンロードしてください。
-> https://github.com/AX-MMD/kk-scene-timeline-info/releases
- 好きな場所に解凍してください。

## 使用方法
- シーンファイルまたはフォルダを `KKSceneTimelineInfo.bat` にドラッグ＆ドロップする
シーンとして指定されます：
* (static)タイムラインが全く使用されていない場合（プリセットアニメーションによる制限を参照）。
* (dynamic;MmSS)タイムラインが使用されるが、キャラクターを動かさない場合（例：カメラ、SFX、VFX）。
* (MMmSS) タイムラインがキャラクターのアニメーションに使用される場合。

## 設定
スクリプトの動作は `config.toml` ファイルを使ってカスタマイズすることができます。以下に利用可能なオプションを示します：

- **`display_only`**：  
  `true`の場合、スクリプトは変更を適用せずに表示のみを行う。 
  デフォルト: `false`

- **`author`**：  
  ファイル名に追加する作者名を指定する。 
  空の場合、作者名は追加されません。 
  完全に削除するかコメントアウトすると、親フォルダの名前を使用します。 
  デフォルト: `""`。

- **`replace_author`**：  
  false`の場合、スクリプトはファイル名の作者を更新しません。 
  デフォルト: `true`

- **`replace_tags`**：  
  もし `true` なら、全てのタグ(`SFX` を除く)を `add_tags` の内容に置き換える(更新するのではなく)。 
  SFX` タグを強制的に削除するには、 `add_tags` に `NoSFX` を追加する。 
  デフォルト: `false`

- **`add_tags`**：  
  追加または置換するタグのリスト。例: `add_tags=["animation", "creampie"]`.  
  デフォルト: `[]`.

- **`no_subfolder`**：  
  false`の場合、サブフォルダはシーンコレクションとして扱われ、各サブフォルダには作者名と合計時間が割り当てられます。 
  個々のシーンはそれぞれの情報を持ちます。 
  デフォルト: `true`

  Individual scenes will still have their own information.  
  Default: `true`
