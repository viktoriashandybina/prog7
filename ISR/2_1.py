import random
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from time import perf_counter


def write_to_file(f, a, b, n_job=None, n_iter=100):

    for i in range(n_iter):
        myFile = open(f, 'a')
        with myFile:
            writer = csv.writer(myFile, delimiter=';')
            n = random.randint(a, b)
            writer.writerows([['# of process: {}'.format(str(n_job)), str(n)]])

    return n


def writing_more(f, a, b, *, n_jobs=2, n_iter=200):

    myFile = open(f, 'w')
    with myFile:
        writer = csv.writer(myFile, delimiter=';')
        writer.writerows([['№ of process', 'RANDOM VALUE']])

    executor = ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, write_to_file, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs

    fs = [
        spawn(a + i * step, a + (i + 1) * step, n_job=i) for i in range(n_jobs)
    ]
    return sum(f.result() for f in as_completed(fs))


if __name__ == '__main__':

    start = perf_counter()
    writing_more('output.csv', 0, 200)
    end = perf_counter()
    print('Время выполнения: {}'.format(end - start))
