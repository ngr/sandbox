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

MIN_LENGTH = 1
MAX_LENGTH = 10000
NUM_TESTS = 1000
DATA_SIZE = 1000

if sys.version_info < (3, 7):
    raise SystemExit('Sorry, this code need Python 3.7+ in order to measure nanoseconds')


# Build random SAMPLES
chars = string.ascii_letters + "".join([str(x) for x in range(10)])
print(chars)

data = []
for _ in range(DATA_SIZE):
    v = "".join([random.choice(chars) for _ in range(MIN_LENGTH, MAX_LENGTH)])
    data.append(v)


def find_ugly(data):
    """
    Effective, though a little ugly-readable solution.
    We construct a dict of tests and POP from it elements when first passed.
    This way not only we solve the task with O(n) complexity, but also
    avoid unneccessary checks of every test on every character.
    """

    tests = {
        'numeric':  lambda x: x.isnumeric(),
        'lower':    lambda x: x.islower(),
        'upper':    lambda x: x.isupper(),
        'length':   lambda x: False,
    }

    i = 0
    for c in data:

        # Keep manual counter, not to call len() every round)
        if 'length' in tests:
            i += 1
            if i == 10:
                del(tests['length'])
                del(i)

        if tests:
            for name, test in tests.items():
                if test(c):
                    # Some test passed. We shall pop it from tests now.
                    break
            else:
                # If not of the tests returned True just continue to next char.
                continue

            del(tests[name])

        if not tests:
            return True


DIGIT_RE = re.compile('\d')
UPPER_CASE_RE = re.compile('[A-Z]')
LOWER_CASE_RE = re.compile('[a-z]')


def find_best_voted(data):
    """
    Return True if password strong and False if not

    A password is strong if it contains at least 10 symbols,
    and one digit, one upper case and one lower case letter.

    (c) PositronicLlama <https://py.checkio.org/user/PositronicLlama/>
    """
    if len(data) < 10:
        return False

    if not DIGIT_RE.search(data):
        return False

    if not UPPER_CASE_RE.search(data):
        return False

    if not LOWER_CASE_RE.search(data):
        return False

    return True

result = defaultdict(float)

for method in [v for k, v in locals().items() if k.startswith('find_')]:
    for _ in range(NUM_TESTS):
        for d in data:
            st = time.perf_counter_ns()
            _ = method(d)
            result[f"{method.__name__}_total"] += time.perf_counter_ns() - st

final = {}
for k, v in result.items():
    final[k.replace('total', 'average')] = v / NUM_TESTS

#result = {k: v / (NUM_TESTS * NUM_DATASETS) for k, v in result.items()}
print(f"Average method execution time (ns):")
for k, v in final.items():
    print(v, '\t', k)

"""
Average method execution time (ns).

With max password lenght 12: 
5560483.247 	 find_ugly_average
1497936.899 	 find_best_voted_average

With max password lenght 10000: 
6187697.346 	 find_ugly_average
1683045.159 	 find_best_voted_average
"""