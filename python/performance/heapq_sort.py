"""
Benchmark speed of sorting using heapq.
"""

import random
import re
import string
import sys
import time

from collections import defaultdict
from heapq import heappush, heappop

DATA_SIZE = 1000000
NUM_TESTS = 100

if sys.version_info < (3, 7):
    raise SystemExit('Sorry, this code need Python 3.7+ in order to measure nanoseconds')

# Build random SAMPLES
data = list([random.randint(1, DATA_SIZE) for _ in range(DATA_SIZE)])

# Have a presorted copy of that 
sorted_data = list(sorted(data))


def find_sorted(data):
    return sorted(data)


def find_heapq(data):
    h = []
    for value in data:
        heappush(h, value)
    return [heappop(h) for i in range(len(h))]


result = defaultdict(float)

for method in [v for k, v in locals().items() if k.startswith('find_')]:
    for _ in range(NUM_TESTS):
        for i, d in enumerate((data, sorted_data)):
            st = time.perf_counter_ns()
            _ = method(d)
            result[f"{method.__name__}{'_best_case' if i == 1 else ''}"] += time.perf_counter_ns() - st

#result = {k: v / (NUM_TESTS * NUM_DATASETS) for k, v in result.items()}
print(f"Average method execution time (ns):")
for k, v in result.items():
    print(v, '\t', k)

    
"""
Average method execution time (ns):
29678073996.0    find_sorted
8047016365.0     find_sorted_best_case
134830049807.0   find_heapq
103546062825.0   find_heapq_best_case
"""
