---
title: 'The lost art of Database Server Initialization.'
date: "2021-06-05T00:00:00+00:00"
draft: false
tags: ['Percona', 'MySQL', 'Recovery', 'Installation']
authors:
  - wayne
images:
  - blog/2021/09/lostart-01.png
slug: lost-art-of-database-server-initialization
---
<br>

With all the DBaaS, IaaS and PaaS environments, sometimes I think the Art of MySQL initialization is becoming a lost art. Many times we just delete the MySQL Server and order a new one.  

Just recently I was talking with a colleague, and this subject came up. We both thought about it and decided we have become spoiled by automation. We were both rusty on this process. This gave me the idea for this post.
![lostart-10](blog/2021/09/lostart-01.png)

You might be thinking why initialize MySQL again? Let's say that you wanted MySQL Server 8.0 not to use mixed case. Yet when the database was initialized the default setting of  `lower_case_table_names = 0` was used. With 8.0 you can't make the change `lower_case_table_names = 1` in the my.cnf and restart MySQL. It won't work, leaving you with two option. One Initialize MySQL a second time, or order a new environment.

Let's look at the steps we would need to change the MySQL server to support only lower case.

You may want to take a backup before you begin these steps if you have already loaded data that you wish to keep.

## The Steps

The steps below assume you are working with a default MySQL
server installation. Modify as needed for a custom installation.

1. Stop the MySQL Server. `$ systemctl start mysqld`

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

If you dont find the temporary password for the root user, review the steps above making sure you did not miss something.

6. Start MySQL.
   ```
   $ systemctl start mysqld
   ```
7. Verify MySQL is running.
   ```
   $ cat /var/log/mysqld.log
   ```
![lostart-10](blog/2021/09/lostart-04.png)

Now you should be able to log into MySQL using the password you got from step 5.

There could be many more reasons to re-initliatize a MySQL Database. This is just one example.
Automation is great. Just remember to pull out your command line tools now and then, so they dont get to rusty.
<hr>
