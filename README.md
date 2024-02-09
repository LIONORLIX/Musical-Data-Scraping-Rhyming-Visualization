# Musical-Data-Scraping-Rhyming-Visualization

This is the CCI_NLP_23_24 mini-project "Broadway Musical Lyrics Dataset Construction and Rhyming Schemes Visualization". 

The project mainly includes 8 directories and a HTML file, referring to 4 parts of the code. 

## Part 1: Web Scraping, NLP and Visualization

The first part is code for web scraping, NLP and visualization, which includes the directories and files below:

- step1_web_scrape
  - step11_musical_list_scrape.py
  - step12_single_musical_info_scrape.py
  - step13_musical_song_lyrics_scrape.py
- step2_clean_dataset
  - step21_clean_dataset.py
- step3_convert_to_rhyme
  - step31_collect_last_word_of_each_sentence.py
  - step32_convert_to_rhyme_cmudict.py
- step4_deep_clean
  - step41_update_none.py
  - step42_guess_pron.py
- step5_rhyme_visualization
  - step_51_draw_heatmap.py

Just follow the index at the beginning of the directory and the Python file name and run all the code. You can go through the entire process of data scraping (step 1), data cleaning (step 2), pronunciation conversion (step 3), deep data cleaning (step 4), and rhyming schemes visualization image generation (step 5). 

## Part 2: Dataset (Output of Part 1)

The second part is the raw data scraped from https://www.allmusicals.com and the output of data cleaning and pronunciation conversion. Images of visualization are also saved in this part. The entire part 2 is located in the directory "data":

- data

  - raw_data_scraped
    - musical_list.csv
    - musicals

  - cleaned_dataset

    - musical_list.csv

    - musicals

      Each subdirectory in musicals has data:

      ​	last_words: lyrics TXT file of each song

      ​	lyrics: last_words TXT file of each song

      ​	rhyming_schemes: rhyming_schemespronunciationTXT file of each song

      ​	patterns: visualization images of each song

      ​	rhyming_pattern.jpg: overview of visualization

## Part 3: Web Interface for Visualization

The third part only includes the HTML file "interface.html".

For proper use of the web interface, it is necessary to open interface.html after placing the entire project on the server. My recommendation is to use Live Server in Visual Studio Code.

Originally, I wanted to deploy the interface page on GitHub using github-page. However, I met some issues with retrieving the correct file path. 

This web interface can be successfully run in localhost. Here is a screenshot:

![Screenshot 2023-12-07 at 20.46.38](readme/Screenshot%202023-12-07%20at%2020.46.38.png)

## Part 4: Debug and Evaluation

The last part contains some records of refining my project. Directory "debug" helped with debugging. Directory "evaluation" helped me with evaluating the result of data cleaning.

