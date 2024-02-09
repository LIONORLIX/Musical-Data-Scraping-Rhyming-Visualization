# Reference
# 
# https://stackoverflow.com/questions/59166664/cmudict-dict-vs-cmudict-entries-python3-nltk
#

import os
import re
import nltk
from nltk.corpus import cmudict
import csv
from pathlib import Path

nltk.download('cmudict')

def get_pron(word):
    return cmudict.dict().get(word)
       

def convert_to_rhyme(original_file_path, target_file_path):

    for root, _, files in os.walk(original_file_path):

        Path(target_file_path).mkdir(parents=True, exist_ok=True)
        
        # Go through each file 
        for file in files:
            # If it is a text file, read it and add it to the list of docuemnts
            # along with the filename (minus the extension)
            if file.endswith(".txt"):
                # print(file) 
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:

                    print(target_file_path+"/"+file)

                    new_content_temp = ""

                    with open(target_file_path+"/"+file, "w") as new_file:

                        lyrics = f.readlines()

                        for line in lyrics:
                            line = line.strip("\n")
                            pron_list = get_pron(line)
                            if pron_list==None:
                                new_content_temp += "---NONE---"
                            else:

                                for item in pron_list[0]:
                                    new_content_temp += item + " "

                            new_content_temp += "\n"     

                        new_file.write(new_content_temp)



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

    original_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/last_words"
    target_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/rhyming_schemes"

    convert_to_rhyme(original_file_path, target_file_path)     