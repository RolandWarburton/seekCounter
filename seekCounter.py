import concurrent.futures
import requests
import threading
from multiprocessing import cpu_count
from functools import partial
import re
from bs4 import BeautifulSoup
from collections import OrderedDict
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

# Extract Job ids from html
def ExtractJobIDs(HTMLcontent):
    jobIDs = re.findall(r"job/[\d]{8}", str(HTMLcontent))
    jobIDs = re.findall(r'\d+', str(jobIDs))
    jobIDs = list(OrderedDict.fromkeys(jobIDs)) 
    return jobIDs

# look for languages. returns a list of languages
def SearchKeywords(jobID, keyWords):
    posts = []
    soup = BeautifulSoup(downloadSite("https://www.seek.com.au/job/" + str(jobID)).content, "lxml")
    for language in keyWords:
        anchor = soup.find(['p', 'li', 'span', 'strong'], text=re.compile(re.escape(language), re.IGNORECASE))
        if anchor:
            # print("found " + str(language) + " in " + str(jobID))
            posts.append(str(language))
    return posts

# Return every job ID for a page
def GetJobIDs(pageNumber, baseURL):
    site = downloadSite(baseURL + "/?page=" + str(pageNumber))
    jobIDs = ExtractJobIDs(site.content)
    return jobIDs

def downloadSite(url):
    requestHTTP = requests.get(url)
    # print(f"download {requestHTTP}")
    return requestHTTP

def UpdateTotalJobs(url):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    return int(' '.join(soup.find("strong", attrs={"data-automation":True})).replace(',', ''))

def main():
    
    baseURL = "https://www.seek.com.au/jobs-in-information-communication-technology/in-Melbourne-CBD-&-Inner-Suburbs-Melbourne-VIC"
    # languages = ["javascript", "node", "c#", "css", "html"]
    languages = ["1 year", "2+ years", "3+ years", "4+ years", "5+ years", "6+ years"]
    jobIDs = []
    posts = []

    # totalPages = int(input(TRED + "Enter number of pages: " + TWHITE))
    totalPages = 100
    start = time.time()

    # get a batch of jobIDs from multiple pages
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(partial(GetJobIDs, baseURL = baseURL), range(totalPages))
        jobIDs.extend(result)

    # process all the jobs
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # page is a list of job IDs on a single page
        for page in jobIDs:
            result = executor.map(partial(SearchKeywords, languages=languages), page)
            for languageArray in result:
                posts.extend(languageArray)

    timeTaken = time.time()-start 
    print("==============================")
    print("RESULTS")
    for language in languages:
        print(str(language) + ": " + str(posts.count(language)))
    print(f"finished in {timeTaken} seconds")
    print("==============================")

if __name__ == "__main__":
    main()

