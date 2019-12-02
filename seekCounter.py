import sys
import math
import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict 
import include.job

TGREEN =  '\033[32m'
TWHITE = '\033[37m'
TRED = '\033[91m'

def GetPageNumber(jobNum):
    return math.floor(jobNum / 22)

def GetJobIDs(content):
    jobIDs = re.findall(r"job/[\d]{8}", str(content))
    jobIDs = re.findall(r'\d+', str(jobIDs))
    jobIDs = list(OrderedDict.fromkeys(jobIDs)) 
    return jobIDs

def main():
    baseURL = "https://www.seek.com.au/jobs-in-information-communication-technology/in-Melbourne-CBD-&-Inner-Suburbs-Melbourne-VIC"
    languages = ["javascript", "node", "c#", "css", "html"]
    jobIDs = []
    posts = []
    itemsPerPage = 22
    pageNumber = 0
    jobNumber = 0
    totalJobs = 1
    customTotal = False
    
    if input(TRED + "custom number of pages (y/n)"):
        customTotal = True
        totalJobs = int(input("total pages: " + TWHITE))
        totalJobs *= itemsPerPage

    while jobNumber < totalJobs:
        # update the url
        url = baseURL + "?page=" + str(pageNumber)

        # get the content from this url
        content = requests.get(url).content
        soup = BeautifulSoup(content, "lxml")

        # get a list of job IDs on this page
        jobIDs = GetJobIDs(content)

        # update the number of jobs in case it changed
        if not customTotal:
            totalJobs = int(' '.join(soup.find("strong", attrs={"data-automation":True})).replace(',', ''))

        # update the page number
        pageNumber += 1
        jobNumber += len(jobIDs)

        print(TGREEN + "Page Number " + str(pageNumber))
        print(str(totalJobs) + " jobs left")
        print("found " + str(len(jobIDs)) + " jobs on this page" + TWHITE)

        for jobID in jobIDs:
            request = requests.get("https://www.seek.com.au/job/" + str(jobID))
            temp = BeautifulSoup(request.text, "lxml")
            for language in languages:
                # print("searching for " + str(language) + " jobs in " + str(jobID))
                regex = re.escape(language)
                anchor = temp.find(['p', 'li', 'span', 'strong'], text=re.compile(regex, re.IGNORECASE))
                if anchor:
                    print("found " + str(language) + " in " + str(jobID))
                    posts.append(str(language))
    
    print("==============================")
    print("RESULTS")
    for language in languages:
        print(str(language) + ": " + str(posts.count(language)))
    print("==============================")

if __name__ == "__main__":
    main()

