import pronouncing
import os
import re
import csv
from pathlib import Path

def collect_last_words_of_each_sentence(original_file_path, target_file_path):

    # Find the files in the directory

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

                    with open(target_file_path+"/"+file, "w") as new_file:

                        lyrics = f.readlines()

                        for line in lyrics:
                            if re.search(r'---$',line):
                                continue
                            else:
                                
                                line = line.strip("\n")
                                line = re.sub(r"^[\^’\'\"“\-]+|[、.…’\s\'»‘\/\\\-\~]+$", "", line)
                                line.replace("’","'")
                                line.replace("‘","")

                                line = line.split()
                                
                                if line == []:
                                    line.append("")
                                
                                last_word = line[len(line)-1].lower()
                                # print(last_word)

                                if last_word == "1":
                                    last_word = "one"
                                elif last_word == "2":
                                    last_word = "two"
                                elif last_word == "3":
                                    last_word = "three"
                                elif last_word == "4":
                                    last_word = "four"
                                elif last_word == "5":
                                    last_word = "five"
                                elif last_word == "6":
                                    last_word = "six"
                                elif last_word == "7":
                                    last_word = "seven"
                                elif last_word == "8":
                                    last_word = "eight"
                                elif last_word == "9":
                                    last_word = "nine"
                                
                                last_word_cleaned = re.sub(r'[\),;:.?!"\}\{\[\]]+', "", last_word)
                                
                                print(last_word_cleaned)
                                
                                new_content_temp += last_word_cleaned + '\n'

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

    original_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/lyrics"
    target_file_path =  "data/cleaned_dataset/musicals/"+dir_name+"/last_words"

    collect_last_words_of_each_sentence(original_file_path, target_file_path)