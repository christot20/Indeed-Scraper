#from geopy.geocoders import Nominatim
import sqlite3
# state_list = ['AL', 'AK', 'AZ', 'AR', 'CA','CO', 
#              'CT', 'DE', 'DC', 'FL', 'GA','HI', 
#              'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 
#              'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
#              'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 
#              'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 
#              'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 
#              'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 
#              'WV', 'WI', 'WY']
#geolocator = Nominatim(user_agent="indeedscraper")

def checker(city, state): #check if state in state list, then check if city in state and return true if true or false if not
    sqliteConnection = sqlite3.connect('locations.db')
    cursor = sqliteConnection.cursor()
    print(city)
    list = cursor.execute("SELECT zip FROM mytable WHERE state = ? AND primary_city = ?;", (state,city)).fetchone()
    print(list)
    sqliteConnection.close()
    if list != None:
        # sqliteConnection.close()
        return True
    # else:
    #     sqliteConnection.close()
    #     return False
    return False

def fixer(text):
    for i in range(len(text)):
        if i == 0:
            text[i].upper()
        elif text[i] == " ":
            text[i+1].upper()
        i += 1
    return text

#new plan, just look through sql database :)
#do it where geocoder thing is
# SELECT city FROM table WHERE state = ? , state

#clean up data to use sql db in ur project (alex the analyst data vid)
#https://www.youtube.com/watch?v=qfyynHBFOsM
#https://www.unitedstateszipcodes.org/zip-code-database/


