from itertools import repeat
from tqdm import tqdm
import concurrent.futures
from unittest import TestCase


def multiprocessing_task(pbar):
    for i in range(200000):
        pbar.update(1)  # No errors but does not work


class MultiprocessingTest(TestCase):
    def test_tqdm(self):
        pbar = tqdm(range(1000000))
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(multiprocessing_task, repeat(pbar), range(5))
