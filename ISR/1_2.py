import threading
import concurrent.futures


def fill_matrix(line, column):
    matrix = []
    for i in range(column):
        matrix.append([])
        for j in range(line):
            matrix[i].append(int(input()))
    return matrix


def print_matrix(matrix):
    for i in matrix:
        print(i)


def line_multiply_column(A, B, z, j, c1, temp):
    s = 0  #сумма для элемента C
    for i in range(0, c1):
        s = s + A[z][i] * B[i][j]
    temp.append(s)
    return temp


def matrix_multiply(A, B):
    C = []  # конечная матрица
    if len(B) != len(A[0]):
        print("Матрицы не могут быть перемножены")
        return None
    else:
        r1 = len(A)  #количество строк в первой матрице
        c1 = len(A[0])  #Количество столбцов в 1
        c2 = len(B[0])  # количество столбцов во 2ой матрице
        for z in range(0, r1):
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=c2) as executor:
                temp = []  #временная матрица
                for j in range(0, c2):
                    future = executor.submit(line_multiply_column, A, B, z, j,
                                             c1, temp)
                    temp = future.result()
                C.append(temp)
                temp = []
    return C


def main():
    #Вводим размер матриц
    line_A = int(input('Элементов в строке в матрицы A: '))
    column_A = int(input('Элементов в столбце в матрицы A: '))
    line_B = int(input('Элементов в строке в матрицы B: '))
    column_B = int(input('Элементов в столбце в матрицы B: '))

    print('Вводим элементы матрицы A')
    A = fill_matrix(line_A, column_A)
    print('A = ')
    print_matrix(A)

    print('Вводим элементы матрицы B')
    B = fill_matrix(line_B, column_B)
    print('B = ')
    print_matrix(B)

    C = matrix_multiply(A, B)
    if C:
        print('C = ')
        print_matrix(C)


if __name__ == '__main__':
    main()
