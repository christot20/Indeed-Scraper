from bs4 import BeautifulSoup
from selenium import webdriver 
from helpers import checker

PATH = "D:\Indeed Scraper\chromedriver.exe"


if __name__ == '__main__':
    #have input to replace city and job title as well as replace spaces with +, look back at that re thing that guy made for jeffreys equation 
    #     
    city = input("Enter name of city to conduct search (E.g. New York City): ").replace(" ", "+")  
    state = input("Enter abbreviation of state to conduct search (E.g. NY): ").strip(" ")
    job = input("Enter name of job to search up (E.g. Data Engineer): ").replace(" ", "+")

    city = city.strip(" ") #remove whitespace
    job = job.strip(" ")


    #checker(city, state) #implement this and import it here
    #if this return true, go through with the search
    
    #maybe use geography thing to see if place actually exists?
    #start with america and move on from there

    if len(state) != 2:
        #quit out of application/raise error
        raise ValueError("Invalid State Received")
    elif checker(city.upper(), state.upper()) == False:
        raise ValueError("Location Received Invalid")
    #else:
    else: #checker comes out false, raise value error as not real city, else do this
        driver = webdriver.Chrome(PATH)
        driver.get(f"https://www.indeed.com/jobs?q={job.upper()}&l={city.upper()}%2C+{state.upper()}&radius=100") #example using ny
        print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
