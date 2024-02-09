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
from nltk.corpus import words 
from nltk.metrics.distance  import edit_distance 
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

correct_words = words.words()

nltk.download('cmudict')

def get_pron(word):
    return cmudict.dict().get(word)

def reduce_lengthening_and_correct(raw_word):

    if raw_word == "" or re.search("[0-9]+",raw_word):
        return raw_word
    else:
        pattern = re.compile(r"(.)\1{2,}")
        pattern.sub(r"\1\1", raw_word)

        if len(raw_word)<=0:
            return raw_word

        temp = [(edit_distance(raw_word, w),w) for w in correct_words if w[0]==raw_word[0]] 

        if len(temp)<=0:
            return raw_word

        return sorted(temp, key = lambda val:val[0])[0][1]


def lemmatization(raw_word):
   return lemmatizer.lemmatize(raw_word.lower())
       

def convert_to_rhyme(original_file_path, target_file_path):

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
                                last_word = words[count].strip("\n")
                                pron_list = None
                                print(last_word)
                                
                                if get_pron(last_word)==None:


                                    if "-" in last_word:
                                        temp_list = last_word.split("-")
                                        # print(temp_list)
                                        if get_pron(temp_list[len(temp_list)-1]) == None:
                                            print()

                                            if get_pron("".join(temp_list)) != None:
                                                pron_list = get_pron("".join(temp_list))
                                            else:
                                                temp_corrected = lemmatization(reduce_lengthening_and_correct(last_word))
                                                if (get_pron(temp_corrected)) != None:
                                                    pron_list = get_pron(temp_corrected)
                                                    print(temp_corrected)
                                        else:
                                            pron_list = get_pron(temp_list[1])
                                    
                                    elif "^" in last_word:
                                    
                                        temp_list = last_word.split("^")
                                        # print(temp_list)
                                        if get_pron(temp_list[len(temp_list)-1]) == None:

                                            if get_pron("".join(temp_list)) != None:
                                                pron_list = get_pron("".join(temp_list))
                                            else:
                                                temp_corrected = lemmatization(reduce_lengthening_and_correct(last_word))
                                                if (get_pron(temp_corrected)) != None:
                                                    pron_list = get_pron(temp_corrected)
                                                    print(temp_corrected)
                                        else:
                                            pron_list = get_pron(temp_list[1])
                                    
                                    elif "/" in last_word:

                                        temp_list = last_word.split("/")
                                        # print(temp_list)
                                        if get_pron(temp_list[len(temp_list)-1]) == None:

                                            if get_pron("".join(temp_list)) != None:
                                                pron_list = get_pron("".join(temp_list))
                                            else:
                                                temp_corrected = lemmatization(reduce_lengthening_and_correct(last_word))
                                                if (get_pron(temp_corrected)) != None:
                                                    pron_list = get_pron(temp_corrected)
                                                    print(temp_corrected)
                                        else:
                                            pron_list = get_pron(temp_list[1])

                                    else:
                                        temp_corrected = lemmatization(reduce_lengthening_and_correct(last_word))
                                        if (get_pron(temp_corrected)) != None:
                                            pron_list = get_pron(temp_corrected)
                                            print(temp_corrected)
                                    
                                else:
                                    pron_list = get_pron(last_word)
                                
                                if pron_list==None:
                                    new_content_temp += "---"+last_word+"---"
                                    
                                else:
                                    for item in pron_list[0]:
                                        new_content_temp += item + " "

                                print(pron_list)
                                
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

    convert_to_rhyme(original_file_path, target_file_path)     