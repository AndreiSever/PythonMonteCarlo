# -*- coding: utf-8 -*-
import sys
import random

def IsCircle():     
    """
    Проверяет попадание точки в радиус круга.
        
    Возврат
    -------
    bool
        Возвращает True если выполняется условие, иначе - False.
    """        
    x = random.random()
    y = random.random()           
    return ((x * x + y * y) <= 1)

if __name__ == '__main__':
    a = sys.stdin.read()
    count=0
    for i in range(int(a)):    
        if (IsCircle()):
            count+=1
    print(count)
    
