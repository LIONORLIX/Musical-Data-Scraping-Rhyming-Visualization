# Reference
# https://stackoverflow.com/questions/59166664/cmudict-dict-vs-cmudict-entries-python3-nltk
#

import os
import re
import nltk
from nltk.corpus import cmudict
import csv
from pathlib import Path
       
def update_none(original_file_path, target_file_path):

    for root, _, files in os.walk(original_file_path):
        
        # Go through each file 
        for file in files:
            # If it is a text file, read it and add it to the list of docuemnts
            # along with the filename (minus the extension)
            count=0
            if file.endswith(".txt"):
                # print(file) 
                new_content_temp = ""
                count = 0

                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:

                    print(target_file_path+"/"+file)
                    prons = f.readlines()
                    # print(prons)

                    with open(target_file_path+"/"+file, "r") as word_file:
                        words = word_file.readlines()
                        
                        # print(words)
                        
                        for line in prons:
                            pron_list=None
                            line = line.strip("\n")
                            
                            if re.search(r"^---.*?---$",line):
                                
                                new_content_temp += "---"+words[count].strip("\n")+"---"
                                
                            else:
                                new_content_temp += line
                            
                            new_content_temp += "\n"   

                            count+=1  

                with open(os.path.join(root, file), 'w', encoding='utf-8') as f:

                    f.write(new_content_temp)

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

    
    original_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/rhyming_schemes"
    target_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/last_words"

    update_none(original_file_path, target_file_path)     