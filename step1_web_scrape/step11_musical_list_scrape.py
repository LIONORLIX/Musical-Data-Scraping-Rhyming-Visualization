#
# Reference 
# https://docs.python.org/3/library/csv.html
# https://blog.csdn.net/lwgkzl/article/details/82147474
# https://segmentfault.com/q/1010000043094655
#

# code of web-scraping is writen besed on example of Week5 course notebook
import csv
import re
import requests
from bs4 import BeautifulSoup

def extract_musical_list(musical_name_list, musical_year_list, musical_url_list,musical_url_cleaned_list,letter):
    # get the url of title list of musicals
    target_url = f'https://www.allmusicals.com/{letter}.htm'
    
    # Make a request to the wikipdia server and check to see we get a response
    response = requests.get(target_url)
    if response.status_code != 200:
        return "Failed to retrieve the page."

    # Use beatiful soup to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the text from the main body using this specific tag
    main_content = soup.select('div.sym-album-list')
    # If we have retrieve content
    if main_content:
        # Find each paragraph
        for title in main_content[0].find_all('a', href=True):
            # And add that paragraph to our main_body_text string

            title_text=title.get_text()
            title_text=re.sub(r', The Lyrics$','',title_text)
            title_text=re.sub(r' Lyrics$','',title_text)
            
            title_url=title['href']
            title_url_cleaned=title_url
            title_url_cleaned=re.sub(fr'^/{letter}/','',title_url_cleaned)
            title_url_cleaned=re.sub(r'\.htm$','',title_url_cleaned)

            musical_name_list.append(title_text)
            musical_url_list.append(title_url)
            musical_url_cleaned_list.append(title_url_cleaned)
            
            print(title_url_cleaned)
            
        for year in main_content[0].find_all('span'):
            # And add that paragraph to our main_body_text string
            musical_year_list.append(year.get_text())

letter_list = []
for letter in range(97,122+1):
    print(chr(letter))
    letter_list.append(chr(letter))

musical_name_list = []
musical_year_list = []
musical_url_list = []
musical_url_cleaned_list = []

csv_path = "data/raw_data_scraped/musical_list.csv"
with open(csv_path,'w') as csv_file:
    csv_write = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_head = ["musical_name", "year","url","url_cleaned"]
    csv_write.writerow(csv_head)

for letter in letter_list:
    extract_musical_list(musical_name_list, musical_year_list,musical_url_list,musical_url_cleaned_list, letter)

for i in range(len(musical_name_list)):
    with open(csv_path,'a+', newline='') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([musical_name_list[i],musical_year_list[i],musical_url_list[i],musical_url_cleaned_list[i]])