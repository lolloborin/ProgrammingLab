
class ExamException(Exception):    
    pass
#===============================
# Classe CSVTimeSeriesFile
#===============================
class CSVTimeSeriesFile():
    def __init__(self,name):
        self.name = name
        self.can_read = True
        try: 
            my_file = open(self.name,'r')
            my_file.readline()
            #print('{}'.format(my_file))
        except : self.can_read = False
    def get_data(self):
        if self.can_read == False:
            raise ExamException('file non leggibile o non aperto')
        data = []
        my_file = open(self.name,'r')
        for line in my_file:
            elements = line.split(',')
            #print(elements)
            if len(elements)>=2:#se le righe di un elemento sono due o piu vedo se posso aggiungerlo
                flag=1#flag che modificherò durante i controlli
                x=elements[0]#salvo la data in x per poterci lavorare
                try: y=x.split('-')#y=[anno,mese]
                except: pass
                if len(y)== 2:#se ho anno e mese:
                    try: y[0]=int(y[0])   #controllo che siano convertibili a interi senò il flag cambia 
                    except:flag=flag*0
                    try: y[1]=int(y[1])
                    except:flag=flag*0
                    if isinstance(y[1],int):
                        if y[1]<1 or y[1]>12:
                            flag=flag*0
                    #se anno o mese non sono interi allora non aggiungo
                    # verifico che i dati siano validi
                        
                    try: elements[1]=elements[1].strip('')
                    except: pass
                    try: elements[1]=int(elements[1])
                    except: pass
                    if (not isinstance(elements[1],int)) or elements[1]<0:
                        flag=flag*0
                    if flag== 1:
                        w=[]
                        w.append(elements[0])
                        w.append(elements[1])
                        data.append(w)
        #controllo che non ci siano duplicati 
        for i in range (0,len(data)):
            #controllo che non ci siano duplicati
            x= data[i]#salvo la sottolista
            y=x[0]#estrapolo la data 
            for j in range(i+1,len(data)):
                a=data[j]#salvo la sottolista di confronto
                b=a[0]#estrapolo la data da confrontare
                if b==y:
                    raise ExamException('inserite due date uguali,ricontrollare: {}'.format(data[i]))
        #controllo che non ci siano elementi fuori posizione
        for i in range(1,len(data)):
            x=data[i]#salvo la sottolista
            y=x[0]#estrapolo la data
            y=y.split('-')#separo anno e mese
            x_1=data[i-1]#salvo la sottolista precedente per il controllo
            y_1=x_1[0]#estrapolo la data
            y_1=y_1.split('-')#separo anno e mese
            #faccio il confronto
            if y[0]<y_1[0]:
                raise ExamException('timestamp fuori posizione: {}'.format(data[i]))
            if y[0]==y_1[0]:
                if y[1]<=y_1[1]:
                    raise ExamException('timestamp fuori posizione: {}'.format(data[i]))
        #print(data)
        my_file.close
        return data

def detect_similar_monthly_variations(time_series,years):
    #controllo che time_series sia una lista e che years siano validi all'interno della lista 
   
    if not isinstance(time_series,list):
        raise ExamException('time_series non è una lista')
    if not isinstance(years,list):
        raise ExameException('years non è una lista')
    if len(years)!= 2:
        raise ExamException('years deve contenere 2 valori')
    try: 
        years[0]=int(years[0])
    except: pass
    try: 
        years[1]=int(years[1])
    except: pass
    if not isinstance(years[0],int):
        raise ExamException('primo anno inserito non valido')
    if not isinstance(years[1],int):
        raise ExamException('secondo anno inserito non valido')
    
    time_series_copia = time_series #mi faccio una copia così posso modificarla a piacimento
    lista_1 = []#lista vuota per il primo anno 
    lista_2 = []#lista vuota per il secondo anno 
    trovato_1= 1#flag trovato per controllare se gli anni nella lista corrispondono a quelli del file
    trovato_2 = 1#secondo flag per controllare se anche il secondo anno esiste
    for i in range(0,len(time_series)):
        #ciclo sulla lista grande per salvarmi i dati che mi interssano 
        x=time_series_copia[i]#la prima sotto-lista la chiamo x
        y=x[0]#la data della sotto-lista la chiamo y
        z=y.split('-')#separo anno e mese z=['anno','mese']
        z[0]=int(z[0])#coverto l'anno in un intero 
        q=[]#creo una lista vuota 
        if z[0]==years[0]:#se l'anno che cerco e quello indicato da years[0] combaciano 
            q.append(z[1])#aggiungo a q il mese 
            q.append(x[1])#aggiungo a q i dati relativi al mese
            lista_1.append(q)#aggiungo a lista_1 [mese,dato]
        elif z[0]==years[1]:#se l'anno che cerco e quello indicato da years[1] combaciano
            q.append(z[1])#aggiungo a q il mese 
            q.append(x[1])#aggiungo a q i dati relativi al mese 
            lista_2.append(q)#aggiungo a lista_2 [mese,dato]
       
        #modifico il flag se gli anni di years sono presenti nel file 
        if z[0]==years[0]:
            trovato_1=trovato_1*0
        if z[0]==years[1]:
            trovato_2=trovato_2*0
    #alzo l'eccezione in base al flag   
    if trovato_1 == 1 or years[1]-years[0]!= 1 or trovato_2 == 1:
        raise ExamException('uno o enrtambi gli anni inseriti non esistono o non sono stati inseriti due anni consecutivi')
# a questo punto avendo le liste coi relativi mesi e valori (già ripulite dall'anno che a questo punto non ci interessa dato che abbiamo già verificato la sua esistenza e correlazione coi dati)
        
    esiti=[]#lista vuota con gli esiti delle nostre differenza 
    #ricerca con Flag, pm
    differenze_1 = []
    #ricerca con flag per vedere le differenze dei valori dei mesi nel primo anno
    for i in range (2,13):
        flag=1
        flag_2=1
        mese_1=0
        for j in range(0,len(lista_1)):
            a=lista_1[j]
            b=a[0]
            b=int(b)
            if b==i:
                flag=flag*0
                mese_1= mese_1+a[1]
        if flag == 0:
            for j in range(0,len(lista_1)):
                a=lista_1[j]
                b=a[0]
                b=int(b)
                if b == i-1:
                    flag_2=flag_2*0
                    c=mese_1-a[1]
                    differenze_1.append(c)
            if flag_2== 1:
                differenze_1.append('niente')
        else: differenze_1.append('niente')
    differenze_2=[]
    #ricerca con flag per vedere le differenza dei valori dei mesi nel secondo anno 
    for i in range (2,13):
        flag=1
        flag_2=1
        mese_1=0
        for j in range(0,len(lista_2)):
            a=lista_2[j]
            b=a[0]
            b=int(b)
            if b==i:
                flag=flag*0
                mese_1= mese_1+a[1]
        if flag == 0:
            for j in range(0,len(lista_2)):
                a=lista_2[j]
                b=a[0]
                b=int(b)
                if b == i-1:
                    flag_2=flag_2*0
                    c=mese_1-a[1]
                    differenze_2.append(c)
            if flag_2== 1:
                differenze_2.append('niente')
        else: differenze_2.append('niente')
    #adesso che ho le liste delle differenza tra mesi adiacenti verifico se è ±2 e le salvo in esiti con true tutto il resto diventa false 
    for i in range (0,len(differenze_1)):
        if differenze_1[i]!= 'niente' and differenze_2[i] != 'niente':
            c=differenze_1[i]-differenze_2[i]
            if c<=2 and c>=-2 or c==0:
                esiti.append(True)
            else: esiti.append(False)
        else: esiti.append(False)
        
    #print(differenze_1)
    #print(differenze_2)
    #print(time_series_copia)
    #print(trovato_1)
    #print(lista_1)
    #print(lista_2)
    #print(esiti)
    return esiti 
#time_series_file = CSVTimeSeriesFile('data.csv')
#time_series = time_series_file.get_data()
#years=[1959,1960]
#ciao=detect_similar_monthly_variations(time_series,years)
