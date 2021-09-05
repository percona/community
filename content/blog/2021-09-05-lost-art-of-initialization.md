---
title: 'The lost art of Database Server Initialization.'
date: "2021-06-05T00:00:00+00:00"
draft: false
tags: ['Percona', 'MySQL', Recovery]
authors:
  - wayne
images:
  - blog/2021/09/lostart-01.png
slug: lost-art-of-atabase-erver-initialization
---
<br>

With all the DBaaS, IaaS and PaaS environments, sometimes I think the Art of Database initialization is becoming a lost art. Many times we just delete the server we created and order a new one.  

Just recently I was talking to a colleague and this subject came up. We both thought about it and decided we have become spoiled from automation. We were both rusty at the process. This gave me the idea for this post.
![lostart-10](blog/2021/09/lostart-01.png)

You might be thinking why initialize the server again? Let's say that you wanted MySQL Server 8.0 not to use mixed case. Yet when the database was initialized the default setting of  'lower_case_table_names = 0' was used. With 8.0 you can't make the change 'lower_case_table_names = 1' in the my.cnf and restart MySQL. It won't work, leaving you with one option. Initialize the server a second time.

Let's look at the steps we would need to change the MySQL server to support only lower case.

You may want to take a backup before you begin these steps if you have already loaded data that you wish to keep.

##  Lets look at the steps.

The steps below assume you are working with a default MySQL
server installation. Modify as needed for a custom installation.

1. Stop the MySQL Server. `systemctl start mysqld`

2. You will need to delete everything out of your current data directory.
   ```
   $ cd /var/lib/mysql
   $ rm -fR *
   ```
3. Edit your my.cnf file and add: `lower_case_table_names=1`
   ```
   $ vi /etc/my.cnf
   ```
   ![lostart-10](blog/2021/09/lostart-02.png)

4. Now initialize mysql.
   ```
   $ /usr/sbin/mysqld --initialize --user=mysql
   ```
5. Get the temporary root password from the `mysqld.log`
   ```
   $ cat /var/log/mysqld.log | grep password
   ```
![lostart-10](blog/2021/09/lostart-03.png)

6. Start MySQL. `systemctl start mysqld`

Now you should be able to log into MySQL using the password you got in step 5.

Your MySQL Server is now up and running.

We all can agree that automation has changed our lives for the better.
