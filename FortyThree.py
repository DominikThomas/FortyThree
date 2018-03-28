import numpy, os
path0='/media/dominik/Windows8_OS/Deimos32python/'
cfgname=glob.glob(path0 + '*.cfg')[0]
f=open(cfgname)
for x in range(0, 20):
    if x==12:
        energy=(f.readline().split())
        channel=(f.readline().split())
    f.readline()
config=numpy.matrix([[float(energy[0]), float(energy[1])], [float(channel[0]), float(channel[1])]])
cd spc_frk
path1=path+'spc_frk'
