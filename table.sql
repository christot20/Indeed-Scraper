CREATE TABLE Jobs_Salaries(
   id INT PRIMARY KEY     NOT NULL,
   job_name       TEXT    NOT NULL,
   job_city       TEXT    NOT NULL,
   job_state      TEXT    NOT NULL,
   indeed_salary  INT,
   salary_range_high   INT,
   salary_range_low   INT,
);

CREATE TABLE Jobs_Keywords( 
   -- id INT PRIMARY KEY     NOT NULL,      maybe do a group by with the other table for this?
   job_name       TEXT    NOT NULL,        --also maybe u can make a table for all words and see what
   job_city       TEXT    NOT NULL,        --was most used word in all of the job desc
   job_state      TEXT    NOT NULL,
   Word_1         TEXT,   NOT NULL,
   Word_2         TEXT,   NOT NULL,
   Word_3         TEXT,   NOT NULL,
);
/*make sure to format each value to an int or to have each
text name,city, etc be uppercase, if salary doesnt exist make
value NULL
make sure to get salary values for associated functions and
to assign them accordingly based on if 0, 1, or 2 values are found
*/