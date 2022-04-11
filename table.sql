CREATE TABLE Jobs(
   id INT PRIMARY KEY     NOT NULL,
   job_name       TEXT    NOT NULL,
   job_city       TEXT    NOT NULL,
   job_state      TEXT    NOT NULL,
   indeed_salary  INT,
   salary_range_high   INT,
   salary_range_low   INT,
);
/*make sure to format each value to an int or to have each
text name,city, etc be uppercase, if salary doesnt exist make
value NULL
make sure to get salary values for associated functions and
to assign them accordingly based on if 0, 1, or 2 values are found
*/