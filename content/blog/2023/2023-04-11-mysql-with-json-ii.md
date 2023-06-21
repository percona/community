---
title: "​​Using the JSON data type with MySQL 8 - Part II"
date: "2023-04-11T00:00:00+00:00"
draft: false
tags: ["json", "mysql", "Databases", "Percona", "Open Source"]
authors:
  - edith_puclla
images:
  - blog/2023/04/00-mjii-intro.jpg
slug: using-the-json-data-type-with-mysql-8-II
---

If you read - [Using the JSON data type with MySQL 8 - Part I](https://percona.community/blog/2023/03/13/using-the-json-data-type-with-mysql-8/), you will see that inserting data into **MySQL** of **JSON** type is a very common and effective practice. Now we'll see how to do it with a **Python** project, using **SQLAlchemy** and **Docker Compose**, which further automates this example. You can run this example using a single command: **docker-compose up**

Before getting down to work, we will review some important concepts:

- **Percona Server for MySQL** is an open source, drop-in replacement for MySQL Community that provides better performance, more scalability, and enhanced security features.
- **SQLAlchemy** is a library that allows us to communicate between Python programs and databases.
- **Docker Compose** is a tool for defining and running multi-container Docker applications.

Let’s start with the structure of this project:

![Project folder structure](blog/2023/04/01-mjii-folders.jpg)

We have a folder called **app** which contains the **db.py** file, and this is where we create the **library** database and establish the connection with this database.

```bash
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@db:3306/library")
```

In this file, we also create the class transactions. This will create the fields for the **library** databases with **SQLAlchemy**; we define the attributes, and they will be the database fields.
We have four attributes: book_id, tittle, publishes, and labels. The last one (labels) of JSON data type.

```bash
class transactions(base):
   __tablename__ = 'book'

   book_id = Column(Integer, primary_key=True)
   title = Column(String(50))
   publisher = Column(String(50))
   labels = Column(JSON)

   def __init__(self, book_id, title, publisher, labels):
       self.book_id = book_id
       self.title = title
       self.publisher = publisher
       self.labels = labels

base.metadata.create_all(engine)
```

Now let's review the Python script called **insert.py**, where we use the transactions class to insert data into the database.

```bash
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

tr1 = db.transactions(1,'Green House', 'Joe Monter', '{"about" : {"gender": "action", "cool": true, "notes": "labeled"}}')

session.add(tr1)
session.commit()
```

Now let's explore the **docker-compose.yaml** file, we have two services, the db and the api

```bash
version: "3.8"
services:
 api:
   build: .
   container_name: api
   depends_on:
     db:
       condition: service_healthy
 db:
   image: percona/percona-server:8.0
   container_name: db
   restart: always
   environment:
     MYSQL_USER: root
     MYSQL_ROOT_PASSWORD: root
     MYSQL_DATABASE: library
   healthcheck:
     test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
     timeout: 20s
     retries: 10
   volumes:
     - my-db:/var/lib/mysql
   ports:
     - "3306:3306"
   expose:
     - "3306"

# Names for volume
volumes:
 my-db:
```

The **db** service uses the **Percona Server for MySQL** image (percona/percona-server:8.0) for the database and has a healthcheck that allows you to confirm when the database is started and ready to receive requests.
The **api** service depends on the **db** service to start. The api service will build a Dockerfile, it does a build of the Python applications (of db.py and insert.py), so in this way, we can insert data into the database when it is ready.

It's time to see the example in action; let's locate it inside the **json-mysql** project and run **docker-compose ps -d**

Once this is done, we can connect to the database and query the table without needing to go inside the container with the following command:

```bash
docker exec -i db mysql -uroot -proot <<< "use library;show tables;select \* from book;describe book;"
```

We can check the data types of our fields and the inserted data. You will also see the JSON data type "labels" data type.

```bash
book_id	title	publisher	labels
1	Green House	Joe Monter	"{\\"about\\" : {\\"gender\\": \\"action\\", \\"cool\\": true, \\"notes\\": \\"labeled\\"}}"
2	El camino	Daniil Zotl	"{\\"about\\" : {\\"gender\\": \\"documental\\", \\"cool\\": true, \\"notes\\": \\"labeled\\"}}"
3	London Bridge	Mario Mesa	"{\\"about\\" : {\\"gender\\": \\"drama\\", \\"cool\\": true, \\"notes\\": \\"labeled\\"}}"
```

```bash
Field	Type	Null	Key	Default	Extra
book_id	int	NO	PRI	NULL	auto_increment
title	varchar(50)	YES		NULL
publisher	varchar(50)	YES		NULL
labels	json	YES		NULL
```

Use “docker compose ps” to see your services running. In this case, we have the “db” service running, which is for the database, and we have “api” with the state “exited,” which means that the scripts to create the database and insert the data into the database “library” was created.

```bash
NAME                COMMAND                  SERVICE             STATUS              PORTS
api                 "/bin/sh -c 'bash -C…"   api                 exited (0)
db                  "/docker-entrypoint.…"   db                  running (healthy)   0.0.0.0:3306->3306/tcp, 33060/tcp
```

It was an example of inserting JSON data into MySQL using SQLAlchemy in Python and docker-compose for deployment.

You can find the project on [GitHub](//github.com/edithturn/json-mysql.git). If there is any other way to make it better happy to hear it so I can improve this project.

You can explore more about [Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server), and if you want to see how this project start check [Using the JSON data type with MySQL 8 - Part I](https://percona.community/blog/2023/03/13/using-the-json-data-type-with-mysql-8/)
