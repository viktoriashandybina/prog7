def  squareSequenceDigit(n):
  i = 1
  sq = 1
  while n > 0:
    sq = i * i
    i += 1
    t = sq # переменная для подсчета разрядности квадрата
    a = 0
    if  (sq / 10) > 1: # будет ли разрядность квадрата больше 1
      while t >= 1:
        t /= 10
        a += 1 # разрядность 
    else:
      a = 1
    n -= a 
  return (pos(sq, n))

def pos(sq, n): # проверка нужной позиции в числе
  if (n == 0):
    return sq % 10
  n = 10 ** (n * -1)
  
  return int(sq / n) % 10

print("n-я цифра последовательности из квадратов целых чисел = ", squareSequenceDigit(5))


    
if __name__ == "__main__":
    squareSequenceDigit(1)
    squareSequenceDigit(2)
    squareSequenceDigit(7)
    squareSequenceDigit(12)
    squareSequenceDigit(17)
    squareSequenceDigit(27)
