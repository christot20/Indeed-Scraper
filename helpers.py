# link to website where csv for db was used: #https://www.unitedstateszipcodes.org/zip-code-database/

import sqlite3

def checker(city, state): # check if state in state list, then check if city in state and return true if true or false if not
    sqliteConnection = sqlite3.connect('locations.db') # connect to db
    cursor = sqliteConnection.cursor() # cursor for query execution
    primary = cursor.execute("SELECT zip FROM mytable WHERE state = ? AND primary_city = ?;", (state,city)).fetchone() # check if city exists in state
    alt = cursor.execute("SELECT zip FROM mytable WHERE state = ? AND acceptable_cities = ?;", (state,city)).fetchone() # checks other names used for cities
    sqliteConnection.close() # close db

    if primary != None or alt != None: # if location exists return true
        return True
    return False # return a no good

# might want to make a sql script to make a new table to hold some of the results you get from scraping
# columns: job, location (city, state), word, frequency, date (maybe, look at how u used it in CS50 web app)
# make learn to use tableau for this stuff here ^ ? (alex the analyst vid on it, analyst porfolio project part 2)