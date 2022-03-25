from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from helpers import checker, fixer

PATH = "D:\Indeed-Scraper\chromedriver.exe"


if __name__ == '__main__':

    city = fixer(input("Enter name of city to conduct search (E.g. New York): "))
    state = input("Enter abbreviation of state to conduct search (E.g. NY): ").upper()
    job = input("Enter name of job to search up (E.g. Data Engineer): ").upper()

    if len(state.strip()) != 2: # checks if state given is invalid
        raise ValueError("Invalid State Received") #quit out of application/raise error
    elif checker(city, state.strip()) == False:
        raise ValueError("Location Received Invalid")

    # checker comes out false, raise value error as not real city, else do this
    city = city.replace(" ", "+") # used for formatting in url
    job = job.replace(" ", "+") # used for formatting in url

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # update to date webdriver installer
    driver.get(f"https://www.indeed.com/jobs?q={job}&l={city.upper()}%2C+{state.strip()}&radius=100") #format indeed link

    print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city

    for tag in driver.find_elements(By.XPATH, '//div[@id="mosaic-provider-jobcards"]//h2[1]/span'):
        print(tag.text) # gets title of that element^

    
    #have selenium click on a box and bs4 scrape the section that becomes visible
    #look up how to scrape everythong from an element in bs4 and how to click something in selenium
    #probably gonna want to make this a function and recurse over it
    #(if next button clicked, load new page, call scrape function, else quit with driver.quit)

    #driver.quit() be sure to use this at the very end when web scraping