CREATE TABLE Jobs_Salaries(
   id INT PRIMARY KEY     NOT NULL,
   job_category   TEXT    NOT NULL,
   job_list_name  TEXT    NOT NULL,
   company_name   TEXT    NOT NULL,
   job_city       TEXT    NOT NULL,
   job_state      TEXT    NOT NULL,
   indeed_salary  TEXT,
   salary_range_high TEXT,
   salary_range_low  TEXT
);

CREATE TABLE Jobs_Keywords( 
   job_category   TEXT    NOT NULL,       
   job_city       TEXT    NOT NULL,        
   job_state      TEXT    NOT NULL,
   word           TEXT    NOT NULL,
   frequency      INT
);
CREATE TABLE Jobs_General_Words( 
   job_category   TEXT    NOT NULL,       
   job_city       TEXT    NOT NULL,        
   job_state      TEXT    NOT NULL,
   word           TEXT    NOT NULL,
   frequency      INT
);
-- /*make sure to format each value to an int or to have each
-- text name,city, etc be uppercase, if salary doesnt exist make
-- value NULL
-- make sure to get salary values for associated functions and
-- to assign them accordingly based on if 0, 1, or 2 values are found
-- */