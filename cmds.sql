DELETE FROM Jobs_Salaries WHERE job_list_name = "DATA SCIENTIST" AND job_state = "CA";
DELETE FROM Jobs_Keywords WHERE job_category = "DATA SCIENTIST" AND job_state = "CA";
DELETE FROM Jobs_General_Words WHERE job_category = "DATA SCIENTIST" AND job_state = "CA";
SELECT * FROM Jobs_Salaries;
SELECT * FROM Jobs_Keywords;
-- SELECT * FROM Jobs_General_Words;