import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# reading data file and storing into a list
wavelength = list()
spctrl_radiance = list()
fptr = open("d3.txt", "r")
reader = csv.reader(fptr)

for i in reader:
    wavelength.append(float(i[0]))
    spctrl_radiance.append(float(i[1]))

# filtering the data
spctrl_radiance_filtered = []

plt.figure()
# First subplot
plt.subplot(2, 1, 1)
plt.plot(wavelength, spctrl_radiance)
# filter
weights = [1, 2, 3, 4, 5, 4, 3, 2, 1]  # Example weights for a window size of 9
for i in range(len(spctrl_radiance)):
    weighted_sum = 0
    weight_sum = 0
    for offset, k in enumerate(range(i - 4, i + 5)):  # Adjust for the window size
        if k < 0:
            continue
        elif k >= len(wavelength):
            continue
        else:
            weighted_sum += spctrl_radiance[k] * weights[offset]  # Apply weights
            weight_sum += weights[offset]  # Sum the weights

    if weight_sum > 0:
        spctrl_radiance_filtered.append(
            weighted_sum / weight_sum
        )  # Compute the weighted mean
    else:
        spctrl_radiance_filtered.append(0)

# Second subplot
plt.subplot(2, 1, 2)
plt.plot(wavelength, spctrl_radiance_filtered)

# Show the plots
plt.show()


spctrl_radiance_filtered = np.array(spctrl_radiance_filtered)
wavelength = np.array(wavelength)

# defining constants
h = 6.626e-34
c = 3e8
Kb = 1.38e-23
Temp = 0  # unknown that will be found out


# modeling my function
def model_T(wavelength, T):
    global h, Kb, c
    num = 2 * h * (c**2)
    din = (wavelength**5) * (np.exp((h * c) / (Kb * T * wavelength)) - 1)
    return num / din


popt, pcov = curve_fit(model_T, wavelength, spctrl_radiance_filtered, p0=[1e4])
spctrl_radiance_filtered_model = model_T(wavelength, popt[0])


Temp = popt[0]  # estimated temperature
# Plot the fitted model against the data
plt.figure()
plt.title("Temperature =" + str(popt[0]) + " K")
plt.plot(wavelength, spctrl_radiance_filtered, label="Original Data")
plt.plot(wavelength, spctrl_radiance_filtered_model, label="Fitted Model")
plt.xlabel("Wavelength in meters")
plt.ylabel("Spectral radiance in watt/steradian/square metre ")
plt.legend()
plt.show()
# Print the parameters
print("Fitted parameter Temperature:", popt[0], " K")


# partial application of function
# estimating Kb
def model_Kb(wavelength, Kb):
    global h, c, Temp
    num = 2 * h * (c**2)
    din = (wavelength**5) * (np.exp((h * c) / (Kb * Temp * wavelength)) - 1)
    return num / din


popt, pcov = curve_fit(model_Kb, wavelength, spctrl_radiance_filtered, p0=[1e-23])
spctrl_radiance_filtered_model = model_Kb(wavelength, popt[0])
# Plot the fitted model against the data
plt.figure()
plt.title("Kb(boltzmann constant) =" + str(popt[0]) + " J⋅K^-1")
plt.plot(wavelength, spctrl_radiance_filtered, label="Original Data")
plt.plot(wavelength, spctrl_radiance_filtered_model, label="Fitted Model")
plt.xlabel("Wavelength in meters")
plt.ylabel("Spectral radiance in watt/steradian/square metre ")
plt.legend()
plt.show()
# Print the parameters
print("Fitted parameter Kb(boltzmann constant):", popt[0], " J⋅K^-1")


# estimating c
def model_c(wavelength, c):
    global h, Kb, Temp
    num = 2 * h * (c**2)
    din = (wavelength**5) * (np.exp((h * c) / (Kb * Temp * wavelength)) - 1)
    return num / din


popt, pcov = curve_fit(model_c, wavelength, spctrl_radiance_filtered, p0=[1e8])
spctrl_radiance_filtered_model = model_c(wavelength, popt[0])
# Plot the fitted model against the data
plt.figure()
plt.title("Speed of Light =" + str(popt[0]) + " m/s")
plt.plot(wavelength, spctrl_radiance_filtered, label="Original Data")
plt.plot(wavelength, spctrl_radiance_filtered_model, label="Fitted Model")
plt.xlabel("Wavelength in meters")
plt.ylabel("Spectral radiance in watt/steradian/square metre ")
plt.legend()
plt.show()
# Print the parameters
print("Fitted parameter c:", popt[0], " m/s")


# estimating h
def model_h(wavelength, h):
    global c, Kb, Temp
    num = 2 * h * (c**2)
    din = (wavelength**5) * (np.exp((h * c) / (Kb * Temp * wavelength)) - 1)
    return num / din


popt, pcov = curve_fit(model_h, wavelength, spctrl_radiance_filtered, p0=[1e-34])
spctrl_radiance_filtered_model = model_h(wavelength, popt[0])
# Plot the fitted model against the data
plt.figure()
plt.title("Planck constant=" + str(popt[0]) + " J⋅Hz^-1")
plt.plot(wavelength, spctrl_radiance_filtered, label="Original Data")
plt.plot(wavelength, spctrl_radiance_filtered_model, label="Fitted Model")
plt.xlabel("Wavelength in meters")
plt.ylabel("Spectral radiance in watt/steradian/square metre")
plt.legend()
plt.show()
# Print the parameters
print("Fitted parameter h:", popt[0], " J⋅Hz^-1")
