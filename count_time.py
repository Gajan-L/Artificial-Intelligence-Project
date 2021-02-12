import time
import functools


def timeit(method):
    @functools.wraps(method)
    def timed(*args, **kw):
        print(f"Search algorithm: {method.__name__}")
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        print(f"Time elapsed of {method.__name__}:{end_time - start_time: 0.10f} sec. ")
        return result
    return timed