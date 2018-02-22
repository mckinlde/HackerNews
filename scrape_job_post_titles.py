## This script scrapes the text of all job postings

from time import sleep
from bs4 import BeautifulSoup
import requests
import re

## First the basics, we need to:
## - get soup from a url; retrieve()
## - get strings of job posting titles; get_titles()
## - get link to next page; get_more()


def retrieve(url: str):
    """retrieves content at the specified url"""
    print("*", url)
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r=requests.get(url, headers=header, verify=False, timeout=5)
    sleep(1)
    soup = BeautifulSoup(r.text, "lxml")

    return soup


def get_titles(soup: BeautifulSoup):
    titles = []
    for _ in soup.find_all("a", class_="storylink"):
        titles.append(_.text)
    return titles


testSoup = retrieve('https://news.ycombinator.com/jobs')
print(get_titles(testSoup))


def get_more(soup: BeautifulSoup):
    more = soup.find("a", class_="morelink")
    return more.get('href')


print(get_more(testSoup))


## Okay, really what I'm interested in is counting the number of times a word appears

def wordCount(string_list: []):
    wordCount = {}
    for _ in string_list:
        for word in re.split('\s', _):  # split with whitespace
            try:
                wordCount[word] += 1
            except KeyError:
                wordCount[word] = 1
    return wordCount


print(wordCount(get_titles(testSoup)))


