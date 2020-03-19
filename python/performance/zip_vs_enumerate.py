import random
import string
import sys
import time

from collections import defaultdict
from functools import wraps
from string import ascii_letters


DATA_SIZE = 10000
STRING_SIZE = 100
NUM_TESTS = 10000

if sys.version_info < (3, 7):
    raise SystemExit('Sorry, this code need Python 3.7+ in order to measure nanoseconds')

benchmark_result = defaultdict(float)


def benchmark(f):
    """ Benchmarking decorator """
    @wraps(f)
    def wrap(*args, **kw):
        st = time.perf_counter_ns()
        result = f(*args, **kw)
        benchmark_result[f.__name__] += time.perf_counter_ns() - st
        return result
    return wrap


def gen_random_string():
    return "".join([random.choice([*ascii_letters, ' ']) for _ in range(STRING_SIZE)])


# Build random string samples
data = list([gen_random_string() for _ in range(DATA_SIZE)])


@benchmark
def bm_zip():
    for a, b in zip(data, data[1:]):
        r = f"Value {a}, Next {b}"


@benchmark
def bm_enumerate():
    for i, a in enumerate(data):
        try:
            r = f"Value {a}, Next {data[i + 1]}"
        except:
            pass


# Running actual tesl
for _ in range(NUM_TESTS):
    bm_zip()
    bm_enumerate()

print(f"Average method execution time (ns):")
for k, v in benchmark_result.items():
    print(v, '\t', k)

"""
Average method execution time (ns):
13584603573.0 	 bm_zip
22779637204.0 	 bm_enumerate
"""
