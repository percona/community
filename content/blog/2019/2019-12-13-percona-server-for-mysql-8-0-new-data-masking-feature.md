---
title: 'Percona Server for MySQL 8.0 – New Data Masking Feature'
date: Fri, 13 Dec 2019 10:43:14 +0000
draft: false
tags: ['data obfuscation', 'data privacy', 'identity protection', 'Intermediate Level', 'MySQL', 'Percona Server for MySQL']
authors:
  - francisco_miguel
images:
  - blog/2019/12/data-masking-Percona-Server-for-MySQL.jpg
slug: percona-server-for-mysql-8-0-new-data-masking-feature
---
 

Database administrators are responsible for maintaining the privacy and integrity of data. When the data contains confidential information, your company has a legal obligation to ensure that privacy is maintained. Even so, being able to access the information contained in that dataset, for example for testing or reporting purposes, has great value so what to do? [MySQL Enterprise Edition](https://dev.mysql.com/doc/refman/8.0/en/data-masking.html) offers data masking and de-identification, so I decided to contribute similar functionality to [Percona Server for MySQL](https://www.percona.com/doc/percona-server/LATEST/security/data-masking.html). In this post, I provide some background context and information on how to use these new functions in practice.

![Data Masking in Percona Server for MySQL 8.0.17](blog/2019/12/data-masking-Percona-Server-for-MySQL.jpg)

Some context
------------

One of the most important assets of any company is data. Having good data allows engineers to build better systems and user experiences. 

Even through our most trivial activities, we continuously generate and share great volumes of data. I'm walking down the street and if I take a look at my phone it's quite straightforward to get recommendations for a place to have lunch. The platform knows that it's almost lunch time and that I have visited this nearby restaurant, or a similar one, a few times in the past. Sounds cool, right? 

But this process could be more manual than we might think at first. Even if the system has implemented things like AI or Machine Learning, a human will have validated the results; they might have taken a peek to ensure that everything is fine; or perhaps they are developing some new cool feature that must be tested... And this means that someone, somewhere has the ability to access my data. Or your data. 

Now, that is not so great, is it? 

In the last decade or so, governments around the world have taken this challenge quite seriously. They have enforced a series of rules to guarantee that the data is not only safely stored, but also safely used. I'm sure you will have heard terms like PCI, GDPR or HIPAA. They contain mandatory guidelines for how our data can be used, for primary or secondary purposes, and if it can be used at all.

Data masking and de-identification
----------------------------------

One of the most basic safeguarding rules is that if the data is to be used for secondary purposes – such as for data analytics – it has to be de-identified in a way that it would make impossible identify the original individual. 

Let's say that the company ACME is storing employee data. 

We will use the [example database of employees](https://github.com/datacharmer/test_db) that's freely available.
```
Employee number
First name
Last name
Birth date
Gender
Hire date
Gross salary
Salary from date
Salary to date
```
We can clearly see that all those fields can be classified as private information. Some of these directly identify the original individual, like employee number or first + last name. Others could be used for indirect identification: I could ask my co-workers their birthday and guess the owner of that data using birth date. 

So, here is where de-identification and data-masking come into play. But what are the differences? 

**De-identification** transforms the original data into something different that could look more or less real. For example, I could de-identify birth date and get a different date. 

However, this method would make that information unusable if I want to see the relationship between salary and employee's age. 

On the other hand, **data-masking** transforms the original data leaving some part untouched. I could mask birth date replacing the month and day for January first. That way, the year would be retained and that would allow us to identify that salary–employee's age relationship. 

Of course, if the dataset I'm working with is not big enough, certain methods of data-masking would be inappropriate as I could still deduce who the data belonged to.

MySQL data masking
------------------

**Oracle's MySQL Enterprise Edition** offers a [de-identification and data-masking solution for MySQL](https://dev.mysql.com/doc/refman/8.0/en/data-masking.html), using a flexible set of functions that cover most of our needs. 

**Percona Server for MySQL 8.0.17** introduces that functionality as [an open source plugin](https://www.percona.com/doc/percona-server/LATEST/security/data-masking.html), and is compatible with Oracle's implementation. You no longer need to code slow and complicated stored procedures to achieve data masking, and you can migrate the processes that were written for the MySQL Enterprise Edition to Percona Server for MySQL. Go grab a cup of coffee and contribute something cool to the community with all that time you have got back. ☺

In the lab
----------

Put on your thinking cap and let's see how it works. 

First we need an instance of Percona MySQL Server 8.0.17 or newer. I think containers are the most flexible way to test new stuff so I will be using that, but you could use a virtual server or just a traditional setup. Let’s download the latest version of Percona MySQL Server in a ready to run container:
```
docker pull percona:8.0.17-1
```
Eventually that command should work but sadly, Percona hadn't built this version of the docker image when this article was written. Doing it yourself is quite simple, though, and by the time you read this it will likely be already there. 

Once in place, Running an instance of Percona MySQL Server has never been so easy:
```
docker run --name ps -e MYSQL_ROOT_PASSWORD=secret -d percona:8.0.17-8
```
We'll logon to the new container:
```
docker exec -ti ps mysql -u root -p
```
Now is the time to download the test database employees from [GitHub](https://github.com/datacharmer/test_db) and load it into our Percona Server. You can follow the official instructions in the project page. 

Next step is to enable the data de-identification and masking feature. Installing the data masking module in Percona MySQL Server is easier than in Oracle.
```
mysql> INSTALL PLUGIN data_masking SONAME 'data_masking.so';
Query OK, 0 rows affected (0.06 sec)
```
This automatically defines a set of global functions in our MySQL instance, so we don't need to do anything else.

### A new concept: Dictionaries

Sometimes we will like to generate new data selecting values from a predefined collection. For example we could want to have first name  values that are really first names and not a random alphanumeric. This will make our masked data looks real, and it’s perfect for creating demo or QA environments. 

For this task we have **dictionaries**. They are nothing more than text files containing a value per line that are loaded into MySQL memory. You need to be aware that the contents of the file are fully loaded into memory and that the dictionary only exists while MySQL is running. So keep this in mind before loading any huge file or after restarting the instance. 

For our lab we will load two dictionaries holding first and last names. You can use these files or create different ones: [first names](https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/first_names.all.txt) and [last names](https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/last_names.all.txt) 

Store the files in a folder of your database server (or container) readable by the mysqld  process.
```
wget https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/first_names.all.txt
docker cp first_names.all.txt ps:/tmp/
wget https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/last_names.all.txt
docker cp last_names.all.txt ps:/tmp/
```
Once the files are in our server we can map them as MySQL dictionaries.
```
mysql> select gen_dictionary_load('/tmp/first_names.all.txt', 'first_names');
+----------------------------------------------------------------+
| gen_dictionary_load('/tmp/first_names.all.txt', 'first_names') |
+----------------------------------------------------------------+
| Dictionary load success                                        |
+----------------------------------------------------------------+
1 row in set (0.04 sec)

mysql> select gen_dictionary_load('/tmp/last_names.all.txt', 'last_names');
+--------------------------------------------------------------+
| gen_dictionary_load('/tmp/last_names.all.txt', 'last_names') |
+--------------------------------------------------------------+
| Dictionary load success                                      |
+--------------------------------------------------------------+
1 row in set (0.03 sec)
```

### Masking some data

Now let's take another look at our employees table
```
mysql> show columns from employees;
+------------+---------------+------+-----+---------+-------+
| Field      | Type          | Null | Key | Default | Extra |
+------------+---------------+------+-----+---------+-------+
| emp_no     | int(11)       | NO   | PRI | NULL    |       |
| birth_date | date          | NO   |     | NULL    |       |
| first_name | varchar(14)   | NO   |     | NULL    |       |
| last_name  | varchar(16)   | NO   |     | NULL    |       |
| gender     | enum('M','F') | NO   |     | NULL    |       |
| hire_date  | date          | NO   |     | NULL    |       |
+------------+---------------+------+-----+---------+-------+
```
Ok, it's very likely we will want to de-identify everything in this table. You can apply different methods to achieve your security requirements, but I will create a view with the following transformations:

*   **emp_no**: get a random value from 900.000.000 to 999.999.999
*   **birth_date**: set it to January 1st of the original year
*   **first_name**: set a random first name from a list of names that we have in a text file
*   **last_name**: set a random last name from a list of names that we have in a text file
*   **gender**: no transformation
*   **hire_date**: set it to January 1st of the original year

```
CREATE VIEW deidentified_employees
AS
SELECT
  gen_range(900000000, 999999999) as emp_no,
  makedate(year(birth_date), 1) as birth_date,
  gen_dictionary('first_names') as first_name,
  gen_dictionary('last_names') as last_name,
  gender,
  makedate(year(hire_date), 1) as hire_date
FROM employees;
```
Let's check how the data looks in our de-identified view.
```
mysql> SELECT * FROM employees LIMIT 10;
+--------+------------+------------+-----------+--------+------------+
| emp_no | birth_date | first_name | last_name | gender | hire_date  |
+--------+------------+------------+-----------+--------+------------+
|  10001 | 1953-09-02 | Georgi     | Facello   | M      | 1986-06-26 |
|  10002 | 1964-06-02 | Bezalel    | Simmel    | F      | 1985-11-21 |
|  10003 | 1959-12-03 | Parto      | Bamford   | M      | 1986-08-28 |
|  10004 | 1954-05-01 | Chirstian  | Koblick   | M      | 1986-12-01 |
|  10005 | 1955-01-21 | Kyoichi    | Maliniak  | M      | 1989-09-12 |
|  10006 | 1953-04-20 | Anneke     | Preusig   | F      | 1989-06-02 |
|  10007 | 1957-05-23 | Tzvetan    | Zielinski | F      | 1989-02-10 |
|  10008 | 1958-02-19 | Saniya     | Kalloufi  | M      | 1994-09-15 |
|  10009 | 1952-04-19 | Sumant     | Peac      | F      | 1985-02-18 |
|  10010 | 1963-06-01 | Duangkaew  | Piveteau  | F      | 1989-08-24 |
+--------+------------+------------+-----------+--------+------------+
10 rows in set (0.00 sec)

mysql> SELECT * FROM deidentified_employees LIMIT 10;
+-----------+------------+------------+---------------+--------+------------+
| emp_no    | birth_date | first_name | last_name     | gender | hire_date  |
+-----------+------------+------------+---------------+--------+------------+
| 930277580 | 1953-01-01 | skaidrīte  | molash        | M      | 1986-01-01 |
| 999241458 | 1964-01-01 | grasen     | cessna        | F      | 1985-01-01 |
| 951699030 | 1959-01-01 | imelda     | josephpauline | M      | 1986-01-01 |
| 985905688 | 1954-01-01 | dunc       | burkhardt     | M      | 1986-01-01 |
| 923987335 | 1955-01-01 | karel      | wanamaker     | M      | 1989-01-01 |
| 917751275 | 1953-01-01 | mikrut     | allee         | F      | 1989-01-01 |
| 992344830 | 1957-01-01 | troyvon    | muma          | F      | 1989-01-01 |
| 980277046 | 1958-01-01 | aliziah    | tiwnkal       | M      | 1994-01-01 |
| 964622691 | 1952-01-01 | dominiq    | legnon        | F      | 1985-01-01 |
| 948247243 | 1963-01-01 | sedale     | tunby         | F      | 1989-01-01 |
+-----------+------------+------------+---------------+--------+------------+
10 rows in set (0.01 sec)
```
The data looks quite different, but remains good enough to apply some analytics and get meaningful results. Let's de-identify the table salaries  this time.
```
mysql> show columns from salaries;
+-----------+---------+------+-----+---------+-------+
| Field     | Type    | Null | Key | Default | Extra |
+-----------+---------+------+-----+---------+-------+
| emp_no    | int(11) | NO   | PRI | NULL    |       |
| salary    | int(11) | NO   |     | NULL    |       |
| from_date | date    | NO   | PRI | NULL    |       |
| to_date   | date    | NO   |     | NULL    |       |
+-----------+---------+------+-----+---------+-------+
```
We could use something like this:
```
CREATE VIEW deidentified_salaries
AS
SELECT
gen_range(900000000, 999999999) as emp_no,
gen_range(40000, 80000) as salary,
mask_inner(date_format(from_date, '%Y-%m-%d'), 4, 0) as from_date,
mask_outer(date_format(to_date, '%Y-%m-%d'), 4, 2, '0') as to_date
FROM salaries;
```
We are using again the function gen_range . For the dates this time we are using the very flexible functions mask_inner  and mask_outer  that replace some characters in the original string. Let's see how the data looks now.

> In a real life exercise we would like to have the same values for emp_no across all the tables to keep referential integrity. This is where I think the original MySQL data-masking plugin falls short, as we don't have deterministic functions using the original value as seed.

```
mysql> SELECT * FROM salaries LIMIT 10;
+--------+--------+------------+------------+
| emp_no | salary | from_date  | to_date    |
+--------+--------+------------+------------+
|  10001 |  60117 | 1986-06-26 | 1987-06-26 |
|  10001 |  62102 | 1987-06-26 | 1988-06-25 |
|  10001 |  66074 | 1988-06-25 | 1989-06-25 |
|  10001 |  66596 | 1989-06-25 | 1990-06-25 |
|  10001 |  66961 | 1990-06-25 | 1991-06-25 |
|  10001 |  71046 | 1991-06-25 | 1992-06-24 |
|  10001 |  74333 | 1992-06-24 | 1993-06-24 |
|  10001 |  75286 | 1993-06-24 | 1994-06-24 |
|  10001 |  75994 | 1994-06-24 | 1995-06-24 |
|  10001 |  76884 | 1995-06-24 | 1996-06-23 |
+--------+--------+------------+------------+
10 rows in set (0.00 sec)

mysql> SELECT * FROM deidentified_salaries LIMIT 10;
+-----------+--------+------------+------------+
| emp_no    | salary | from_date  | to_date    |
+-----------+--------+------------+------------+
| 929824695 | 61543  | 1986XXXXXX | 0000-06-00 |
| 954275265 | 63138  | 1987XXXXXX | 0000-06-00 |
| 948145700 | 53448  | 1988XXXXXX | 0000-06-00 |
| 937927997 | 54704  | 1989XXXXXX | 0000-06-00 |
| 978459605 | 78179  | 1990XXXXXX | 0000-06-00 |
| 993464164 | 75526  | 1991XXXXXX | 0000-06-00 |
| 946692434 | 51788  | 1992XXXXXX | 0000-06-00 |
| 979870243 | 54807  | 1993XXXXXX | 0000-06-00 |
| 958708118 | 70647  | 1994XXXXXX | 0000-06-00 |
| 945701146 | 76056  | 1995XXXXXX | 0000-06-00 |
+-----------+--------+------------+------------+
10 rows in set (0.00 sec)
```

### Clean-up

Remember that when you're done, you can free up memory by removing the dictionaries. Restarting the instance will also remove the dictionaries.
```
mysql> SELECT gen_dictionary_drop('first_names');
+------------------------------------+
| gen_dictionary_drop('first_names') |
+------------------------------------+
| Dictionary removed                 |
+------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT gen_dictionary_drop('last_names');
+------------------------------------+
| gen_dictionary_drop('last_names') |
+------------------------------------+
| Dictionary removed                 |
+------------------------------------+
1 row in set (0.01 sec)
```
If you use the MySQL data-masking plugin to define different levels of access to the data, remember that you will need to load the dictionaries each time the instance is restarted. With this usage, for example, you could control the data that someone in support has access to, very much like a bargain-basement virtual private database solution. (I'm not proposing this for production systems!)

Other de-identification and masking functions
---------------------------------------------

Percona Server for MySQL Data-Masking includes more functions that the ones we've seen here. We have specialized functions for Primary Account Numbers (PAN), Social Security Numbers (SSN), phone numbers, e-Mail addresses... And also generic functions that will allow us to de-identify types without a specialized method. Being an open source plugin it should be quite easy to implement any additional methods and contribute it to the broader community.

Next Steps
----------

Using these functions we can de-identify and mask any existing dataset. But if you are populating a lower level environment using production data you would want to store the transformed data only. To achieve this you could choose between various options.

*   **Small volumes of data**: use "de-identified" views to export the data and load into a new database using mysqldump or mysqlpump.
*   **Medium volumes of data**: Clone the original database and de-identify locally the data using updates.
*   **Large volumes of data option one**: using replication, create a master -> slave chain with STATEMENT binlog format and define triggers de-identifying the data on the slave. Your master can be a slave to the master (using log_slave_updates), so you don't need to run your primary master in STATEMENT mode.
*   **Large volumes of data option two**: using multiplexing in [ProxySQL](https://www.proxysql.com/), configure ProxySQL to send writes to a clone server where you have defined triggers to de-identify the data.

Future developments
-------------------

While de-identifying complex schemas we could find that, for example, the name of a person is stored in multiple tables (de-normalized tables). In this case, these functions would generate different names and the resulting data will look broken. You can solve this using a variant of the dictionary functions that will obtain the value based on the original value and passed as parameter:
```
gen_dictionary_deterministic('Francisco', 'first_names')
```
This not-yet-available function would always return the same value using that dictionary file, but in such a way that the de-identification cannot be reversed. Oracle doesn't currently support this, so we will expand Percona Data-Masking plugin to introduce this as a unique feature. However, that will be in another contribution, so stay tuned for more exciting changes to Percona Server for MySQL Data Masking. 

_--_ 

_Image: Photo by [Finan Akbar](https://unsplash.com/@finan?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/mask?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_ 

The content in this blog is provided in good faith by members of the open source community. Percona has not edited or tested the technical content (although in this case, of course, we have tested the data masking feature incorporated into Percona Server for MySQL 8.0/17, just not the examples in this blog). Views expressed are the authors’ own. When using the advice from this or any other online resource test ideas before applying them to your production systems, and always secure a working back up.