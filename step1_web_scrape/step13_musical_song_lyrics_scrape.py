# code of web-scraping is writen besed on example of Week5 course notebook
import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def extract_lyrics(url,file_path):
    
    # Make a request to the wikipdia server and check to see we get a response
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the page."
    
    # Use beatiful soup to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Empty string to put our content
    main_body_text = ""
    # Get the text from the main body using this specific tag
    main_content = soup.select('div#page')
    
    # If we have retrieve content
    if main_content:
        with open(file_path, "w") as myfile:
        
            # Find each paragraph
            for paragraph in main_content[0]:
                # And add that paragraph to our main_body_text string
                main_body_text += paragraph.get_text().strip()
                #Add a new line after each paragraph
                main_body_text += '\n'

            myfile.write(main_body_text)


musical_url_cleaned_list = []

musical_list_path = "data/musical_list_temp.csv"
# musical_list_path = "data/raw_data_scraped/musical_list.csv"
with open(musical_list_path, newline='') as csv_file:
 
    #get csv content to read the url
    content = csv.reader(csv_file, delimiter='\t', quotechar='"')
    next(content)

    for row in content:
        musical_url_cleaned_list.append(row[3])

for dir in musical_url_cleaned_list: 
    
    Path("data/raw_data_scraped/musicals/"+dir+"/lyrics").mkdir(parents=True, exist_ok=True)

    song_list_path = "data/raw_data_scraped/musicals/"+dir+"/song_list.csv"

    with open(song_list_path, newline='') as csv_file:
        #get csv content to read the url
        content = csv.reader(csv_file, delimiter='\t', quotechar='"')
        next(content)
        for row in content:
            print(dir + " - " + row[0])
            txt_path = "data/raw_data_scraped/musicals/"+dir+"/lyrics/"+row[0].lower().strip().replace("/", "OR").replace(" ", "-")+".txt"
            extract_lyrics(row[1],txt_path)

