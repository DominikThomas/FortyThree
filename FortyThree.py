#import matplotlib
#matplotlib.use("Qt4Agg")
import numpy as np, os, glob #, matplotlib.pyplot as plt
vaha=50
sirka=2
cykl=20 #počet cyklů na vyhlazení pozadí 
vyhlazeni="NE"
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
path1=path0+'spc_frk'
os.chdir(path1)
soubor=glob.glob(path1 + '/*.FRK')
for i1 in range(0, len(soubor)):
    #print(i1)
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
        l1=G0[i6]
        l2=G0[i6+sirka]
        while True:
            l1-=1
            if(l1==0 or Z[max(l1,1)]<-0.1):
                break
        if l1==0:
            l1=1
        H0.append(l1)
        if(l2<len(C2)):
            while True:
                l2+=1
                if(l2==len(C2) or Z[l2]>0.1):
                    break
            H1.append(l2-1)
        else:
            H1.append(l2)
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
    for i8 in range (0,len(H01)):
        G20.append(C2[Y.index(max(Y[H01[i8]:H11[i8]]))]) #energie maxima píku
        G21.append(sum(Y[H01[i8]:H11[i8]])) #suma píku i s pozadím
        G22.append(H01[i8]) #levý okraj píku
        G23.append(H11[i8]) #pravý okraj píku
        # # #G24.append(0) #příprava na dosazení pozadí #zde se nesmí dosazovat 0, nutno, aby zůstalo prázdné
        G25.append(len(Y[H01[i8]:H11[i8]])) #šířka píku v kanálech
    pozadi=[]
    for i9 in range (0, len(G23)):
        pozadi.append(Y[G23[i9]])
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
    G24.extend(pozadi)
    #plot
    #plt.figure(i1)
    X=[0]*len(G23)
    for i in range (0,len(G23)):
        X[i]=C2[G23[i]]
#    plt.plot(C2, Y)
#    plt.plot(X, pozadi, 'r')
#plt.show()
print('Hotovo!')
    
    
#del(i0,i1,i2,Y,Y0,C,C2)

    
    