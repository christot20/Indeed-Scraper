from bs4 import BeautifulSoup
import requests
import time
import urllib.request 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from helpers import checker, scrape_amount

PATH = "D:\Indeed-Scraper\chromedriver.exe"

def scrape(num):
    for i in range(num):
        time.sleep(4)
        pop_up = driver.find_elements(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')
        if len(pop_up) != 0:
            pop_up[0].click() #check if pop up exists and remove it if yes
            #continue
        for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]/a'): #iterates over every link
            
            tag.click()
            
            #try to add an exception handler for if it cant find an iframe to skip the link, started working on it in the commented out script under
            #so far works well, uses time.sleep to wait out the pop up
            
            #job = driver.find_element(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]')
            element = driver.find_element(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]/iframe[@title="Selected Job Details"]') #maybe make this elements instead of element and 
                                                                                                                        #do what u did for checking if there is next button (if cnditional)
            url = element.get_attribute("src")
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("div", {"class":"jobsearch-JobInfoHeader-title-container"})
            result = soup.find("div", {"id":"jobDescriptionText"})
            print("--------------------------------")
            print(title.text) #changed finding the title to using bs4 scraping the job page, commented out the moving in and out of frames, check gitub for differences

            #can prob get rid of stuff under me
            #maybe try to make this stuff above a function and call it whenever a next page button is found
            #implement next page finder and also allow user to choose how many times to go next, probably give a prompt before?
            #afterwards use the nlp library from datacamp website
            #captchas are issue, try to see if u can get around it (try out undetected chromedirver and if it doesnt work take code u pushed back here)

            # driver.switch_to.frame("vjs-container-iframe")
            # new_title = driver.find_element(By.XPATH, '//div[@class="jobsearch-JobComponent-embeddedHeader"]//h1')
            # #print(new_title.text)
            # driver.switch_to.default_content()

            print(result.text) #prints text in given url
        
        #add something here to check if next button is there, if yes, click it, if not break loop and say max pages found and dirver.quit
        next_pg = driver.find_elements(By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')
        if len(next_pg) == 0:
            break
        else:
            next_pg[0].click() #check if next button exists and click it if yes, else break the loop
            i += 1

        #add a thing here that quits if no next button is found
        #check stuff above driver switch to see what to do

        #new plan, have this whole stuff in func be in loop, make it so loops num(parameter) amount of times incluiding clicking to new page
        #if new page isnt found, break out of loop and quit the driver

    driver.quit()

if __name__ == '__main__':

    city = input("Enter name of city to conduct search (E.g. New York): ").title()
    state = input("Enter abbreviation of state to conduct search (E.g. NY): ").upper()
    job = input("Enter name of job to search up (E.g. Data Engineer): ").upper()
    user_choice = scrape_amount()

    if len(state.strip()) != 2: # checks if state given is invalid
        raise ValueError("Invalid State Received") #quit out of application/raise error
    elif checker(city, state.strip()) == False:
        raise ValueError("Location Received Invalid")

    # checker comes out false, raise value error as not real city, else do this
    city = city.replace(" ", "+") # used for formatting in url
    job = job.replace(" ", "+") # used for formatting in url

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # update to date webdriver installer
    driver.get(f"https://www.indeed.com/jobs?q={job}&l={city.upper()}%2C+{state.strip()}&radius=100") #format indeed link
    
    # page_source = driver.page_source
    # #print(page_source)
    # s = requests.Session()
    # soup = BeautifulSoup(page_source, "html.parser")

    print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city

    # for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//h2[1]/span'):
    #     print(tag.text) # gets title of that element^
    
    #print(driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//a[@target="_blank"]'))
    #print(len(driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//a[@target="_blank"]')))

    #for in in range(user choice of how far to go):

    scrape(user_choice)

        #check if there is a next button for a certian amount of times and click it
        # for i in range(user choice)
        # call scrape function using stuff above
        # if next button exists
        # click it and do stuff above again (make it a function)
        # else break


        #working for now, gets the title of each job listing from the iframe
        #try to get it to click next after going through all the iframes
        #try scraping the iframes



        #print("sus") #it prints this but stops at the second tag.click()

            #//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]//iframe[@id="vjs-container-iframe"]
        

        #find how to click each a tag

        #try to find out why selenium closes automatically
        #might be it here: https://stackoverflow.com/questions/43612340/chromedriver-closing-after-test

    
    #have selenium click on a box and bs4 scrape the section that becomes visible
    #look up how to scrape everythong from an element in bs4 and how to click something in selenium
    #probably gonna want to make this a function and recurse over it
    #(if next button clicked, load new page, call scrape function, else quit with driver.quit)

    #//div[@id="mosaic-provider-jobcards"]//a[@target="_blank"]  <-- xpath for getting to links
    #https://stackoverflow.com/questions/27006698/selenium-iterating-through-groups-of-elements   how to iterate over list of these things

    #driver.quit() be sure to use this at the very end when web scraping













# from bs4 import BeautifulSoup
# import requests
# import time
# import urllib.request 
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By

# from helpers import checker, scrape_amount

# # PATH = "D:\Indeed-Scraper\chromedriver.exe"

# def scrape(num):
#     for i in range(num):
#         pop_up = driver.find_elements(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')
#         if len(pop_up) != 0:
#             pop_up[0].click()
#             #continue
#         for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]/a'): #iterates over every link
#             # for titles in tag.find_elements(By.XPATH, './/h2/span'): #gets the title from each link, gonna want to start clikcing and scrpaing on this loop
#             #     print(titles.text)
#             #print(tag.text) # gets title of that element^

#             #for titles in tag:
#             #time.sleep(5)

#             tag.click()
#             #make something here to check if the iframe exists and do everything under me, if not continue

#             job_desc = driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]/iframe')
#             if len(job_desc) == 0:
#                 continue
#             else:
#                 job = driver.find_element(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]')
#                 element = driver.find_element(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]/iframe')

#                 url = element.get_attribute("src")
#                 html = urllib.request.urlopen(url)
#                 soup = BeautifulSoup(html, "html.parser")
#                 #title = soup.find("h1", {"class":"icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"})
#                 result = soup.find("div", {"id":"jobDescriptionText"})
#                 print("--------------------------------")
#                 #print(title.text)
#                 # print(result.text) #prints text in given url

#                 #can prob get rid of stuff under me
#                 #maybe try to make this stuff above a function and call it whenever a next page button is found
#                 #implement next page finder and also allow user to choose how many times to go next, probably give a prompt before?
#                 #afterwards use the nlp library from datacamp website
#                 #captchas are issue, try to see if u can get around it (try out undetected chromedirver and if it doesnt work take code u pushed back here)

#                 #make a function handling nlp stuff and have the body of the job description be a variable for the input
#                 #look on data camp articl for more info on nlp and how to store the words

#                 driver.switch_to.frame("vjs-container-iframe")
#                 #for words in 
#                 new_title = driver.find_element(By.XPATH, '//div[@class="jobsearch-JobComponent-embeddedHeader"]//h1')
#                 print(new_title.text)
#                 driver.switch_to.default_content()

#                 print(result.text) #prints text in given url
            
#             #add something here to check if next button is there, if yes, click it, if not break loop and say max pages found and dirver.quit
#                 next_pg = driver.find_elements(By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')
#                 if len(next_pg) == 0:
#                     break
#                 else:
#                     next_pg[0].click()
#                     i += 1

#         #add a thing here that quits if no next button is found
#         #check stuff above driver switch to see what to do

#         #new plan, have this whole stuff in func be in loop, make it so loops num(parameter) amount of times incluiding clicking to new page
#         #if new page isnt found, break out of loop and quit the driver

#     driver.quit()

# if __name__ == '__main__':

#     city = input("Enter name of city to conduct search (E.g. New York): ").title()
#     state = input("Enter abbreviation of state to conduct search (E.g. NY): ").upper()
#     job = (input("Enter name of job to search up (E.g. Data Engineer): ").upper()).replace(" ", "+")
#     user_choice = scrape_amount()

#     if len(state.strip()) != 2: # checks if state given is invalid
#         raise ValueError("Invalid State Received") #quit out of application/raise error
#     elif checker(city, state.strip()) == False:
#         raise ValueError("Location Received Invalid")

#     # checker comes out false, raise value error as not real city, else do this
#     city = city.replace(" ", "+") # used for formatting in url
#     # job = job.replace(" ", "+") # used for formatting in url

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # update to date webdriver installer
#     driver.get(f"https://www.indeed.com/jobs?q={job}&l={city.upper()}%2C+{state.strip()}&radius=100") #format indeed link
    
#     # page_source = driver.page_source
#     # #print(page_source)
#     # s = requests.Session()
#     # soup = BeautifulSoup(page_source, "html.parser")

#     print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city

#     # for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//h2[1]/span'):
#     #     print(tag.text) # gets title of that element^
    
#     #print(driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//a[@target="_blank"]'))
#     #print(len(driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//a[@target="_blank"]')))

#     #for in in range(user choice of how far to go):
#     #time.sleep(3)
#     scrape(user_choice)

#         #check if there is a next button for a certian amount of times and click it
#         # for i in range(user choice)
#         # call scrape function using stuff above
#         # if next button exists
#         # click it and do stuff above again (make it a function)
#         # else break


#         #working for now, gets the title of each job listing from the iframe
#         #try to get it to click next after going through all the iframes
#         #try scraping the iframes



#         #print("sus") #it prints this but stops at the second tag.click()

#             #//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]//iframe[@id="vjs-container-iframe"]
        

#         #find how to click each a tag

#         #try to find out why selenium closes automatically
#         #might be it here: https://stackoverflow.com/questions/43612340/chromedriver-closing-after-test

    
#     #have selenium click on a box and bs4 scrape the section that becomes visible
#     #look up how to scrape everythong from an element in bs4 and how to click something in selenium
#     #probably gonna want to make this a function and recurse over it
#     #(if next button clicked, load new page, call scrape function, else quit with driver.quit)

#     #//div[@id="mosaic-provider-jobcards"]//a[@target="_blank"]  <-- xpath for getting to links
#     #https://stackoverflow.com/questions/27006698/selenium-iterating-through-groups-of-elements   how to iterate over list of these things

#     #driver.quit() be sure to use this at the very end when web scraping