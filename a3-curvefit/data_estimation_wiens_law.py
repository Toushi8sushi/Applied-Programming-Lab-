import csv 
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

'''check units everywhere'''
wavelength=list()
spctrl_radiance=list()
fptr=open('d3.txt','r')
reader=csv.reader(fptr)

for i in reader:
    wavelength.append(float(i[0]))
    spctrl_radiance.append(float(i[1]))
#remove the bad data
wavelength=wavelength[27:]
spctrl_radiance=spctrl_radiance[27:]

spctrl_radiance_filtered = [] 

plt.figure()
# First subplot
plt.subplot(2,1, 1)
plt.plot(wavelength, spctrl_radiance) #x,y
# filter
weights = [1, 2, 3, 4, 5, 4, 3, 2, 1]  # Example weights for a window size of 9
for i in range(len(spctrl_radiance)):
    weighted_sum = 0
    weight_sum = 0
    for offset, k in enumerate(range(i-4, i+5)):  # Adjust for the window size
        if k < 0:
            continue
        elif k >= len(wavelength):
            continue
        else:
            weighted_sum += spctrl_radiance[k] * weights[offset]  # Apply weights
            weight_sum += weights[offset]  # Sum the weights
    
    if weight_sum > 0:
        spctrl_radiance_filtered.append(weighted_sum / weight_sum)  # Compute the weighted mean
    else:
        spctrl_radiance_filtered.append(0) 

# Second subplot
plt.subplot(2,1, 2)
plt.plot(wavelength, spctrl_radiance_filtered)

# Show the plots
plt.show()


spctrl_radiance_filtered=np.array(spctrl_radiance_filtered)
wavelength=np.array(wavelength)

#a=2*h*c^2
#b=h*c/Kb*T
def model(wavelength,a,b):
    num=a
    din=((wavelength**5)*(np.exp(b/wavelength)-1))
    return num/din

h=1e-34
c=1e8
Kb=1e-23
T=10**3
a=(2*h)*c**2
b=(h*c)/(Kb*T)

popt, pcov = curve_fit(model, wavelength, spctrl_radiance_filtered, p0=[a,b])
spctrl_radiance_filtered_model = model(wavelength, popt[0], popt[1])

# Plot the fitted model against the data
plt.figure()
plt.plot(wavelength, spctrl_radiance_filtered, label="Original Data")
plt.plot(wavelength, spctrl_radiance_filtered_model, label="Fitted Model")
plt.legend()
plt.show()
# Print the parameters
print("Fitted parameters:", popt) 

'''using wiens displacement law on the smoothened curve'''
max_radiance=np.max(spctrl_radiance_filtered_model)
index_max=np.where(spctrl_radiance_filtered_model ==  max_radiance)
peak_wavelength=wavelength[index_max][0] # corresponding wavelength
B=2.897771955e-3
temp=B/peak_wavelength
T=temp
print('temperature=',temp)

'''performing partial application'''
def model_c(wavelength,c):
    global h,Kb,T
    num=(2*(c**2))*h
    din=((wavelength**5)*(np.exp((h*c)/(Kb*T*wavelength)-1)))
    return num/din

popt, pcov = curve_fit(model_c, wavelength, spctrl_radiance_filtered, p0=[1e8])
print(popt[0])
c=popt[0]



def model_h(wavelength,h):
    global c,Kb,T
    num=(2*(c**2))*h
    din=((wavelength**5)*(np.exp((h*c)/(Kb*T*wavelength)-1)))
    return num/din

popt, pcov = curve_fit(model_h, wavelength, spctrl_radiance_filtered, p0=[1e-34])
print(popt[0])