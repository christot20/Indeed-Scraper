from bs4 import BeautifulSoup
from selenium import webdriver 
from helpers import checker, fixer

PATH = "C:\Program Files (x86)\chromedriver.exe"


if __name__ == '__main__':
    #have input to replace city and job title as well as replace spaces with +, look back at that re thing that guy made for jeffreys equation 
    #     
    city = input("Enter name of city to conduct search (E.g. New York): ")
    city = fixer(city)
    state = input("Enter abbreviation of state to conduct search (E.g. NY): ").upper()
    job = input("Enter name of job to search up (E.g. Data Engineer): ").upper()

    if len(state.strip()) != 2:
        #quit out of application/raise error
        raise ValueError("Invalid State Received")
    elif checker(city, state.strip()) == False:
        raise ValueError("Location Received Invalid")
    #else:
    else: #checker comes out false, raise value error as not real city, else do this
        city = city.replace(" ", "+")
        job = job.replace(" ", "+")
        driver = webdriver.Chrome(PATH)
        driver.get(f"https://www.indeed.com/jobs?q={job.upper()}&l={city.upper()}%2C+{state.upper()}&radius=100") #example using ny
        print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
