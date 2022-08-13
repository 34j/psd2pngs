from setuptools import setup, find_packages
from distutils.util import convert_path

module_globals = {}
with open(convert_path('psd2pngs/version.py')) as f:
    exec(f.read(), module_globals)

setup(
    name="psd2pngs",
    version=module_globals['__version__'],
    description="Convert a PSD file to PNG files.",
    author="34j",
    url="https://github.com/34j/psd2pngs",
    packages=find_packages() + find_packages('psd2pngs'),
    install_requires=['psd_tools', 'click', 'tqdm', 'pillow'],
    license='MIT',
    entry_points={
        "console_scripts": [
            "psd2pngs = psd2pngs.__main__:psd2pngs",
        ],
    }
)
