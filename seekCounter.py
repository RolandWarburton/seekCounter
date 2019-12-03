import sys
import math
import concurrent.futures
import requests
import threading
import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict 
import include.job

TGREEN =  '\033[32m'
TWHITE = '\033[37m'
TRED = '\033[91m'

f = open('a.txt', 'w')

def GetPageNumber(jobNum):
    return math.floor(jobNum / 22)

def GetJobIDs(content):
    jobIDs = re.findall(r"job/[\d]{8}", str(content))
    jobIDs = re.findall(r'\d+', str(jobIDs))
    jobIDs = list(OrderedDict.fromkeys(jobIDs)) 
    return jobIDs

def threadTest(jobID, languages):
    posts = []
    soup = BeautifulSoup(download_site("https://www.seek.com.au/job/" + str(jobID)), "lxml")
    for language in languages:
        anchor = soup.find(['p', 'li', 'span', 'strong'], text=re.compile(re.escape(language), re.IGNORECASE))
        if anchor:
            # print("found " + str(language) + " in " + str(jobID))
            posts.append(str(language))
    if posts: print(str(posts) + jobID)
    return posts

def download_site(url):
    requestHTTP = requests.get(url).content
    return requestHTTP

def UpdateTotalJobs(url):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    return int(' '.join(soup.find("strong", attrs={"data-automation":True})).replace(',', ''))


def main():
    baseURL = "https://www.seek.com.au/jobs-in-information-communication-technology/in-Melbourne-CBD-&-Inner-Suburbs-Melbourne-VIC"
    languages = ["javascript", "node", "c#", "css", "html", "Manager"]
    jobIDs = []
    posts = []
    pageNumber = 1

    totalPages = int(input(TRED + "Enter number of pages: " + TWHITE))

    while pageNumber < totalPages+1:
        print(TGREEN + "Page Number " + str(pageNumber) + TWHITE)
        url = baseURL + "?page=" + str(pageNumber)
        content = requests.get(url).content
        jobIDs = GetJobIDs(content)
        with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
            for jID in jobIDs:
                future = executor.submit(threadTest, jID, languages)
                posts.extend(future.result())
            pass
        pageNumber += 1

    # print(posts)        
    print("==============================")
    print("RESULTS")
    for language in languages:
        print(str(language) + ": " + str(posts.count(language)))
    print("==============================")

    f.close()
if __name__ == "__main__":
    main()

