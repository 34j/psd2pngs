from setuptools import setup, find_packages
from distutils.util import convert_path

module_globals = {}
with open(convert_path("psd2pngs/version.py")) as f:
    exec(f.read(), module_globals)

setup(
    name="psd2pngs",
    version=module_globals["__version__"],
    description="Convert a PSD file to PNG files.",
    author="34j",
    url="https://github.com/34j/psd2pngs",
    packages=find_packages("psd2pngs"),
    install_requires=["psd_tools", "click", "tqdm", "pillow", "pyhumps"],
    license="MIT License",
    entry_points={
        "console_scripts": [
            "psd2pngs = psd2pngs.__main__:psd2pngs",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Intended Audience :: End Users/Desktop",
    ],
)
