---
title: 'Database Schema Management Via Liquibase'
date: Thu, 01 Oct 2020 22:30:04 +0000
draft: false
tags: ['ronak.rahman', 'MySQL', 'PostgreSQL', 'Tools']
authors:
  - ronak_rahman
images:
  - blog/2020/10/Liquibase.jpg
slug: database-schema-management-via-liquibase
---

Creating the database for an application is simple and easy. However, database script management gets complicated in a hurry when you need to support multiple versions, work with multiple teams, and apply the same changes to multiple types of databases.  

One open-source tool that helps teams track, version, and deploy database schema changes is [Liquibase](https://www.liquibase.org). It executes database scripts sequentially, allows for the automatic creation and execution of rollback scripts for failed updates, and provides an easy way to use the same scripts and apply them to different types of databases. To illustrate how Liquibase works, here's an example using PostgreSQL.   

##### System set up:

*   [Download the latest version of Liquibase](https://www.liquibase.org/download). 
*   [Download the JDBC driver jar file for PostgreSQL](https://jdbc.postgresql.org/download.html).
*   Ensure the liquibase.bat file’s path is set to a location in the PATH System variable.

To test your connection, try running Liquibase with the JDBC driver located in the same directory as Liquibase:
```
liquibase
--driver=org.postgresql.Driver
--classpath=postgresql-9.2-1002-jdbc4.jar
--url="jdbc:postgresql://<IP OR HOSTNAME>:<PORT>/<DATABASE>" 
--changeLogFile=db.changelog-1.0.xml
--username=<POSTGRESQL USERNAME>
--password=<POSTGRESQL PASSWORD>
```

##### **Create a changelog file:**

A Liquibase database _changelog_ is an XML, JSON, YAML, or SQL file that describes all changes that need to be performed to update the database. In most cases, you want to create one file for each release. Each file consists of one or more _changesets_. (Note: The XML, JSON, and YAML definitions allow for abstraction, meaning that Liquibase is able to apply the same changes to any database. You can use database-specific SQL, as well.) 

Create a project folder called **LiquibasePostgres**. In that folder, let’s create our database changelog. Create a new text file named **dbchangelog.xml**. Drop this code into the file:
```
<?xml version="1.0" encoding="UTF-8"?> 
<databaseChangeLog 
xmlns="http://www.liquibase.org/xml/ns/dbchangelog" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.9.xsd"> 
</databaseChangeLog>
```
In the same **LiquibasePostgres** folder, create a [**liquibase.properties** file](https://docs.liquibase.com/workflows/liquibase-community/creating-config-properties.html). Drop this code in with your username and password.
```
changeLogFile: C:\\Users\\Administrator\\LiquibasePostgreSQL\\dbchangelog.xml 
url: jdbc:postgresql://localhost:5432/MYDATABASE 
username: postgres 
password: password 
driver: org.postgresql.Driver 
classpath: ../../Liquibase_Drivers/postgresql-42.2.8.jar
```
Now it’s time to write some code to generate your Postgres database. Let’s create our first _changeset_.  

A changeset describes a set of changes that Liquibase executes. A best practice to keep in mind when using changesets is to have only one logical change per _changeset_. Each _changeset_ is identified by the name of the author and an id. Liquibase stores this information together with the name of the _changelog_ file in a _databasechangelog table_ to keep track of your changes. 

In the **databasechangelog.xml** file, add the following _changeset_:
```
<?xml version="1.0" encoding="UTF-8"?> 
<databaseChangeLog 
xmlns="http://www.liquibase.org/xml/ns/dbchangelog" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.9.xsd">

<changeSet id="1" author="lucy"> 
<createTable tableName="department"> 
<column name="id" type="int"> 
<constraints primaryKey="true" nullable="false"/> 
</column> 
<column name="name" type="varchar(50)"> 
<constraints nullable="false"/> 
</column> 
<column name="active" type="boolean" 
defaultValueBoolean="true"/> 
</createTable> 
</changeSet> 
</databaseChangeLog>
```
Now that you understand the basics, you can easily start using Liquibase on any existing database. In this case, a Postgres database project you’re already working on. To achieve a starting point, you’ll need to generate a changelog based on your current database. 

Provide the connection information (described earlier) and use the [generateChangeLog command](https://docs.liquibase.com/commands/community/generatechangelog.html). The generateChangeLog command generates a changelog file that contains all your objects (represented as changesets) and places the file in the same directory where the command was run.
```
liquibase –driver=org.postgresql.Driver \\
–classpath=myFiles\\postgresql-9.4.1212.jre7.jar \\
–changeLogFile=myFiles/db.changelog-1.0.xml \\
–url=”jdbc:postgresql://localhost:5432/MYDATABASE” \\
–username=postgres \\
–password=postgres \\
generateChangeLog
```
If you already have a database, generating the changelog is a lot easier (and a whole lot faster) than writing it yourself. [Here are some instructions on how to get started using an existing database](https://docs.liquibase.com/workflows/liquibase-community/existing-project.html). Always review the generated changesets so that you can be sure everything looks as it should. 

##### Executing Liquibase:

There are [3 primary ways to run Liquibase](https://www.liquibase.org/blog/3-ways-to-run-liquibase). You can use command line or a Maven plugin to create the database as part of your build or deployment process. You can also use a Servlet, Spring, or CDI Listener to automatically create or update the database at application startup. [Liquibase also has an official Docker image](https://hub.docker.com/r/liquibase/liquibase). 

##### Summing Up:

A version-based database migration process allows you to evolve your database together with your application code and to automatically apply database updates when you deploy a new release. In our next blog, we’ll walk you through how to combine Liquibase with a Percona extension to achieve zero-downtime schema changes.