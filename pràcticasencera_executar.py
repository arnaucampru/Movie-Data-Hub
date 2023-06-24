from statistics import mode
import numpy as np
from numpy import array

#------------------------------------------------------------------------------

def load_data_usrs(path):
    #UserID :: Gènere :: Edat :: Ocupació :: Codi postal
    fitxer=open("ml-1m\\users.dat","r")
    diccionari={}
    
    for contingut in fitxer.readlines():
        fitxer_separat=contingut.split("::")
        #tenim una llista del fitxer línea a línea separat (,) per:
        #UserID , Gènere , Edat , Ocupació , Codi postal
        for i in range(5):
            if i==0:   
                x=str(fitxer_separat[i])
            if i==1:   
                a=str(fitxer_separat[i])
            if i==2:
                b=int(fitxer_separat[i])
            if i==3:    
                c=str(fitxer_separat[i])
            if i==4:
                d=str(fitxer_separat[i])[0:-1]   #pq no apareixi \n
                t=(a,b,c,d)    #crear tupla amb els valors del diccionari
                #tenim una tupla amb
                #Gènere , Edat , Ocupació , Codi postal
                diccionari[x]=t    #posar-li clau a la tupla del diccionari
                
    fitxer.close()
    return(diccionari)
    
#------------------------------------------------------------------------------


z=load_data_usrs("ml-1m\\users.dat")
print(z['16']) 


#------------------------------------------------------------------------------

def load_data_movies(path):
    fitxer=open("ml-1m\\movies.dat","r")
    diccionari={}
    
    for contingut in fitxer.readlines():
        fitxer_separat=contingut.split("::")

        for i in range(3):
            if i==0:    #títol pel.lícula
                x=str(fitxer_separat[i])
            if i==1:    #any
                a=str(fitxer_separat[i])[0:-6]
                b=str(fitxer_separat[i])[-5:-1]
            if i==2:    #gènere
                c=str(fitxer_separat[i])[0:-1]    #pq no apareixi \n   
                c=c.split("|")     #la funció split crea una llista [llista]
                diccionari[x]=a,b,c     #x=MovieID
                
    fitxer.close()
    return(diccionari)

#------------------------------------------------------------------------------


z=load_data_movies("ml-1m\\movies.dat")
print(z['2405'])


#------------------------------------------------------------------------------

def load_data_ratings(path,nu,nm):
    #UserID :: MovieID :: Rating :: Timestamp
    #nu=nombre d'usuaris que ha de tenir la matriu
    #nu_max=6040
    #nm=nombre de pel.lícules que ha de tenir la matriu
    #nm_max=3952
    fitxer=open("ml-1m\\ratings.dat","r")
    matriu=np.zeros((nu,nm),dtype=np.uint64)    #inicialitzar una matriu amb tot zeros
    
    for contingut in fitxer.readlines():
        fitxer_separat=contingut.split("::")
        
        for i in range(3):
            if i==0:
                a=int(fitxer_separat[i])    #UserID
            if i==1:
                b=int(fitxer_separat[i])    #MovieID
            if i==2:
                c=int(fitxer_separat[i])    #Rating
                matriu[a,b]=c
    fitxer.close()
    #return=matriu numpy amb: UserID , MovieID , Rating
    return(matriu)

#------------------------------------------------------------------------------


z=load_data_ratings("ml-1m\\ratings.dat",6041,3953)
print(z[1714,2405])    #ha de donar 3


#------------------------------------------------------------------------------

#assignació dels 3 diccionaris a variables per a facilitar la feina
d1=load_data_usrs("ml-1m\\users.dat")
d2=load_data_movies("ml-1m\\movies.dat")
d3=load_data_ratings("ml-1m\\ratings.dat",6041,3953)

#==============================================================================

#Exercici1---------------------------------------------------------------------

def exercici1(d2):
    any_alien=[d2[x][1] for x in d2 if d2[x][0]=="Alien "]
    print(any_alien[0])
    
exercici1(d2)

#Exercici2---------------------------------------------------------------------

def exercici2(d2):
    llista1=[x for x in d2 if "Film-Noir" in d2[x][2]]
    #llista amb els MovieID's de les pel.lícules de cine negre
    temp=0
    decada_final=0
    for decada in range(1900,2000,10):
        cont=0
        for anys in llista1:
            if decada<=int(d2[anys][1])<=int(decada+9):
                cont+=1
        if cont>temp:
            temp=cont
            decada_final=decada
    return(print(decada_final))

exercici2(d2)

#Exercici3---------------------------------------------------------------------

def exercici3(d1):
    llista1=[d1[x][1] for x in d1 if d1[x][0]=="F" and d1[x][2]=="20"]
    #llista amb els rangs d'edat de les dones escriptores
    rangedat=mode(llista1)
    #la funció mode ens compta l'element més repetit d'una llista
    cont=llista1.count(rangedat)
    print("El rang d'edat més repetit és el rang de",str(rangedat)+". N'hi ha",str(cont)+".")

exercici3(d1)

#Exercici4---------------------------------------------------------------------

def exercici4(d2):
    cont=0
    llista=[]
    for i in d2:
        if "Horror" in d2[i][2]:
            cont+=1
            llista.append(d2[i][0])
    return(print("N'hi ha",str(cont)+".\nSón:",llista))

exercici4(d2)

#Exercici5---------------------------------------------------------------------

def exercici5(d2):
    llista1=[]
    llista2=[]
    for i in d2:
        if "Musical" in d2[i][2] and d2[i][1]<str(1950):
            llista1.append(d2[i][0])    #musicals més antics que 1950
    for i in llista1:
        paraules=len(i.split(" "))
        paraules-=1    #pq al final de cada títol hi ha un espai que no hem de comptar
        if paraules<=3:
            llista2.append(i)
            llista2.sort()    #ordenar la llista alfabèticament
    return(print(llista2))
    
exercici5(d2)

#Exercici6---------------------------------------------------------------------

def exercici6(d1,d3):
    UserID=0
    puntuacions=0
    files=d3.shape[0]
    columnes=d3.shape[1]
    for i in range(1,files):    #mirar files (UserID's) d'una en una
        cont=0
        for j in range(1,columnes):    #mirar columnes (MovieID's) d'una en una
            if d3[i][j]!=0:    #si un usuari ha puntuat una pel.lícula
                cont+=1
        if cont>puntuacions:
            puntuacions=cont
            UserID=i    #emmagatzema l'ID de l'usuari
    return(print("L'usuari que ha puntuat més pel.lícules és el número:",str(UserID)+".\nGènere, edat, professió, codi postal (respectivament):",str(d1[str(UserID)])+"."))

exercici6(d1,d3)

#Exercici7---------------------------------------------------------------------

def exercici7(d2,d3):
    suma_d=0
    suma_h=0
    cont_d=0
    cont_h=0
    for MovieID in d2:
        if d2[MovieID][0]=="Reservoir Dogs ":    #si la posició 0 (títol) és Reservoir Dogs
            clau=MovieID
    for UserID in d1:
        if d3[int(UserID)][int(clau)]!=0:    #si la puntuació no és 0
            if d1[UserID][0]=="F":
                cont_d+=1
                suma_d+=d3[int(UserID)][int(clau)]
            else:
                cont_h+=1
                suma_h+=d3[int(UserID)][int(clau)]
    return(print("La mitjana de la pel.lícula Reservoir Dogs és:\nHomes:",str(suma_h/cont_h)+"; Dones:",suma_d/cont_d))

exercici7(d2,d3)

#Exercici8---------------------------------------------------------------------

def exercici8(d1,d2,d3):
    auxiliar=0
    diccionari_ratings={"F":[],"M":[]}
    MovieID_disparitat=""
    for MovieID in d2:    #recórrer MovieID's
        suma_F=0
        suma_M=0
        cont_F=0
        cont_M=0
        for UserID in d1:    #recórrer UserID's
            if d3[int(UserID)][int(MovieID)]>0:   #si la puntuació és més gran de 0
                if d1[UserID][0]=="F":    #si l'usuari és una dona
                    cont_F+=1    #(per a fer la mitjana)
                    suma_F+=d3[int(UserID)][int(MovieID)]    #emmagatzemar la puntuació
                elif d1[UserID][0]=="M":    #si l'usuari és un home
                    cont_M+=1    #(per a fer la mitjana)
                    suma_M+=d3[int(UserID)][int(MovieID)]    #emmagatzemar la puntuació
        if cont_F>3 and cont_M>3:   #condició de que tinguin més de 3 puntuacions
            if abs(suma_F/cont_F-suma_M/cont_M)>auxiliar:    #per a fer la disparitat
                auxiliar=abs(suma_F/cont_F-suma_M/cont_M)
                MovieID_disparitat=MovieID    #guardar la pel.lícula amb més disparitat
    for UserID in d1:
        if d3[int(UserID)][int(MovieID_disparitat)]!=0:   #si la puntuació no és 0
            if d1[UserID][0]=="F":
                diccionari_ratings["F"].append((d3[int(UserID)][int(MovieID_disparitat)]))
            elif d1[UserID][0]=="M":
                diccionari_ratings["M"].append((d3[int(UserID)][int(MovieID_disparitat)]))
    frase="La pel.lícula amb més disparitat de puntuacions és",d2[MovieID_disparitat]
    frase+="Llistat de puntuacions de cada gènere:",diccionari_ratings
    return(print(frase))
    
exercici8(d1,d2,d3)

#Exercici9---------------------------------------------------------------------

def exercici9(d1,d2,d3):
    llista1=[int(UserID) for UserID in d1 if d1[UserID][2]=="15"]
    #llista amb els UsersID's dels científics
    llista2=[int(MovieID) for MovieID in d2 if "Sci-Fi" in d2[MovieID][2]]
    #llista amb les MoviesID's de Sci-Fi
    aux=d3[llista1,:]
    matriu=aux[:,llista2]
    #matriu amb files=UserID's i columnes=MovieID's
    peli=""
    mitjana=0
    auxiliar=0
    for MovieID in range(len(llista2)):
        cont3=0
        suma=0
        for UserID in range(len(llista1)):
            if matriu[UserID][MovieID]>0:
                cont3+=1
                suma+=matriu[UserID][MovieID]
        if cont3>=3:
            mitjana=suma/cont3
            if mitjana>auxiliar:
                peli=MovieID
                auxiliar=mitjana
    return(print(d2[str(llista2[peli])]))
    #llista2[peli]=MovieID de la pel.lícula que busquem
    #d2[str(llista2[peli])])=pel.lícula que busquem

exercici9(d1,d2,d3)

#Exercici10--------------------------------------------------------------------

def exercici10(d1,d2,d3):
    llista=[int(x) for x in d1 if d1[x][1]>=45]
    #llista amb els UserID's dels majors de 45 anys)
    matriu=d3[llista,:]
    tmp=10
    pelicula=""
    for MovieID in range(len(d2)):
        cont=0
        puntuacions=0
        for UserID in range(len(llista)):
            if matriu[UserID][MovieID]!=0:
                cont+=1
                puntuacions+=matriu[UserID][MovieID]
        if cont>0 and (puntuacions/cont)<tmp:
            tmp=puntuacions/cont
            pelicula=MovieID
            #MovieID de la pel.lícula pitjor puntuada pels usuaris majors de 45 anys
    #d2[pelicula]=MovieID de la pel.lícula que busquem
    return(print(d2[str(pelicula)]))

exercici10(d1,d2,d3)

#Exercici11--------------------------------------------------------------------
#OPCIÓ 1: Considerem les pel.lícules per separat

def exercici11(d1,d2,d3):
    primera=[int(x) for x in d2 if "Maximum Overdrive " in d2[x][0]]    #MovieID1
    segona=[int(x) for x in d2 if d2[x][0]=="Blade "]    #MovieID2
    tercera=[int(x) for x in d2 if "Willow " in d2[x][0]]    #MovieID3
    quarta=[int(x) for x in d2 if "Halloween II " in d2[x][0]]    #MovieID4
    llista1=[primera[0],segona[0],tercera[0],quarta[0]]   
    #MovieID's de les pel.lícules corresponents
    #els [0] són pq no apareixin llistes dins la llista principal
    usuaris=[]
    for MovieID in llista1:
        for UserID in range(len(d1)):
            if d3[UserID][MovieID]>=3:
                usuaris.append(UserID)
    usuaris_final=sorted(list(set(usuaris)))
    #crear una llista dels UserID's no repetits ordenats numèricament
    return(print(usuaris_final))
    
exercici11(d1,d2,d3)

#OPCIÓ 2: Considerem les pel.lícules en conjunt

def exercici11(d1,d2,d3):
    primera=[int(x) for x in d2 if "Maximum Overdrive " in d2[x][0]]    #MovieID1
    segona=[int(x) for x in d2 if d2[x][0]=="Blade "]    #MovieID2
    tercera=[int(x) for x in d2 if "Willow " in d2[x][0]]    #MovieID3
    quarta=[int(x) for x in d2 if "Halloween II " in d2[x][0]]    #MovieID4
    llista1=[primera[0],segona[0],tercera[0],quarta[0]]   
    #MovieID's de les pel.lícules corresponents
    #els [0] són pq no apareixin llistes dins la llista principal
    usuaris=[]
    for MovieID in llista1:
        for UserID in range(len(d1)):
            if d3[UserID][MovieID]>=3:
                usuaris.append(UserID)
    usuaris.sort()
    #usuaris=llista amb totes els UserID's que han puntuat les pel.lícules anteriors amb més d'un 3
    usuaris_final=[]
    for usuari in usuaris:
        cont=usuaris.count(usuari)
        if cont==4:
            usuaris_final.append(usuari)
    #usuaris_final=llista amb els usuaris (repetits 4 vegades) que han puntuat les 4 pel.lícules amb més d'un 3
    return(print(sorted(list(set(usuaris_final)))))
    #retornar una llista dels UserID's no repetits ordenats numèricament
    
exercici11(d1,d2,d3)

#Exercici12--------------------------------------------------------------------

def millors(llista,d1,d3):
    peli1=""
    peli2=""
    peli3=""
    for peli in llista:
        suma=0
        cont=0
        aux1=0
        for usuari in d1:
            if d3[int(usuari)][int(peli)]!=0:
                suma+=d3[int(usuari)][int(peli)]
                cont+=1
        if cont!=0 and (suma/cont)>aux1:
            aux1=suma/cont
            peli1=d2[str(peli)][0]
            peliID1=peli
    
    for peli in llista:
        suma=0
        cont=0
        aux1=0
        for usuari in d1:
            if d3[int(usuari)][int(peli)]!=0:
                suma+=d3[int(usuari)][int(peli)]
                cont+=1
        if cont!=0 and (suma/cont)>aux1 and peli!=peliID1:
            aux1=suma/cont
            peli2=d2[str(peli)][0]
            peliID2=peli
            
    for peli in llista:
        suma=0
        cont=0
        aux1=0
        for usuari in d1:
            if d3[int(usuari)][int(peli)]!=0:
                suma+=d3[int(usuari)][int(peli)]
                cont+=1
        if cont!=0 and (suma/cont)>aux1 and peli!=peliID1 and peli!=peliID2:
            aux1=suma/cont
            peli3=d2[str(peli)][0]

    return(str(peli1),str(peli2),str(peli3))

#------------------------------------------------------------------------------

def exercici12(d1,d2,d3):
    action=[int(x) for x in d2 if "Action" in d2[x][2]]
    paction=millors(action,d1,d3)
    frase="Action:",paction
    adventure=[int(x) for x in d2 if "Adventure" in d2[x][2]]
    padventure=millors(adventure,d1,d3)
    frase+="Adventure:",padventure
    animation=[int(x) for x in d2 if "Animation" in d2[x][2]]
    panimation=millors(animation,d1,d3)
    frase+="Animation:",panimation
    childrens=[int(x) for x in d2 if "Children's" in d2[x][2]]
    pchildrens=millors(childrens,d1,d3)
    frase+="Children's:",pchildrens
    comedy=[int(x) for x in d2 if "Comedy" in d2[x][2]]
    pcomedy=millors(comedy,d1,d3)
    frase+="Comedy:",pcomedy
    crime=[int(x) for x in d2 if "Crime" in d2[x][2]]
    pcrime=millors(crime,d1,d3)
    frase+="Crime:",pcrime
    documentary=[int(x) for x in d2 if "Documentary" in d2[x][2]]
    pdocumentary=millors(documentary,d1,d3)
    frase+="Documentary:",pdocumentary
    drama=[int(x) for x in d2 if "Drama" in d2[x][2]]
    pdrama=millors(drama,d1,d3)
    frase+="Drama:",pdrama
    fantasy=[int(x) for x in d2 if "Fantasy" in d2[x][2]]
    pfantasy=millors(fantasy,d1,d3)
    frase+="Fantasy:",pfantasy
    filmnoir=[int(x) for x in d2 if "Film-Noir" in d2[x][2]]
    pfilmnoir=millors(filmnoir,d1,d3)
    frase+="Film-noir:",pfilmnoir
    horror=[int(x) for x in d2 if "Horror" in d2[x][2]]
    phorror=millors(horror,d1,d3)
    frase+="Horror:",phorror
    musical=[int(x) for x in d2 if "Musical" in d2[x][2]]
    pmusical=millors(musical,d1,d3)
    frase+="Musical:",pmusical
    mystery=[int(x) for x in d2 if "Mystery" in d2[x][2]]
    pmystery=millors(mystery,d1,d3)
    frase+="Mystery:",pmystery
    romance=[int(x) for x in d2 if "Romance" in d2[x][2]]
    promance=millors(romance,d1,d3)
    frase+="Romance:",promance
    scifi=[int(x) for x in d2 if "Sci-Fi" in d2[x][2]]
    pscifi=millors(scifi,d1,d3)
    frase+="Sci-fi:",pscifi
    thriller=[int(x) for x in d2 if "Thriller" in d2[x][2]]
    pthriller=millors(thriller,d1,d3)
    frase+="Thriller:",pthriller
    war=[int(x) for x in d2 if "War" in d2[x][2]]
    pwar=millors(war,d1,d3)
    frase+="War:",pwar
    western=[int(x) for x in d2 if "Western" in d2[x][2]]
    pwestern=millors(western,d1,d3)
    frase+="Western:",pwestern
    return(print(frase))
    
exercici12(d1,d2,d3)

#Exercici13--------------------------------------------------------------------

def exercici13(d1,d2,d3):
    millor=0
    pitjor=5
    UserIDmillor=0
    UserIDpitjor=10
    for UserID in range(len(d1)):
        cont=0
        suma=0
        for MovieID in range(len(d2)):
            if d3[UserID][MovieID]!=0:
                suma+=d3[UserID][MovieID]
                cont+=1
        if cont!=0 and (suma/cont)>millor:
            millor=suma/cont
            UserIDmillor=UserID
            
    for UserID in range(len(d1)):
        cont=0
        suma=0
        for MovieID in range(len(d2)):
            if d3[UserID][MovieID]!=0:
                suma+=d3[UserID][MovieID]
                cont+=1
        if cont!=0 and (suma/cont)<pitjor:
            pitjor=suma/cont
            UserIDpitjor=UserID
    return(print(UserIDmillor,"i",UserIDpitjor))
            
exercici13(d1,d2,d3)

#Exercici14--------------------------------------------------------------------

def exercici14(d1,d2,d3):
    aux=0
    peliID=0
    for MovieID in range(len(d2)):
        llista=[]
        for UserID in range(len(d1)):   
            if d3[UserID][MovieID]!=0:
                llista.append(d3[UserID][MovieID])
        vector=array(llista)
        desviacio=vector.std()
        if desviacio>aux:
            peliID=MovieID
            aux=desviacio
    print(d2[str(peliID)])
    
exercici14(d1,d2,d3)

#Exercici15--------------------------------------------------------------------

#Ens trobem amb el problema que no sabem ben bé el criteri que hem de fer servir
#per a considerar una pel.lícula com a 2a part, ja que si fem que ho siguin les 
#pel.lícules que contenen: " 2 ", la pel.lícula "Endless Summer 2, The",
#no és considerada una 2a part. En canvi, si fem que ho siguin les pel.lícules
#que contenen: " 2", la pel.lícula "Godzilla 2000", és considerada com a 2a part.
#Per últim, si fem que ho siguin les pel.lícules que contenen: "2", la pel.lícula
#"Vanya on 42nd Street", és considerada com a 2a part.
#Tot i això, creiem que el procediment és correcta, i que la mitjana és realitzada
#correctament.

def exercici15(d1,d2,d3):
    llista1=[int(x) for x in d2 if " II " in d2[x][0] or " 2 " in d2[x][0]]
    #llista amb els MovieID's de les pel.lícules que són 2es parts
    matriu=d3[:,llista1]
    suma=0
    cont=0
    for MovieID in range(len(llista1)):
        for UserID in range(len(d1)):
            if matriu[UserID][MovieID]!=0:
                suma+=matriu[UserID][MovieID]
                cont+=1
    return(print(suma/cont))
   
exercici15(d1,d2,d3)

#==============================================================================

ratings=np.array([[4, 1, 5, 2, 4, 5, 0, 1, 3, 1, 5, 1, 5, 0, 0], 

                   [5, 1, 3, 5, 1, 2, 4, 3, 0, 0, 5, 1, 4, 1, 0], 

                   [1, 0, 1, 0, 5, 1, 5, 4, 2, 1, 1, 0, 4, 1, 2], 

                   [0, 1, 3, 1, 0, 1, 3, 4, 4, 0, 5, 3, 2, 0, 4], 

                   [3, 3, 4, 2, 0, 2, 4, 1, 4, 0, 0, 3, 0, 0, 0], 

                   [4, 0, 1, 2, 2, 4, 2, 1, 2, 1, 5, 3, 5, 3, 4], 

                   [2, 4, 3, 2, 1, 2, 0, 0, 3, 0, 5, 5, 0, 0, 0], 

                   [5, 5, 5, 4, 4, 4, 2, 1, 0, 1, 4, 3, 5, 3, 3], 

                   [5, 1, 3, 0, 1, 4, 5, 4, 0, 4, 5, 0, 1, 0, 0], 

                   [2, 3, 1, 5, 3, 1, 4, 1, 1, 2, 5, 0, 4, 0, 5]])


user=np.array([1, 0, 0, 2, 4, 0, 1, 4, 0, 0, 0, 0, 0, 3, 5])

#------------------------------------------------------------------------------

mitjana_ratings=[]
aux=0
for puntuacions in ratings:
    suma=0
    divisio=0
    for puntuacio in puntuacions:
        if puntuacio!=0 and aux<10:
            suma+=puntuacio
            divisio+=1
    mitjana_ratings.append(suma/divisio)
print(mitjana_ratings)    
#llista amb les puntuacions mitjanes de cada usuari random de ratings (1-10)

#------------------------------------------------------------------------------

mitjana_user=[]
suma=0
divisio=0
for puntuacio in user:
    if puntuacio!=0:
        suma+=puntuacio
        divisio+=1
mitjana_user.append(suma/divisio)
print(mitjana_user)
#llista amb la puntuació mitjana de l'usuari principal user

#------------------------------------------------------------------------------

similitud_cos=[]
for s in range(ratings.shape[0]):
    a=0
    b=0
    c=0
    for i in range(ratings.shape[1]):
        if ratings[s][i]>0 and user[i]>0:
        #s=files(usuaris) i=columnes(pel.lícules)
            a+=ratings[s][i]*user[i]
            b+=pow(ratings[s][i],2)
            c+=pow(user[i], 2)
    similitud_cos.append(a/(pow(b, 0.5)*pow(c, 0.5)))
#similitud_cosinus=llista amb les similituds cosinus entre user i cada usuari random (1-10)

#------------------------------------------------------------------------------

sim_cos_index=[]
index=1
for i in similitud_cos:
    aux=[]
    aux+=index,i
    sim_cos_index.append(aux)
    index+=1
#sim_cos_index=llista de llistes formades per l'index d'usuari i la seva respectiva similitud cosinus
sim_cos_index.sort(key=lambda x: x[1])
#sim_cos_index=mateixa llista que abans, però ordenada respecte la seva respectiva similitud cosinus
max1=(sim_cos_index[-1])
max2=(sim_cos_index[-2])
max3=(sim_cos_index[-3])
print(max1,max2,max3)

#------------------------------------------------------------------------------

def operacio(p):
    p=p-1
    #El fet que cada vegada fem que la variable p(puntuació) sigui un número
    #menys que la puntuació que hem de prediure a l'usuari, es deu a que la
    #puntuació número 2 (per exemple), equival a la posició 1 en la llista user.
    suma_num=0
    suma_den=0
    for i in range(0,10):
    #és de 0 a 9 pq hi ha 10 usuaris (posicions 0-9)
        if ratings[i][p]!=0:
            num=similitud_cos[i]*((ratings[i][p])-(mitjana_ratings[i]))
            den=similitud_cos[i]
            suma_num+=num
            suma_den=abs(suma_den+den)
        i+=1
    resultat=mitjana_user+(suma_num/suma_den)
    return((resultat[0]))


pelis_recomanables=[]
cont=1
for i in user:
    aux=[]
    if i==0:
    #per a predir només els espais on hi hagi un 0 de l'array user
        res=operacio(cont)
        aux+=cont,res
        pelis_recomanables.append(aux)
    cont+=1
#pelis_recomanables=llista de llistes formades per l'índex de la pel.lícula i el seu respectiu valor predit
pelis_recomanables.sort(key=lambda x: x[1])
#pelis_recomanables=mateixa llista que abans, però ordenada respecte el seu respectiu valor predit

peli1=(pelis_recomanables[-1])
peli2=(pelis_recomanables[-2])
peli3=(pelis_recomanables[-3])
print(peli1,peli2,peli3)

#==============================================================================
#Puntuacions de pel.lícules----------------------------------------------------

#1. Toy Story (1) = 3
#2. Apollo 13 (150) = 5
#3. Quiz Show (300) = 5
#4. With Honors (450) = 1 
#5. Love and a .45 (600) = 5 
#6. Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (750) = 2
#7. American in Paris, An (900) = 3
#8. Looking for Richard (1050) = 3
#9. Aliens (1200) = 1
#10. Omen, The (1350) = 2
#11. Grosse Pointe Blank (1500) = 4
#12. Washington Square (1650) = 5
#13. Suicide Kings (1799) = 4
#14. In the Heat of the Night (1950) = 2
#15. Splash (2100) = 2
#16. Men Don't Leave (2250) = 4
#17. Prancer (2400) = 5
#18. Haunting, The (2550) = 1
#19. South Park: Bigger, Longer and Uncut (2700) = 1
#20. Public Access (2850) = 5

#------------------------------------------------------------------------------

def filtrar(d1,d3,puntuades):
    usuaris=[]
    for usuari in d1:
        cont=0
        for peliid in puntuades:
            if d3[int(usuari)][int(peliid)]!=0:
                cont+=1
        if cont>=3:
            usuaris.append(int(usuari))
    return(usuaris)
    
id_pelis_puntuades=np.array([1,150,300,450,600,900,1050,1200,1350,1500,1650,1799,1950,2100,2250,2400,2550,2700,2850])
usuarisid=filtrar(d1,d3,id_pelis_puntuades)
#usuarisid=llista amb els UserID's dels usuaris que han puntuat al menys 3 de les pel.lícules que nosaltres hem puntuat
ratings=d3[usuarisid,:]
#ratings=matriu amb les puntuacions dels usuarisid i totes les pel.lícules

#------------------------------------------------------------------------------

user=np.zeros((1,3953))
user[0][1]=3
user[0][150]=5
user[0][300]=5
user[0][450]=1
user[0][600]=5
user[0][750]=2
user[0][900]=3
user[0][1050]=3
user[0][1200]=1
user[0][1350]=2
user[0][1500]=4
user[0][1650]=5
user[0][1799]=4
user[0][1950]=2
user[0][2100]=2
user[0][2250]=4
user[0][2400]=5
user[0][2550]=1
user[0][2700]=1
user[0][2850]=5
#user=array amb puntuacions personals aplicades a les determinades pel.lícules

#------------------------------------------------------------------------------

mitjana_ratings=[]
aux=0
for puntuacions in ratings:
    suma=0
    divisio=0
    for puntuacio in puntuacions:
        if puntuacio!=0 and aux<10:
            suma+=puntuacio
            divisio+=1
    mitjana_ratings.append(suma/divisio)
print(mitjana_ratings)    

#------------------------------------------------------------------------------

mitjana_user=[]
suma=0
divisio=0
for puntuacio in user[0]:
    if puntuacio!=0:
        suma+=puntuacio
        divisio+=1
mitjana_user.append(suma/divisio)
print(mitjana_user)

#------------------------------------------------------------------------------

similitud_cos=[]
for s in range(ratings.shape[0]):
    a=0
    b=0
    c=0
    for i in range(ratings.shape[1]):
        if ratings[s][i]>0 and user[0][i]>0:
            a+=ratings[s][i]*user[0][i]
            b+=pow(ratings[s][i],2)
            c+=pow(user[0][i], 2)
    similitud_cos.append(a/(pow(b, 0.5)*pow(c, 0.5)))

#------------------------------------------------------------------------------

sim_cos_index=[]
index=1
for i in similitud_cos:
    aux=[]
    aux+=index,i
    sim_cos_index.append(aux)
    index+=1
#sim_cos_index=llista amb llistes formades per l'index d'usuari i la seva respectiva similitud cosinus
sim_cos_index.sort(key=lambda x: x[1])
#sim_cos_index=mateixa llista que abans, però ordenada respecte la seva respectiva similitud cosinus
max1=(sim_cos_index[-1])
max2=(sim_cos_index[-2])
max3=(sim_cos_index[-3])
max4=(sim_cos_index[-4])
max5=(sim_cos_index[-5])
max6=(sim_cos_index[-6])
max7=(sim_cos_index[-7])
max8=(sim_cos_index[-8])
max9=(sim_cos_index[-9])
max10=(sim_cos_index[-10])
print(max1,max2,max3,max4,max5,max6,max7,max8,max9,max10)

#------------------------------------------------------------------------------

def operacio(p):
    p=p-1
    #El fet que cada vegada fem que la variable p(puntuació) sigui un número
    #menys que la puntuació que hem de prediure a l'usuari, es deu a que la
    #puntuació número 2 (per exemple), equival a la posició 1.
    suma_num=0
    suma_den=0
    for i in range(len(usuarisid)-1):
        if ratings[i][p]!=0:
            num=similitud_cos[i]*((ratings[i][p])-(mitjana_ratings[i]))
            den=similitud_cos[i]
            suma_num+=num
            suma_den=abs(suma_den+den)
        i+=1
    if suma_den!=0:
    #mirar si la pel.lícula l'ha puntuat algun usuari. Sinó, no podem fer l'operació, ja que el denominador serà 0
        resultat=mitjana_user+(suma_num/suma_den)
        return((resultat[0]))
    else:
        return(0)
        #això ho fem perquè sinó, python posarà un "None" (explicat més endavant)
        
pelis_recomanables=[]
cont=1
for i in user[0]:
    aux=[]
    if i==0:
        res=operacio(cont)
        aux+=cont,res
        pelis_recomanables.append(aux)
    cont+=1

print(pelis_recomanables)
#pelis_recomanables=llista de llistes formades per l'índex de la pel.lícula i el seu respectiu valor predit
pelis_recomanables.sort(key=lambda x: x[1])
#pelis_recomanables=mateixa llista que abans, però ordenada respecte el seu respectiu valor predit
#si tinguessim un "None" en alguna predicció, no podriem ordenar-ho

peli1=(pelis_recomanables[-1])
print(d2[str(peli1[0])])
peli2=(pelis_recomanables[-2])
print(d2[str(peli2[0])])
peli3=(pelis_recomanables[-3])
print(d2[str(peli3[0])])
peli4=(pelis_recomanables[-4])
print(d2[str(peli4[0])])
peli5=(pelis_recomanables[-5])
print(d2[str(peli5[0])])
peli6=(pelis_recomanables[-6])
print(d2[str(peli6[0])])
peli7=(pelis_recomanables[-7])
print(d2[str(peli7[0])])
peli8=(pelis_recomanables[-8])
print(d2[str(peli8[0])])
peli9=(pelis_recomanables[-9])
print(d2[str(peli9[0])])
peli10=(pelis_recomanables[-10])
print(d2[str(peli10[0])])