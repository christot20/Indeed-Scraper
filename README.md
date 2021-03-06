# Indeed-Scraper
This bot utilizes the selenium python library to navigate between webpages and 
scrape values from said webpages. The purpose of this bot is to search through a user specified
amount of jobs (given there are that meany jobs) and provide data in the frequently used words, technologies used on the job, name of the job, location of the job (US only), name of company of the job listing, and salary
ranges (if provided) of the job. The general word frequency data is found by search through the given job descrption and filtering out stop words with the NLTK library. The technology key words are based on a list I made of commonly used programs, tools, technolgies, and skills of the given set of data jobs. The salaries are separated into 2 categories, low end and high end. The salaries are provided by either the employer or estimated by Indeed and are then put in a range using a function for easy categorization, yet the raw salaries are also saved in the DB if so desired. Not every job listing is provided with a salary, however, and those jobs are given "None" values as their salaries as to not effect the data.

This bot only works on the 5 data jobs listed in US locations. The bot searches
through a SQL table of known US locations provided by the US Postal Service to verify if the location exists.

The bot runs in certain time intervals to avoid being caught by captchas and is effective (as far as I tested)
to at least 500 jobs at a single execution without failure.

The bot saves the data to a sqlite3 database for viewing purposes and data can be converted to a csv
if so desired using the sqlite3 terminal. The bot also provides a visualization at the end of its execution
with seaborn plot of the word frequency and salaries.

Provided are some folders of data samples collected of different jobs in different locations. These folders contain
some of the figures of the data during the bot's execution. CSVs are also provided and all the data is stored in the locations.db file in their respective tables. There is also a provided folder of SQL scripts used during the project, 2 of which were for creating the tables of the DB and the other for data exploration and creating CSVs.

I did this project to gain some experience in data scraping, navigation, collecting, and visualization. A tableau dashboard is also provided based on the CSVs of the data given for data analysts. I was able to utilize Python, Web Scraping, SQL, and Tableau (3 of which are used often in the data field) during this project and gain some new skills.

Tableau dashboard: https://public.tableau.com/app/profile/thomas.j.christo/viz/DataAnalystVisualization/Dashboard1

# Some General Findings:
1. Machine Learning Engineers and Data Scientists are usually paid higher than Engineers and Analysts
2. It was generally harder to get salary data from locations outside of the East and West Coast and Salaries from San Francisco, Seattle, and New York were higher than in other cities across the board.
3. SQL and Python were very common technolgies used in each job type while specific skills, ci/cd, tableau/excel, model training and deep learning, are found depeneding on certain job types.
4. There are PLENTY of data jobs of each category in the cities tested in this project, each search was given thousands of results.

All these values are accurate as of 4/28/2022 and should not be taken at face value as this was merely created as a project to learn from. All data values were provided by Indeed.com.