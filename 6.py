from datetime import datetime
from subprocess import Popen, PIPE
import random, threading, subprocess
from multiprocessing import Process, Lock, Value, Array,Manager,Queue
from queue import Queue as QQ
class PI: 
    """
    Класс для расчета числа ПИ.
    """      
    def __init__(self):
        """
        Инициалирует переменные.

        Атрибуты
        --------
        pointNumber : int
            Общее количество точек. (Значение 10000000)
        memoryPointNumber : int
            Количество точек при которых запоминаем промежуточное значение. (Значение 1000000)
        pointArr : array
            Массив с определенным количеством точек для каждого потока.
        radius : int
            Радиус круга. (Значение 1)
        threadCount : int
            Количество потоков. (Значение 4)
        aPi : int
            Число ПИ вычисленное методом Лейбница. (Значение 0)
        """
        self.pointNumber = 10000000
        self.memoryPointNumber= 1000000
        self.pointArr=[]
        self.radius=1
        self.threadCount = 4
        self.aPi=0
        prom = self.memoryPointNumber//self.threadCount
        for i in range(self.threadCount-1):
            self.pointArr.append(prom)
        self.pointArr.append(prom+(self.memoryPointNumber-prom*self.threadCount))
    def LeibnicPI(self):
        """
        Расчитывает число Пи методом Лейбница.
        """
        i=0
        self.aPi=0
        while i<self.pointNumber: 
            self.aPi += pow(-1, i) / (2 * i + 1)
            i+=1
        self.aPi = 4 * self.aPi
        print("Пи Лейбница:",self.aPi)
        print("----------------------------------------------")

    def Thred(self):
        """
        Распараллеливает методом Thread. Находит число ПИ методом Монте-Карло.
        """
        aPiarr = []
        timearr= []
        procs = []        
        y=1
        count=0
        queue = QQ()
        startTime = datetime.now()
        while y<11:
            i=0
            while i < self.threadCount: 
                proc = threading.Thread(target=self.MonteCarloMethod, args=(self.pointArr[i], queue))
                procs.append(proc)
                proc.start()
                i+=1            
            for proc in procs:
                proc.join()
            for i in range(self.threadCount):
                count+=queue.get()
            timearr.append(datetime.now()-startTime)
            aPiarr.append(abs(self.aPi-4*(count/(y*self.memoryPointNumber))))   
            procs = []
            y+=1
        endTime = datetime.now()        
        print("Pi Thread: ", 4.0 * (count / self.pointNumber))
        print("Точность расчета:", abs(self.aPi - 4.0 * (count / self.pointNumber)))
        print("Время выполнения Thread: ", endTime - startTime)
        print("Промежуточное время:")
        for time in timearr: 
            print(str(time))                
        print("Массив отклонений:", aPiarr)
        print("----------------------------------------------")    
    def Multiproc(self): 
        """
        Распараллеливает методом Multiprocessing. Находит число ПИ методом Монте-Карло.
        """
        aPiarr = []
        timearr= []
        y=1
        count=0
        queue = Queue()        
        procs = []
        startTime = datetime.now()
        while y<11:
            i=0
            while i < self.threadCount: 
                proc = Process(target=self.MonteCarloMethod, args=(self.pointArr[i],queue))
                procs.append(proc)
                proc.start()
                i+=1  
            for proc in procs:
                proc.join()
            for i in range(self.threadCount):
                count+=queue.get()
            timearr.append(datetime.now()-startTime)
            aPiarr.append(abs(self.aPi-4*(count/(y*self.memoryPointNumber)))) 
            procs = []
            y+=1
        endTime = datetime.now()                      
        print("Pi Multiproc:",4.0 * (count / self.pointNumber))
        print("Точность расчета:", abs(self.aPi-4.0 * (count / self.pointNumber)))
        print("Время выполнения Multiproc: ", endTime - startTime)
        print("Промежуточное время:")
        for time in timearr: 
            print(str(time))                
        print("Массив отклонений:", aPiarr)
        print("----------------------------------------------")
    def MonteCarloMethod(self, points, queue):
        """
        Подсчитывает количество попавших в радиус круга точек.
        
        Параметры
        ---------
        points : int
            Количество точек.
        queue
            Очередь содержащая количество попавших точек.
        """
        count=0
        start=0
        while start < points:    
            if (self.IsCircle()):
                count+=1
            start+=1
        queue.put(count)
        
    def IsCircle(self):  
        """
        Проверяет попадание точки в радиус круга.
        
        Возврат
        -------
        bool
            Возвращает True если выполняется условие, иначе - False.
        """         
        x = random.random()
        y = random.random()           
        return ((x * x + y * y) <= self.radius * self.radius)

    def subproc(self):
        """
        Распараллеливает методом Subprocess. Находит число ПИ методом Монте-Карло.
        
        Ошибка
        ------
        Exception
            Возникает при любой ошибке.
        """
        count=0
        aPiarr = []
        timearr = []
        startTime = datetime.now()
        i=1
        try:
            while i<11:
                processes = [Popen('python sub.py',stdin=PIPE, stdout=PIPE,shell=True) for i in range(self.threadCount)]
                inc=0
                for p in processes[:]:
                    p.stdin.write(str(self.pointArr[inc]).encode('UTF-8'))
                    p.stdin.close()   
                    inc+=1
                while processes:
                    for p in processes[:]:
                        if p.poll() is not None:
                            con = p.stdout.read().decode('UTF-8')
                            count+=float(con[:-2])
                            p.stdout.close()
                            processes.remove(p)
                timearr.append(datetime.now()-startTime)
                aPiarr.append(abs(self.aPi-4*(count/(i*self.memoryPointNumber))))
                i+=1
        except Exception as e:
            print(e)
            return
        endTime = datetime.now()
        print("Pi Subprocess: ", 4.0 * (count/self.pointNumber ))
        print("Точность расчета: ", abs(self.aPi - 4.0 * (count/self.pointNumber)))
        print("Время выполнения Subprocess: ", endTime - startTime)
        print("Промежуточное время: ")
        for time1 in timearr: 
            print(str(time1))
        print("Массив отклонений:", aPiarr)
        print("----------------------------------------------")

    def Single(self):
        """
        Находит число ПИ методом Монте-Карло последовательно.
        """
        count = 0
        allcount = 0
        aPiarr = []
        timearr= []
        startTime = datetime.now()
        for i in range(self.pointNumber):
            if (self.IsCircle()):
                count+=1           
            allcount+=1
            if (allcount % self.memoryPointNumber == 0):
                aPiarr.append(abs(self.aPi - 4 * (count / allcount)))
                timearr.append(datetime.now() - startTime)
        endTime = datetime.now() 
        print("Pi Single: ", 4.0 * (count / self.pointNumber))
        print("Точность расчета: ", abs(self.aPi - 4.0 * (count / self.pointNumber)))
        print("Время выполнения Single: ", endTime - startTime)
        print("Промежуточное время: ")
        for time in timearr: 
            print(str(time))                
        print("Массив отклонений: ", aPiarr)
        print("----------------------------------------------")

if __name__ == '__main__':
    clas= PI()
    clas.LeibnicPI()
    clas.Thred()  
    #clas.Multiproc()
    #clas.subproc() 
    clas.Single()
