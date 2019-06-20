"""
Finding Pythagorean Triplet in the array.

Returns True if there is a triplet (a, b, c) that satisfies a^2 + b^2 = c^2.
I feel that there should be better solutions...
"""

import random
import time

_logg = print


def check_simple(data):
    sq = sorted([x ** 2 for x in data])

    # Iterate the possible `sum` from the RIGHT.
    for ic, c in enumerate(sq[::-1]):

        # Iterate possible `a` from the RIGHT
        for ia, a in enumerate(sq[ic::-1]):

            # Possible `b` from the LEFT till meet the `a`.
            for b in sq[:-(ic + ia)]:
                if a + b == c:
                    return True
    return False


def check_stupid(data):
    sq = sorted([x ** 2 for x in data])
    for a in sq:
        for b in sq:
            if a + b in sq:
                return True
    return False


def check_dumb(data):
    sq = [x ** 2 for x in data]
    for a in sq:
        for b in sq:
            if a + b in sq:
                return True
    return False


if __name__ == '__main__':
    SAMPLE_TRUE = [3, 1, 4, 6, 5]
    testdata = [random.randint(1, 1000000) for _ in range(500)]

    assert check_dumb(SAMPLE_TRUE)
    st = time.perf_counter()
    assert check_dumb(testdata) is False, "We have a low chance of True, but skip it for benchmarking."
    _logg(f"Time using check_dumb: {time.perf_counter() - st}")

    assert check_stupid(SAMPLE_TRUE)
    st = time.perf_counter()
    assert check_stupid(testdata) is False, "We have a low chance of True, but skip it for benchmarking."
    _logg(f"Time using check_stupid: {time.perf_counter() - st}")

    assert check_simple(SAMPLE_TRUE)
    st = time.perf_counter()
    assert check_simple(testdata) is False, "We have a low chance of True, but skip it for benchmarking."
    _logg(f"Time using check_simple: {time.perf_counter() - st}")
