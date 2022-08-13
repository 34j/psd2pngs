from itertools import repeat
from typing import TypedDict
from PIL import Image
from psd_tools import PSDImage
from pathlib import Path
import click
from tqdm import tqdm
import concurrent.futures
from logging import getLogger, DEBUG
import multiprocessing
from unittest import TestCase

class PsdToolsTest(TestCase):
    def test_open_multiple(self):
        for i in range(20):
            self.open_task()
        self.assertTrue(True)
        
    def test_open_multiple_multiprocessing(self):   
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.open_task, repeat(self, 20), range(20))
        self.assertTrue(True)
        
    def open_task(self):
        psd = PSDImage.open(r'E:\1.素材\琴葉葵立ち絵v01.09\test\test.psd')
        name = psd.name