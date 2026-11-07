import concurrent.futures
from itertools import repeat
from unittest import TestCase

from tqdm import tqdm


def multiprocessing_task(pbar):
    for _i in range(200000):
        pbar.update(1)  # No errors but does not work


class MultiprocessingTest(TestCase):
    def test_tqdm(self):
        pbar = tqdm(range(1000000))
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(multiprocessing_task, repeat(pbar), range(5))
