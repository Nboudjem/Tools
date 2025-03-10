import math
import numpy as np
try:
    import matplotlib.pyplot as plt
    matplot = True
except:
    print("Note: matplotlib not installed, plotting is not possible\n")
    matplot = False

#Define Lorentzian function
def lorentzian(dx,fwhm):
    def Lx(x,fwhm):
        return (fwhm/(2*np.pi))/(x**2+(fwhm/2)**2)
    xmin = -100*fwhm
    xmax = abs(xmin)
    xarr = np.arange(xmin,xmax,dx)
    if len(xarr) % 2 == 1:
        xarr = np.append(xarr,xarr[-1]+dx)
    yarr = np.zeros(len(xarr))
    for i in range(len(xarr)):
        yarr[i] = Lx(xarr[i],fwhm)
    return xarr,yarr

#Define Gaussian function
def gaussian(dx,fwhm):
    sigma = fwhm/(2*math.sqrt(2*math.log(2)))
    def Gx(x,sigma):
        return 1/(sigma*math.sqrt(2*np.pi))*math.exp(-x**2/(2*sigma**2))
    xmin = -20*fwhm
    xmax = abs(xmin)
    xarr = np.arange(xmin,xmax,dx)
    if len(xarr) % 2 == 1:
        xarr = np.append(xarr,xarr[-1]+dx)
    yarr = np.zeros(len(xarr))
    for i in range(len(xarr)):
        yarr[i] = Gx(xarr[i],sigma)
    return xarr,yarr

#Function to get essential input data
def get_input_data():
    print("\nConvolve a spectrum with Gaussian or Lorentzian function\n")
    func_type = input("Convolve with Gaussian (G) or Lorentzian (L) function?: ")
    func_type = func_type.strip().lower()
    func_width = float(input("\nEnter convolving function FWHM: "))
    out_file = input("\nEnter output file name: ")
    out_file = out_file.strip()
    out_plt = input("\nPlot result (Y/N)?: ")
    out_plt = out_plt.strip().lower()
    print("\nEnter spectrum to be convolved (x,y), Empty line stops input")
    x_spec = np.array([])
    y_spec = np.array([])
    while True:
        try:
            xy = input()
        except EOFError:
            return func_type,func_width,x_spec,y_spec,out_file,out_plt
            break

        if len(xy) == 0:
            return func_type,func_width,x_spec,y_spec,out_file,out_plt
            break
        try:
            x,y = xy.split()
        except:
            x,y = xy.split(",")
        x_spec = np.append(x_spec,[float(x)])
        y_spec = np.append(y_spec,[float(y)])

#Get input
type_conv, wid_conv, x_spec, y_spec, out_file, out_plt = get_input_data()

#Calculate dx and check for errors
dx_spec = 0
for i in range(1,len(x_spec)):
    dx_spec += x_spec[i]-x_spec[i-1]
dx_spec = dx_spec/float(len(x_spec)-1)
#Is dx constant
tol_dx = 0.0001
for i in range(1,len(x_spec)):
    if abs(x_spec[i]-x_spec[i-1]-dx_spec)/dx_spec > tol_dx:
        print("Error: Input spectrum dx is not constant, program stop!")
        exit()
#Is dx too large
tol_w = 10.0
print("\nCalculated dx: ",dx_spec)
if dx_spec > wid_conv/tol_w:
    print("Warning: Input spectrum dx might be too large in for the given FWHM!")

#Form convolving function
if type_conv == "l" or type_conv == "lorentzian":
    x_conv,y_conv = lorentzian(dx_spec,wid_conv)
elif type_conv == "g" or type_conv == "gaussian" :
    x_conv,y_conv = gaussian(dx_spec,wid_conv)
else:
    print("Error: Convolving function type not recognized, program stop!")
    exit()

#Convolve
FxG = np.convolve(y_spec,y_conv)*dx_spec

#Calculate some checking integrals
y_spec_int = np.trapz(y_spec,dx=dx_spec)
y_conv_int = np.trapz(y_conv,dx=dx_spec)
FxG_int = np.trapz(FxG,dx=dx_spec)
print("-Integrals-",\
    "\nI(F):",y_spec_int,\
    "\nI("+type_conv[0].upper()+"):",y_conv_int,\
    "\nI(F)*I("+type_conv[0].upper()+"):",y_spec_int*y_conv_int,\
    "\nI(Fx"+type_conv[0].upper()+"):",FxG_int,\
    "\nI_diff:",FxG_int-y_spec_int*y_conv_int)

#Set convolved result to the original x-range
FxG = FxG[int(len(x_conv)/2):int(len(x_conv)/2)+len(x_spec)]

#Write to file
ofl = open(out_file,"w")
for i in range(len(FxG)):
    ofl.write(str(x_spec[i])+","+str(FxG[i])+"\n")
ofl.close()
print("Output written to file: ",out_file)

#Plot spectra
if matplot and (out_plt == "y" or out_plt == "yes"):
    fig, ax = plt.subplots()
    ax.plot(x_spec,FxG,'b')
    ax.plot(x_spec,y_spec,'r')
    ax.set(title='Original (red) and convolved (blue) spectrum')
    plt.show()
