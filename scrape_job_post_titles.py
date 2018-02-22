## This script scrapes the text of all job postings

from time import sleep
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

## First the basics, we need to:
## - get soup from a url; retrieve()
## - get strings of job posting titles; get_titles()
## - get link to next page; get_more()


def retrieve(url: str):
    """retrieves content at the specified url"""
    print("*", url)
    header = {'User-Agent': 'Mozilla/5.0'}
                            #' (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r=requests.get(url, headers=header, verify=False, timeout=5)
    sleep(3) ## We really gotta sleep to stay under HN's radar
    soup = BeautifulSoup(r.text, "lxml")

    return soup


def get_titles(soup: BeautifulSoup):
    titles = []
    for _ in soup.find_all("a", class_="storylink"):
        titles.append(_.text)
    return titles


testSoup = retrieve('https://news.ycombinator.com/jobs')
sleep(1)
print(get_titles(testSoup))


def get_more(soup: BeautifulSoup):
    more = soup.find("a", class_="morelink")
    try:
        link = more.get('href')
    except AttributeError:
        return None
    return link


print(get_more(testSoup))


## Okay, really what I'm interested in is counting the number of times a word appears

def wordCount(string_list: [], currentCount: {}):
    for _ in string_list:
        for word in re.split('\s', _):  # split with whitespace
            try:
                currentCount[word] += 1
            except KeyError:
                currentCount[word] = 1
    return currentCount


print(wordCount(get_titles(testSoup), {}))

print('Done Testing')


## Rock on, now let's write a loop that'll update our dict for every new page

initial_link = 'https://news.ycombinator.com/jobs'
soup = retrieve(initial_link)
sleep(1)
next_link = get_more(soup)
words = {}
pageCounter = 0
while next_link is not None:
    newTitles = get_titles(soup)
    wordCount(newTitles, words)
    soup = retrieve('https://news.ycombinator.com/' + next_link)
    next_link = get_more(soup)
    pageCounter += 1
    print(pageCounter)
    print(', ' + next_link)

## Okay, at this point I theoretically have a dict of words and their counts
## HN is blocking my requests so I can't test, but assuming it works I need to put that in
## a DB for it to be useful

connection = mysql.connector.connect(host="localhost", port=3306, user="semdemo", passwd="demo", db="semdemo")
db = connection.cursor(prepared=True)

db.execute("""
        CREATE TABLE IF NOT EXISTS HN_JOBS (
            word VARCHAR(256) NOT NULL PRIMARY KEY,
            count int(20) NOT NULL DEFAULT 0
        )""")
connection.commit()

for k, v in words.items():
    db.execute("insert into HN_JOBS(word, count) values(?,?)", [k, v])
    connection.commit()
