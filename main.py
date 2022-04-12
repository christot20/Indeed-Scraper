from bs4 import BeautifulSoup
import requests
import time
#import urllib2
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
import numpy as np



from helpers import checker, sal_assigner, scrape_amount, sal_range, hour_range, sal_range_est, sal_range_month, sal_assigner_less, data_jobs, key_words

#PATH = "D:\Indeed-Scraper\chromedriver.exe"
words = {}
freq_key_words = {}
high_salaries = {}
low_salaries = {}
nltk.download('stopwords')
plt.rcParams['toolbar'] = 'None'

def sortdict(dictionary, sorted_vals):
    sort_dict = {}
    for i in sorted_vals:
        for k in dictionary.keys():
            if dictionary[k] == i:
                sort_dict[k] = dictionary[k]  #label the plots
                break
    return sort_dict

def plotter(dicti, name):                   # look to see if more values are needed in the keywords, see if keywords are being detected
                 # sort the graphs to be highest first and go down, also title the plots
    sorted_values = sorted(dicti.values(), reverse=True)
    new_dict = sortdict(dicti, sorted_values)
    ranges = list(new_dict.keys())
    values = list(new_dict.values())
    sns.set_theme()
    plt.title(name)
    plt.xlabel("Salary Ranges")
    plt.ylabel("Counts")
    plt.bar(range(len(new_dict)), values, tick_label=ranges) #try to make word plots like these and find a way to cut how many words shown
    plt.show()                                                      #reverse plot and shit for freq dist

def word_plotter(dicti, name):
    # #%matplotlib inline
    # #vals = sorted(dict, key=dict.get, reverse=True)
    # sns.set_theme()
    # freqdist1 = nltk.FreqDist(dicti)
    # #plt.xticks(rotation=60)
    # freqdist1.plot(25)                # have the plot give the name of the job and place its checking as its title
    # #return False
    sorted_values = sorted(dicti.values(), reverse=True)
    new_dict = sortdict(dicti, sorted_values)
    ranges = list(new_dict.keys())
    values = list(new_dict.values())
    sns.set_theme()
    # plt.xlabel('Words', fontsize=12)
    # plt.ylabel('Counts', fontsize=16)
    plt.title(name)
    plt.bar(range(len(new_dict)), values, tick_label=ranges) #try to make word plots like these and find a way to cut how many words shown
    plt.xlim(1, 10) #try to space out values somehow, or rotate them at least
    plt.xticks(rotation = 25)
    plt.show() 

def kword_extract(kword):
    if kword in key_words:
        if not kword in freq_key_words:  #was fixing up keywords, mabe make function?
            freq_key_words[kword] = 1    #more stuff to do above in plotter comments
        else:
            freq_key_words[kword] += 1

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
                continue 
            elif not new_word in words:
                words[new_word.lower()] = 1
                kword_extract(new_word.lower())
                # try to make a pandas data frame from the dict with key being word and val being its count
            else:
                words[new_word.lower()] += 1
                kword_extract(new_word.lower())
        else:
            continue 
def sal_dict(salary, sdict):
    if not salary in sdict:
        sdict[salary] = 1
            # try to make a pandas data frame from the dict with key being word and val being its count
    else:
        sdict[salary] += 1
    #print(sdict) 

def sal_extract(salary):
    print(salary)
    z = 0
    for i in range(len(salary)):
        if salary[i] == "$":
            z += 1
        #return i    #check how many values there are  
    print(z)    
    if "year" in salary:      #salary scraping
        salary.replace(",","")  #remove commas
        if z > 1:
            low_val, high_val = sal_assigner(salary)
            if "Estimated" in salary:
                new_salary_high = sal_range_est(float(high_val)) # will go through these functions to get salary range
                new_salary_low = sal_range_est(float(low_val))
            else:
                new_salary_high = sal_range(float(high_val)) # will go through these functions to get salary range
                new_salary_low = sal_range(float(low_val))
            #try to find if its an horuly or salary value, if there is one or two of them, new salary value range based on number
            #will need to make the values into numbers at some point, need to work on that
            #make a fucntion in helpers to determine what range value is in
            #one fucntion for hourly and one for salaries
            sal_dict(new_salary_high, high_salaries)   # add new salary ranges to dict
            sal_dict(new_salary_low, low_salaries)  # will want to make the processes for if i > 1 or not into functions
                                                    # you also need to split this up with if estimated is in the string or not (diff vals)
        else: #if only 1 val
            value = sal_assigner_less(salary)
            new_salary_high = sal_range(float(value)) # will go through these functions to get salary range
            new_salary_low = sal_range(float(value))
            sal_dict(new_salary_high, high_salaries)
            sal_dict(new_salary_low, low_salaries)
    elif "month" in salary:      #salary scraping
        salary.replace(",","")  #remove commas
        if z > 1:
            low_val, high_val = sal_assigner(salary)
            new_salary_high = sal_range_month(float(high_val)) # will go through these functions to get salary range
            new_salary_low = sal_range_month(float(low_val))
            sal_dict(new_salary_high, high_salaries)   # add new salary ranges to dict
            sal_dict(new_salary_low, low_salaries)  # will want to make the processes for if i > 1 or not into functions
                                                    # you also need to split this up with if estimated is in the string or not (diff vals)
        else: #if only 1 val
            value = sal_assigner_less(salary)
            new_salary_high = sal_range_month(float(value)) # will go through these functions to get salary range
            new_salary_low = sal_range_month(float(value))
            sal_dict(new_salary_high, high_salaries)
            sal_dict(new_salary_low, low_salaries)
    elif "hour" in salary: #if hour in string
        if z > 1: #will need seaparate function to determine hourly pay to yearly
            low_val, high_val = sal_assigner(salary) #might want to make the processes above a function for getting th values
            new_salary_high = hour_range(float(high_val)) # will go through these functions to get salary range
            new_salary_low = hour_range(float(low_val))
            sal_dict(new_salary_high, high_salaries)
            sal_dict(new_salary_low, low_salaries)
        else: #if only 1 val
            value = sal_assigner_less(salary)
            new_salary_high = hour_range(float(value)) # will go through these functions to get salary range
            new_salary_low = hour_range(float(value))
            sal_dict(new_salary_high, high_salaries)
            sal_dict(new_salary_low, low_salaries)
    print(high_salaries)
    print("--------------------------------")
    print(low_salaries)

def sal_scrape(element):
    if element.find_elements(By.XPATH, './/div[@class="metadata salary-snippet-container"]') == []:
        if element.find_elements(By.XPATH, './/span[@class="estimated-salary"]') == []:
            return False
        else:
            salary = element.find_elements(By.XPATH, './/span[@class="estimated-salary"]')[0].text
            #print(salary)
            sal_extract(salary)
    else:
        salary = element.find_elements(By.XPATH, './/div[@class="metadata salary-snippet-container"]')[0].text
        #print(salary)
        sal_extract(salary)

def scrape(num):
    for i in range(num):
        page_title = driver.title
        try: 
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')))
            driver.find_element(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]').click()
        except WebDriverException:
            continue
        finally:
            for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]/a'): #iterates over every link
                #tag.click()
                #time.sleep(2) 
                # handles = driver.window_handles
                # if len(handles) > 1:
                #     driver.switch_to.window(handles[1]) #test to see if u keep getting hi or not
                #     driver.close()
                #     driver.switch_to.window(handles[0])
                # else:
                #     continue
                # WebDriverWait(driver, 10).until(EC.visibility_of((tag)))                       #issue wirth skipping pages seem to stem off of contiue statemetns, watch them
                # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((tag)))            #also might want to make range of search to be 25 miles at most so that locations are correct
                try:                                                                        #was getting ct places for NY
                    WebDriverWait(driver, 10).until(EC.visibility_of((tag)))                       #issue wirth skipping pages seem to stem off of contiue statemetns, watch them
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((tag)))              #also try to redirect yourself if u go to different page by accident
                    #time.sleep(1)
                    tag.click()
                    #time.sleep(2) #maybe use webdriver.wait? use this to close any tabs that get opened by accident
                    try: 
                        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')))
                        driver.find_element(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]').click()
                    except WebDriverException:
                        pass
                    handles = driver.window_handles
                    if len(handles) > 1:
                        driver.switch_to.window(handles[1]) #test to see if u keep getting hi or not
                        driver.close()
                        driver.switch_to.window(handles[0])
                    elif driver.title != page_title:
                        driver.back()
                    element = driver.find_element(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//section[@id="vjs-container"]/iframe[@title="Selected Job Details"]') 
                    url = element.get_attribute("src")
                    html = requests.get(url).text #win 10060 error, see how to fix it, test this out on opensuse machine
                    soup = BeautifulSoup(html, "html.parser")                                               #also find a way to get it to close a popup each time, look at loop and what u used b4
                    title = soup.find("div", {"class":"jobsearch-JobInfoHeader-title-container"})
                    result = soup.find("div", {"id":"jobDescriptionText"})
                    print("--------------------------------")
                    print(title.text)
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
                #WebDriverWait(driver, 4).until(EC.visibility_of((By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')))
                WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')))
                driver.find_element(By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]').click()
                i += 1
            except WebDriverException:
                print("bye")
                break          
        # if len(next_pg) == 0:
        #     break
        # else:
        #     next_pg[0].click() #check if next button exists and click it if yes, else break the loop
        #     i += 1
    word_plotter(words, "General Word Frequency")
    word_plotter(freq_key_words, "KeyWord Frequency")
    plotter(high_salaries, "Salary High End")
    plotter(low_salaries, "Salary Low End")
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
    driver.get(f"https://www.indeed.com/jobs?q={job}&l={city.upper()}%2C+{state.strip()}&radius=25") #format indeed link
    driver.maximize_window()

    print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
    scrape(user_choice)