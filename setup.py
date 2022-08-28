from pathlib import Path
from setuptools import setup, find_packages

module_globals = {}
with open(Path(__file__).parent / "psd2pngs" / "version.py") as f:
    exec(f.read(), module_globals)

setup(
    name="psd2pngs",
    version=module_globals["__version__"],
    description="Convert a PSD file to PNG files while maintaining the layer hierarchy.",
    author="34j",
    url="https://github.com/34j/psd2pngs",
    packages=find_packages("psd2pngs"),
    install_requires=["psd_tools", "click", "tqdm", "pillow", "pyhumps"],
    license="MIT",
    python_requires='>=3.9',
    long_description=(Path(__file__).parent / "Readme.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "psd2pngs = psd2pngs.__main__:psd2pngs",
        ],
    },
    keywords="psd",
    project_urls={
        'Documentation': 'https://psd2pngs.readthedocs.io/',
        'Github': 'https://github.com/34j/psd2pngs',
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Intended Audience :: End Users/Desktop",
    ],
)
