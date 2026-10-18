# OneClickKnife

カッターと投影先を選び、右クリックから **ナイフ投影** を実行するBlenderアドオンです。
標準のKnife Projectに必要な編集モードへの切り替えと選択操作をまとめます。

## ダウンロード

**[OneClickKnife.zipをダウンロード](https://github.com/yoogen99/OneClickKnife/raw/refs/heads/main/OneClickKnife.zip)**

上のリンクはmainブランチの配布ZIPです。バージョンごとの配布物は
[Releases](https://github.com/yoogen99/OneClickKnife/releases)に掲載します。
リリースがまだない場合は上のリンクを使用してください。
GitHubの「Code > Download ZIP」は開発用ソース一式なので、インストールには上記の配布ZIPを使用してください。

## 対応環境

- Blender向けの従来形式（レガシー）のアドオンです。
- アドオンが宣言する最低バージョンは **Blender 3.6** です。すべてのバージョンでの動作を保証するものではありません。
- 外部Pythonライブラリのインストールは不要です。
- Blender Extensionsへの登録や自動更新には対応していません。

配布ZIPの内容と、有効化・無効化・再有効化をWindows版Blender **4.3.2 / 5.2.2 LTS** で確認しています。
この確認には、実際の投影結果・貫通・取り消しの操作確認は含みません。Blender 3.6での実機確認は未実施です。

## インストール

1. `OneClickKnife.zip` をダウンロードします。**解凍は不要**です。
2. Blenderで **編集 > プリファレンス > アドオン** を開きます。
3. Blender 3.6～4.1では **インストール（Install）**、4.2以降では右上のメニューから **ディスクからインストール（Install from Disk）** を選び、ZIPを指定します。バージョンによっては **Install Legacy Add-on** と表示されます。
4. `OneClickKnife` を検索し、チェックを入れて有効化します。

表示名や配置はBlenderのバージョン・表示言語によって異なります。
[Blender公式のアドオン導入ガイド](https://docs.blender.org/manual/en/4.3/editors/preferences/addons.html)も参照してください。

## 使い方

1. 3Dビューポートを **オブジェクトモード** にします。
2. カッターになる **メッシュまたはカーブを1個** 選択します。
3. `Shift` を押しながら、投影先の **メッシュを1個** 最後に選択します。投影先がアクティブなオブジェクトになっていることを確認してください。
4. 投影したい方向にビューを合わせます。正面・上面などの平行投影ビューにすると方向を合わせやすくなります。
5. 3Dビューポート内で右クリックし、**ナイフ投影** を選びます。

完了するとオブジェクトモードに戻ります。投影先を編集モードに切り替えると、追加された切断線を確認できます。
操作を取り消すには `Ctrl+Z` を使います。

既定では手前側だけを切断します。裏側も切る場合は、実行直後に `F9` で
**最後の操作を調整** を開き、**貫通** をオンにしてください。

## 制約と困ったとき

| 状況 | 確認すること |
| --- | --- |
| 「ナイフ投影」が無効 | オブジェクトモードで、カッター1個と投影先1個の計2個だけを選択してください。最後に選択する投影先はメッシュである必要があります。 |
| 項目が見つからない | アドオンを有効にし、3Dビューポートのオブジェクトモードで右クリックしてください。 |
| 切断されない・エラーになる | カッターの輪郭が投影先の面と重なっているか確認してください。メッシュのカッターには境界辺または面を持たない辺が必要です。閉じた立体メッシュはそのままでは輪郭として使えません。 |
| 切断方向が想定と違う | オブジェクトの向きではなく、実行時の3Dビュー方向で投影されます。 |
| 裏側に切断線がない | 実行直後の `F9` パネルで「貫通」をオンにしてください。 |
| ZIPの導入でmanifestのエラーになる | 配布ZIPを選び、従来形式のアドオンをインストールする操作を使用してください。 |

このアドオンはBlender標準のKnife Projectを呼び出します。ブーリアン演算による立体の切り抜きや、複数カッターの一括処理は行いません。
詳細は[公式Knife Projectマニュアル](https://docs.blender.org/manual/en/4.3/modeling/meshes/editing/mesh/knife_project.html)を参照してください。

## 更新・アンインストール

- **更新:** 新しい配布ZIPをダウンロードし、既存のOneClickKnifeを無効化してから同じ手順でインストールし直します。Blenderを再起動し、有効化とバージョンを確認してください。
- **削除:** プリファレンスのアドオン一覧でOneClickKnifeを無効化し、詳細欄の **削除（Remove）** を選びます。

## 不具合報告

[GitHub Issues](https://github.com/yoogen99/OneClickKnife/issues)に、Blenderのバージョン、OS、再現手順、表示されたエラーを記載してください。
可能であれば、問題を再現できる最小限の `.blend` ファイルや画面の画像を添付してください。
変更内容は[更新履歴](CHANGELOG.md)に記載します。

## 開発・配布手順

Python 3.10以降で、リポジトリのルートから次を実行します。追加ライブラリは不要です。

```console
python scripts/build_release.py
```

`dist/OneClickKnife.zip` が生成されます。ZIPには `OneClickKnife/` フォルダー配下に
本体、README、ライセンス、更新履歴だけを含めます。
GitHubの直接ダウンロード用ZIPを更新するには、次を実行してください。

```console
python scripts/build_release.py --output OneClickKnife.zip
```

公開時は以下の順に作業します。

1. `__init__.py` の `bl_info["version"]` と `CHANGELOG.md` を更新します。
2. Blenderでインストール、有効化、カッターによる投影、貫通、取り消し、無効化を確認します。
3. 配布ZIPを再生成し、ソースと一緒にコミットしてGitHubへpushします。
4. バージョンと一致するタグ（例: `v1.0.1`）を作成してpushします。

GitHub Actionsが構文とZIPの同期を確認し、タグのバージョンが本体と一致すると
`OneClickKnife.zip` を添付したGitHub Releaseを作成します。
通常のpush・pull requestでは配布ZIPをActionsの成果物として保存します。
ActionsではBlender上の投影結果までは検証しないため、公開前の手動確認が必要です。

## ライセンス

**GNU General Public License v3.0 or later（GPL-3.0-or-later）**。
全文は[LICENSE](LICENSE)を参照してください。
