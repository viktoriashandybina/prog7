def matrix_multiply():  
    #Вводим размер матриц
    strA = int(input('Элементов в строке в матрицы A: '))
    stlA = int(input('Элементов в столбце в матрицы A: ')) 
    strB = int(input('Элементов в строке в матрицы B: '))
    stlB = int(input('Элементов в столбце в матрицы B: '))
    
    print('Вводим элементы матрицы A')
    A = []
    for i in range(stlA) :
        A.append([])
        for j in range(strA) :
            A[i].append(int(input()))        
    print('A = ')
    for i in A :
        print(i)
    print('Вводим элементы матрицы B')
    B = []
    for i in range(stlB) :
        B.append([])
        for j in range(strB) :
            B[i].append(int(input()))
    print('B = ')
    for i in B :
        print(i)
#Умножение
    s=0        #сумма для элемента C
    temp=[]    #временная матрица
    C=[]       # конечная матрица
    if len(B)!=len(A[0]):
        print("Матрицы не могут быть перемножены")        
    else:
        r1=len(A) #количество строк в первой матрице
        c1=len(A[0]) #Количество столбцов в 1   
        c2=len(B[0])  # количество столбцов во 2ой матрице
        for z in range(0,r1):
            for j in range(0,c2):
                for i in range(0,c1):
                   s=s+A[z][i]*B[i][j]
                temp.append(s)
                s=0
            C.append(temp)
            temp=[]           
    print("C = ")
    for i in C :
        print(i)

matrix_multiply()
