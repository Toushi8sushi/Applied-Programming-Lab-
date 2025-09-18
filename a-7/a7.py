import numpy as np 
import math as m 
import matplotlib.pyplot as plt
# Main system parameters: number of mics, number of samples in time
Nmics = 64
Nsamp =75

# Source: x,y coordinates: x: 0+, y: [-Y, +Y] where Y determined by pitch and Nmics
src = (0, 0)
# Spacing between microphones
pitch = 0.1
# proxy for sampling rate
dist_per_samp = 0.1
# Speed of sound in the medium
C = 2.0
# Time dilation factor for sinc pulse: how narrow
SincP = 5.0

mics = np.zeros((Nmics, 2))

# Define positions based on the number of microphones and pitch
ymin = Nmics // 2
if Nmics % 2 == 0:
    # Even number of microphones, skip zero by using two ranges and concatenating them
    y_positions = np.concatenate((np.arange(-ymin, 0), np.arange(1, ymin + 1))) * pitch
else:
    # Odd number of microphones, include zero
    y_positions = np.arange(-ymin, ymin + 1) * pitch

# Set the y-coordinates for the microphones
mics[:, 1] = y_positions

print('mics position \n',mics,'\n')
mic_positions_dict = {str(i): list(mics[i-1]) for i in range(1,Nmics+1)}

# Output the dictionary
print("Microphone positions dictionary:\n", mic_positions_dict)

# Location of point obstacle
obstacle = (3,-1)

# Source sound wave- time axis and wave
# sinc wave with narrowness determined by parameter
t = 0 # CODE Nsamp time instants with spacing of dist_per_samp
def wsrc(t):
    return np.sinc(SincP*t)

'''x=np.linspace(0,20,1000)
plt.plot(x,wsrc(x))
plt.show()'''

# Distance from src to a mic after reflecting through pt
def dist(src, pt, mic):
    d1 = m.dist(src, mic)
    d2 = m.dist(pt, mic) # CODE distance from pt to mic
    return d1 + d2


audio_data=np.loadtxt('rx2.txt',dtype=float)
audio_data=np.flipud(audio_data)
# virtically flippping the grid to match the indexing that is being used in the dicitonary 

#---------------DEALY AND SUM ALGORITHM-------------------

# here we dont need till nsamps, only till the x coord of the obstacle is enough 
k=int(not (Nmics%2))
grid = np.zeros((Nsamp, Nmics+k)) #x and y coordinates of the grid 
#one extra y coordinate for even no of mics at origin i skipped 


''' Steps '''
# 1) going through each point on the grid 
# 2) for all mics -> calucating the distance to each mic and the delay
# 3) adding the value of the delayed signal from each mic at that point on the grip 
# 4) visualize it with a heat map 

#x>=0


'''x_index=0
grid = np.zeros((Nsamp, Nmics+k, 2))
print(grid.shape)
for x in np.arange(dist_per_samp, (Nsamp)* dist_per_samp + dist_per_samp, dist_per_samp):
    y_index=0
    if Nmics % 2 == 0:
        # Even number of microphones, skip zero
        for y in np.arange(-(Nmics//2), (Nmics//2) +1)* pitch :
            grid[x_index][y_index]=(x,y)
            y_index+=1

    else:
        # Odd number of microphones, start from -pitch*(Nmics//2) to avoid -0.2
        for y in np.linspace(-pitch * (Nmics // 2 ), pitch * (Nmics // 2), Nmics):
            grid[x_index][y_index]=(x,y)
            y_index+=1
        
    x_index+=1
    
print(grid)'''


x_index = 0
for x in np.arange(dist_per_samp, Nsamp * dist_per_samp + dist_per_samp, dist_per_samp):
    y_index = 0
    for y_index in range(Nmics + k):
        y = (y_index - Nmics // 2) * pitch  # Convert y_index to actual y position
        
        # For each point (x, y), calculate the delayed signal from each mic
        for p in mic_positions_dict:
            delay = (dist(src, (x, y), mic_positions_dict[p])) / C
            grid[x_index, y_index] += audio_data[int(p) - 1][int(delay / dist_per_samp)]  # Add delayed signal
        
    x_index += 1

# Visualize the result as a heatmap
plt.imshow(grid.T, cmap="viridis", aspect="auto")
plt.colorbar(label="Intensity")
plt.title("Heatmap of 2D Array")
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.savefig("heatmap.png")

# Plotting the audio samples for each mic position
n_rows, n_cols = audio_data.shape
plt.figure(figsize=(10, n_rows // 8))  # Adjust the figure size as needed
for i in range(n_rows):
    plt.plot(audio_data[i] + i)  # Offset each row by i on the y-axis

# Labeling the graph
plt.title("Delay and Sum Algorithm")
plt.xlabel("mic data")
plt.ylabel("mic position")

# Display the plot
plt.savefig("sound_samples.png")



