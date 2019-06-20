import time

_logg = print


def check_naive(data):
    a = b = c = 0

    for i, x in enumerate(sorted(data)):
        a, b, c = b, c, x
        r = a * b * c
        # _logg(r) # Do something with the result.
    return r


if __name__ == '__main__':
    SAMPLE_TRUE = list(range(1, 6))

    assert check_naive(SAMPLE_TRUE) == 60, "Sample test failed"
    
    st = time.perf_counter()
    r = check_naive(list(range(1, 10000000)))
    assert r == 999999400000109999994, "Long test failed."
    _logg(f"Time using check_dumb: {time.perf_counter() - st}")
