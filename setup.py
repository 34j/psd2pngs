from setuptools import setup, find_packages
from psd2pngs import __version__
setup(
    name="psd2pngs",
    version=__version__,
    description="Convert a PSD file to PNG files.",
    author="34j",
    url="https://github.com/34j/psd2pngs",
    packages=find_packages() + find_packages('psd2pngs'),
    install_requires=['psd_tools', 'click', 'tqdm'],
    license='MIT',
    entry_points={
        "console_scripts": [
            "psd2pngs = psd2pngs.__main__:psd2pngs",
        ],
    }
)
