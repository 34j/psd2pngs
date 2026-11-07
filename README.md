# psd2pngs

<p align="center">
  <a href="https://github.com/34j/psd2pngs/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/34j/psd2pngs/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status">
  </a>
  <a href="https://psd2pngs.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/psd2pngs.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
</p>
<p align="center">
  <a href="https://codecov.io/gh/34j/psd2pngs">
    <img src="https://img.shields.io/codecov/c/github/34j/psd2pngs.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/j178/prek">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json" alt="prek">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/psd2pngs/">
    <img src="https://img.shields.io/pypi/v/psd2pngs.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/psd2pngs.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/psd2pngs.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://psd2pngs.readthedocs.io" target="_blank">https://psd2pngs.readthedocs.io </a>

**Source Code**: <a href="https://github.com/34j/psd2pngs" target="_blank">https://github.com/34j/psd2pngs </a>

---

Convert a PSD file to PNG files while maintaining the layer hierarchy.

## Introduction

psd2pngs converts a psd file to png files while maintaining the layer hierarchy and performing the appropriate renaming, using multiprocessing.
You do not have to read this long docs, just download [![Executable](https://img.shields.io/badge/psd2pngs.exe-Click-darkblue)](https://github.com/34j/psd2pngs/releases) and open a psd file with it!

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
pip install .
python -m psd2pngs from.psd
```

### Option 4. Executable version - Compiling yourself using pip

```shell
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install .
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
pip install .
pip install pyinstaller
pyinstaller src/psd2pngs/__main__.py --onefile -n psd2pngs
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
