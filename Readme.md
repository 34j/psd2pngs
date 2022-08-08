# psd2pngs

<span style="font-size: 200%;">[日本語の説明](#日本語の説明)</span>

psd2pngs is an application that converts psd files to png files while maintaining the layer hierarchy and performing the appropriate renaming.
An onefile executable(.exe) file `psd2pngs.exe` is also available here.

## Executable version (recommended)

### Installation

- Download the latest release from Releases.

### Usage

- Just open `.psd` file with this app.
- Alternatively, you can use this app from the command prompt by adding the path to the folder where this app is located to the PATH:

```shell
psd2pngs from.psd
```

#### Compiling yourself

```shell
pip install click tqdm psd_tools
pyinstaller psd2pngs.py --onefile
```

### Python script

```shell
pip install click tqdm psd_tools
psd2pngs.py from.psd
```

## 日本語の説明

psd2pngsは、psdファイルをレイヤーの階層構造を維持したままpngファイルに変換し、適切なリネームを行うアプリケーションです。
1ファイルにまとまったWindows用実行ファイル`psd2pngs.exe`も配布しています。

### インストール方法

- Releasesから最新のリリースをダウンロードします。

### 使い方

- psdファイルを右クリックし、`プログラムから開く`を使ってこのアプリで開きます。
- または、PATHにこのアプリが置かれているフォルダのパスを追加することによって、コマンドプロンプトから使う事もできます。

```shell
psd2pngs from.psd
```
