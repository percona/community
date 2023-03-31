---
title: "How to prevent unauthorized users from connecting to ProxySQL"
date: "2023-03-30T00:00:00+00:00"
draft: false
tags: ["Databases", "Percona", "ProxySQL", "LoadBalancer"]
authors:
  - valentin_traen
images:
  - blog/2023/03/proxysql_user_management_cover.jpg
---

ProxySQL is a great load balancer which however suffers from some shortcomings concerning the management of MySQL users. ProxySQL provides a firewall which, in my case, is not complete enough to properly manage users and secure their access. Indeed, this firewall does not accept subnets and keeps unauthorized connections in ProxySQL. We cannot then be sure of not suffering a DDOS attack on our ProxySQL instance. In this article, I will explain how I managed to overcome this problem.

## Reminder of the principle of connection through ProxySQL

To understand what follows, you have to bear in mind how ProxySQL connects to MySQL. The user connects to Proxysql which then establishes the connection to MySQL. For this, ProxySQL maintains MySQL users in its internal database. The names of MySQL users, their passwords as well as the MySQL destination server are entered in the mysql_users table. At each connection request to a MySQL server, ProxySQL checks the presence of the user in the mysql_users table to connect itself to MySQL with this same user.

Something is missing, isn't it?

Yes, the host associated with each MySQL user is missing!

In MySQL, users are configured to only be able to connect from ProxySQL. In ProxySQL we don't have this information. By default, all users can therefore connect to ProxySQL from any IP address and ProxySQL will open connections to MySQL for them. As I specified in the introduction, ProxySQL provides a Firewall to overcome this problem, but this one is not really satisfactory.

## Prevent connection to ProxySQL with an unauthorized user

In this part, our ProxySQL instance will allow user _bob_ to connect to the MySQL (*mysql_server*) instance. _Bob_ is allowed to connect from *IP_1* but cannot from *IP_2*. The ProxySQL instance is running on *IP_PROXYSQL*.

In MySQL, user *bob* was created like this:

```sql
CREATE USER 'bob'@'IP_PROXYSQL' IDENTIFIED BY 'PASSWORD';
```

In ProxySQL, let's create *bob* like this:
```sql
INSERT INTO mysql_users(username,password,default_hostgroup) VALUES ('bob','PASSWORD',0);
LOAD MYSQL USERS TO RUNTIME;
SAVE MYSQL USERS TO DISK;
```
and declare the MySQL server like this:
```sql
INSERT INTO mysql_servers(hostgroup_id,hostname) VALUES (1,'mysql_server');
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```
As you may have noticed, I didn't declare the same hostgroup when creating the user and the server. Hostgroup 0 does not correspond to any MySQL server. By default, our user bob will therefore be able to connect to ProxySQL but his queries will not be redirected to any MySQL server. Let's move on to host management. I will declare each authorized host in the mysql_query_rules table. In ProxySQL, this table is used, among other things, to assign different parameters to a connection. You see what I mean? Let's declare our rule!
```sql
INSERT INTO mysql_query_rules (rule_id,active,username,client_addr,destination_hostgroup,apply) VALUES (1,1,'bob','IP_1',1,1);
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
```
I have just declared a rule indicating that all requests coming from user bob connected from *IP_1* must be played on host 1. And icing on the cake, *IP_1* can be a subnet (*IP_1%*), which would not have could not be possible with the firewall. From now on, bob will be able to perform queries from IP_1 and get results from MySQL. If bob plays a request from IP_2, he will not be able to obtain a result since the hostgroup queried will be 0 which does not correspond to any MySQL server. However, this is not satisfactory. Nothing prevents bob from creating a very large number of connections from *IP_2*. It won't reach any MySQL servers but may be able to crash my ProxySQL instance. It's time to deal with those unauthorized connections!

ProxySQL provides a scheduler which will be very useful here. This scheduler will allow us to play a bash script every x ms. I created this script in the ProxySQL datadir:

*kill_connections.sh*
```bash
#!/bin/bash

PROXYSQL_USERNAME="${1}"
PROXYSQL_PASSWORD="${2}"
PROXYSQL_HOSTNAME="127.0.0.1"
PROXYSQL_PORT="6032"

mysql -u$PROXYSQL_USERNAME -p$PROXYSQL_PASSWORD -h$PROXYSQL_HOSTNAME -P$PROXYSQL_PORT -e "SELECT SessionID,user,cli_host FROM stats_mysql_processlist WHERE hostgroup = 0" | while read SessionID user cli_host; do
    if [ $SessionID != "SessionID" ]; then
            enabled_account=$(mysql -u$PROXYSQL_USERNAME -p$PROXYSQL_PASSWORD -h$PROXYSQL_HOSTNAME -P$PROXYSQL_PORT -se"SELECT count(*) FROM mysql_query_rules WHERE username = '$user' and '$cli_host' LIKE client_addr;")
            if [[ "$enabled_account" -eq 0 ]]; then
                mysql -u$PROXYSQL_USERNAME -p$PROXYSQL_PASSWORD -h$PROXYSQL_HOSTNAME -P$PROXYSQL_PORT -e "KILL CONNECTION $SessionID"
            fi

    fi
done
```
This script lists all the connections opened in ProxySQL on hostgroup 0. It then checks whether the connected user/host pair is authorized using the mysql_query_rules table. If not, the connection is killed. Let's activate the scheduler in ProxySQL:
```sql
INSERT INTO scheduler(filename, arg1, arg2, interval_ms) VALUES ('kill_connections.sh','proxysql_admin_user','proxysql_admin_password', 1000);
LOAD SCHEDULER TO RUNTIME;
SAVE SCHEDULER TO DISK;
```
Now, any connection opened in ProxySQL but not authorized will be automatically killed!

>  **_WARNING:_**  unfortunately, the ProxySQL scheduler does not work like the MySQL scheduler. It is necessary to open the connection from a .sh file and therefore to indicate the ProxySQL administration credentials. These identifiers will then be visible by monitoring the list of server processes. To avoid this problem, I advise you to indicate the identifiers directly in the .sh file and to protect this file correctly on your server.

## Additional Information

When I deploy ProxySQL, I always create a rule with a very high rule_id to block unauthorized connections; this is an additional barrier in case I forget something:
```sql
INSERT INTO mysql_query_rules (rule_id,active,error_msg,destination_hostgroup) VALUES (999999999,1,'ProxySQL : Access denied',0);
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
```
This rule redirects unauthorized connections to hostgroup 0 (if ever a user was declared in mysql_users with a hostgroup leading to a MySQL server) and displays an error message for each request.
I create all my rules to manage hosts with a rule_id > or = 10000. This allows me to have 9999 empty slots if I ever want to create other priority rules in mysql_query_rules.
```sql
INSERT INTO mysql_query_rules (rule_id,active,username,client_addr,apply) VALUES ((SELECT IFNULL(MAX(rule_id)+1,10000) FROM mysql_query_rules WHERE rule_id != (SELECT MAX(rule_id) FROM mysql_query_rules) AND rule_id > 9999),1,'USERNAME','HOST',1);
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
```
Don't hesitate to ask me questions, I'll be happy to answer them.


