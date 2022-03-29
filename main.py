from bs4 import BeautifulSoup
import requests
import time
import urllib.request 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns



from helpers import checker, scrape_amount

#PATH = "D:\Indeed-Scraper\chromedriver.exe"
words = {}
nltk.download('stopwords')

def plotter():
    #%matplotlib inline
    sns.set()
    freqdist1 = nltk.FreqDist(words)
    freqdist1.plot(25)
    #return False

#https://stackoverflow.com/questions/1692388/python-list-of-dict-if-exists-increment-a-dict-value-if-not-append-a-new-dic
def extract(text):
    # words = {}
    
    #try to also add words to another sqllite db for tableau visualization
    #use pandas for quick visualizations (data frame)

    word = re.findall("\w+", text) #might want to change this to extract numbers or any other descrepnacies
    stop_words = nltk.corpus.stopwords.words('english')
    for new_word in word:
        if new_word not in stop_words:
            if not new_word in words:
                words[new_word.lower()] = 1
                # try to make a pandas data frame from the dict with key being word and val being its count
            else:
                words[new_word.lower()] += 1
        else:
            continue
    print(words)
    #time.sleep(10)
    #return words                       

def scrape(num):
    for i in range(num):
        try: 
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')))
        except WebDriverException:
            continue
        finally:
            for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]/a'): #iterates over every link
                #tag.click()
                #time.sleep(2) 
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((tag)))
                try:
                    tag.click()
                    element = driver.find_element(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]/iframe[@title="Selected Job Details"]') #maybe make this elements instead of element and                                                                                                                 #do what u did for checking if there is next button (if cnditional)
                    url = element.get_attribute("src")
                    html = urllib.request.urlopen(url)
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.find("div", {"class":"jobsearch-JobInfoHeader-title-container"})
                    result = soup.find("div", {"id":"jobDescriptionText"})
                    print("--------------------------------")
                    print(title.text) #changed finding the title to using bs4 scraping the job page, commented out the moving in and out of frames, check gitub for differences
                    print(result.text) #prints text in given url

                    extract(result.text)

                except WebDriverException:
                    print("rer")
                    #add a variable here to count how many skipped
                    continue  
                except AttributeError:
                    print("sus")
                    #add a variable here to count how many skipped
                    continue              
        next_pg = driver.find_elements(By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')
        if len(next_pg) == 0:
            break
        else:
            next_pg[0].click() #check if next button exists and click it if yes, else break the loop
            i += 1
    plotter()
    time.sleep(20)
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
    driver.maximize_window()

    print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
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