"""
Benchmark speed of searching the substring in data using different approaches.
"""

import random
import re
import string
import sys
import time
from collections import defaultdict


PATTERN = 'hello world elisha and nick 123 BAZOOKA'
DATA_SIZE = 1000000
NUM_TESTS = 1000
NUM_DATASETS = 10

if sys.version_info < (3, 7):
    raise SystemExit('Sorry, this code need Python 3.7+ in order to measure nanoseconds')

# Build random SAMPLES
htmls = ["".join([random.choice(string.ascii_letters + string.digits + ' ') for _ in range(DATA_SIZE)])
         for _ in range(NUM_DATASETS)]

pattern = re.compile(PATTERN)


def find_in(p, data):
    return True if p in data else False


def find_re(p, data):
    return re.match(p, data)


def find_re_compiled(_, data):
    return re.match(pattern, data)


result = defaultdict(float)

for method in [v for k, v in locals().items() if k.startswith('find_')]:
    for _ in range(NUM_TESTS):
        for html in htmls:
            st = time.perf_counter_ns()
            _ = method(PATTERN, html)
            result[method.__name__] += time.perf_counter_ns() - st

result = {k: v / (NUM_TESTS * NUM_DATASETS) for k, v in result.items()}
print(f"Average method execution time (ns): {result}")
