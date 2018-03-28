import numpy, os, glob
path0='/media/dominik/Windows8_OS/Deimos32python/'
os.chdir(path0)
cfgname=glob.glob(path0 + '/*.cfg')[0]
f0=open(cfgname)
for x in range(0, 20):
    if x==12:
        config0=(f0.readline().split())
        config1=(f0.readline().split())
    f0.readline()
newconfig0=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
newconfig1=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
path1=path0+'spc_frk'
os.chdir(path1)
soubor=glob.glob(path1 + '/*.FRK')
for i0 in range(0, len(soubor)):
    Y0=[0]*8192
    f1=open(soubor[i0])
    for i1 in range(0, 8192):
        Y0[i1]=int(''.join(f1.readline().split()))
    Y=[0]*8192