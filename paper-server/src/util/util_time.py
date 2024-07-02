from time import time
from contextlib import contextmanager


@contextmanager
def timer():
    start_time = time()
    yield
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        return result

    return wrapper
