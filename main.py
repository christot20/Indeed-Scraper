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



from helpers import checker, scrape_amount, data_jobs

#PATH = "D:\Indeed-Scraper\chromedriver.exe"
words = {}
salaries = {}
nltk.download('stopwords')

def plotter(dict):
    #%matplotlib inline
    sns.set()
    freqdist1 = nltk.FreqDist(dict)
    freqdist1.plot(25)                # have the plot give the name of the job and place its checking as its title
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
            if re.search('[a-zA-Z]', new_word) == None:
                continue #try to maybe limit it to tech jobs?, get list of tech job names and force that to be used
                # add data to a sql db by job name, city, state, word, and frequency
                # use db for tableau visualizations
                # maybe just get salaries?, would be easier, for now...
                # list of tech skills, porgramming languages, oses, maybe just count those?
                # list of data skills, their salaries and positions, and where they are
                # big data job stuff, make new repo with that, keep this for later
                #make list of jobs to search throug in helpers
            elif not new_word in words:
                words[new_word.lower()] = 1
                # try to make a pandas data frame from the dict with key being word and val being its count
            else:
                words[new_word.lower()] += 1
        else:
            continue
    #print(words)
    #time.sleep(10)
    #return words                       
def sal_scrape(element):
    if element.find_elements(By.XPATH, './/div[@class="metadata salary-snippet-container"]') == []:
        if element.find_elements(By.XPATH, './/span[@class="estimated-salary"]') == []:
            return False
        else:
            salary = element.find_elements(By.XPATH, './/span[@class="estimated-salary"]')[0].text
            sal_extract(salary)
    else:
        salary = element.find_elements(By.XPATH, './/div[@class="metadata salary-snippet-container"]')[0].text
        sal_extract(salary)

def sal_extract(salary):
    if not salary in salaries:
        salaries[salary] = 1
            # try to make a pandas data frame from the dict with key being word and val being its count
    else:
        salaries[salary] += 1
    print(salaries)

def scrape(num):
    for i in range(num):
        try: 
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')))
            driver.find_element(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]').click()
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
                    sal_scrape(tag)
                    extract(result.text)

                except WebDriverException:
                    print("rer")
                    #add a variable here to count how many skipped
                    continue  
                except AttributeError:
                    print("sus")
                    #add a variable here to count how many skipped
                    continue    
        
            try: 
                print("hi")
                WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')))
                driver.find_element(By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]').click()
            except WebDriverException:
                print("bye")
                break          
        # if len(next_pg) == 0:
        #     break
        # else:
        #     next_pg[0].click() #check if next button exists and click it if yes, else break the loop
        #     i += 1
    plotter(words)
    plotter(salaries)
    #time.sleep(20)
    driver.quit()

if __name__ == '__main__':
    # maybe add list of jobs to look through here
    for i in range(len(data_jobs)):
        print(f"{i+1}. {data_jobs[i]} ")

    city = input("Enter name of city to conduct search (E.g. New York): ").title()
    state = input("Enter abbreviation of state to conduct search (E.g. NY): ").upper()
    job = input("Enter name of job to search up (E.g. Data Engineer): ").upper()
    user_choice = scrape_amount()

    if len(state.strip()) != 2: # checks if state given is invalid
        raise ValueError("Invalid State Received") 
    elif checker(city, state.strip()) == False:
        raise ValueError("Location Received Invalid")
    elif job.title() not in data_jobs:
        raise ValueError("Job Title Not In List of Accepted Jobs")
    # checker comes out false, raise value error as not real city, else do this
    city = city.replace(" ", "+") # used for formatting in url
    job = job.replace(" ", "+") # used for formatting in url

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # update to date webdriver installer
    driver.get(f"https://www.indeed.com/jobs?q={job}&l={city.upper()}%2C+{state.strip()}&radius=100") #format indeed link
    driver.maximize_window()

    print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
    scrape(user_choice)