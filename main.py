from bs4 import BeautifulSoup
from selenium import webdriver 

PATH = "D:\Indeed Scraper\chromedriver.exe"


if __name__ == '__main__':
    #have input to replace city and job title as well as replace spaces with +, look back at that re thing that guy made for jeffreys equation 
    city = input("Enter name of city to conduct search (E.g. New York City): ")  #make the input all caps
    state = input("Enter abbreviation of state to conduct search (E.g. NY): ")
    job = input("Enter name of job to search up (E.g. Data Engineer): ")
    city.replace(" ", "+")
    job.replace(" ", "+")

    #WebDriverWait wait = new WebDriverWait(driver, 100)
    if job != "" and city != "" and state != "":
        driver = webdriver.Chrome(PATH)
        driver.get(f"https://www.indeed.com/jobs?q={job.upper()}&l={city.upper()}%2C+{state.upper()}&radius=100") #example using ny
        print(driver.title) #prints out total number of jobs with that title in 100 mile radius of that city
