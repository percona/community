---
title: "PostgreSQL: Query Optimization With Python and PgBouncer"
date: "2023-04-25T00:00:00+00:00"
draft: false
tags: ["PostgreSQL", "Python"]
authors:
  - mario_garcia
images:
  - blog/2023/04/database-application.jpg
slug: postgresql-query-optimization-with-python-and-pgbouncer
---

![Database application](/blog/2023/04/database-application.jpg "Database application by Nick Youngson CC BY-SA 3.0 Pix4free")

A few months ago I wrote a few blog posts on how to generate test data for your database project using Python, which you can find on the Percona blog and the Community blog:

- [How To Generate Test Data for MySQL with Python](https://www.percona.com/blog/how-to-generate-test-data-for-mysql-with-python/)
- [How To Generate Test Data for MongoDB With Python](https://www.percona.com/blog/how-to-generate-test-data-for-mongodb-with-python/)
- [How To Generate Test Data for Your Database Project With Python](https://percona.community/blog/2023/01/09/how-to-generate-test-data-for-your-database-project-with-python/)

The basic idea is to create a script that uses [Faker](https://github.com/joke2k/faker), a Python library for generating fake data, and what the script does is

- Divide the whole process into every CPU core available by implementing multiprocessing
- The script will generate a total of 60 thousand records, divided by the number of CPU cores minus one
- Each set of records is stored in a Pandas DataFrame, then concatenated into a single DataFrame
- The DataFrame is inserted into the database using Pandas’ `to_sql` method, and pymongo’s `insert_many` method

How can the script be optimized? Instead of generating the data, storing it in a DataFrame, and then inserting it into the database, you can make every CPU core insert the data while generating it without storing it elsewhere before running the corresponding SQL statements. Multiprocessing is implemented to use every CPU core available but you also need to configure a connection pool for your PostgreSQL server.

Through this blog post, you will learn how to install and configure PgBouncer with Python to implement a connection pool for your application.

## PgBouncer
[PgBouncer](https://www.pgbouncer.org/) is a PostgreSQL connection pooler. Any target application can be connected to PgBouncer as if it were a PostgreSQL server, and PgBouncer will create a connection to the actual server, or it will reuse one of its existing connections.

The aim of PgBouncer is to lower the performance impact of opening new connections to PostgreSQL.

### Installation
Ir you’re an Ubuntu user, you can install PgBouncer from the repositories:

```
$ sudo apt install pgbouncer -y
```

If not available in the repositories, you can follow the instructions below for both Debian and Ubuntu as mentioned in the Scaleway documentation

1. Create the `apt` repository configuration file

```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

2. Import the repository signing key

```
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
```

3. Update the `apt` package manager

```
$ sudo apt update
```

4. Install PgBouncer using `apt`

```
$ sudo apt install pgbouncer -y
```

### Configuration
After installing PgBouncer, edit the configuration files, as stated in the Scaleway [documentation](https://www.scaleway.com/en/docs/tutorials/install-pgbouncer/).

1. Set up the PostgreSQL server details in `/etc/pgbouncer/pgbouncer.ini`

```
database_name = host=localhost port=5432 dbname=database_name
```

You may also want to set `listen_addr` to `*` if you want to to listen to TCP connections on all addresses or set a list of IP addresses.

Default `listen_port` is `6432`

From [this article](https://www.compose.com/articles/how-to-pool-postgresql-connections-with-pgbouncer/) by Abdullah Alger,  the settings `max_client_conn` and `default_pool_size`, the former refers to the number of applications that will make connections and the latter is how many server connections per database. The defaults are set at `100` and `20`, respectively.

2. Edit the `/etc/pgbouncer/userlist.txt` file and add your PostgreSQL credentials

```
“username” “password”
```

3. Add the IP address of the PgBouncer server to the PostgreSQL `pg_hba.conf` file

```
host all all PGBOUNCER_IP/NETMASK trust
```

By default, PgBouncer comes with `trust` authentication method. The trust method can be used in a development environment but is not recommended for production. For production, `hba` authentication is recommended.

4. After configuring PgBouncer, restart both the PostgreSQL and PgBouncer services

```
sudo systemctl reload postgresql
sudo systemctl reload pgbouncer
```

For more information about additional configuration options, check the PgBouncer [documentation](https://www.pgbouncer.org/config.html).

## Python
### Requirements
#### Dependencies

Make sure all the dependencies are installed before creating the Python script that will generate the data for your project.

You can create a `requirements.txt` file with the following content:

```
tqdm
faker
psycopg2
```

Or if you’re using Anaconda, create an `environment.yml` file:

```
name: percona
dependencies:
  - python=3.10
  - tqdm
  - faker
  - psycopg2
```

You can change the Python version as this script has been proven to work with these versions of Python: 3.7, 3.8, 3.9, 3.10, and 3.11.

Run the following command if you’re using `pip`:

```
pip install -r requirements.txt
```

Or run the following statement to configure the project environment when using Anaconda:

```
conda env create -f environment.yml
```

#### Database

Now that you have the dependencies installed, you must create a database named `company`.

Log into PostgreSQL:

```
$ sudo su postgres
$ psql
```

Create the `company` database:

```
create database company;
```

And create the `employees` table:

```
create table employees(
  id         serial        primary key,
  fist_name  varchar(50)   not null,
  last_name  varchar(50)   not null,
  job        varchar(100)  not null,   
  address    varchar(200)  not null,
  city       varchar(100)  not null,
  email      varchar(50)   not null
);
```

### Inserting Data
Now it’s time to create the Python script that will generate the data and insert it into the database.

```
from multiprocessing import Pool, cpu_count
import psycopg2
from tqdm import tqdm
from faker import Faker

fake = Faker()
num_cores = cpu_count() - 1

def insert_data(arg):
    x = int(60000/num_cores)
    print(x)
    with psycopg2.connect(database="database_name", user="user", password="password", host="localhost", port="6432") as conn:
        with conn.cursor() as cursor:
            for i in tqdm(range(x), desc="Inserting Data"):
                sql = "INSERT INTO employees (first_name, last_name, job, address, city, email) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (fake.first_name(), fake.last_name(), fake.job(), fake.address(), fake.city(), fake.email())
                cursor.execute(sql, val)

if __name__=="__main__":
    with Pool() as pool:
        pool.map(insert_data, range(num_cores))
```

At first, the multiprocessing pool is created, and configured to use all available CPU cores minus one. Each core will call the `insert_data()` function.

On each call to the function, a connection to the database will be established through the default port (6432) of PgBouncer, meaning that the application will open a number of connections equal to `num_cores`, a variable that contains the number of CPU cores being used.

Then, the data will be generated with Faker and inserted into the database by executing the corresponding SQL statements.

In a CPU with 16 cores, the number of records inserted into the database on each call to the function will be equal to 60 thousand divided by 15, that is 4 thousand SQL statements executed.

This way you can modify the script and optimize it by configuring a connection pool with PgBouncer.