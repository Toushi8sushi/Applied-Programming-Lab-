import qwerty_layout as l
import random
import sim_annealing_functions as functions
import copy
import math as m

# change this variable to generate a corresponding heatmap
#plain english text
input_text_1 = """
FICTION: Trees were swaying , though gently , and their leaves were rustling as if in applause to the change in the weather . <p> This had been going on for several days . The men and women who gauge the climate on television were exultant over the unusual run of good weather as if it was they who had brought it on .
MAGAZINE: The ability to approach every hunting situation with the same kind of open mind and without pre-conceived notions about " how it 's supposed to be done " is a trait all of the best deer hunters share . Plus , it 's a lot of fun to pull off-the-wall stunts that actually work in special situations .
NEWSPAPER: The protesters here certainly know what they do n't like : war , globalization , capitalism , drug laws , immigrant detention centers , a high-speed train line and , inexplicably , the Olympic torch . <p> " This is a discussion of war , " said Claudio Robba , 25 , one of maybe 150 protesters at a piazza , 
ACADEMIC: Synthesizing knowledge of the connections between above-surface and below-surface biodiversity was considered a priority to be addressed at a second workshop , since it would help to yield information on keystone species and interactions in ecosystem processes assess the extent of species 
SPOKEN: @SUMMIT It should be a C-note. @Mr._CARY_ANDERSON That's it. @Mr_ ANDERSON Oh, very good. See, you didn't have to get nervous, Mr. Cronick. You were really very good at it. @SUMMIT All right. @Mr._ANDERSON You -- you were coming fast and furious here. It was great. I could sleep. @
"""
#A python code for matrix multiplication 
input_text_2 = """
f=open("mat.txt","r")
def ini(n):
    Matrix=list()
    for i in range(n):
        line = f.readline().strip().split()
        Matrix.append([int(x) for x in line])
    return Matrix  
def print_mat(A):
    for i in range(n):
        print(A[i])

def matrix_multi(A,B):
    C=list()
    for i in range(n):
        c=list()
        for k in range(n):
            sum=0
            for j in range(n):
                sum+=A[i][j]*B[j][k]
            c.append(sum)
        C.append(c)
    return C

def matrix(A=ini(n),B=ini(n)):
    print_mat(A)
    print()
    print_mat(B)
    print()
    print_mat(matrix_multi(B,A))
matrix()
"""
#a paragraph by shakesphere 
input_text_3='''
What's he that wishes so?
My cousin Westmoreland? No, my fair cousin:
If we are mark'd to die, we are enow
To do our country loss; and if to live,
The fewer men, the greater share of honour.
God's will! I pray thee, wish not one man more.
By Jove, I am not covetous for gold,
Nor care I who doth feed upon my cost;
It yearns me not if men my garments wear;
Such outward things dwell not in my desires:
But if it be a sin to covet honour,
I am the most offending soul alive.
No, faith, my coz, wish not a man from England:
God's peace! I would not lose so great an honour
As one man more, methinks, would share from me
For the best hope I have. O, do not wish one more!
Rather proclaim it, Westmoreland, through my host,
That he which hath no stomach to this fight,
'''
#a hindi sentence typed in engligh 
input_text_4='''
Ye hindi mai likya hai , muje lagtha hai ke jab Hindi, english mai type ho to akhri results alag aa sakta hai kyuki jo shabd
hindi mai sabse zada istemal hota hai wo english se alag hoga iseliya mai ye sample text likraha hu taki mai ye test kar pau  
'''
# counting all the letters and storing it in a dictionnary with its frequency

# uncommment one of the following lines and leave the others commented

letter_count_dictionary = functions.letter_count(input_text_1, l)
#letter_count_dictionary = functions.letter_count(input_text_2,l)
#letter_count_dictionary = functions.letter_count(input_text_3, l)
#letter_count_dictionary = functions.letter_count(input_text_4, l)

def total_travel_distance(letter_count_dictionary, layout_keys, layout_charecter):
    # charecter set to be given from the layout
    distance = 0
    for i in letter_count_dictionary:
        # multiply distance by frequency
        distance += (
            functions.calc_distance(i, layout_keys, layout_charecter)
            * letter_count_dictionary[i]
        )
    return distance


print(
    "Original travel distance=",
    total_travel_distance(letter_count_dictionary, l.keys, l.characters),
)

# to print the dictionary with the key and its frequency
# print("freq_dictionary", letter_count_dictionary)


modified_layout_keys = copy.deepcopy(l.keys)

#function to update layout for simulated annealing

def update_layout(layout):
    # getting the keys in the dictionary
    keys_list = list(layout.keys())
    # I will not consider the following keys to be moved in simulated annealing

    unwanted_keys = [
        "Shift_L",
        "Shift_R",
        "Space",
        "Alt_L",
        "Alt_R",
        "Ctrl_L",
        "Ctrl_R",
    ]
    for j in unwanted_keys:
        keys_list.remove(j)

    # getting random keys to swap positions
    random_keys = random.sample(keys_list, 2)
    key1, key2 = random_keys[0], random_keys[1]

    flag1 = False
    flag2 = False

    # checking for homerow keys
    if layout[key1]["start"] == key1:  # if it is a home row key
        flag1 = True

    if layout[key2]["start"] == key2:  # this key a home row key
        flag2 = True

    if flag1 and flag2:  # both are home keys
        temp1 = layout[key1].copy()
        layout[key1] = layout[key2].copy()
        layout[key2] = temp1

        # changing the starting positions of keys as home row got updated
        for i in layout:
            check = layout[i]["start"]
            if check == key1:
                layout[i]["start"] = key2
            elif check == key2:
                layout[i]["start"] = key1

    elif flag1:  # key1 is in the homerow
        for i in layout:
            if layout[i]["start"] == key1:
                layout[i]["start"] = key2

        temp1 = layout[key1].copy()
        layout[key1] = layout[key2].copy()
        layout[key2] = temp1

    elif flag2:  # key2 is in the home row
        for i in layout:
            if layout[i]["start"] == key2:
                layout[i]["start"] = key1

        temp1 = layout[key1].copy()
        layout[key1] = layout[key2].copy()
        layout[key2] = temp1

    else:  # both are not home row keys
        temp1 = layout[key1].copy()
        layout[key1] = layout[key2].copy()
        layout[key2] = temp1

    return modified_layout_keys


"""---------START OF SIMULATED ANNEALING------------"""
current_best_list = list()
distance_list = list()


def sim_annealing(current_best_list, distance_list):
    high_temperature = 10000
    current_temp = high_temperature + 0
    cooling_rate = 0.999
    low_temperature = 4.5

    current_travel_distance = total_travel_distance(
        letter_count_dictionary, modified_layout_keys, l.characters
    )
    distance_list.append(current_travel_distance)

    current_best = current_travel_distance + 0

    current_best_list.append(current_best)
    best_layout = copy.deepcopy(modified_layout_keys)

    new_travel_dist = 0

    while current_temp >= low_temperature:
        # new layout is generated
        update_layout(modified_layout_keys)
        new_travel_dist = total_travel_distance(
            letter_count_dictionary, modified_layout_keys, l.characters
        )

        if new_travel_dist < current_travel_distance:
            current_travel_distance = new_travel_dist
            distance_list.append(new_travel_dist)
        else:
            probablity = m.exp(-(current_temp / high_temperature))
            if random.random() >= probablity:
                current_travel_distance = new_travel_dist
                distance_list.append(new_travel_dist)
            else:
                continue

        # keeping track of the best solution
        if new_travel_dist < current_best:
            current_best_list.append(new_travel_dist)
            current_best = new_travel_dist + 0
            best_layout = copy.deepcopy(modified_layout_keys)
        else:
            current_best_list.append(current_best)

        # cooling the temperature
        current_temp *= cooling_rate

    return best_layout, current_best_list[-1]


best_layout, final_distance = sim_annealing(current_best_list, distance_list)


# change ' ' to  Space to be used in the further functions as a reference in the querty_layout
if " " in letter_count_dictionary:
    letter_count_dictionary["Space"] = letter_count_dictionary[" "]
    del letter_count_dictionary[" "]

print("Final travel distance=", final_distance)


functions.keyboard_heatmap_generator(
    letter_count_dictionary, l.keys, "Heat Map of Key frequency", "ee23b152_heatmap.png"
)
functions.keyboard_heatmap_generator(
    letter_count_dictionary,
    modified_layout_keys,
    "Final Keyboard Layout",
    "ee23b152_final_heatmap.png",
)
functions.keyboard_heatmap_generator(
    letter_count_dictionary, best_layout, "Best Keyboard Layout", "ee23b152_best_heatmap.png"
)

functions.plot_master(distance_list, current_best_list)
