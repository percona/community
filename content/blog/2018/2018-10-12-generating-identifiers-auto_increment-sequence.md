---
title: 'Generating Identifiers – from AUTO_INCREMENT to Sequence'
date: Fri, 12 Oct 2018 11:00:58 +0000
draft: false
tags: ['author-devart', 'auto_increment', 'dbForge', 'developer tools', 'Entry Level', 'generate id', 'GUI tools', 'MariaDB', 'MyISAM', 'MySQL', 'primary key', 'sequence', 'Tools', 'trigger']
authors:
  - alexey_mikotkin
images:
  - blog/2018/09/generating-complex-sequences.png
slug: generating-identifiers-auto_increment-sequence
---

There are a number of options for generating ID values for your tables. In this post, Alexey Mikotkin of Devart explores your choices for generating identifiers with a look at auto_increment, triggers, UUID and sequences.

AUTO_INCREMENT
---------------

Frequently, we happen to need to fill tables with unique identifiers. Naturally, the first example of such identifiers is PRIMARY KEY data. These are usually integer values hidden from the user since their specific values are unimportant. 

When adding a row to a table, you need to take this new key value from somewhere. You can set up your own process of generating a new identifier, but MySQL comes to the aid of the user with the [AUTO_INCREMENT](https://dev.mysql.com/doc/refman/8.0/en/example-auto-increment.html) column setting. It is set as a column attribute and allows you to generate unique integer identifiers. As an example, consider the `**users**` table, the primary key includes an `**id**` column of type INT:
```
CREATE TABLE users (
  id int NOT NULL AUTO_INCREMENT,
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  email varchar(254) NOT NULL,
PRIMARY KEY (id)
);
```
Inserting a NULL value into the `**id**` field leads to the generation of a unique value; inserting 0 value is also possible unless the [NO_AUTO_VALUE_ON_ZERO](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_no_auto_value_on_zero) Server SQL Mode is enabled:
```
INSERT INTO users(id, first_name, last_name, email) VALUES (NULL, 'Simon', 'Wood', 'simon@testhost.com');
INSERT INTO users(id, first_name, last_name, email) VALUES (0, 'Peter', 'Hopper', 'peter@testhost.com');
```
It is possible to omit the `**id**` column. The same result is obtained with:
```
INSERT INTO users(first_name, last_name, email) VALUES ('Simon', 'Wood', 'simon@testhost.com');
INSERT INTO users(first_name, last_name, email) VALUES ('Peter', 'Hopper', 'peter@testhost.com');
```
The selection will provide the following result: 
![select from users table in dbForge studio](blog/2018/09/select-from-users-table.png) 
_Select from users table shown in dbForge Studio_

You can get the automatically generated value using the [LAST_INSERT_ID()](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_last-insert-id) session function. This value can be used to insert a new row into a related table. 

There are aspects to consider when using AUTO_INCREMENT, here are some:

*   In the case of rollback of a data insertion transaction, no data will be added to a table. However, the AUTO_INCREMENT counter will increase, and the next time you insert a row in the table, holes will appear in the table.
*   In the case of multiple data inserts with a single INSERT command, the LAST_INSERT_ID() function will return an automatically generated value for the first row.
*   The problem with the AUTO_INCREMENT counter value is described in [Bug #199 - Innodb autoincrement stats los on restart](https://bugs.mysql.com/bug.php?id=199).

For example, let's consider several cases of using AUTO_INCREMENT for `**table1**`:
```
CREATE TABLE table1 (
  id int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id)
)
ENGINE = INNODB; -- transactional table

-- Insert operations.
INSERT INTO table1 VALUES (NULL); -- 1
INSERT INTO table1 VALUES (NULL); -- 2
INSERT INTO table1 VALUES (NULL); -- 3
SELECT LAST_INSERT_ID() INTO @p1; -- 3

-- Insert operations within commited transaction.
START TRANSACTION;
INSERT INTO table1 VALUES (NULL); -- 4
INSERT INTO table1 VALUES (NULL); -- 5
INSERT INTO table1 VALUES (NULL); -- 6
COMMIT;
SELECT LAST_INSERT_ID() INTO @p3; -- 6

-- Insert operations within rolled back transaction.
START TRANSACTION;
INSERT INTO table1 VALUES (NULL); -- 7 won't be inserted (hole)
INSERT INTO table1 VALUES (NULL); -- 8 won't be inserted (hole)
INSERT INTO table1 VALUES (NULL); -- 9 won't be inserted (hole)
ROLLBACK;
SELECT LAST_INSERT_ID() INTO @p2; -- 9

-- Insert multiple rows operation.
INSERT INTO table1 VALUES (NULL), (NULL), (NULL); -- 10, 11, 12
SELECT LAST_INSERT_ID() INTO @p4; -- 10

-- Let’s check which LAST_INSERT_ID() values were at different stages of the script execution:
SELECT @p1, @p2, @p3, @p4;
+------+------+------+------+
| @p1  | @p2  | @p3  | @p4  |
+------+------+------+------+
|    3 |    9 |    6 |   10 |
+------+------+------+------+

-- The data selection from the table shows that there are holes in the table in the values of identifiers:
SELECT * FROM table1;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
|  4 |
|  5 |
|  6 |
| 10 |
| 11 |
| 12 |
+----+
```
**Note: **The next AUTO_INCREMENT value for the table can be parsed from the [SHOW CREATE TABLE](https://dev.mysql.com/doc/refman/8.0/en/show-create-table.html) result or read from the AUTO_INCREMENT field of the [INFORMATION_SCHEMA TABLES](https://dev.mysql.com/doc/refman/8.0/en/tables-table.html) table. 

The rarer case is when the primary key is surrogate — it consists of two columns. The **MyISAM engine** has an interesting solution that provides the possibility of generating values for such keys. Let’s consider the example:
```
CREATE TABLE roomdetails (
  room char(30) NOT NULL,
  id int NOT NULL AUTO_INCREMENT,
PRIMARY KEY (room, id)
)
ENGINE = MYISAM;

INSERT INTO roomdetails VALUES ('ManClothing', NULL);
INSERT INTO roomdetails VALUES ('WomanClothing', NULL);
INSERT INTO roomdetails VALUES ('WomanClothing', NULL);
INSERT INTO roomdetails VALUES ('WomanClothing', NULL);
INSERT INTO roomdetails VALUES ('Fitting', NULL);
INSERT INTO roomdetails VALUES ('ManClothing', NULL);
```
It is quite a convenient solution: ![select from roomdetails table](blog/2018/09/select-from-roomdetails-table.png)

### Special values auto generation

The possibilities of the AUTO_INCREMENT attribute are limited because it can be used only for generating simple integer values. But what about complex identifier values? For example, depending on the date/time or [A0001, A0002, B0150...]). To be sure, such values should not be used in primary keys, but they might be used for some auxiliary identifiers. 

The generation of such unique values can be automated, but it will be necessary to write code for such purposes. We can use the **BEFORE INSERT** trigger to perform the actions we need. 

Let’s consider a simple example. We have the `**sensors`** table for sensors registration. Each sensor in the table has its own name, location, and type: 1 –analog, 2 –discrete, 3 –valve. Moreover, each sensor should be marked with a unique label like [symbolic representation of the sensor type + a unique 4-digit number] where the symbolic representation corresponds to such values [AN, DS, VL]. 

In our case, it is necessary to form values like these [DS0001, DS0002...] and insert them into the `**label`** column. 

When the trigger is executed, it is necessary to understand if any sensors of this type exist in the table. It is enough to assign number “1” to the first sensor of a certain type when it is added to the table. 

In case such sensors already exist, it is necessary to find the maximum value of the identifier in this group and form a new one by incrementing the value by 1. Naturally, it is necessary to take into account that the label should start with the desired symbol and the number should be 4-digit. 

So, here is the table and the trigger creation script:
```
CREATE TABLE sensors (
  id int NOT NULL AUTO_INCREMENT,
  type int NOT NULL,
  name varchar(255) DEFAULT NULL,
  `position` int DEFAULT NULL,
  label char(6) NOT NULL,
PRIMARY KEY (id)
);

DELIMITER $$

CREATE TRIGGER trigger_sensors
BEFORE INSERT
ON sensors
FOR EACH ROW
BEGIN
  IF (NEW.label IS NULL) THEN
    -- Find max existed label for specified sensor type
    SELECT
      MAX(label) INTO @max_label
    FROM
      sensors
    WHERE
      type = NEW.type;

    IF (@max_label IS NULL) THEN
      SET @label =
        CASE NEW.type
        WHEN 1 THEN 'AN'
        WHEN 2 THEN 'DS'
        WHEN 3 THEN 'VL'
        ELSE 'UNKNOWN'
      END;

      -- Set first sensor label
      SET NEW.label = CONCAT(@label, '0001');
    ELSE
      -- Set next sensor label
      SET NEW.label = CONCAT(SUBSTR(@max_label, 1, 2), LPAD(SUBSTR(@max_label, 3) + 1, 4, '0'));
    END IF;
  END IF;
END$$

DELIMITER;
```
The code for generating a new identifier can, of course, be more complex. In this case, it is desirable to implement some of the code as a stored procedure/function. Let’s try to add several sensors to the table and look at the result of the labels generation:
```
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 1, 'temperature 1', 10, 'AN0025'); -- Set exact label value 'AN0025'
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 1, 'temperature 2', 11, NULL);
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 1, 'pressure 1', 15, NULL);
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 2, 'door 1', 10, NULL);
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 2, 'door 2', 11, NULL);
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 3, 'valve 1', 20, NULL);
INSERT INTO sensors (id, type, name, `position`, label) VALUES (NULL, 3, 'valve 2', 21, NULL);
```
![generating complex keys](blog/2018/09/generating-complex-sequences.png)

### Using UUID

Another version of the identification data is worth mentioning - Universal Unique Identifier (UUID), also known as GUID. This is a 128-bit number suitable for use in primary keys. 

A UUUI value can be represented as a string - CHAR(36)/VARCHAR(36) or a binary value - BINARY(16). Benefits:

*   Ability to generate values ​​from the outside, for example from an application.
*   UUID values ​​are unique across tables and databases since the standard assumes uniqueness in space and time.
*   There is a specification - [A Universally Unique IDentifier (UUID) URN Namespace](http://www.ietf.org/rfc/rfc4122.txt).

Disadvantages:

*   Possible performance problems.
*   Data increase.
*   More complex data analysis (debugging).

To generate this value, MySQL function **UUID()** is used. New functions have been added to Oracle MySQL 8.0 server to work with UUID values ​​- UUID_TO_BIN, BIN_TO_UUID, IS_UUID. Learn more about it at the Oracle MySQL website - [UUID()](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid) 

The code shows the use of UUID values:
```
CREATE TABLE table_uuid (id binary(16) PRIMARY KEY);

INSERT INTO table_uuid VALUES(UUID_TO_BIN(UUID()));
INSERT INTO table_uuid VALUES(UUID_TO_BIN(UUID()));
INSERT INTO table_uuid VALUES(UUID_TO_BIN(UUID()));

SELECT BIN_TO_UUID(id) FROM table_uuid;
+--------------------------------------+
| BIN_TO_UUID(id)                      |
+--------------------------------------+
| d9008d47-cdf4-11e8-8d6f-0242ac11001b |
| d900e2b2-cdf4-11e8-8d6f-0242ac11001b |
| d9015ce9-cdf4-11e8-8d6f-0242ac11001b |
+--------------------------------------+
```
You may also find useful the following article - [Store UUID in an optimized way](https://www.percona.com/blog/2014/12/19/store-uuid-optimized-way/).

### Using sequences

Some databases support the object type called Sequence that allows generating sequences of numbers. The Oracle MySQL server does not support this object type yet but the MariaDB 10.3 server has the **Sequence** engine that allows working with the [Sequence](https://mariadb.com/kb/en/library/sequence-overview/) object. 

The Sequence engine provides DDL commands for creating and modifying sequences as well as several auxiliary functions for working with the values. It is possible to specify the following parameters while creating a named sequence: START – a start value, INCREMENT – a step, MINVALUE/MAXVALUE – the minimum and maximum value; CACHE – the size of the cache values; CYCLE/NOCYCLE – the sequence cyclicity. For more information, see the [CREATE SEQUENCE documentation](https://mariadb.com/kb/en/library/create-sequence/). 

Moreover, the sequence can be used to generate unique numeric values.  This possibility can be considered as an alternative to AUTO_INCREMENT but the sequence additionally provides an opportunity to specify a step of the values. Let’s take a look at this example by using the `**users`** table. The sequence object `**users_seq`** will be used to fill the values of the primary key. It is enough to specify the **NEXT VALUE FOR** function in the **DEFAULT** property of the column:
```
CREATE SEQUENCE users_seq;

CREATE TABLE users (
  id int NOT NULL DEFAULT (NEXT VALUE FOR users_seq),
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  email varchar(254) NOT NULL,
PRIMARY KEY (id)
);

INSERT INTO users (first_name, last_name, email) VALUES ('Simon', 'Wood', 'simon@testhost.com');
INSERT INTO users (first_name, last_name, email) VALUES ('Peter', 'Hopper', 'peter@testhost.com');
```
Table content output: 
![using sequences for pk generation](blog/2018/09/using-sequences-for-pk.png)

Information
-----------

The images for this article were produced while using [dbForge Studio for MySQL Express Edition,](https://www.devart.com/dbforge/mysql/studio/) a download is available from [https://www.devart.com/dbforge/mysql/studio/download.html](https://www.devart.com/dbforge/mysql/studio/download.html)

#### It's free!

**Thank you to community reviewer [Jean-François Gagné](https://jfg-mysql.blogspot.com/) for his review and suggestions for this post.** 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors' own. When using the advice from this or any other online resource **test** ideas before applying them to your production systems, and **always **secure a working back up._