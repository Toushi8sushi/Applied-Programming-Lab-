import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math as m
from matplotlib.colors import LinearSegmentedColormap


def letter_count(s, l):
    # dictionary to store the letters and the frequency of their occurance
    result_dictionary = {}
    for char in s:
        # ignoring tab and enter
        if char == "\n" or char == "\t":
            continue
        else:
            char_alias = l.characters[char]

            if len(char_alias) == 1:
                result_dictionary[char] = result_dictionary.get(char, 0) + 1
            else:
                # special keys like shift and capital letters require pressing 2 keys so they are handeled seperately
                result_dictionary[char_alias[0]] = (
                    result_dictionary.get(char_alias[0], 0) + 1
                )
                result_dictionary[char_alias[1]] = (
                    result_dictionary.get(char_alias[1], 0) + 1
                )

    return result_dictionary


def distance_formula(pos1, pos2):
    a = m.dist(pos1, pos2)
    return a


def calc_distance(c, layout_keys, layout_charecter):
    # dictionary corresponding to the layout is imported to be used in this function
    keys = layout_keys
    characters = layout_charecter

    # handling capital letters
    if c.isupper():
        char_info = characters[c]
        if len(char_info) == 2:  # its length should be 2
            sum = 0
            # first the distance to press shift
            # the first index contains the name of the shift key
            shift_info = keys[char_info[0]]
            # getting the distance of of typing shift from its start position and its location
            sum += distance_formula(shift_info["pos"], keys[shift_info["start"]]["pos"])

            # similarly the distance to type the key is calculated
            pos = keys[char_info[1]]["pos"]
            start_pos = keys[char_info[1]]["start"]
            sum += distance_formula(pos, keys[start_pos]["pos"])
            return sum

    # handling lower case letters and numbers
    elif c.isalnum():
        char_info = characters[c]
        if len(char_info) == 1:
            start = keys[c]["start"]
            if start == c:
                return 0
            else:
                pos = keys[c]["pos"]
                start_pos = keys[keys[c]["start"]]["pos"]
                return distance_formula(pos, start_pos)
    # finally handling all the special case charecters
    else:
        if len(c) != 1:  # a key which needs a shift to be pressed
            symbol_info = keys[c]
            pos = symbol_info["pos"]
            start_pos = keys[symbol_info["start"]]["pos"]
            return distance_formula(pos, start_pos)
        if c == " ":
            # distance to type a space is zero
            return 0
        else:
            symbol_info = characters[c]
            if len(symbol_info) == 1:
                key_info = keys[c]
                start = key_info["start"]
                pos = key_info["pos"]
                start_pos = keys[key_info["start"]]["pos"]
                return distance_formula(pos, start_pos)
            else:
                # shift distance
                sum = 0
                # first distance to a shift key
                shift_info = keys[symbol_info[0]]
                sum += distance_formula(
                    shift_info["pos"], keys[shift_info["start"]]["pos"]
                )

                pos = keys[symbol_info[1]]["pos"]
                start_pos = keys[symbol_info[1]]["start"]
                sum += distance_formula(pos, keys[start_pos]["pos"])
                return sum


def keyboard_heatmap_generator(
    letter_count_dictionary, input_layout_keys, image_title, image_file_name
):
    # importing keys
    keys = input_layout_keys
    # storing the location to plot the heatmaps
    x_coords = []
    y_coords = []

    # garbage value which will be changed later
    max_x = -500
    max_y = -500

    key_width = 1
    key_height = 1
    space_key_width = 4
    fig, ax = plt.subplots(figsize=(12, 6))

    # Draw keyboard layout and determine max_x, max_y
    for i in keys:
        if len(keys[i]) != 2:  # Handle special characters like @, ^
            continue
        else:
            pos = keys[i]["pos"]
            x_coords.append(pos[0])
            y_coords.append(pos[1])

            # updating the maximum size of the image
            if pos[0] > max_x:
                max_x = pos[0]
            if pos[1] > max_y:
                max_y = pos[1]

            # zorder defines the position of the key in the final image
            if i == "Space":
                location = (pos[0] - space_key_width / 2, pos[1] - key_height / 2)
                rect = patches.Rectangle(
                    location,
                    space_key_width,
                    key_height,
                    edgecolor="black",
                    facecolor="lightgray",
                    zorder=1,
                )
                ax.add_patch(rect)  # Add rectangle for the key
                ax.text(
                    pos[0], pos[1], i, ha="center", va="center", fontsize=12, zorder=2
                )
            else:
                # Draw rectangle for each key
                location = (pos[0] - key_width / 2, pos[1] - key_height / 2)
                rect = patches.Rectangle(
                    location,
                    key_width,
                    key_height,
                    edgecolor="black",
                    facecolor="lightgray",
                    zorder=1,
                )
                ax.add_patch(rect)  # Add rectangle for the key
                ax.text(
                    pos[0], pos[1], i, ha="center", va="center", fontsize=12, zorder=2
                )

    # setting the limits of the image
    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-1, max_y + 1)
    ax.set_aspect("equal")
    ax.axis("off")

    # Heatmap calculation part
    # here we set the limit for the heatmap to be layer on the image
    min_x = -1
    min_y = -1
    max_x += 1
    max_y += 1

    # increase the value of the resolution for a more detailed image
    x_resolution = 300
    y_resolution = int((x_resolution * max_y) / max_x)

    # Create an empty 2D array for the heatmap
    heatmap = np.zeros((x_resolution, y_resolution))

    # defining the limit up to which to draw the heatmap
    circle = 0.95

    # Define the heatmap mass function which will give a value to the heatmap for each key at its coordinates
    def heatmap_mass_function(x, y, frequency):
        # result will give me the extent up to which i need to plot my heatmap
        result = m.exp(-((x) ** 2 + (y) ** 2))

        if result >= circle:
            # i want the top of the heatmap to be flat
            return frequency
        else:
            # I will create contours in the surrounding area
            if result < 0.7:
                return 0
            else:
                # picked by me to give a good contour
                new_result = m.exp(-4 * ((x) ** 2 + (y) ** 2)) * (frequency / circle)
                return new_result

    # Define grid step size to plot the heatmap on
    x_step = (max_x - min_x) / x_resolution
    y_step = (max_y - min_y) / y_resolution

    # Fill the 2D array with values from the heatmap_mass_function
    for i in range(x_resolution):
        for j in range(y_resolution):
            x = min_x + i * x_step
            y = min_y + j * y_step

            # Calculate heatmap contribution for each letter's position
            for k in letter_count_dictionary:
                # ignoring space remove this to include it
                if k == "Space":
                    continue

                # adding heatmap at each coordinate
                pos = keys[k]["pos"]
                heatmap[i, j] += heatmap_mass_function(
                    x - pos[0], y - pos[1], letter_count_dictionary[k]
                )

    # Define contour levels based on the heatmap values (low to high)
    masked_heatmap = np.ma.masked_less(heatmap, 0.9)
    levels = np.linspace(0.8, np.max(heatmap), 6)  # 6 levels for the colors

    # Define custom colormap: violet for lowest, Red for highest
    colors = [
        "#0000ff",
        "#00ffff",
        "#00ff00",
        "#ffff00",
        "#ff7f00",
        "#ff0000",
    ]
    vibrant_cmap = LinearSegmentedColormap.from_list("vibrant", colors, N=256)

    # Plot filled contours with the correct colormap
    # zorder defines the position of the heatmap
    contour_plot = ax.contourf(
        masked_heatmap.T,
        levels=levels,
        extent=[min_x, max_x, min_y, max_y],
        cmap=vibrant_cmap,
        alpha=0.5,
        zorder=3,
    )

    # Add colorbar for contour plot
    fig.colorbar(contour_plot, ax=ax, label="Contour Value")

    plt.title(image_title)
    plt.savefig(image_file_name)
    plt.show()


def plot_master(path_length_list, current_best_list):
    x = len(path_length_list)
    X = np.linspace(1, x, x)

    plt.plot(X, path_length_list, label="Current Distance")
    plt.plot(X, current_best_list, label="Current Best Distance")

    # Adding labels to the axes
    plt.xlabel("Iteration")
    plt.ylabel("Value")

    # Adding a title (optional)
    plt.title("Distance vs. Iterations ")

    # Adding a legend
    plt.legend()

    # Show the plot
    plt.show()
