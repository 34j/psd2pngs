# psd2pngs

[![Licence](https://img.shields.io/github/license/34j/psd2pngs)](./License.txt)
[![Executable](https://img.shields.io/badge/OneFile_.exe-Click-darkblue)](https://github.com/34j/psd2pngs/releases)
[![Japanese Explanation](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%AE%E8%AA%AC%E6%98%8E-Click-blue)](#日本語の説明)

## Introduction

psd2pngs converts a psd file to png files while maintaining the layer hierarchy and performing the appropriate renaming, using multiprocessing.
An onefile executable(.exe) file [`psd2pngs.exe`](https://github.com/34j/psd2pngs/releases) is also available.

## Example

![Screenshot GIF](Example.gif)

Note that this GIF is in fast forward.

## Usage

### Using as an app

- Just open `.psd` file with this app. ([Executable version](https://github.com/34j/psd2pngs/releases) only.)
- Alternatively, this app can also be used with command prompt.

```shell
> psd2pngs -h
Usage: psd2pngs [OPTIONS] PSD_PATH

Options:
  -v, --version              Show the version and exit.
  -o, --out PATH             Output directory path. If not specified, output
                             to the same directory as the PSD file.
  -s, --single-process       Force not to use multiprocessing.
  -t, --tasks-count INTEGER  Number of tasks. Recommended to be less than or
                             equal to the number of CPUs (32) because the   
                             process maximizes the use of CPUs.
  -j, --json                 Output JSON file containing layer information in
                             snake case.
  -jc, --json-camel-case     Output JSON file containing layer information in
                             camel case.
  -h, -?, --help             Show this message and exit.
```

The type of content of Output JSON file (snake_case) is the following.

```python
class LayerInfo(NamedTuple):
    local_path: str
    name: str
    safe_name: str
    is_visible: bool
    is_group: bool
    children: "Iterable[LayerInfo]"
```

The type of content of Output JSON file (camelCase) is the following.

```python
class LayerInfo(NamedTuple):
    localPath: str
    name: str
    safeName: str
    isVisible: bool
    isGroup: bool
    children: "Iterable[LayerInfo]"
```

### Using as a module

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psd2pngs)](https://pypi.org/project/psd2pngs/)
[![PyPI](https://img.shields.io/pypi/dm/psd2pngs)](https://pypi.org/project/psd2pngs/)
[![PyPI](https://img.shields.io/pypi/status/psd2pngs)](https://pypi.org/project/psd2pngs/)
[![Read the Docs](https://img.shields.io/readthedocs/psd2pngs?label=Docs%20%28Click%29)](https://psd2pngs.readthedocs.io/)
[![Contributors](https://img.shields.io/github/contributors/34j/psd2pngs)](https://github.com/34j/psd2pngs/graphs/contributors)

See the [documentation (readthedocs.io)](https://psd2pngs.readthedocs.io/).

## Installation

### Option 1. Executable version

Download the latest release from [Releases](https://github.com/34j/psd2pngs/releases).

### Option 2. Python version using pip install

```shell
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install psd2pngs
psd2pngs from.psd
```

### Option 3. Python version using git clone

```shell
git clone https://github.com/34j/psd2pngs.git
cd ./psd2pngs
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install -r requirements.txt
python -m psd2pngs from.psd
```

### Option 4. Executable version - Compiling yourself using pip

```shell
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install psd2pngs
pip install pyinstaller
pyinstaller venv/Lib/site-packages/psd2pngs/__main__.py --onefile -n psd2pngs
move "./dist/psd2pngs.exe" "./"
./psd2pngs from.psd
```

### Option 5. Executable version - Compiling yourself using git

```shell
git clone https://github.com/34j/psd2pngs.git
cd ./psd2pngs
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install -r requirements.txt
pip install pyinstaller
pyinstaller psd2pngs/__main__.py --onefile -n psd2pngs
move "./dist/psd2pngs.exe" "./"
./psd2pngs from.psd
```

## 日本語の説明

psd2pngsは、psdファイルをレイヤーの階層構造を維持したままpngファイルに変換し、適切なリネームを行うアプリケーションです。
1ファイルにまとまったWindows用実行ファイル[`psd2pngs.exe`](https://github.com/34j/psd2pngs/releases)も配布しています。

### インストール方法

- [Releases](https://github.com/34j/psd2pngs/releases)から最新のリリースをダウンロードします。

### 使い方

- psdファイルを右クリックし、`プログラムから開く`を使ってこのアプリで開きます。
