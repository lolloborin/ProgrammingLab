class ExamException(Exception):
    pass
class MovingAverage():
    def __init__(self,finestra):
        if not(isinstance(finestra,int)):
            raise ExamException('la finestra deve essere un valore intero')
        if finestra < 1:
            raise ExamException('la finestra deve essere almeno 2')
        self.finestra = finestra 
    def compute(self,lista):
        if not (isinstance(lista,list)):
            raise ExamException('si deve isnerire una lista')
        elif len(lista)<1: raise ExamException('la lsita deve almeno contenere 2 elementi')
        for i in range(0,len(lista)):
            if not ((isinstance(lista[i],int)) or (isinstance(lista[i],float))):
                raise ExamException('la lista deve contenere solo valori int o float')
        if self.finestra > len(lista): raise ExamException('la finestra deve essere piu piccola delle lista')
        media = []
        for i in range(0,len(lista)+1-self.finestra):
            tmp = 0
            for j in range(0,self.finestra):
                tmp += lista[i+j]
            media.append(tmp/self.finestra)
        print(media)
        return media

#lista1 = MovingAverage(2)
#lista1.compute([1,4])


    