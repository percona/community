---
title: 'Export to JSON from MySQL All Ready for MongoDB'
date: Tue, 16 Oct 2018 15:18:36 +0000
draft: false
tags: ['author_aftabkhan', 'Entry Level', 'export data', 'MongoDB', 'MySQL', 'tools', 'Tools']
authors:
  - aftab_khan
images:
  - blog/2018/10/export-data-to-JSON-from-MySQL.jpg
---

This post walks through how to export data from [MySQL](https://dev.mysql.com/)® into JSON format, ready to ingest into [MongoDB](https://www.mongodb.com/)®. Starting from MySQL 5.7+, there is native support for JSON. MySQL provides functions that actually create JSON values, so I will be using these functions in this article to export to JSON from MySQL:

*   JSON_OBJECT
*   JSON_ARRAY

These functions make it easy to convert MySQL data to JSON e.g.
```
mysql> SELECT json_object('employee_id', emp_no, 'first_name', first_name ) AS 'JSON' FROM employees LIMIT 2;
+------------------------------------------------+
| JSON |
+------------------------------------------------+
| {"first_name": "Aamer", "employee_id": 444117} |
| {"first_name": "Aamer", "employee_id": 409151} |
+------------------------------------------------+
2 rows in set (0.00 sec)
```
In this article, I will be using the employees sample database available from here: [https://dev.mysql.com/doc/employee/en/employees-installation.html](https://dev.mysql.com/doc/employee/en/employees-installation.html) 

You can find the employees schema on [dev.mysql.com](https://dev.mysql.com/doc/employee/en/images/employees-schema.png).

When mapping relations with collections, generally there is no one to one mapping, you would want to merge data from some MySQL tables into a single collection.

Export data to JSON format
--------------------------

To export data, I have constructed the following SQL (the data is combined from 3 different tables: employees, salaries, and departments):
```
SELECT json_pretty(json_object(
'emp_no', emp.emp_no, 
'first_name', emp.first_name, 
'last_name', emp.last_name, 
'hire_date',
json_object("$date", DATE_FORMAT(emp.hire_date,'%Y-%m-%dT%TZ')),
'Department', JSON_ARRAY(json_object('dept_id', dept.dept_no, 'dept_name', dept.dept_name)), 
'Salary', s.salary)) AS 'json' 
FROM employees emp
INNER JOIN salaries s ON s.emp_no=emp.emp_no
INNER JOIN current_dept_emp c on c.emp_no = emp.emp_no
INNER JOIN departments dept on dept.dept_no = c.dept_no
LIMIT 1;

Output:

*************************** 1. row ***************************
json: {
"Salary": 60117,
"emp_no": 10001,
"hire_date": "1986-06-26",
"last_name": "Facello",
"Department": [
{
"dept_id": "d005",
"dept_name": "Development"
}
],
"first_name": "Georgi"
}
```
You can see from this that json_object did not convert 'hire_date' column value to be compatible with MongoDB.  We have to convert date into ISODate format:
```
mysql> select json_object('hire_date', hire_date) AS "Original Date", json_object('hire_date', DATE_FORMAT(hire_date,'%Y-%m-%dT%TZ')) AS "ISODate" from employees limit 1;
+-----------------------------+---------------------------------------+
| Original Date | ISODate |
+-----------------------------+---------------------------------------+
| {"hire_date": "1985-01-01"} | {"hire_date": "1985-01-01T00:00:00Z"} |
+-----------------------------+---------------------------------------+
1 row in set (0.00 sec)


```
Next, we dump the output to a file (the above query is slightly modified) e.g.
```
SELECT json_object(
'emp_no', emp.emp_no,
'first_name', emp.first_name, 
'last_name', emp.last_name, 
'hire_date', json_object("$date", DATE_FORMAT(emp.hire_date,'%Y-%m-%dT%TZ')), 
'Department', JSON_ARRAY(json_object('dept_id', dept.dept_no, 'dept_name', dept.dept_name)),
'Salary', s.salary) as 'json' 
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/employees.json' ## IMPORTANT you may want to adjust outfile path here
FROM employees emp
INNER JOIN salaries s ON s.emp_no=emp.emp_no
INNER JOIN current_dept_emp c on c.emp_no = emp.emp_no
INNER JOIN departments dept on dept.dept_no = c.dept_no
```

Importing data
--------------

To load the file employees.json  into MongoDB, I use the [mongoimport](https://docs.mongodb.com/manual/reference/program/mongoimport/) utility.  It's a multi-threaded tool that can load large files efficiently.
```
# mongoimport --db test --collection employees --drop < employees.json
2018-10-05T12:32:30.401+0100 connected to: localhost
2018-10-05T12:32:30.401+0100 dropping: test.employees
2018-10-05T12:32:33.400+0100 test.employees 34.0MB
2018-10-05T12:32:36.401+0100 test.employees 67.3MB
2018-10-05T12:32:39.399+0100 test.employees 100MB
2018-10-05T12:32:42.400+0100 test.employees 134MB
2018-10-05T12:32:45.401+0100 test.employees 168MB
2018-10-05T12:32:48.402+0100 test.employees 202MB
2018-10-05T12:32:51.402+0100 test.employees 235MB
2018-10-05T12:32:54.400+0100 test.employees 269MB
2018-10-05T12:32:57.400+0100 test.employees 303MB
2018-10-05T12:33:00.403+0100 test.employees 335MB
2018-10-05T12:33:03.404+0100 test.employees 368MB
2018-10-05T12:33:06.399+0100 test.employees 397MB
2018-10-05T12:33:09.400+0100 test.employees 430MB
2018-10-05T12:33:12.400+0100 test.employees 465MB
2018-10-05T12:33:15.403+0100 test.employees 499MB
2018-10-05T12:33:18.401+0100 test.employees 530MB
2018-10-05T12:33:18.589+0100 test.employees 533MB
2018-10-05T12:33:18.589+0100 imported 2844047 documents
```

Validate
--------

```
> db.employees.find({}).pretty()
{
"_id" : ObjectId("5bb740cfd73e26bf45435181"),
"Salary" : 60117,
"emp_no" : 10001,
"hire_date" : ISODate("1986-06-26T00:00:00Z"),
"last_name" : "Facello",
"Department" : [
{
"dept_id" : "d005",
"dept_name" : "Development"
}
],
"first_name" : "Georgi"
}
```
We have successfully migrated some data from MySQL to MongoDB! 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors’ own. When using the advice from this or any other online resource **test** ideas before applying them to your production systems, and **always **secure a working back up._