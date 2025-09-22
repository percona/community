---
title: "Audit Log Filter Component"
date: "2025-09-18T00:00:00+00:00"
tags: ["Opensource", "Audit Log", "filter", "component", "MySQL", "Community", "Percona Server", "PXC"]
categories: ["MySQL"]
authors:
  - wayne
images:
  - blog/2025/09/audit-log-filter.png
  
---
The audit log filter component in MySQL 8.4 provides administrators with a powerful mechanism for auditing database activity at a fine-grained level. While it offers significant flexibility—such as selectively logging events based on users, hosts, or event types—it can also be challenging to understand and configure correctly.

In this article, we will examine how the audit log filter component works, walk through its core concepts, and share practical tips for configuring and managing audit filters effectively. Our goal is to help you leverage this feature to improve observability, meet compliance requirements, and reduce unnecessary logging overhead.

### Enabling Audit Log Filter
We will be using Percona Server 8.4.4 or higher in the examples below. First, we need to enable the audit log filter component. To install the audit log filter component, we need to run the following command:
```
mysql -u root -p < /usr/share/percona-server/mysql/share/audit_log_filter_linux_install.sql
```
Verify that the audit log filter component is enabled by running:
```
select * from mysql.component;
+--------------+--------------------+-----------------------------------+
| component_id | component_group_id | component_urn                     |
+--------------+--------------------+-----------------------------------+
|            2 |                  1 | file://component_audit_log_filter |
+--------------+--------------------+-----------------------------------+
1 row in set (0.00 sec)
```

Installing the component creates two new tables in the mysql system database: audit_log_filter and audit_log_user. These tables store the audit log filter definitions and the user-to-filter mappings. Together, they are referred to as the audit log filter tables.

```
+------------------------------------------------------+
| Tables_in_mysql                                      |
+------------------------------------------------------+
| audit_log_filter                                     |
| audit_log_user                                       |
+------------------------------------------------------+
```

Although the configuration is persisted in these tables, they are not usually modified directly with INSERT or UPDATE statements. Instead, MySQL provides built-in functions such as:

* audit_log_filter_set_filter()
* audit_log_filter_set_user() 

To manage filter definitions and user assignments safely.

Configure the my.cnf file to define the desired audit log output format and specify the location of the audit.log file. In the example below, the log format is set to JSON, but other formats (e.g., NEW or OLD) can also be configured depending on your requirements. The audit log file can be written to any path accessible to the MySQL server process.

Example Changes:
```
[mysqld]
# auditlog 
audit_log_filter.format=JSON
audit_log_filter.file=/var/lib/mysql/audit.log
```
Restart mysql server to apply the changes:
```
sudo systemctl restart mysqld
```
The audit log filter install is complete. Now we can start using the audit log filter component. 

### Creating Audit Log Filters
The audit log filter component in MySQL 8.4 provides fine-grained control over database auditing. Instead of logging all events indiscriminately, administrators can define audit log filters, which are rule sets that determine exactly which events should be captured and which should be excluded.

This allows you to:

* Log only the activity relevant to security, compliance, or troubleshooting.
* Reduce unnecessary noise and audit log volume.
* Apply different filters to specific users, hosts, or accounts for tailored auditing.

Because filters can be customized and assigned at the user or host level, the audit log filter component offers both flexibility and efficiency, making it a powerful mechanism for monitoring and securing database activity while minimizing overhead.

Lets create a rule that will log all events:
```
SELECT audit_log_filter_set_filter('log_all_events', '{ "filter": {"log": true } }');
```
Lets assign the rule to the user:
```
SELECT audit_log_filter_set_user('%', 'log_all_events');
SELECT audit_log_filter_flush();
```
Now all users will have all their events logged.

Before proceeding, ensure that the jq utility is installed on your system. The installation commands provided in the examples below are compatible with both RHEL-based and Debian-based distributions.

RHEL builds
```
sudo yum install jq
```
Debian builds
```
sudo apt install jq
```
To validate that the audit log filter is functioning as expected, we can inspect the raw contents of the audit.log file. Since the log entries are in JSON format, using jq provides an efficient way to query and extract specific events. For example, to filter and display only connection-related events, run:
```
cat audit.log | jq '.[]|select(.class=="connection")'
```
This command streams the log file, parses the JSON structure, and returns only entries where the "class" field is equal to "connection". This approach allows for targeted analysis, making it easier to verify filter behavior, troubleshoot issues, or monitor specific event classes without manually parsing large volumes of log data.

Example Output:
```
{
  "timestamp": "2025-07-24 07:18:00",
  "id": 27110,
  "class": "connection",
  "event": "connect",
  "connection_id": 415,
  "account": {
    "user": "wayne",
    "host": "localhost"
  },
  "login": {
    "user": "wayne",
    "os": "",
    "ip": "",
    "proxy": ""
  },
  "connection_data": {
    "connection_type": "socket",
    "status": 0,
    "db": ""
  },
  "connection_attributes": {
    "_pid": "717914",
    "_platform": "aarch64",
    "_os": "Linux",
    "_client_name": "libmysql",
    "os_user": "wayne",
    "_client_version": "8.4.5-5",
    "program_name": "mysql"
  }
}
```
I’ll cover more advanced filter configurations in a follow-up post—stay tuned for Part 2 of the Audit Log Filter Component series.

In summary, the audit log filter component in MySQL 8.4 provides administrators with a flexible and fine-grained approach to database auditing. By tailoring filters to specific users, hosts, and event types, you can ensure that only the most relevant activity is logged, making it easier to meet compliance requirements while reducing overhead. With proper configuration and careful use of filters, you can transform the audit log from a noisy data dump into a precise monitoring tool that strengthens both security and observability in your MySQL environment.