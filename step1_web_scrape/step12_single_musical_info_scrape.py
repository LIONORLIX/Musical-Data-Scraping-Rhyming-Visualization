#
# Reference
# https://docs.python.org/3/library/csv.html
# https://linuxhint.com/skip-header-row-csv-python/
# https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories
#

# code of web-scraping is writen besed on example of Week5 course notebook
import csv
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def extract_single_musical_info(url,song_name_list,song_url_list):
    # get the url of title list of musicals
    target_url = f'https://www.allmusicals.com{url}'
    
    # Make a request to the wikipdia server and check to see we get a response
    response = requests.get(target_url)
    if response.status_code != 200:
        return "Failed to retrieve the page."

    # Use beatiful soup to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the text from the main body using this specific tag
    main_content = soup.select('section.lyrics-list')
    # If we have retrieve content
    if main_content:
        # Find each paragraph
        for title in main_content[0].find_all('a', href=True):
            # And add that paragraph to our main_body_text string
            title_text=title.get_text().strip()
            title_url=title['href']
            if title_text !="":
                song_name_list.append(title_text)
                song_url_list.append(title_url)
            print(title_url)

def extract_musical_review(url,txt_path):
    # get the url of title list of musicals
    target_url = f'https://www.allmusicals.com/lyrics/{url}/review.htm'
    
    # Make a request to the wikipdia server and check to see we get a response
    response = requests.get(target_url)
    if response.status_code != 200:
        return "Failed to retrieve the page."

    # Use beatiful soup to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    main_body_text = ""
    # Get the text from the main body using this specific tag
    main_content = soup.select('div#page')
    # If we have retrieve content
    if main_content:
        # Find each paragraph
        with open(txt_path, "w") as txt_file:
            for paragraph in main_content[0]:
                main_body_text += paragraph.get_text().strip()
                #Add a new line after each paragraph
                main_body_text += '\n'
            txt_file.write(main_body_text)




musical_url_cleaned_list = []
musical_url_list = []

musical_list_path = "data/musical_list_temp.csv"
# musical_list_path = "data/raw_data_scraped/musical_list.csv"
with open(musical_list_path, newline='') as csv_file:
   
    
    #get csv content to read the url
    content = csv.reader(csv_file, delimiter='\t', quotechar='"')
    next(content) 
    for row in content:
        musical_url_list.append(row[2])
        musical_url_cleaned_list.append(row[3])

for i in range(len(musical_url_list)): 

    song_name_list = []
    song_url_list = []

    Path("data/raw_data_scraped/musicals/"+musical_url_cleaned_list[i]).mkdir(parents=True, exist_ok=True)
    csv_path = "data/raw_data_scraped/musicals/"+musical_url_cleaned_list[i]+"/song_list.csv"
    with open(csv_path,'w') as csv_file:
        csv_write = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_head = ["song-name", "url"]
        csv_write.writerow(csv_head)

    txt_path = "data/raw_data_scraped/musicals/"+musical_url_cleaned_list[i]+"/review.txt"
    extract_musical_review(musical_url_cleaned_list[i],txt_path)

    extract_single_musical_info(musical_url_list[i],song_name_list,song_url_list)

    for j in range(len(song_name_list)):
        with open(csv_path,'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([song_name_list[j],song_url_list[j]])