import time
from time import sleep


def implementation_time(func):
    start_time: time.time = time.time()

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        end_time: time.time = time.time()
        print(f"Время исполнения {func.__name__} - > {end_time - start_time:.4f}")

    return inner


if __name__ == "__main__":
    @implementation_time
    def sleep_sec(secs: int):
        sleep(secs + 1)


    sleep_sec(2)
