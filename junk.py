             # pass
                # future = executor.submit(threadTest, jobPageURL)
                # return_value =  future.result()
                # for val in return_value:
                #     posts.append(val)
    
    # for _ in range(1):
    #     url = baseURL + "?page=" + str(pageNumber)

    # for thread in threads:
    #     thread.join()
    
    

    # if input(TRED + "custom number of pages (y/n)") == 'y':
    #     customTotal = True
    #     totalJobs = int(input("total pages: " + TWHITE))
    #     totalJobs *= itemsPerPage

    # while jobNumber < totalJobs:
    #     # update the url
    #     url = baseURL + "?page=" + str(pageNumber)

    #     # get the content from this url
    #     content = requests.get(url).content
    #     soup = BeautifulSoup(content, "lxml")

    #     # get a list of job IDs on this page
    #     jobIDs = GetJobIDs(content)

    #     # update the number of jobs in case it changed
    #     if not customTotal:
    #         totalJobs = int(' '.join(soup.find("strong", attrs={"data-automation":True})).replace(',', ''))

    #     # update the page number
    #     pageNumber += 1
    #     jobNumber += len(jobIDs)

    #     print(TGREEN + "Page Number " + str(pageNumber))
    #     print(str(totalJobs) + " jobs left")
    #     print("found " + str(len(jobIDs)) + " jobs on this page" + TWHITE)

        