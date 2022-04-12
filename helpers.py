# link to website where csv for db was used: #https://www.unitedstateszipcodes.org/zip-code-database/

import sqlite3

data_jobs = ["Data Scientist", "Data Engineer", "Data Analyst", "Data Architect", "Machine Learning Engineer"]

key_words = ["python","sql","mysql","postgresql", "nosql","mongodb","tableau","excel","ai","artificial intelligence","ml","machine learning",
            "r","matlab","data visualization","data cleaning","linear algebra","calculus","statistics","pytorch",
            "tensorflow","jupyter notebook","pandas","numpy","matplotlib","seaborn","scipy","spreadsheets","writing",
            "speaking","communication","neural net","neural network", "neural networks","models","modelling","algorithms",
            "programming","mathematics","ci/cd","continuous integration","continuous deployment", "continuous delivery",
            "bash","powershell","windows","linux","unix","git","version control","deep learning","automation","data wrangling",
            "big data","processing","c","c++","c/c++","perl","java","sas","hadoop","spark","hive","pig","probability",
            "data manipulation","julia","machine learning algorithms","supervised learning","unsupervised learning",
            "semi-supervised learning","reinforcement learning","linear regression","logistic regression","decision tree",
            "svm algorithm","naive bayes algorithm","knn algorithm","knn","svm","support vector machine","naive bayes","k-means",
            "random forest","random forest algorithm","dimensionality reduction","gradient boosting","adaboosting",
            "sklearn","scikit-learn","scikit learn","scikit","scala","hpcc","storm","cloudera","rapidminer","spss","docker","kubernetes","mapreduce",
            "cassandra","data transformation","hevo data","matillion","etl","pentaho data integration","talend","infosphere datastage",
            "data ingestion","apache","data warehousing","aws","aws glue","stitch","data buffering","kinesis","redis cache",
            "redis","GCP","azure","openstack","openshift","qlik","tibco spotfire","plotly","coding","golang","hbase","sql databases",
            "sql database","scripting","dbms","data models","security","performance","scalability","data recovery","reliabilty",
            "migration","data migration","monitor","management systems","relational database","cloud","mining","data mining",
            "predictive modeling","natrual language processing","nltk","nlp","agile","data structures","hyposthesis testing",
            "optimization","predictive models","kafka","weka","apiori","apiori algorithm", "oop","object oriented", "b.s.", "m.s.",
            "phd.","computer science","solid","kiss","testing", "flink", "sqoop","flume","javascript","computer vision","pipelines",
            "segmentation","A/B testing","power analyses","keras","scalability","binary classification","multiclass classification",
            "regression","searching"]

def sal_assigner_less(sal):
    value = ""
    for j in range(len(sal)):
        if sal[j] == ".":
            value += sal[j]
        elif sal[j].isdigit() == True:
            value += sal[j]
    return value

def sal_assigner(sal):
    low_val = ""
    high_val = ""
    k = 0
    for j in range(len(sal)):
        if sal[j] == "$":
            k += 1
        if k == 1:
            if sal[j] == ".":
                low_val += sal[j]
            elif sal[j].isdigit() == True:
                low_val += sal[j]
        elif k == 2:
            if sal[j] == ".":
                high_val += sal[j]           # test out and see if decimal hourly pay is working (like 26.98)
            elif sal[j].isdigit() == True:   #decimals work, try to make graphs look better, implement sql db
                high_val += sal[j]           #make new sql db and add data into there
    return low_val, high_val                 #job_name, job_state, job_city, job_salary_high, job_salary_low, keywords
                                             #create a list of keywords and implement the NLTK thing to count them, used to find skills
#ranges: <50K, 50K, 75K, 100K, 125K, 150K, 200K>
def sal_range(value):
    #check range of value here
    if value < 50000:
        return "50K-"
    elif 50000 <= value < 75000:
        return "50K+"
    elif 75000 <= value < 100000:
        return "75K+"
    elif 100000 <= value < 125000:
        return "100K+"
    elif 125000 <= value < 150000:
        return "125K+"
    elif 150000 <= value < 200000:
        return "150K+"
    elif 200000 <= value:
        return "200K+"

def sal_range_month(value):
    if value < 4167:
        return "50K-"
    elif 4167 <= value < 6250:
        return "50K+"
    elif 6250 <= value < 8333:
        return "75K+"
    elif 8333 <= value < 10417:
        return "100K+"
    elif 10417 <= value < 12500:
        return "125K+"
    elif 12500 <= value < 16667:     # add a function for months and check if the by hour numbers look good (no period was found b4)
        return "150K+"
    elif 16667 <= value:
        return "200K+"

def hour_range(value):
    #check range of value here
    if value < 26:
        return "50K-"
    elif 26 <= value < 39:
        return "50K+"
    elif 39 <= value < 51:
        return "75K+"
    elif 51 <= value < 64:
        return "100K+"
    elif 64 <= value < 77:
        return "125K+"           #fix how decimals are handled and check what the number is on each func call
    elif 77 <= value < 103:     # add a function for months and check if the by hour numbers look good (no period was found b4)
        return "150K+"
    elif 103 <= value:
        return "200K+"

def sal_range_est(value):
    #check range of value here
    if value < 50:
        return "50K-"
    elif 50 <= value < 75:
        return "50K+"
    elif 75 <= value < 100:
        return "75K+"
    elif 100 <= value < 125:
        return "100K+"
    elif 125 <= value < 150:
        return "125K+"
    elif 150 <= value < 200:
        return "150K+"
    elif 200 <= value:
        return "200K+"

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