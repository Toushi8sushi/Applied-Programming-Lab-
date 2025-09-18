import qwerty_layout as l
import random
import sim_annealing_functions as functions
import copy

# change this variable to generate a corresponding heatmap
input_text = "My name is Toshith and my roll no is EE23B152"
#counting all the letters and storing it in a dictionnary with its frequency 
letter_count_dictionary = functions.letter_count(input_text,l)

def total_travel_distance(letter_count_dictionary,layout):
    distance = 0
    for i in letter_count_dictionary:
        # multiply distance by frequency
        distance += functions.calc_distance(i, layout) * letter_count_dictionary[i]
    return distance


#print("distance=", total_travel_distance(letter_count_dictionary,l))
#print("freq_dictionary", letter_count_dictionary)

# change ' ' to  Space to be used in the further functions as a reference in the querty_layout
if " " in letter_count_dictionary:
    letter_count_dictionary["Space"] = letter_count_dictionary[" "]
    del letter_count_dictionary[" "]

functions.keyboard_heatmap_generator(letter_count_dictionary,l.keys,"Heat Map of Key frequency","heatmap_ee23b152.png")

'''---------START OF SIMULATED ANNEALING------------'''
modified_layout_keys=copy.deepcopy(l.keys)

def update_layout(layout):
    keys_list=list(layout.keys())
    for i in range(20):
        random_keys = random.sample(keys_list, 2)
        if 'Space' in random_keys:
            continue
       
        key1,key2=random_keys[0],random_keys[1]

        '''random_keys=['d','k']
        key1,key2=random_keys[0],random_keys[1]'''

        flag1=False
        flag2=False

        if layout[key1]['start'] == key1: #if it is a home row key
            flag1=True
            print(random_keys,i,'flag1')
        if layout[key2]['start'] == key2: #this key a home row key
            flag2=True
            print(random_keys,i,'flag2')

        if flag1 and flag2:#both are home keys 
            temp1=layout[key1].copy()
            #print(random_keys,i,'both flag')
            layout[key1]=layout[key2].copy()
            layout[key2]=temp1

            #changing the starting positions of keys as home row got updated
            for i in layout:
                check=layout[i]['start']
                if check==key1:
                    layout[i]['start']=key2
                elif check== key2:
                    layout[i]['start']=key1 

        elif flag1: # key1 is in the homerow

            for i in layout:
                if layout[i]['start']==key1:
                    layout[i]['start']=key2

            temp1=layout[key1].copy()
            layout[key1]=layout[key2].copy()
            layout[key2]=temp1

        elif flag2:#key2 is in the home row 
            for i in layout:
                if layout[i]['start']==key2:
                    layout[i]['start']=key1

            temp1=layout[key1].copy()
            layout[key1]=layout[key2].copy()
            layout[key2]=temp1

        else: #both are not home row keys
            temp1=layout[key1].copy()
            print(random_keys,i,'no flag')
            layout[key1]=layout[key2].copy()
            layout[key2]=temp1

    return modified_layout_keys

modified_layout_keys=update_layout(modified_layout_keys)
functions.keyboard_heatmap_generator(letter_count_dictionary,modified_layout_keys,"updated keyboard",'ee.png')
'''for i in modified_layout_keys:
    print(i,modified_layout_keys[i])'''