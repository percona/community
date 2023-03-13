---
title: 'How To Generate Test Data for Your Database Project With Python'
date: "2023-01-09T00:00:00+00:00"
draft: false
tags: ['Python', 'MySQL', 'PostgreSQL', 'MongoDB']
authors:
  - mario_garcia
images:
  - blog/2023/01/testing_data.png
slug: how-to-generate-test-data-for-your-database-project-with-python
---

If you need test data for the database of your project, you can get a dataset from [Kaggle](https://kaggle.com) or use a data generator. In the first case, if you need to process the data before inserting it into the database, you can use [Pandas](https://pandas.pydata.org/), a widely used Python library for data analysis. This library supports different formats, including CSV and JSON, and it also provides a method for inserting data into a SQL database.

If you choose a data generator instead, you can find one for [MySQL](https://github.com/Percona-Lab/mysql_random_data_load) in one of the repositories on our [Percona Lab](https://github.com/Percona-Lab) GitHub account. Are you using other database technologies? You can follow the guides I already published where I explain how to create your own data generator for [MySQL](https://www.percona.com/blog/how-to-generate-test-data-for-mysql-with-python/) (it could work for PostgreSQL) and [MongoDB](https://www.percona.com/blog/how-to-generate-test-data-for-mongodb-with-python/).

If you create you’re own data generator, this is the process you must follow:

* Generate fake data using Faker
* Store generated data in a Pandas DataFrame
* Establish a connection to your database
* Insert the content of the DataFrame into the database

## Requirements
### Dependencies
Make sure all the dependencies are installed before creating the Python script that will generate the data for your project.

You can create a `requirements.txt` file with the following content:

```
pandas
tqdm
faker
```

Or if you’re using Anaconda, create an `environment.yml` file:

```yaml
name: percona
dependencies:
  - python=3.10
  - pandas
  - tqdm
  - faker
```

You can change the Python version as this script has been proven to work with these versions of Python: 3.7, 3.8, 3.9, 3.10, and 3.11.

Depending on the database technology you’re using, you must add the corresponding package to your `requirements.txt` or `environment.yml` file:

* MySQL → `PyMySQL`
* PostgreSQL → `psycopg2`
* MongoDB → `pymongo`

Run the following command if you’re using `pip`:

```bash
pip install -r requirements.txt
```

Or run the following statement to configure the project environment when using Anaconda:

```bash
conda env create -f environment.yml
```

### Database
Now that you have the dependencies installed, you must create a database named `company`, for MySQL or PostgreSQL.

Log into MySQL:

```bash
$ mysql -u root -p
```

Replace `root` with your username, if necessary, and replace `localhost` with the IP address or URL of your MySQL server instance if needed.

Or log into PostgreSQL:

```bash
$ sudo su postgres
$ psql
```

and create the `company` database:

```sql
create database company;
```

You don’t need to create the MongoDB database previously.

## Creating a Pandas DataFrame
Before creating the script, it’s important to know that we need to implement multiprocessing for optimizing the execution time of the script.

[Multiprocessing](https://docs.python.org/3/library/multiprocessing.html) is a way to take advantage of the CPU cores available in the computer where the script is running. In Python, single-CPU use is caused by the [global interpreter lock](https://realpython.com/python-gil/), which allows only one thread to carry the Python interpreter at any given time. With multiprocessing, all the workload is divided into every CPU core available. For more information see [this blog post](https://urban-institute.medium.com/using-multiprocessing-to-make-python-code-faster-23ea5ef996ba).

Now, let’s start creating our own data generator. First, a `modules` directory needs to be created, and inside the directory, we will create a module named `dataframe.py`. This module will be imported later into our main script, and this is where we define the method that will generate the data.

You need to import the required libraries and methods:

```python
from multiprocessing import cpu_count
import pandas as pd
from tqdm import tqdm
from faker import Faker
```

* `pandas`. Data generated with Faker will be stored in a Pandas DataFrame before being imported into the database.
* `tqdm()`. This method is required for adding a progress bar to show the progress of the DataFrame creation.
* `Faker()`. It’s the generator from the faker library.
* `cpu_count()`. This is a method from the multiprocessing module that will return the number of cores available.

Then, a faker generator will be created and initialized, by calling the `Faker()` method. This is required to generate data by accessing the properties in the Faker library.

And we determine the number of cores of the CPU available, by calling the `cpu_count()` method and assigning this value to the `num_cores variable`.

```python
fake = Faker()
num_cores = cpu_count() - 1
```

`num_cores` is a variable that stores the value returned after calling the `cpu_count()` method. We use all the cores minus one to avoid freezing the computer.

```python
def create_dataframe(arg):
    x = int(60000/num_cores)
    data = pd.DataFrame()
    for i in tqdm(range(x), desc='Creating DataFrame'):
        data.loc[i, 'first_name'] = fake.first_name()
        data.loc[i, 'last_name'] = fake.last_name()
        data.loc[i, 'job'] = fake.job()
        data.loc[i, 'company'] = fake.company()
        data.loc[i, 'address'] = fake.address()
        data.loc[i, 'city'] = fake.city()
        data.loc[i, 'country'] = fake.country()
        data.loc[i, 'email'] = fake.email()
    return data
```

Then, we define the `create_dataframe()` function, where:

* `x` is the variable that will determine the number of iterations of the `for` loop where the DataFrame is created.
* `data` is an empty DataFrame that will later be fulfilled with data generated with Faker.
* Pandas [DataFrame.loc](https://www.geeksforgeeks.org/python-pandas-dataframe-loc/) attribute provides access to a group of rows and columns by their label(s). In each iteration, a row of data is added to the DataFrame and this attribute allows assigning values to each column.

The DataFrame that is created after calling this function will have the following columns:

```bash
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   first_name  60000 non-null  object
 1   last_name   60000 non-null  object
 2   job         60000 non-null  object
 3   company     60000 non-null  object
 4   address     60000 non-null  object
 5   country     60000 non-null  object
 6   city        60000 non-null  object
 7   email       60000 non-null  object
```

**Note**: The script is generating 60 thousand records but it can be adapted to your project, you can modify this value in the `x` variable.

## Connection to the Database
### MySQL and PostgreSQL
Before inserting the data previously generated with Faker, we need to establish a connection to the database, and for doing this the SQLAlchemy library will be used.

[SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
engine = create_engine("mysql+pymysql://user:password@localhost/company")
Session = sessionmaker(bind=engine)
```

From SQLAlchemy, we import the `create_engine()` and the `sessionmaker()` methods. The first one is for connecting to the database, and the second one is for creating a session bond to the engine object.

Don’t forget to replace `user`, `password`, and `localhost` with your authentication details. Save this code in the `modules` directory and name it as `base.py`.

For PostgreSQL, replace:

```python
engine = create_engine("mysql+pymysql://user:password@localhost/company")
```

With:

```python
engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/company")
```

### Database Schema Definition
For MySQL and PostgreSQL, the schema of the database can be defined through the [Schema Definition Language](https://docs.sqlalchemy.org/en/14/core/schema.html) provided by SQLAlchemy, but as we’re only creating one table and importing the DataFrame by calling Pandas to_sql() method, this is not necessary.


When calling Pandas `to_sql()` method, we define the schema as follows:

```python
from sqlalchemy.types import *
schema = {
    "first_name": String(50),
    "last_name": String(50),
    "job": String(100),
    "company": String(100),
    "address": String(200),
    "city": String(100),
    "country" String(100),
    "email": String(50)
}
```

Then we pass the `schema` variable as a parameter to this method.

Save this code in the `modules` directory with the name `schema.py`.

### MongoDB
Before inserting the data previously generated with Faker, we need to establish a connection to the database, and for doing this the [PyMongo](https://pypi.org/project/pymongo/) library will be used.

```python
from pymongo import MongoClient
 
uri = "mongodb://user:password@localhost:27017/"
client = MongoClient(uri)
```

From PyMongo, we import the `MongoClient()` method.

Don’t forget to replace `user`, `password`, `localhost`, and `port` (27017) with your authentication details. Save this code in the modules directory and name it `base.py`.


## Generating Your Data
### MySQL and PostgreSQL
All the required modules are now ready to be imported into the main script, now it’s time to create the `sql.py` script. First, import the required libraries:

```python
from multiprocessing import Pool
from multiprocessing import cpu_count
import pandas as pd
```

From multiprocessing, `Pool()` and `cpu_count()` are required. The [Python Multiprocessing Pool](https://superfastpython.com/multiprocessing-pool-python/#:~:text=The%20Python%20Multiprocessing%20Pool%20class,Processes%20and%20Threads%20in%20Python.) class allows you to create and manage process pools in Python.

Then, import the modules previously created:

```python
from modules.dataframe import create_dataframe
from modules.schema import schema
from modules.base import Session, engine
```

Now we create the multiprocessing pool, configured to use all available CPU cores minus one. Each core will call the `create_dataframe()` function and create a DataFrame with 4 thousand records. After each call to the function has finished, all the DataFrames created will be concatenated into a single one.

```python
if __name__ == "__main__":
    num_cores = cpu_count() - 1
    with Pool() as pool:
        data = pd.concat(pool.map(create_dataframe, range(num_cores)))
    data.to_sql(name='employees', con=engine, if_exists = 'append', index=False, dtype=schema)
```

And finally, we will insert the DataFrame into the MySQL database by calling the `to_sql()` method. All the data will be stored in a table named employees.

The table `employees` is created without a primary key, so we execute the following SQL statement to add an `id` column that is set to be the primary key of the table.

```python
with engine.connect() as conn:
        conn.execute("ALTER TABLE employees ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")
```

For PostgreSQL, replace this line:

```python
conn.execute("ALTER TABLE employees ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")
```

With:

```python
conn.execute("ALTER TABLE employees ADD COLUMN id SERIAL PRIMARY KEY;")
```

### MongoDB
All the required modules are now ready to be imported into the main script, now it’s time to create the `mongodb.py` script. First, import the required libraries:

```python
from multiprocessing import Pool
from multiprocessing import cpu_count
import pandas as pd
```

From multiprocessing, `Pool()` and `cpu_count()` are required. The [Python Multiprocessing Pool](https://superfastpython.com/multiprocessing-pool-python/#:~:text=The%20Python%20Multiprocessing%20Pool%20class,Processes%20and%20Threads%20in%20Python.) class allows you to create and manage process pools in Python.

Then, import the modules previously created:

```python
from modules.dataframe import create_dataframe
from modules.base import client
```

Now we create the multiprocessing pool, configured to use all available CPU cores minus one. Each core will call the `create_dataframe()` function and create a DataFrame with 4 thousand records. After each call to the function has finished, all the DataFrames created will be concatenated into a single one.

```python
if __name__ == "__main__":
    num_cores = cpu_count() - 1
    with Pool() as pool:
        data = pd.concat(pool.map(create_dataframe, range(num_cores)))
    data_dict = data.to_dict('records')
    db = client["company"]
    collection = db["employees"]
    collection.insert_many(data_dict)
```

After logging into the MongoDB server, we specify the database and the collection where the data will be stored.

And finally, we will insert the DataFrame into MongoDB by calling the `insert_many()` method. All the data will be stored in a collection named `employees`.

## Running the script
Run the following statement to populate the table:

```bash
$ python sql.py
```

Or:

```bash
$ python mongodb.py
```

![Multiprocessing](/blog/2023/01/multiprocessing.png)

Execution time depends on the CPU cores available on your machine. I'm running this script on an Intel i7 1260P that has 16 cores, but using 15.

![CPU Utilization](/blog/2023/01/cpu-utilization.png)

## Query Your Data
Once the script finishes, you can check the data in the database.

### MySQL and PostgreSQL

Connect to the `company` database.

MySQL:

```sql
use company;
```

PostgreSQL:

```sql
\c company
```

Then, get the number of records.

```sql
select count(*) from employees;
```

The `count()` function returns the number of records in the `employees` table.

```bash
+----------+
| count(*) |
+----------+
|    60000 |
+----------+
1 row in set (0.22 sec)
```

### MongoDB
```
use company;
db.employees.count()
```

The `count()` function returns the number of records in the `employees` table.

```
60000
```

Or you can display the records in the `employees` table:

```
db.employees.find().pretty()
```

The code shown in this blog post can be found on my GitHub account in the [data-generator](https://github.com/mattdark/data-generator) repository.
