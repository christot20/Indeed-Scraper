# link to website where csv for db was used: #https://www.unitedstateszipcodes.org/zip-code-database/

import sqlite3

data_jobs = ["Data Scientist", "Data Engineer", "Data Analyst", "Data Architect", "Machine Learning Engineer",
            "Business Intelligence Analyst", "Business Analyst", "Statistician", "Quantitative Analyst",
            "Operations Analyst", "Marketing Analyst", "Database Administrator"]
def checker(city, state): # check if state in state list, then check if city in state and return true if true or false if not
    sqliteConnection = sqlite3.connect('locations.db') # connect to db
    cursor = sqliteConnection.cursor() # cursor for query execution
    primary = cursor.execute("SELECT zip FROM mytable WHERE state = ? AND primary_city = ?;", (state,city)).fetchone() # check if city exists in state
    alt = cursor.execute("SELECT zip FROM mytable WHERE state = ? AND acceptable_cities = ?;", (state,city)).fetchone() # checks other names used for cities
    sqliteConnection.close() # close db

    if primary != None or alt != None: # if location exists return true
        return True
    return False # return a no good

#https://stackoverflow.com/questions/33112377/python-verifying-if-input-is-int-and-greater-than-0
def scrape_amount():
    while True:
        amount = input("Enter how many pages to scrape: ")
        try:
            val = int(amount)
            if val >= 0:
                break
            else:
                print("Amount can't be negative, try again")
        except ValueError:
            print("Amount must be a number, try again")
    return val

# might want to make a sql script to make a new table to hold some of the results you get from scraping
# columns: job, location (city, state), word, frequency, date (maybe, look at how u used it in CS50 web app)
# make learn to use tableau for this stuff here ^ ? (alex the analyst vid on it, analyst porfolio project part 2)