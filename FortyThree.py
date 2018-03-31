#!/usr/bin/python
# -*- coding: utf-8 -*-

#import matplotlib
#matplotlib.use("Qt4Agg")

import numpy as np, os, glob, sys, matplotlib.pyplot as plt

## Vstupní konstanty

sirka=2
cykl=40 #počet cyklů na vyhlazení pozadí 
vyhlazeni="NE" #zda vyhlazovat samotné spektrum
vaha=50 #váha prostřední hodnoty při vyhlazování spektra
ampl=-10000 #diskriminace dle plochy píku bez pozadí, píky s plochou menší než 'ampl' nebudou vypsány ve výstupním souboru 
#grafy=input('Chcete na závěr vyhodnocování zobrazit grafy spekter a pozadí? ')
grafy='a'
## Načtení a zpracování konfiguračního souboru

path0='/media/dominik/Windows8_OS/Deimos32python/'
os.chdir(path0)
cfgname=glob.glob(path0 + '/*.cfg')[0]
f0=open(cfgname)
for i0 in range(0, 20):
    if i0==12:
        config0=(f0.readline().split())
        config1=(f0.readline().split())
    f0.readline()
newconfig0=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
newconfig1=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))

## Načtení a zpracování souborů FRK ze spektrometru Deimos32

pathFRK=path0+'spc_frk'
os.chdir(pathFRK)
soubor=glob.glob(pathFRK + '/*.FRK')
print ('Zpracovávám následující soubory:')
#for i0b in range(0, len(soubor)):
#    print (i0b, soubor[i0b].replace(pathFRK + '/', ''))
for i1 in range(5,6): # 1): #
    #print(i1)
    print (i1, soubor[i1].replace(pathFRK + '/', ''))
    Y0=[0]*8192
    f1=open(soubor[i1])
    for i2 in range(0, len(Y0)):
        Y0[i2]=float(''.join(f1.readline().split()))
    Y=[0]*8192 #spektrum
    if(vyhlazeni=="ANO"):
        for i3 in range(1, len(Y0)-1):
            Y[i3]=(Y0[i3-1]+vaha*Y0[i3]+Y0[i3+1])/(2+vaha)
        del(i3)
    elif(vyhlazeni=="NE"):
        Y=Y0
    else:
        print("Chyba parametru 'vyhlazeni'. Nutno zadat ANO nebo NE")
        break
    C2=[0]*8192 #energie
    C=[0]*8192 #kanál
    Z=[0]*8192 #derivace spektra
    C[0]=1
    C2[0]=newconfig0+newconfig1
    for i4 in range(1, len(C2)):
        C[i4]=i4+1
        C2[i4]=newconfig0+(i4+1)*newconfig1
        Z[i4]=Y[i4]-Y[i4-1]
    G0=[] #kanál přibližného středu píku (derivace mění znaménko)
    G1=[] #energie přibližného středu píku (derivace mění znaménko)
    H0=[] #levé okraje píků
    H1=[] #pravé okraje píků
    for i5 in range(0, len(Z)-sirka):
        if(Z[i5+sirka]<0):
            G0.append(C[i5])
            G1.append(C2[i5])
    for i6 in range(0, len(G0)-sirka):
        if (i6==0):
            l11=G0[i6]
            l12=0
        l1=max(G0[i6],l12+1)
        l2=max(l1+sirka,l11)
        if (l1>len(Z) or l2>len(Z)):
            break
        while True:
            l1-=1
            if(l1==0 or l1==l12 or Z[max(l1,1)]<-0.1):
                break
        if l1==0:
            l1=1
        H0.append(l1)
        if(l2<len(C2)):
            while True:
                l2+=1
                if(l2==(len(C2)-1) or l2>len(C2) or Z[l2]>0.1):
                    break
            H1.append(l2)
        else:
            H1.append(l2-1)
        l11=l1
        l12=l2
    del l1, l2, l12, l11
    H01=[H0[0]]
    H11=[H1[0]]
    for i7 in range (1, len(H0)): #odstranění duplicitních píků
        if (H0[i7-1],H1[i7-1])!=(H0[i7],H1[i7]):
            H01.append(H0[i7])
            H11.append(H1[i7])
    G20=[] #energie maxima píku
    G21=[] #suma píku i s pozadím
    G22=[] #levý okraj píku
    G23=[] #pravý okraj píku
    G24=[] #pozadí
    G25=[] #šířka píku v kanálech
    G26=[] #plocha píku bez pozadí
    for i8 in range (0,len(H01)):
        maximum, index = max((val, idx) for idx, val in enumerate(Y[H01[i8]:H11[i8]]))
        G20.append(C2[H01[i8]+index]) #energie maxima píku
        G21.append(sum(Y[H01[i8]:H11[i8]])) #suma píku i s pozadím
        G22.append(H01[i8]) #levý okraj píku
        G23.append(H11[i8]) #pravý okraj píku
        # # #G24.append(0) #příprava na dosazení pozadí #zde se nesmí dosazovat 0, nutno, aby zůstalo prázdné
        G25.append(len(Y[H01[i8]:H11[i8]])) #šířka píku v kanálech
    pozadi=[]
    for i9 in range (0, len(G23)):
        pozadi.append(Y[G23[i9]])   #Něco je špatně...

## Vyhlazování pozadí
    
    for i10 in range (0,cykl):
        P0=[]
        P0.extend(pozadi)
        pozadi=[]
        P1=[0.0]*len(P0)
        P1[0]=P0[0]
        P1[len(P0)-1]=P0[len(P0)-1]
        for i11 in range (1,len(P0)-1):
            P1[i11]=min(P0[i11],np.mean([P0[i11-1],P0[i11],P0[i11+1]]))
        pozadi.extend(P1) 
    
    
    PP=[0.0]*len(C2)
    for i9e in range (0,len(G23)-1):
        PP[G23[i9e]]=pozadi[i9e]
        inkrement=(pozadi[i9e+1]-pozadi[i9e])/(G23[i9e+1]-G23[i9e])
        for i9f in range (0,(G23[i9e+1]-G23[i9e])):
            PP[G23[i9e]+i9f]=PP[G23[i9e]]+i9f*inkrement
    
    for i10 in range (0,int(cykl/4)):
        P0=[]
        P0.extend(PP)
        PP=[]
        P1=[0.0]*len(P0)
        P1[0]=P0[0]
        P1[len(P0)-1]=P0[len(P0)-1]
        for i11 in range (1,len(P0)-1):
            if (i10<(cykl)):
                P1[i11]=min(Y[i11],np.mean([P0[i11-1],P0[i11],P0[i11+1]]))
            else:
                P1[i11]=np.mean([P0[i11-1],P0[i11],P0[i11+1]])
        PP.extend(P1)    
    for i10a in range (0,len(G23)):
        G24.append(PP[G23[i10a]])    
    
    G26.append(G21[0]-(Y[G22[0]]/2+G24[0]/2)*G25[0])
    for i9b in range(1,len(G25)):
        G26.append(G21[i9b]-sum(PP[G22[i9b]:G23[i9b]]))
        
    for i9c in range(0,len(G26)):
        if G26[i9c]<ampl:
            G20[i9c]=[];G21[i9c]=[];G22[i9c]=[];G23[i9c]=[];G24[i9c]=[];G25[i9c]=[];G26[i9c]=[]
    for i9d in range(0,G20.count([])):
        G20.remove([]);G21.remove([]);G22.remove([]);G23.remove([]);G24.remove([]);G25.remove([]);G26.remove([])
## Vykreslení spektra a pozadí
    
    plt.figure(i1)
    plt.title(soubor[i1].replace(pathFRK + '/' , '').replace('.FRK',''))
    plt.xlabel('Energie (keV)')
    plt.ylabel('Cetnost (-)')
    plt.plot(C2, Y) #vykreslení spektra
    plt.plot(C2, PP, 'r') #vykreslení pozadí
    import scipy.signal
    ZX=Y
    for i in range(0,50):
        XY=scipy.signal.savgol_filter(ZX, 11, 2)
        ZX=XY
    ZY=[0]*len(ZX)
    for i in range (0,len(ZX)):
        ZY[i]=min(Y[i],ZX[i])
    for i in range(0,50):
        XY=scipy.signal.savgol_filter(ZY, 11, 2)
        ZY=XY
    XY=ZY
    plt.plot(C2, XY, 'k') 
    
## Načtení hodnot tlive treal a data ze souboru txt     
    
    text=glob.glob(soubor[i1].replace('spc_frk', 'txt').replace('.FRK','.TXT'))
    f2=open(text[0])
    for i in range(0,7):
        if i==6:
            Time=f2.readline().replace('                  ','').replace('\r\n', '')
            Treal=f2.readline().replace('                   ','').replace(' sec\r\n', '')
            Tlive=f2.readline().replace('                   ','').replace(' sec\r\n', '')
        f2.readline()
        
## Zapisování dat do souboru
    
    vystup = open(soubor[i1].replace(pathFRK + '/', '').replace('FRK','OUTpy'),'w')
    #vystup.write('Vyhodnocováno souborem: %s \n \n' %(str(os.path.basename(__file__))))
    vystup.write('%s \n%s \n%s \n \n' %(Time, Treal, Tlive)) 
    vystup.write('Energie (keV)                Plocha (-)\n')
    for i in range (0,len(G20)):
        vystup.write('%13f            %14f \n' % (G20[i], G26[i]) )
    vystup.close
    
    
if (grafy=='ano') or (grafy=='Ano') or (grafy=='a') or (grafy=='A') or (grafy=='1') or (grafy=='Y') or (grafy=='y') or (grafy=='yes') or (grafy=='Yes'):
    print('Hotovo! Zobrazuji grafy.')
    plt.show()
else:
    print('Hotovo!')
    
#del(i0,i1,i2,Y,Y0,C,C2)
    
