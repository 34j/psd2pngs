from setuptools import setup, find_packages

setup(
    name="psd2pngs",
    version="1.1.0",
    description="Convert a PSD file to PNG files.",
    author="34j",
    url="https://github.com/34j/psd2pngs",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "bin = psd2pngs.__main__:psd2pngs",
        ],
    }
)
