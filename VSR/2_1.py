import concurrent.futures
import timeit

matrix_multiply = lambda x, y: [[sum(a * b for a, b in zip(i, j)) for j in zip(*y)] for i in x]
A = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
B = [(9, 8, 7), (6, 5, 4), (3, 2, 1)]

def run_in_threads(n_th=2):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_th) as executor:
        future = executor.submit(matrix_multiply, A, B)
        return future.result()

print(run_in_threads())
tt = timeit.timeit(run_in_threads, number=1000)
print(tt)
