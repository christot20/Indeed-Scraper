import time
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


from helpers import checker, sal_assigner, scrape_amount, sal_range, hour_range, sal_range_est, sal_range_day, sal_range_month, sal_assigner_less, sortdict, titlefixer, sql_add, sql_size, sql_word_add, link_reformatting, data_jobs, key_words

words = {}
freq_key_words = {}
high_salaries = {}
low_salaries = {}
nltk.download('stopwords')
plt.rcParams['toolbar'] = 'None'

def plotter(dicti, name):                   
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
    sorted_values = sorted(dicti.values(), reverse=True)
    new_dict = sortdict(dicti, sorted_values)
    ranges = list(new_dict.keys())
    values = list(new_dict.values())
    sns.set_theme()
    plt.title(name)
    plt.bar(range(len(new_dict)), values, tick_label=ranges) #try to make word plots like these and find a way to cut how many words shown
    plt.xlim(0, 20) #try to space out values somehow, or rotate them at least
    plt.xticks(rotation = 25)
    plt.xticks(fontsize = 6)
    plt.show() 

def kword_extract(kword):
    if kword in key_words:
        if not kword in freq_key_words:  #was fixing up keywords, mabe make function?
            freq_key_words[kword] = 1    #more stuff to do above in plotter comments
        else:
            freq_key_words[kword] += 1

#https://stackoverflow.com/questions/1692388/python-list-of-dict-if-exists-increment-a-dict-value-if-not-append-a-new-dic
def extract(text):
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
    elif "day" in salary:      #salary scraping
        if z > 1:
            low_val, high_val = sal_assigner(salary)
            new_salary_high = sal_range_day(float(high_val)) # will go through these functions to get salary range
            new_salary_low = sal_range_day(float(low_val))
            sal_dict(new_salary_high, high_salaries)   # add new salary ranges to dict
            sal_dict(new_salary_low, low_salaries)  # will want to make the processes for if i > 1 or not into functions
                                                    # you also need to split this up with if estimated is in the string or not (diff vals)
        else: #if only 1 val
            value = sal_assigner_less(salary)
            new_salary_high = sal_range_day(float(value)) # will go through these functions to get salary range
            new_salary_low = sal_range_day(float(value))
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
    #if z > 0:
    return new_salary_high, new_salary_low

def sal_scrape(element):
    if element.find_elements(By.XPATH, './/div[@class="metadata salary-snippet-container"]') == []:
        if element.find_elements(By.XPATH, './/span[@class="estimated-salary"]') == []:
            return "None", "None", "None" #works for now, remove job post and start sql integration
        else:
            salary = element.find_elements(By.XPATH, './/span[@class="estimated-salary"]')[0].text
            #print(salary)
            high, low = sal_extract(salary)
    else:
        salary = element.find_elements(By.XPATH, './/div[@class="metadata salary-snippet-container"]')[0].text
        #print(salary)
        high, low = sal_extract(salary)
    return high, low, salary

def scrape(num, city, state, job):
    #result = []
    i = 0
    while i != num:
        print(i)
        try: 
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')))
            driver.find_element(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]').click()
        except WebDriverException:
            pass
        for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]/a'): #iterates over every link
            try:   
                #page_title = driver.title #check if this works                                                                    #was getting ct places for NY
                WebDriverWait(driver, 10).until(EC.visibility_of((tag)))                       #issue wirth skipping pages seem to stem off of contiue statemetns, watch them
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((tag)))              #also try to redirect yourself if u go to different page by accident
                #time.sleep(1)
                tag.click()
                #time.sleep(2) #maybe use webdriver.wait? use this to close any tabs that get opened by accident
                try: 
                    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]')))
                    driver.find_element(By.XPATH, '//div[@id="popover-x"]/button[@aria-label="Close"]').click()
                    pass
                except WebDriverException:
                    pass
                handles = driver.window_handles
                if len(handles) > 1:
                    print("More tabs")
                    driver.switch_to.window(handles[1]) #test to see if u keep getting hi or not
                    time.sleep(4)
                    driver.close()
                    driver.switch_to.window(handles[0])
                    break
                if "grpKey" in str(driver.current_url):
                    print("Redirect")
                    driver.back()
                    driver.back()
                    time.sleep(4)
                    break
                time.sleep(2)
                iframe = driver.find_element(By.CSS_SELECTOR, '#vjs-container-iframe')
                driver.switch_to.frame(iframe)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@id="jobDescriptionText"]')))
                result = driver.find_element(By.CSS_SELECTOR, '#jobDescriptionText').text
                title = driver.find_element(By.XPATH, '//h1[@class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title is-embedded"]').text
                comp_title = driver.find_elements(By.XPATH, '//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]')[1].text
                #test this thing here^ ## works
                #also look on bottom to see what to do
                #comp_title = comp_title_raw[1].text
                #make csv for keywords too
                driver.switch_to.default_content()
                time.sleep(3)
                high, low, raw = sal_scrape(tag) #get the high and low values here and incorporate sql db adding here 
                extract(result) #also try to get the actual job title and remove the job post stuff from it
                print("--------------------------------")
                print(f"{city} {state} {job}")
                new_title = titlefixer(title)
                print(new_title)
                print(comp_title) #company titles
                print(raw) #actual salary text element
                print(f"{high} {low}") #sql integration and getting actual values of salary?
                print("--------------------------------") #maybe change paramters for size/search preferences?, like 25 miles, ort by rekevance, etc
                id = sql_size()
                print(id)
                values = (id, job, new_title, comp_title, city, state, raw, high, low)
                sql_add(values, "salaries")
                #get job company name
                i += 1
                print(i)    # good fucking shit, now just get more data and tableau it
                print(num)   # be sure to push new stuff to the repo and even stress test to see how far it can scrape
                if i == num:
                    break
            except WebDriverException as error:
                print(error)
                continue  
            except AttributeError as error: #test nout new york data analyst
                print(error)
                continue 
        if i == num:
            break          
        try: # id 449 is where data analyst stuff ends in sql
            print("Navigating to new page")
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]')))
            driver.find_element(By.XPATH, '//nav[@role="navigation"]//a[@aria-label="Next"]').click()    
            print(i)
        except WebDriverException:
            print("Manually navigating to new page")
            try:
                next = driver.find_element(By.XPATH, '//div[@id="searchCount"]').text
                link = str(driver.current_url)
                new_link = link_reformatting(next, link)
                driver.get(new_link)
            except WebDriverException:
                break              

    sql_word_add("freq words", freq_key_words, job, city, state)
    sql_word_add("words", words, job, city, state)
    word_plotter(words, "General Word Frequency")
    word_plotter(freq_key_words, "KeyWord Frequency")
    plotter(high_salaries, "Salary High End")
    plotter(low_salaries, "Salary Low End") #double check everything is working and you did everything u want
    #time.sleep(20)                    start doing scrapes of 20 for locations and jobs and tableau them
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
    driver.get(f"https://www.indeed.com/jobs?q={job}&l={city.upper()}%2C+{state.strip()}&radius=0") #format indeed link
    driver.maximize_window()

    print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
    scrape(user_choice, city.replace("+", " "), state, job.replace("+", " "))

    #main issues: captchas are cock blocking the script, otherwise seems good so far
    #idk if time.sleep will help, but u can try
    #make a file with a bunch of sql scripts showing certian data, like words used per job,how many jobs with certain salary, where they are, etc