#!/bin/env python3

"""
this script is to scrape all the videoids of a youtube playlist
"""


import requests
from bs4 import BeautifulSoup
import json
import re

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


url = "https://www.youtube.com/playlist?list=PL285ATFsHGY-xqJX-f9OxpYpiMmCjJCZx"
page = requests.get(url)


def inspect_all():
    soup = BeautifulSoup(page.content, 'html.parser')
    for idx, i in enumerate(soup.find_all('script')):
        print(i)
        print(idx)
        input('break')

def inspect_keyword(keyword):
    soup = BeautifulSoup(page.content, 'html.parser')
    for idx, i in enumerate(soup.find_all('script')):
        if keyword in str(i):
            process(str(i))
            print(idx)
            input('break')


def process(string):
    pattern = r"window.*;"
    for i in re.findall(pattern, string):
        result = re.search(r" {.*};$",i)
        obj = json.loads(result.group(0)[:-1][1:])

        videoids = json_extract(obj, "videoId")
        #print(set(videoids))
        for vid in set(videoids):
            print("https://www.youtube.com/watch?v={}".format(vid))


        exit()


inspect_keyword('window["ytInitialData"]')




