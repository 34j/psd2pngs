# psd2pngs

<span style="font-size: 300%;">[日本語の説明](#日本語の説明)</span>

psd2pngs is an application that converts psd files to png files while maintaining the layer hierarchy and performing the appropriate renaming.
An onefile executable(.exe) file [`psd2pngs.exe`](https://github.com/34j/psd2pngs/releases) is also available here.

## Option 1. Executable version

### Installation

- Download the latest release from [Releases](https://github.com/34j/psd2pngs/releases).

### Usage

- Just open `.psd` file with this app.
- Alternatively, you can use this app from the command prompt by adding the path to the folder where this app is located to the PATH:

```shell
psd2pngs from.psd
```

## Option 2. Python version

```shell
py -m venv venv
pip install git+https://github.com/34j/psd2pngs.git
venv/Scripts/Activate.ps1
psd2pngs from.psd
```

## Option 3. Compile yourself

```shell
pip install pyinstaller
pyinstaller __main__.py --onefile
```

## 日本語の説明

psd2pngsは、psdファイルをレイヤーの階層構造を維持したままpngファイルに変換し、適切なリネームを行うアプリケーションです。
1ファイルにまとまったWindows用実行ファイル[`psd2pngs.exe`](https://github.com/34j/psd2pngs/releases)も配布しています。

### インストール方法

- [Releases](https://github.com/34j/psd2pngs/releases)から最新のリリースをダウンロードします。

### 使い方

- psdファイルを右クリックし、`プログラムから開く`を使ってこのアプリで開きます。
- または、PATHにこのアプリが置かれているフォルダのパスを追加することによって、コマンドプロンプトから使う事もできます。

```shell
psd2pngs from.psd
```
