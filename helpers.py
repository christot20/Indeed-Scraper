from geopy.geocoders import Nominatim
state_list = ['AL', 'AK', 'AZ', 'AR', 'CA','CO', 
             'CT', 'DE', 'DC', 'FL', 'GA','HI', 
             'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 
             'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
             'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 
             'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 
             'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 
             'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 
             'WV', 'WI', 'WY']
geolocator = Nominatim(user_agent="indeedscraper")

def checker(city, state): #check if state in state list, then check if city in state and return true if true or false if not
        if state not in state_list:
            return False
        elif geocoder.google(f"{city}, {state}") == "<[REQUEST_DENIED] Google - Geocode [empty]>":     #over here, might be able to get rid of top thing too, implement sql grabbing
            return False
        else:
            return True
    #return False

me = "Seattle"
you = "NJ"
#print(f'{me}, {you}')
print(geolocator.geocode('Seattle, WA'))
print(geolocator.geocode(f'{me}, {you}'))

#new plan, just look through sql database :)
#do it where geocoder thing is
# SELECT city FROM table WHERE state = ? , state

#clean up data to use sql db in ur project (alex the analyst data vid)
#https://www.youtube.com/watch?v=qfyynHBFOsM
#https://www.unitedstateszipcodes.org/zip-code-database/


