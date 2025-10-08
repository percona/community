---
title: "Audit Log Filters Part II"
date: "2025-10-08T00:00:00+00:00"
tags: ["Opensource", "Audit Log", "filter", "component", "MySQL", "Community", "Percona Server", "PXC"]
categories: ["MySQL"]
authors:
  - wayne
images:
  - blog/2025/10/audit-log-filters.png
  
---
In my first post on the [MySQL 8.4 Audit Log Filter component](https://percona.community/blog/2025/09/18/audit-log-filter-component/), I covered how to install the component and configure a basic filter that captures all events. The Audit Log Filter framework offers a highly granular and configurable auditing mechanism, enabling administrators to log specific events based on criteria such as user, host, or event type. This selective approach enhances observability, supports compliance initiatives, and minimizes unnecessary logging overhead.

In this follow-up, we’ll take a deeper technical look at defining and optimizing audit log filters to capture only the most relevant database activities—delivering actionable audit data while significantly reducing noise and log volume.

### Example 1

Audit all events:

```
SELECT audit_log_filter_set_filter('log_all_events', '{
  "filter": {"log": true}
}');
```
Once this filter is created and assigned to a user (for example, with SELECT audit_log_filter_set_user('%', 'log_all_events');), every database event triggered by that user—or by all users if % is used—will be written to the audit log file.

In short:

This is the most permissive audit configuration possible. It’s typically used:
1. As a baseline test to verify that the audit log component is working.
2. In diagnostic or forensic scenarios where full visibility is required.

For production environments, however, it’s recommended to create more selective filters (e.g., by event class, command type, or user) to reduce log volume and improve performance. Which we will go into more detail in the upcoming examples. 

### Example 2

Log table access:

```
select audit_log_filter_set_filter('log_table_access', '{
  "filter": {
    "class": [
      { "name": "table_access" },
      { "name": "connection" },
      { "name": "general" }
    ]
  }
}');
```

#### Included Event Classes

1. table_access
  Logs events when MySQL reads from or writes to tables.
    * Useful for tracking which users or applications are accessing specific tables.
    * Helps in auditing data access patterns and detecting unauthorized data reads/writes.

2. connection
  Logs connection-related events such as user logins, logouts, and failed authentication attempts.
    * Important for tracking session activity and security auditing.

3. general
  Logs general query execution events—like statements sent to the server (e.g., SELECT, INSERT, UPDATE, etc.).
    * Useful for general SQL activity auditing.

#### What It Does Functionally

After this filter is defined and assigned to a user or host (for example, with
SELECT audit_log_filter_set_user('%', 'log_table_access');), MySQL will only log events that fall into one of these three classes.

All other event types—like administrative commands, stored program executions, or system-level actions—will be excluded from the audit log.

#### Why use this filter

This configuration strikes a balance between completeness and efficiency:

  * Captures key operational and access-related activity.
  * Avoids excessive log volume from irrelevant events.
  * Suitable for data access auditing, security monitoring, and compliance logging.

In short, log_table_access provides targeted visibility into table usage, connections, and general query activity—ideal for environments where tracking who accessed what data is more important than recording every internal event.

### Example 3

```
SELECT audit_log_filter_set_filter('log_minimum', '{
  "filter": {
    "class":
    [ { "name": "connection" }, { "name": "table_access", "event": [
      { "name": "delete"}, { "name": "insert"}, { "name": "update"} ]
    } ]
  }
}');
```

#### Included Event Classes

1. "class": "connection"
    * Logs all connection-level events:
    * connect: when a user logs in.
    * disconnect: when a session ends.
    * Failed logins and other connection-related actions.

Purpose: provides visibility into who connected, from where, and when.

2. "class": "table_access" with "event": [...]
    * Limits logging to specific table access events:
      *  "delete" → when rows are deleted.
      * "insert" → when new rows are added.
      * "update" → when existing rows are modified.
    * Read operations (like SELECT) and metadata queries are excluded.

#### What It Does Functionally

Once assigned to a user or host (e.g.
SELECT audit_log_filter_set_user('%', 'log_minimum');), this filter will produce audit entries only when:

  * A user connects or disconnects from MySQL.
  * A user performs a DML (Data Manipulation Language) operation that changes data in a table.

All other events — such as simple SELECT queries, schema reads, or administrative commands — will be ignored.

#### Why Use This Filter

This is a minimalist, high-value audit configuration. It’s designed to:
  * Track security-relevant activity (connections and data changes).
  * Meet compliance requirements with low performance overhead.
  * Prevent excessive logging and disk usage.

In Short log_minimum is an efficient auditing strategy for production environments where you only need to know:

  * Who accessed the database, and
  * What data they changed.

It gives you essential accountability and change tracking without the overhead of logging every read or administrative event.

### Example 4

```
SELECT audit_log_filter_set_filter('log_connections', '{
  "filter": {
    "class": [
      { "name": "connection",
        "event": [
          { "name": "connect"},
          { "name": "disconnect"}
        ]
      }
    ]
  }
}');
```
#### Included Event Classes
1. "class": "connection"
This class captures events related to user sessions and authentication.

2. "event": ["connect", "disconnect"]
    * connect, Logged when a client establishes a connection to the MySQL server.
    Includes details like username, host, client program, IP address, and connection method.
    * disconnect, Logged when that client session ends or times out.
    Useful for tracking session duration and identifying abnormal terminations.

#### Why Use This Filter

This filter is particularly useful when you need to:
  * Monitor user logins and logouts without recording query activity.  
  * Audit connection patterns (e.g., who connected, from where, and when).  
  * Maintain minimal log size and low overhead.  
  * Support security investigations or session tracking without performance impact.

In short the log_connections filter provides a focused, low-overhead auditing strategy that records only connection lifecycle events. It’s ideal for environments where you primarily need to know who connected to the database, when, and from where without capturing every SQL statement or table access.

### Examaple 5
```
SELECT audit_log_filter_set_filter('log_full_table_access', '{
  "filter": {
    "class": [
      {
        "name": "connection",
        "event": [
          { "name": "connect"},
          { "name": "disconnect"}
        ]
      },
      {
        "name": "query",
        "event": [
          {
            "name": "start",
            "log": {
              "or": [
                { "field": { "name": "sql_command_id", "value": "select"} },
                { "field": { "name": "sql_command_id", "value": "insert"} },
                { "field": { "name": "sql_command_id", "value": "update"} },
                { "field": { "name": "sql_command_id", "value": "delete"} },
                { "field": { "name": "sql_command_id", "value": "truncate"} },
                { "field": { "name": "sql_command_id", "value": "create_table"} },
                { "field": { "name": "sql_command_id", "value": "alter_table"} },
                { "field": { "name": "sql_command_id", "value": "drop_table"} }
              ]
            }
          }
        ]
      }
    ]
  }
}');
```
This statement defines a MySQL Audit Log Filter called log_full_table_access, which is designed to capture both connection activity and all table-related SQL operations — including reads, writes, and schema changes. It provides broad visibility into how users interact with tables in the database while filtering out unrelated or low-value events.

#### Included Event Classes

After assigning it to users or hosts (e.g.
SELECT audit_log_filter_set_user('%', 'log_full_table_access');), MySQL will log:

  * Connection lifecycle events (connect, disconnect)
  * All DML statements (SELECT, INSERT, UPDATE, DELETE, TRUNCATE)
  * All DDL statements that create, modify, or remove tables (CREATE TABLE, ALTER TABLE, DROP TABLE)

Everything else — administrative commands, stored procedure calls, replication control, etc. — will be excluded.

#### Why Use This Filter

This filter offers a comprehensive audit view of how users interact with data and schema structures — perfect for compliance, forensic analysis, or access accountability.
It ensures that all table reads, writes, and structure changes are tracked without overwhelming the log with irrelevant internal events.

In Short, log_full_table_access provides a broad but targeted audit scope:
  * Tracks connections for user session context.
  * Logs all table-level operations, both data and schema-related.
  * Delivers complete visibility into how data is accessed and changed, making it ideal for security auditing and regulatory compliance scenarios.

### Final Summary

The MySQL 8.4 Audit Log Filter component provides a powerful and flexible framework for controlling how database activity is captured and logged. By allowing administrators to define granular filters based on event class, event type, user, or host, it transforms auditing from an all-or-nothing process into a precisely tuned observability tool.

In this post, we explored a range of filter examples—from the most permissive (log_all_events) to more focused configurations like log_minimum, log_connections, and log_full_table_access. Each serves a different operational or compliance purpose:

  * log_all_events – Captures every event for baseline validation or forensic debugging.
  * log_table_access – Balances visibility and performance by logging table, connection, and general query activity.
  * log_minimum – Targets critical actions such as connections and data modifications, providing essential accountability with minimal overhead.
  * log_connections – Focuses solely on login and logout events, ideal for lightweight session auditing.
  * log_full_table_access – Delivers comprehensive insight into all table-level DML and DDL operations along with connection tracking, suitable for compliance and change auditing.

By tailoring filters to specific operational needs, administrators can significantly reduce log volume, improve performance, and focus on high-value security and compliance events. The result is a leaner, more informative audit log that provides actionable insight into how users and applications interact with your MySQL environment—without the burden of unnecessary data.

### Reference
  * blah
  * blah

### Special Thanks to:
  Yura Sorokin for the collabotration to making this blog post happen.