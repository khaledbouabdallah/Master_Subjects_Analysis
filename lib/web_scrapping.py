from bs4 import BeautifulSoup
import re
import os
import json
import pandas as pd

DATA_PATH = "raw_data/"

articles = []
for file_name in os.listdir(DATA_PATH):  # Iterate over the HTML raw files
    with open(DATA_PATH + file_name, "r", encoding='utf-8') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    # Get table that contains the information we are interested in
    table = soup.find("table", {"id": "filterrific_results"})
    # get tags that contain usefull information
    rows = [content for content in table.contents if content.name]
    # split the tags per teacher
    teachers = []
    for i in range(0, len(rows), 3):
        teacher = [rows[i], rows[i + 2]]
        teachers.append(teacher)
    for teacher in teachers:
        # Pulling name and grade of each teacher:  'Enseignant NAME (GRADE)'
        text = teacher[0].th.text
        text = re.split(pattern='Enseignant', string=text)[1][2:]
        text = re.split(pattern='\(', string=text)
        name = text[0].strip()
        grade = text[1][:-1]
        # splitting the data per article
        articles_teacher = teacher[1].find_all('tr')
        print(f'{name}:{len(articles_teacher)}')
        # populating  articles information into a dictionary
        for article in articles_teacher:
            infos = article.find_all('td')
            date, time, _ = re.split(pattern=' ', string=infos[9].text)
            article_dict = {
                'Id': infos[0].text,
                'Title': infos[1].text.strip(),
                'Author': name,
                'Grade': grade,
                'Taken': bool(infos[2].text.strip()),
                'Priority 1': infos[3].text.strip(),
                'Priority 2': infos[4].text.strip(),
                'Priority 3': infos[5].text.strip(),
                'Priority 4': infos[6].text.strip(),
                'Priority 5': infos[7].text.strip(),
                'Date': date,
                'Time': time,
            }
            articles.append(article_dict)

# Saving in JSON
with open('dataset/result.json', 'w') as fp:
    json.dump(articles, fp)

# Saving in CSV
df = pd.read_json(r'dataset/result.json')
df.to_csv(r'dataset/subjects_master_2022.csv', index=None)
