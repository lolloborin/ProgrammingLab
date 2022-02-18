class ExamException(Exception):
    pass
class Diff():
    def __init__(self,ratio=1):
        if not ((isinstance(ratio,int)) or (isinstance(ratio,float)) or (isinstance(ratio,list))):
            raise ExamException('il valore inserito nel campo ratio deve essere un intero o un float')
        if isinstance(ratio,list):
            #if len(ratio)!= 1:
            raise ExamException('la lista deve contenere al massimo un elemento')
            #else: new_ratio = ratio[0]
            #if new_ratio <= 0:
             #   raise ExamException('non puoi dividere per 0')
            #else: self.ratio = new_ratio
        if ratio > 0:
            self.ratio = ratio
        else: raise ExamException('ratio deve essere maggiore di 0')

        
    def compute(self,value):
        if not isinstance(value,list):
            raise ExamException('value deve essere una lista')
        for i in range(0,len(value)):
            '''if isinstance(value[i],str):
                    print(value[i])
                    if not value[i].isdigit():
                        raise ExamException('la stringa "{}" non è convertibile'.format(value[i]))
                    value[i] = float(value[i])'''
            if not (isinstance(value[i],int) or isinstance(value[i],float)):
                raise ExamException('la lista contine valori non utilizzabili: inserir solo int,float o str converibile a numero intero')
        lista_1=[]
        if len(value)== 1 :
            raise ExamException('lista troppo piccola')
        else:
            for i in range(0,len(value)-1):
                result=(value[i+1]-value[i])/self.ratio
                lista_1.append(result)
        
        print(lista_1)
        return lista_1
    