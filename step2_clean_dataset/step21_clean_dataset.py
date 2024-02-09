# Code Reference
# https://docs.python.org/3/library/re.html#search-vs-match

import os
import re
import csv
from pathlib import Path

def load_text_documents(original_file_path, target_file_path):

    # Find the files in the directory
    empty_line_conut = 0

    is_quote = 0

    for root, _, files in os.walk(original_file_path):

        Path(target_file_path).mkdir(parents=True, exist_ok=True)
        
        # Go through each file 
        for file in files:
            # If it is a text file, read it and add it to the list of docuemnts
            # along with the filename (minus the extension)
            if file.endswith(".txt"):
                # print(file)
                
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    # print(f.readlines())
                    print(target_file_path+"/"+file)

                    new_content_temp = ""

                    with open(target_file_path+"/"+file, "w") as cleaned_file:

                        lyrics = f.readlines()

                        title = "------ "+lyrics[1].strip('\n')+" ------"
                        new_content_temp += title + "\n"

                        lyrics = lyrics[2:(len(lyrics)-5)]

                        for line in lyrics:
                            # print(empty_line_conut)

                            if line == '\n':
                                empty_line_conut += 1
                                continue
                            else:
                                #find all non-lyrics text
                                if empty_line_conut >= 2:
                                    empty_line_conut = 0
                                    if re.search(r':$',line):
                                        singer = "--- "+line.strip('\n').strip(':')+" ---"
                                        new_content_temp += singer + "\n"

                                    elif re.search(r'(^\[.+)\]$',line):
                                        singer = "--- "+line.strip('\n').replace("[","").replace("]","")+" ---"
                                        new_content_temp += singer + "\n"

                                    elif re.search(r'^[A-Z\s.&,:]+$',line):

                                        singer = "--- "+line.strip('\n')+" ---"
                                        new_content_temp += singer + "\n"

                                    elif re.search(r'Instrumental',line):

                                        singer = "--- Instrumental ---"
                                        new_content_temp += singer + "\n"
                                        
                                    else:
                                        singer = "--- Unknown ---"
                                        new_content_temp += singer + "\n"
                                        new_content_temp +=  line

                                elif re.search(r'^\(.+\)$',line):
                                    empty_line_conut = 0
                                else:

                                    empty_line_conut = 0
                                    line = re.sub(r'"',"",line)

                                    new_content_temp +=  line

                        new_content_temp +=  '------ fin ------' + "\n"

                        cleaned_file.write(new_content_temp)

musical_url_cleaned_list = []

musical_list_path = "data/raw_data_scraped/musical_list.csv"

with open(musical_list_path, newline='') as csv_file:
 
    #get csv content to read the url
    content = csv.reader(csv_file, delimiter='\t', quotechar='"')
    next(content)

    for row in content:
        musical_url_cleaned_list.append(row[3])

for dir_name in musical_url_cleaned_list: 

    original_file_path =  "data/raw_data_scraped/musicals/"+dir_name+"/lyrics"
    target_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/lyrics"

    load_text_documents(original_file_path, target_file_path)