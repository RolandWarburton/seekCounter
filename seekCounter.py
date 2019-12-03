import sys
import math
import concurrent.futures
import requests
import threading
from multiprocessing import cpu_count
from itertools import product
from itertools import repeat
from functools import partial
import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict 
import include.job
import time

# ProcessPoolExecutor runs each of your workers in its own separate child process.
# ThreadPoolExecutor runs each of your workers in separate threads within the main process.

# I/O bound = ThreadPoolExecutor
# avoid GIL (Global Interpreter Lock) = ProcessPoolExecutor

# what is GIL: GIL ensures that your program is 'thread safe'. 
# GIL allows exactly one thread to execute at a time, even for multi-core programs.

TGREEN =  '\033[32m'
TWHITE = '\033[37m'
TRED = '\033[91m'

f = open('a.txt', 'w')

def GetPageNumber(jobNum):
    return math.floor(jobNum / 22)

# Extract Job ids from html
def ExtractJobIDs(content):
    jobIDs = re.findall(r"job/[\d]{8}", str(content))
    jobIDs = re.findall(r'\d+', str(jobIDs))
    jobIDs = list(OrderedDict.fromkeys(jobIDs)) 
    return jobIDs

def SearchKeywords(jobID, languages):
    posts = []
    soup = BeautifulSoup(downloadSite("https://www.seek.com.au/job/" + str(jobID)).content, "lxml")
    for language in languages:
        anchor = soup.find(['p', 'li', 'span', 'strong'], text=re.compile(re.escape(language), re.IGNORECASE))
        if anchor:
            # print("found " + str(language) + " in " + str(jobID))
            posts.append(str(language))
    if posts: print(str(posts) + jobID)
    return posts

# Return EVERY job ID. use with caution
def GetJobIDs(page):
    return NotImplemented

def downloadSite(url):
    requestHTTP = requests.get(url)
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

    # totalPages = int(input(TRED + "Enter number of pages: " + TWHITE))
    totalPages = 2
    start = time.time()

    # supposed to be getting a batch of jobIDs from different pages
    # for pageNum in range(totalPages):
    #     GetJobIDs()
    #     jobIDs.extend()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     result = executor.map(partial(ExtractJobIDs), baseURL + str(range(totalPages)))
    #     # print(result)
    #     # posts.extend(result)

    while pageNumber < totalPages+1:
        print(TGREEN + "Page Number " + str(pageNumber) + TWHITE)
        url = baseURL + "?page=" + str(pageNumber)
        content = requests.get(url).content
        jobIDs = ExtractJobIDs(content)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            result = executor.map(partial(SearchKeywords, languages=languages), jobIDs)
            posts.extend(result)
        pageNumber += 1

    timeTaken = time.time()-start 
    print("==============================")
    print("RESULTS")
    for language in languages:
        print(str(language) + ": " + str(posts.count(language)))
    print(f"finished in {timeTaken} seconds")
    print("==============================")
    

    f.close()
if __name__ == "__main__":
    main()

