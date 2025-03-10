from operator import itemgetter
import sys
import math

filename = sys.argv[1]

hartree=27.21138602
ttoau=2.418884326505*10**(-17)

#Read data from file
lines=[]
with open(filename) as data:
    for line in data:
        sl=line.split()
        if len(sl)==8:
            lines.append(map(int,sl[0:4])+map(float,sl[4:7]))            

#Sort
lines=sorted(lines,key=itemgetter(0,2))

#Get different initial states
ilev=list(set(zip(*lines)[0]))

#Calculate widts
iwid=[]
for lev in ilev:
    iwid.append(sum([line[6] for line in lines if lev==line[0]]))

#Normalize decay rates
for i,lev in enumerate(ilev):
    for j,line in enumerate(lines):
        if lev==line[0]:
            lines[j][5]=lines[j][6]/iwid[i]
            lines[j][6]=iwid[i]*ttoau*hartree

#Print to screen            
print("\n")
print("    Radiative rate table from FAC file:",filename)
print(" ----------------------------------------------------------")
print('%5s %5s %4s %3s %12s %14s %10s' % ("i","f","2Ji","2Jf","Epho(eV)","(i->f)/Sum(i)","Gam(eV)"))
print(" ----------------------------------------------------------")
for l in lines:
    print('%5i %5i %4i %3i %12.4f %14.6e %10.4f' % (l[0],l[2],l[1],l[3],l[4],l[5],l[6]))
print(" ----------------------------------------------------------")

print("\n")
print('%5s %10s %12s %12s' % ("i","H-L(fs)","Gam(H)","Gam(eV)"))
print(" -----------------------------------------")
for lev,wid in zip(ilev,iwid):
    print('%5i %10.4f %12.6f %12.6f' % (lev,1.0/wid*10**15,wid*ttoau,wid*ttoau*hartree))
print(" -----------------------------------------")
print("\n")

