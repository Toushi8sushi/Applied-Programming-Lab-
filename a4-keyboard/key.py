import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import qwerty_layout as l 
import math as m

input_text='^)_))*((()*))dhfsa'

def letter_count(s):
    result_dictionary = {}
    for char in s:
        char_alias=l.characters[char]
        if len(char_alias) == 1:
            result_dictionary[char] = result_dictionary.get(char, 0) + 1
        else:
            result_dictionary[char_alias[0]] = result_dictionary.get(char_alias[0], 0) + 1
            result_dictionary[char_alias[1]] = result_dictionary.get(char_alias[1], 0) + 1

    return result_dictionary

letter_count_dictionary=letter_count(input_text)

def distance_formula(pos1, pos2):
    a=m.dist(pos1,pos2)
    return a

def calc_distance(c, layout):
    keys=layout.keys
    characters=layout.characters

    if c.isupper():
        char_info=characters[c]
        if len(char_info) == 2:
            sum=0
            #first shift
            shift_info=keys[char_info[0]]
            sum+=distance_formula(shift_info['pos'],keys[shift_info['start']]['pos'])
            
            pos=keys[char_info[1]]['pos']
            start_pos=keys[char_info[1]]['start']
            sum+= distance_formula(pos,keys[start_pos]['pos'])
            return sum
            
    elif c.isalnum():
        char_info=characters[c]
        if len(char_info) == 1:
            start=keys[c]['start']
            if start == c:
                return 0
            else:
                pos=keys[c]['pos']
                start_pos=keys[keys[c]['start']]['pos']
                return distance_formula(pos,start_pos)
    else:
        if len(c) !=1 : # might be a shift
            symbol_info=keys[c]
            pos=symbol_info['pos']
            start_pos=keys[symbol_info['start']]['pos']
            return distance_formula(pos,start_pos)
        if c==' ':
            #distance to type a space is zero
            return 0 
        else:
            symbol_info=characters[c]
            if len(symbol_info)==1:
                key_info=keys[c]
                start=key_info['start']
                pos=key_info['pos']
                start_pos=keys[key_info['start']]['pos']
                return distance_formula(pos,start_pos)
            else:
                #shift distance
                sum=0
                #first shift
                shift_info=keys[symbol_info[0]]
                sum+=distance_formula(shift_info['pos'],keys[shift_info['start']]['pos'])
                
                pos=keys[symbol_info[1]]['pos']
                start_pos=keys[symbol_info[1]]['start']
                sum+= distance_formula(pos,keys[start_pos]['pos'])
                return sum

def total_travel_dist(letter_count_dictionary):
    distance=0
    for i in letter_count_dictionary:
        #multiply distance by frequency 
        distance+=calc_distance(i,l)*letter_count_dictionary[i]
    return distance

print("distance=",total_travel_dist(letter_count_dictionary))
print("freq_list",letter_count_dictionary)

#change ' ' to  space to be used in the further functions 
if ' ' in letter_count_dictionary:
    letter_count_dictionary['Space']=letter_count_dictionary[' ']
    del letter_count_dictionary[' ']

def keyboard_image_generator(input_layout):
    keys = input_layout.keys
    x_coords = []
    y_coords = []
    max_x = -500
    max_y = -500

    key_width = 1
    key_height = 1
    fig, ax = plt.subplots(figsize=(12, 6))

    # Draw keyboard layout and determine max_x, max_y
    for i in keys:
        if len(keys[i]) != 2:  # Handle special characters like @, ^
            continue
        else:
            pos = keys[i]['pos']
            x_coords.append(pos[0])
            y_coords.append(pos[1])
            if pos[0] > max_x:
                max_x = pos[0]
            if pos[1] > max_y:
                max_y = pos[1]

            # Draw rectangle for each key
            location = (pos[0] - key_width / 2, pos[1] - key_height / 2)
            rect = patches.Rectangle(location, key_width, key_height, edgecolor='black', facecolor='lightgray', zorder=1)
            ax.add_patch(rect)  # Add rectangle for the key
            ax.text(pos[0], pos[1], i, ha='center', va='center', fontsize=12, zorder=2)

    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-1, max_y + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Heatmap calculation part
    min_x = -1
    min_y = -1
    max_x += 1
    max_y += 1

    x_resolution = 500
    y_resolution = int((x_resolution * max_y) / max_x)

    # Create an empty 2D array for the heatmap
    heatmap = np.zeros((x_resolution, y_resolution))

    circle = 0.95

    # Define the heatmap mass function
    def heatmap_mass_function(x, y, frequency):
        result = m.exp(-((x) ** 2 + (y) ** 2))
        if result >= circle:
            return frequency
        else:
            if result < 0.7:
                return 0
            else:
                new_result = m.exp(-4* ((x) ** 2 + (y) ** 2)) * (frequency / circle)
                return new_result

    # Define grid step size
    x_step = (max_x - min_x) / x_resolution
    y_step = (max_y - min_y) / y_resolution

    # Fill the 2D array with values from the heatmap_mass_function
    for i in range(x_resolution):
        for j in range(y_resolution):
            x = min_x + i * x_step
            y = min_y + j * y_step
            
            # Calculate heatmap contribution for each letter's position
            for k in letter_count_dictionary:
                if k == 'Space':#ignoring space 
                    continue
                pos = keys[k]['pos']
                heatmap[i, j] += heatmap_mass_function(x - pos[0], y - pos[1], letter_count_dictionary[k])
    
    # Overlay the heatmap on the same ax (reusing the one used for the keyboard layout)
    heatmap_plot = ax.imshow(heatmap.T, extent=[min_x, max_x, min_y, max_y], origin='lower', cmap='jet', alpha=0.7, zorder=3)

    # Add colorbar using fig.colorbar instead of plt.colorbar
    fig.colorbar(heatmap_plot, ax=ax, label='Heatmap Value')

    # Invert the y-axis if necessary
    #ax.invert_yaxis()

    # Display the final plot with heatmap overlay
    plt.title('Heatmap Overlaid on Keyboard Layout')
    plt.show()

    return max_x, max_y
    #--------below one was generated by chatgpt above one is mine 
    '''
    # Define contour levels based on the heatmap values (low to high)
    levels = np.linspace(np.min(heatmap), np.max(heatmap), 7)  # 7 levels for the colors

    # Define custom colormap: White for lowest, Red for highest
    colors = ["#ffffff", "#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff7f00", "#ff0000"] # White (lowest) to Red (highest)
    vibrant_cmap = LinearSegmentedColormap.from_list("vibrant", colors, N=256)  # Proper order: white to red

    # Plot filled contours with the correct colormap
    contour_plot = ax.contourf(heatmap.T, levels=levels, extent=[min_x, max_x, min_y, max_y], cmap=vibrant_cmap, alpha=0.5, zorder=3)

    # Add colorbar for contour plot
    fig.colorbar(contour_plot, ax=ax, label='Contour Value')

    # Display the final plot with contour overlay
    plt.title('Heat Map of Key frequency')
    plt.savefig('heatmap.png')
    plt.show()

    return max_x, max_y'''

max_x,max_y=keyboard_image_generator(l)

