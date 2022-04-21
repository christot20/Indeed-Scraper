# link to website where csv for db was used: #https://www.unitedstateszipcodes.org/zip-code-database/

import sqlite3

data_jobs = ["Data Scientist", "Data Engineer", "Data Analyst", "Data Architect", "Machine Learning Engineer"]

key_words = ["python","sql","mysql","postgresql", "nosql","mongodb","tableau","excel","ai","artificial intelligence","ml","machine learning",
            "r","matlab","data visualization","data cleaning","linear algebra","calculus","statistics","pytorch",
            "tensorflow","jupyter notebook","pandas","numpy","matplotlib","seaborn","scipy","spreadsheets",
            "ci","cd","neural net","neural network", "neural networks","models","modelling","algorithms",
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
            "regression","searching","ssis","powerbi"]

def titlefixer(text):
    for i in range(len(text)):
        ex_len = len(text) - i
        if text[i: i + ex_len] == "- job post":
            new_title = text[0 : i-1]
            return new_title

def sortdict(dictionary, sorted_vals):
    sort_dict = {}
    for i in sorted_vals:
        for k in dictionary.keys():
            if dictionary[k] == i:
                sort_dict[k] = dictionary[k]  #label the plots
                #break
    #print(sort_dict)
    return sort_dict

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

def sal_range_day(value):
    #check range of value here
    if value < 192:
        return "50K-"
    elif 192 <= value < 288:
        return "50K+"
    elif 288 <= value < 385:
        return "75K+"
    elif 385 <= value < 481:
        return "100K+"
    elif 481 <= value < 577:
        return "125K+"           #fix how decimals are handled and check what the number is on each func call
    elif 577 <= value < 769:     # add a function for months and check if the by hour numbers look good (no period was found b4)
        return "150K+"
    elif 769 <= value:
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

def sql_size():
    sqliteConnection = sqlite3.connect("locations.db") # connect to db
    cursor = sqliteConnection.cursor() # cursor for query execution
    cursor.execute("SELECT COUNT(*) FROM Jobs_Salaries")
    id = cursor.fetchone()[0]
    cursor.close()
    sqliteConnection.close()
    return int(id)

def sql_add(values, name):
    try:
        sqliteConnection = sqlite3.connect("locations.db") # connect to db
        cursor = sqliteConnection.cursor() # cursor for query execution
        if len(values) > 5:
            sql = """INSERT INTO Jobs_Salaries(id, job_list_name, job_category, company_name,
                    job_city, job_state, indeed_salary, salary_range_high, salary_range_low) 
                    VALUES(?,?,?,?,?,?,?,?,?)"""
            cursor.execute(sql, values) 
            sqliteConnection.commit()
        else:
            if name == "freq words":
                sql = """INSERT INTO Jobs_Keywords(job_category, job_city, job_state, 
                        word, frequency) VALUES(?,?,?,?,?)"""
                cursor.execute(sql, values) 
                sqliteConnection.commit()
            else:
                sql = """INSERT INTO Jobs_General_Words(job_category, job_city, job_state, 
                        word, frequency) VALUES(?,?,?,?,?)"""
                cursor.execute(sql, values) 
                sqliteConnection.commit()
        #print("Successfully added to DB")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def sql_word_add(name, dicti, job, city, state):
    sorted_values = sorted(dicti.values(), reverse=True)
    new_dict = sortdict(dicti, sorted_values)
    for k, v in new_dict.items():
        word = k
        frequency = v
        values = (job, city, state, word, frequency) # is able to add words to freq db
        sql_add(values, name)

#https://stackoverflow.com/questions/33112377/python-verifying-if-input-is-int-and-greater-than-0
def scrape_amount():
    while True:
        amount = input("Enter how many jobs do you want to scrape: ")
        try:
            val = int(amount)
            if val >= 0:
                break
            else:
                print("Amount can't be negative, try again")
        except ValueError:
            print("Amount must be a number, try again")
    return val

def link_reformatting(next, link):
    print(next[5:])
    word = next[5:]
    print(word)
    for k in range(len(word)):
        if word[k].isdigit() == False:
            word = word[:-abs(len(word) - k)]
            break
            #next = next[:remove]
    print(word)
    word = int(word)
    #next = driver.find_element(By.XPATH, '//div[@id="searchCountPages"]').
    start_word = ""
    index = link.find(("start="))
    for j in range(int(index), len(link)):
        if link[j] != "&":
            start_word += link[j]
        else:
            break
    print(start_word)
    new_link = link.replace(start_word, f"start={word}0")
    print(new_link)
    return new_link