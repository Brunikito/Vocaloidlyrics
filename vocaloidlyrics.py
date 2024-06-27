import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import os

# text cleaning
def clean(element):
    return re.sub(r'\u3000', ' ', element.text.strip())

# get the title in all the avaiable languages
def gettitles():
    titles = []
    split1 = (clean(soup.find('table', {'align': 'center'}).find_all('tr')[2])).split('Romaji: ')
    titles.append(split1[0])
    if len(split1) == 2:
        split2 = split1[1].split('Official English: ')
        titles.append(split2[0])
        if len(split2) == 2:
            titles.append(split2[1])
    return titles

# clear the terminal
def clearterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# insert page url first try
clearterminal()
print('Insert the url of the page (from vocaloidlyrics.fandom)')
url = input()
urlin = True
if url[:39] == "https://vocaloidlyrics.fandom.com/wiki/"[:39]:
    if requests.get(url).status_code < 300:
        urlin = False

# insert page url subsequent tries
while urlin:
    clearterminal()
    print('Please insert a valid url')
    url = input()
    if url[:39] == "https://vocaloidlyrics.fandom.com/wiki/"[:39]:
        if requests.get(url).status_code < 300:
            urlin = False

# getting the html
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

# getting the titles
titles = gettitles()

# getting the avaiable languages
Table = soup.find('table', {'style':'width:100%'})
languages = [title.text.strip() for title in Table.find_all('b')]

# getting the lyrics in all avaiable languages
Body = Table.find_all('tr')[(len(languages)-1):]
lines = []
for line in Body:
    if line.find('td', {'class': 'merged bold italic'}) == None:
        if line.find('br') == None:
            lines.append([clean(line.find_all('td')[x]) for x in range(len(languages))])
        else:
            lines.append(['' for x in range(len(languages))])
    else:
        lines.append([clean(line.find('td', {'class': 'merged bold italic'})) for x in range(len(languages))])
lyrics = np.array(lines)

# user interface
language = True
have_lang = True
while language:
    clearterminal()

    # error message
    if not have_lang:
        print("Sorry, but we don't have that language yet", '\n')
    
    # print titles
    print('Original title: ', titles[0])
    if len(titles) >= 2:
        print('Romaji: ', titles[1])
    if len(titles) == 3:
        print('Official English: ', titles[2])
    print()

    # insert language
    print('Which language would you like?[jp/rmj/en]')
    lang = input()

    # Japanese
    if lang == 'jp':
        clearterminal()
        if len(languages) >= 1:
            language = False
            print(titles[0], '\n')
            for line in lyrics:
                print(line[0])
        else:
            have_lang = False
        print('\n')
    
    # Romaji
    elif lang == 'rmj':
        clearterminal()
        if len(languages) >= 2:
            print(titles[1], '\n') if len(titles) >= 2 else print(titles[0], '\n')
            language = False
            for line in lyrics:
                print(line[1])
        else:
            have_lang = False
        print('\n')

    # English
    elif lang == 'en':
        clearterminal()
        if len(languages) >= 3:
            print(titles[2], '\n') if len(titles) == 3 else print(titles[0], '\n')
            language = False
            for line in lyrics:
                print(line[2])
        else:
            have_lang = False
        print('\n')