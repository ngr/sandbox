"""
Benchmark speed of sorting using heapq.
"""
import random
import sys
from pprint import pprint

from sosw.app import Processor as SoswProcessor
from sosw.components.benchmark import benchmark

DATA_SIZE = 100_000_000
NUM_TESTS = 10_000_000

if sys.version_info < (3, 7):
    raise SystemExit('Sorry, this code need Python 3.7+ in order to measure nanoseconds')


class Processor(SoswProcessor):

    def __init__(self, *args, **kwargs):
        # Build random SAMPLES
        self.data_s = set(str(random.randint(1, DATA_SIZE * 1000) for _ in range(DATA_SIZE)))
        self.data_l = list(str(random.randint(1, DATA_SIZE * 1000) for _ in range(DATA_SIZE)))

        super().__init__(*args, **kwargs)


    @benchmark
    def find_in_list(self):
        return 146 in self.data_l

    @benchmark
    def find_in_set(self):
        return 146 in self.data_s


    def __call__(self, *args, **kwargs):
        for name in ['find_in_list', 'find_in_set']:
            method = getattr(self, name)
            for _ in range(NUM_TESTS):
                method()


if __name__ == '__main__':
    p = Processor()
    p()

    pprint(p.get_stats())

"""
Average method execution time (ns):
 'time_find_in_list':   6.8,
 'time_find_in_set':    1.6,
"""
