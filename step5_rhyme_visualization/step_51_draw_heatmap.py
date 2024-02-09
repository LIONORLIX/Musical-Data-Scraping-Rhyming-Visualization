#https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap
#https://seaborn.pydata.org/generated/seaborn.heatmap.html
#https://stackoverflow.com/questions/42712304/seaborn-heatmap-subplots-keep-axis-ratio-consistent
#https://blog.csdn.net/wws_2017/article/details/107259257
#https://stackoverflow.com/questions/52273546/matplotlib-typeerror-axessubplot-object-is-not-subscriptable
#https://blog.csdn.net/qq_42951560/article/details/110004178

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import re
import os
import csv
from pathlib import Path

def get_file_count(original_file_path):
    count = 0
    for root, _, files in os.walk(original_file_path):

        # Go through each file 
        for file in files:
            count+=1
    return count

def load_file_for_visualization(original_file_path,last_word_file_path,dir_name):

    count = 0
    
    for root, _, files in os.walk(original_file_path):

        # Go through each file 
        for file in files:

            if file.endswith(".txt"):
                
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:

                    # print(original_file_path+"/"+file)

                    if (f==[]):
                        continue

                    visulize_rhyming_pattern(compare_similarity(get_single_rhyming(f)),get_last_word(last_word_file_path + '/'+file),file,dir_name)

                count+=1

def get_last_word(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        last_word_list = []
        lyrics = f.readlines()

        for line in lyrics:
            last_word_list.append(line.strip("\n"))

        if last_word_list == []:
            return(["","","",""])

        return last_word_list

def get_single_rhyming(file):

    rhyming_scheme_list = []

    lyrics = file.readlines()

    for line in lyrics:

        if line=="\n" :
            continue
        else:
            pron_list = []

            for item in line.split():
                pron_list.append(item)

            rhyming_scheme_list.append(pron_list)

    return rhyming_scheme_list


def compare_similarity(rhyming_scheme_list):

    similarity_matrix = []

    if rhyming_scheme_list==[]:
        return np.matrix([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    for item in rhyming_scheme_list:

        similarity_vector = []
        # print(item)
        if re.search(r"^---.*?---$",item[0]):
            for compared_item in rhyming_scheme_list:
                if (item == compared_item):
                    similarity_vector.append(1.0)
                else:
                    similarity_vector.append(0.0)
        else:
            for compared_item in rhyming_scheme_list:

                length = min(len(item),len(compared_item))
                count = 0

                for i in range(length-1,-1,-1):
                    if (item[i] == compared_item[i]):
                        count+=1
                    elif (item[i] != compared_item[i]):
                        break
                similarity = count/length
                similarity_vector.append(similarity)

        similarity_matrix.append(similarity_vector)

    return np.matrix(similarity_matrix)

        
def visulize_rhyming_pattern(similarity_matrix,last_word_list,file_name,dir_name):

    print(dir_name, "  ", file_name)

    fig, ax = plt.subplots(figsize=(len(similarity_matrix)/5, len(similarity_matrix)*0.8/5))

    similarity_dataframe = pd.DataFrame(similarity_matrix, index=last_word_list, columns=last_word_list)
    
    ax.set_title(file_name.strip(".txt").replace("-"," "))
    
    map = sns.heatmap(similarity_dataframe, cbar=True, ax=ax)
    map.set_aspect('equal', adjustable='box')

    plt.savefig("data/cleaned_dataset/musicals/"+dir_name+"/patterns/"+file_name.strip(".txt")+".jpg", bbox_inches='tight')


musical_url_cleaned_list = []

musical_list_path = "data/musical_list_temp.csv"
# musical_list_path = "data/raw_data_scraped/musical_list.csv"
with open(musical_list_path, newline='') as csv_file:
 
    #get csv content to read the url
    content = csv.reader(csv_file, delimiter='\t', quotechar='"')
    next(content)

    for row in content:
        musical_url_cleaned_list.append(row[3])

for dir_name in musical_url_cleaned_list: 

    print(dir_name)

    original_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/rhyming_schemes"
    last_word_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/last_words"

    file_num=get_file_count(original_file_path)

    column = 1
    row = file_num
    # if (file_num%column != 0):
    #     row = file_num//column+1
    # else:
    #     row = file_num//column
    if row == 0:
        row=1


    Path("data/cleaned_dataset/musicals/"+dir_name+"/patterns").mkdir(parents=True, exist_ok=True)
    
    # fig, axes = plt.subplots(row, column, figsize=(4* column, 4 * row*0.8),squeeze=False)

    # load_file_for_visualization(original_file_path,last_word_file_path,axes.flatten())
    load_file_for_visualization(original_file_path,last_word_file_path,dir_name)

    

    # plt.show()    
