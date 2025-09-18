import numpy as np 
import math as m 
import matplotlib.pyplot as plt

# Main system parameters: number of mics, number of samples in time
Nmics = 64
Nsamp = 200

# Source: x,y coordinates: x: 0+, y: [-Y, +Y] where Y determined by pitch and Nmics
src = (0, 0)
# Spacing between microphones
pitch = 0.1
# proxy for sampling rate
dist_per_samp = 0.1
# Speed of sound in the medium
C = 2.0

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

print('Microphones position \n', mics, '\n')
mic_positions_dict = {str(i): list(mics[i-1]) for i in range(1, Nmics+1)}

# Output the dictionary
print("Microphone positions dictionary:\n", mic_positions_dict)

# Distance from src to a mic after reflecting through pt
def dist(src, pt, mic):
    d1 = m.dist(src, pt)  # Distance from source to point
    d2 = m.dist(pt, mic)  # Distance from point to mic
    return d1 + d2


audio_data = np.loadtxt('rx3.txt', dtype=float)

# Calculate evenly spaced indices based on Nmics
indices = np.linspace(0, audio_data.shape[0] - 1, Nmics, dtype=int)
print(indices)
audio_data = audio_data[indices, :]  # Select only the required rows
audio_data = np.flipud(audio_data)  # Flip the grid to match the indexing


#---------------DEALY AND SUM ALGORITHM-------------------
''' Steps '''
# 1) going through each point on the grid 
# 2) for all mics -> calucating the distance to each mic and the delay
# 3) adding the value of the delayed signal from each mic at that point on the grip 
# 4) visualize it with a heat map 

#x>=0
# Prepare the grid for the Delay and Sum algorithm
grid = np.zeros((Nsamp, Nmics))  

# Iterate over each point on the grid
for x_index, x in enumerate(np.arange(dist_per_samp, Nsamp * dist_per_samp + dist_per_samp, dist_per_samp)):
    for y_index in range(Nmics):
        # Convert y_index to actual y position using the microphone configuration
        y = (y_index - Nmics // 2) * pitch  # Assuming mic positions are centered
        
        # For each mic, calculate the delay and add the delayed signal to the grid
        for p, mic_pos in mic_positions_dict.items():
            # Calculate the delay for the current microphone
            delay = dist(src, (x, y), mic_pos) 
            delay_index = int(delay / dist_per_samp) # Convert delay to sample index
            
            if delay_index < audio_data.shape[1]:  # Make sure the delay is within the bounds of the audio data
                grid[x_index, y_index] += audio_data[int(p) - 1, delay_index]  # Add the delayed signal

extent = [0, Nsamp * dist_per_samp, -Nmics/2 * pitch, Nmics/2 * pitch]
plt.imshow(grid.T, cmap="viridis", aspect="auto", extent=extent)
plt.colorbar(label="Intensity")
plt.title("Heatmap ")
plt.ylabel("Microphone)")
#plt.savefig("heatmap_ee23b152png")
plt.show()

# Plotting the audio samples for each mic position
n_rows, n_cols = audio_data.shape
plt.figure(figsize=(10, n_rows // 8))  # Adjust the figure size as needed
for i in range(n_rows):
    plt.plot(audio_data[i] + i)  # Offset each row by i on the y-axis

# Labeling the graph
plt.title("Delay and Sum Algorithm")
plt.xlabel("Mic Data")
plt.ylabel("Mic Position")
#plt.savefig("sound_samples_ee23b152.png")
plt.show()
