-- DELETE FROM Jobs_Salaries WHERE job_list_name = "MACHINE LEARNING ENGINEER";
-- DELETE FROM Jobs_Keywords WHERE job_category = "MACHINE LEARNING ENGINEER";
-- DELETE FROM Jobs_General_Words WHERE job_category = "MACHINE LEARNING ENGINEER";
-- SELECT * FROM Jobs_Salaries;
-- SELECT * FROM Jobs_Keywords;
-- SELECT * FROM Jobs_General_Words;

-- .headers on 
-- .mode csv 
-- .output analystKWNY.csv
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "NY";
-- .output analystKWSF.csv
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "CA";
-- .output analystKWChicago.csv
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "IL";
-- .output analystKWSeattle.csv
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "WA";
-- .output analystKWBoston.csv
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "MA";
-- .output analystKWAustin.csv
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "TX";
-- .exit

-- make csv for keywords, tableau thing with csv to excel, 
-- SELECT * FROM Jobs_Keywords WHERE job_category = "DATA ANALYST" AND job_state = "NY"
-- look at article to make it csv
-- see if writing all the commands in here and running it will get it done at once?
-- like write down the header and other stuff and change the output file and the command and try it
-- before just doing it over and over in the terminal

-- and some sql data exploration commands like finding amount of jobs in NY with salary over 100k low end
-- use this file for exploration
-- id say get a cont for how many jobs have actual salaries (dont have none for low and high end)
-- how many are over or under a certain threshhold, where they are, and what jobs they are
-- also try to get top 5 key words of each job in each city

-- also work on readme

--amount of jobs in db with a salary listing given
SELECT COUNT(job_list_name) FROM Jobs_Salaries
WHERE indeed_salary != "None";

name of job, company name, and provided salary of jobs with at least 100k in DB
SELECT job_category, company_name, indeed_salary FROM Jobs_Salaries 
WHERE salary_range_low IN ('100K+', '125K+', '150K+', '200K+');

-- gives the top 5 companies found in the db and orders by how often they are found
SELECT company_name, COUNT(company_name) FROM Jobs_Salaries
GROUP BY company_name
ORDER BY COUNT(company_name) DESC
LIMIT 5;

-- gives amount of jobs with at least 100K salaries for each job type from the DB
SELECT job_list_name, COUNT(job_list_name) FROM Jobs_Salaries 
WHERE salary_range_low IN ('100K+', '125K+', '150K+', '200K+')
GROUP BY job_list_name
ORDER BY COUNT(job_list_name) DESC;

-- gives amount of job posts with a given salary for each job type
SELECT job_list_name, COUNT(job_list_name) FROM Jobs_Salaries 
WHERE indeed_salary != "None"
GROUP BY job_list_name
ORDER BY COUNT(job_list_name) DESC;

-- gives amount of jobs with given salary and amount of jobs above and below 100K
-- https://stackoverflow.com/questions/72006544/join-two-sql-select-statements-and-have-output-in-different-columns
SELECT job_list_name, 
       SUM(indeed_salary != 'None'),
       SUM(salary_range_high IN ('100K+', '125K+', '150K+', '200K+')),
       SUM(salary_range_high IN ('75K+', '50K+', '50K-'))
FROM Jobs_Salaries
GROUP BY job_list_name
ORDER BY job_list_name;

-- gets top key word values and their count for each job
SELECT job_category, word, frequency FROM Jobs_Keywords
GROUP BY job_category
ORDER BY frequency DESC;

-- gets top 5 key words for each job type
SELECT * FROM 
(SELECT DISTINCT job_category, word FROM Jobs_Keywords
WHERE job_category = "DATA ANALYST"
ORDER BY frequency DESC
LIMIT 5)
UNION
SELECT * FROM 
(SELECT DISTINCT job_category, word FROM Jobs_Keywords
WHERE job_category = "DATA ENGINEER"
ORDER BY frequency DESC
LIMIT 5)
UNION
SELECT * FROM 
(SELECT DISTINCT job_category, word FROM Jobs_Keywords
WHERE job_category = "DATA SCIENTIST"
ORDER BY frequency DESC
LIMIT 5)
UNION
SELECT * FROM 
(SELECT DISTINCT job_category, word FROM Jobs_Keywords
WHERE job_category = "MACHINE LEARNING ENGINEER"
ORDER BY frequency DESC
LIMIT 5);