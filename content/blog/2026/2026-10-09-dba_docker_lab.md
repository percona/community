---
title: "Docker DBA Lab"
date: "2026-10-12T00:00:00+00:00"
tags: ["OpenSource", "Percona", "MySQL", "Docker", "PostgreSQL", "PMM", "PXC"]
categories: ["MySQL"]
authors:
  - wayne
images:
  - blog/2026/10/dba_docker_lab.png
---

# Building a Database DBA Lab with Docker, PostgreSQL, MySQL, and Percona Monitoring and Management

*How I built a local database playground, learned a few lessons the hard way, and created a practical command reference along the way.*

## Introduction

One of the best ways to learn database administration is to get your hands dirty.

Documentation is important, but there's something different about building your own environment, breaking it, troubleshooting it, and eventually understanding why everything works.

Recently, I decided to create a local database lab using Docker Desktop on my Mac. My goal was straightforward: build an environment where I could experiment with MySQL, PostgreSQL, Percona XtraDB Cluster (PXC), and Percona Monitoring and Management (PMM), without worrying about disrupting a production environment.

What started as a few containers quickly became a much more interesting learning experience.

Along the way, I ran into Docker networking problems, container persistence challenges, cluster bootstrap issues, and PostgreSQL monitoring configuration. This article shows the setup I recommend after working through those problems, so you can start with the right foundation instead of discovering it at the end.

## 1. Building the Lab

The foundation of my environment is Docker Desktop.

The lab includes:

- Percona Server for MySQL 8.4
- A three-node Percona XtraDB Cluster
- PostgreSQL 17
- PMM Server and PMM Client
- Persistent Docker volumes
- A shared Docker network

The architecture looks like this:

```text
Docker Desktop
│
├── pmm-network
│   ├── pmm-server
│   ├── pmm-client
│   ├── percona-server
│   ├── postgres-server
│   ├── pxc1
│   ├── pxc2
│   └── pxc3
│
└── Persistent Docker Volumes
    ├── pmm-data
    ├── pmm-client-data
    ├── mysql-data
    ├── postgres-data
    ├── pxc1_data
    ├── pxc2_data
    └── pxc3_data
```

There are two ways to build this.

### Option A (recommended): Docker Compose

Docker Compose lets you define every container, volume, and network attachment in one file. The whole lab becomes reproducible: one command brings it up, one command shuts it down, and nothing depends on remembering which `docker run` flags you used weeks ago.

I started out with individual `docker run` commands and later moved everything to Compose. If I were starting again, I would begin here.

First, keep passwords out of the Compose file by putting them in a `.env` file next to it (and out of version control):

```bash
# .env
MYSQL_ROOT_PASSWORD=change-me
PXC_ROOT_PASSWORD=change-me
POSTGRES_PASSWORD=change-me
PMM_ADMIN_PASSWORD=change-me
PG_MONITOR_PASSWORD=change-me
MYSQL_MONITOR_PASSWORD=change-me
```

Then define the lab in `docker-compose.yml`:

```yaml
services:
  pmm-server:
    image: percona/pmm-server:3.9.1
    platform: linux/amd64
    container_name: pmm-server
    ports:
      - "443:8443"
    volumes:
      - pmm-data:/srv
    networks: [pmm-network]

  pmm-client:
    image: percona/pmm-client:3.9.1
    container_name: pmm-client
    depends_on: [pmm-server]
    environment:
      PMM_AGENT_SERVER_ADDRESS: pmm-server:8443
      PMM_AGENT_SERVER_USERNAME: admin
      PMM_AGENT_SERVER_PASSWORD: ${PMM_ADMIN_PASSWORD}
      PMM_AGENT_SERVER_INSECURE_TLS: 1
      PMM_AGENT_SETUP: 1
      PMM_AGENT_CONFIG_FILE: config/pmm-agent.yaml
    volumes:
      - pmm-client-data:/usr/local/percona/pmm/config
    networks: [pmm-network]

  percona-server:
    image: percona/percona-server:8.4.11
    container_name: percona-server
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    networks: [pmm-network]

  postgres-server:
    image: postgres:17
    container_name: postgres-server
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    command: >
      postgres
      -c shared_preload_libraries=pg_stat_statements
      -c track_io_timing=on
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks: [pmm-network]

  pxc1:
    image: percona/percona-xtradb-cluster:8.4.11
    container_name: pxc1
    environment:
      CLUSTER_NAME: pxc-lab
      MYSQL_ROOT_PASSWORD: ${PXC_ROOT_PASSWORD}
    volumes:
    - pxc1_data:/var/lib/mysql
    - ./certs:/etc/mysql/certs:ro
    - ./conf.d:/etc/percona-xtradb-cluster.conf.d:ro
    stop_grace_period: 120s
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-uroot", "-p${PXC_ROOT_PASSWORD}"]
      interval: 10s
      retries: 30
    networks: [pmm-network]
    ports:
      - "3307:3306"

  pxc2:
    image: percona/percona-xtradb-cluster:8.4.11
    container_name: pxc2
    environment:
      CLUSTER_NAME: pxc-lab
      CLUSTER_JOIN: pxc1
      MYSQL_ROOT_PASSWORD: ${PXC_ROOT_PASSWORD}
    volumes:
      - pxc2_data:/var/lib/mysql
      - ./certs:/etc/mysql/certs:ro
      - ./conf.d:/etc/percona-xtradb-cluster.conf.d:ro
    stop_grace_period: 120s
    depends_on:
      pxc1:
        condition: service_healthy
    networks: [pmm-network]
    ports:
      - "3308:3306"

  pxc3:
    image: percona/percona-xtradb-cluster:8.4.11
    container_name: pxc3
    environment:
      CLUSTER_NAME: pxc-lab
      CLUSTER_JOIN: pxc1
      MYSQL_ROOT_PASSWORD: ${PXC_ROOT_PASSWORD}
    volumes:
      - pxc3_data:/var/lib/mysql
      - ./certs:/etc/mysql/certs:ro
      - ./conf.d:/etc/percona-xtradb-cluster.conf.d:ro
    stop_grace_period: 120s
    depends_on:
      - pxc2
    networks: [pmm-network]
    ports:
      - "3309:3306"

networks:
  pmm-network:
    name: pmm-network

volumes:
  pmm-data:
  pmm-client-data:
  mysql-data:
  postgres-data:
  pxc1_data:
  pxc2_data:
  pxc3_data:
```

A few design choices are worth calling out, because each one comes from a problem I hit:

- **Volumes and the network are declared up front.** Every database has persistent storage and is attached to `pmm-network` from the moment it is created, so there is nothing to wire up afterward.
- **All PXC nodes share the same SSL certificates.** Mismatched certificates were behind several of my early cluster join failures.
- **`stop_grace_period: 120s`** gives each PXC node time to shut down cleanly instead of being killed (exit code 137).
- **`depends_on` defines the PXC order.** Compose starts `pxc1` first and waits for it to be healthy before the others join. On shutdown, Compose stops dependents first, so the nodes leave in the order `pxc3`, `pxc2`, `pxc1`.

Bring the lab up and down with:

```bash
docker compose up -d
docker compose stop      # stops containers, keeps everything
docker compose down      # removes containers, keeps named volumes
```

### Option B (alternative): Individual `docker run` commands

If you prefer to build containers one at a time, or want to understand what Compose is doing for you, you can create the network yourself and attach containers to it:

```bash
docker network create pmm-network

docker run -d --name postgres-server \
  --network pmm-network \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:17
```

An existing container can be attached later:

```bash
docker network connect pmm-network postgres-server
```

This works, but you are responsible for recreating each container with exactly the same flags, volumes, and network settings every time. That is the main reason I recommend Option A. Whichever option you choose, avoid mixing the two for the same lab, because it becomes hard to tell which containers are managed by Compose and which are not.

### A networking lesson that applies either way

At one point, PMM couldn't resolve my PostgreSQL container:

```text
lookup postgres-server on 127.0.0.11:53: no such host
```

The problem wasn't PostgreSQL or PMM. The PostgreSQL container was stopped, so it had no active network endpoint, and Docker's internal DNS had nothing to return.

That was an important reminder: **always verify the container and network state before troubleshooting the application.**

## 2. Making Monitoring Persistent with PMM

Once the databases were running, I wanted visibility into their performance.

PMM provides dashboards and metrics for MySQL, PXC, and PostgreSQL. It consists of a server that stores and visualizes monitoring data and a client agent that collects database metrics.

The key thing to understand is that persistent storage and service registration are related, but they are not the same thing.

PMM Server maintains the monitoring inventory, while PMM Client has its own configuration and agent identity. If the client is recreated with a new identity, the association between the client and its registered services is lost. In my early setup, after recreating containers, the client listing showed only the basic agents:

```text
pmm_agent       Connected
node_exporter   Running
vmagent         Running
```

Two things prevent this, and both should be in place from the start:

1. **A persistent volume for the client configuration.** In the Compose file above, `pmm-client-data` keeps the agent identity across restarts and recreations.
2. **An idempotent registration script.** It adds each database only if it isn't already registered, so it is safe to run after every `docker compose up`.

Before registering, create a monitoring user in each database. For PostgreSQL, for example:

```sql
CREATE USER pmm WITH PASSWORD 'change-me';
GRANT pg_monitor TO pmm;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

Then the registration script, which reads credentials from the `.env` file rather than hardcoding them:

```bash
#!/usr/bin/env bash
# register-pmm.sh
set -euo pipefail
source .env

registered() {
  docker exec pmm-client pmm-admin list | grep -qw "$1"
}

if ! registered postgres-server; then
  docker exec pmm-client pmm-admin add postgresql \
    --username=pmm \
    --password="$PG_MONITOR_PASSWORD" \
    --host=postgres-server \
    --port=5432 \
    postgres-server
fi

for node in percona-server pxc1 pxc2 pxc3; do
  if ! registered "$node"; then
    docker exec pmm-client pmm-admin add mysql \
      --username=pmm \
      --password="$MYSQL_MONITOR_PASSWORD" \
      --host="$node" \
      --port=3306 \
      --query-source=perfschema \
      "$node"
  fi
done

docker exec pmm-client pmm-admin list
```

The takeaway: **a monitoring system should be designed to survive a restart, not just work immediately after installation.**

## 3. Learning PostgreSQL Through Real Workloads

With PostgreSQL running and connected to PMM, I wanted to do more than look at an idle dashboard.

I used sysbench to generate a workload against PostgreSQL 17.

My test environment included ten tables with approximately 750,000 rows each, giving me about 7.5 million rows to experiment with.

A sample workload command looked like this:

```bash
sysbench \
  --db-driver=pgsql \
  --pgsql-host=127.0.0.1 \
  --pgsql-port=5432 \
  --pgsql-user=postgres \
  --pgsql-db=sbtest \
  --tables=10 \
  --table-size=750000 \
  --threads=16 \
  --time=300 \
  --report-interval=5 \
  oltp_read_write run
```

With the workload running, PMM became much more interesting.

I could observe database activity, disk latency, query execution statistics, and changes in resource utilization.

This also helped me understand an important distinction: PostgreSQL tuple activity is not the same thing as SQL queries per second.

One query can read or return many tuples. Looking only at tuple counts without understanding the underlying queries can lead to incorrect conclusions about workload intensity.

## 4. Understanding PostgreSQL Query Performance

One of the most useful PostgreSQL features for troubleshooting is `EXPLAIN`.

For example:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM sbtest1
WHERE id BETWEEN 100 AND 200;
```

This shows the execution plan, actual execution measurements, and buffer activity.

I started paying attention to several key pieces of information:

- Whether PostgreSQL used a sequential scan or an index
- Estimated versus actual rows
- Execution time
- Buffer hits and reads
- Number of execution loops

Because the Compose file loads `pg_stat_statements` at startup, query statistics are aggregated from the beginning.

A useful query is:

```sql
SELECT
    calls,
    total_exec_time,
    mean_exec_time,
    rows,
    LEFT(query, 100) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

This provides a different perspective from looking at individual slow queries.

A query that takes only a fraction of a millisecond might still consume substantial cumulative execution time if it runs hundreds of thousands of times.

For a DBA, both individual latency and aggregate workload matter.

## 5. MVCC, Dead Tuples, and VACUUM

My next learning objective was understanding PostgreSQL's Multi-Version Concurrency Control (MVCC).

Unlike an in-place overwrite model, PostgreSQL commonly creates a new row version when a row is updated.

Older versions may remain until PostgreSQL determines they are no longer needed.

That leads directly to one of PostgreSQL's most important maintenance mechanisms: VACUUM.

I experimented with updating large numbers of rows:

```sql
UPDATE sbtest1
SET k = k + 1
WHERE id <= 300000;
```

Then checked the table statistics:

```sql
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    last_autovacuum,
    autovacuum_count
FROM pg_stat_user_tables
WHERE relname = 'sbtest1';
```

This gave me a practical way to observe dead tuple estimates and autovacuum activity.

I also explored what happens when a long-running transaction holds an old snapshot.

By starting a `REPEATABLE READ` transaction and leaving it open while another session updated rows, I could demonstrate how PostgreSQL may need to retain older row versions.

That helped connect several important DBA concepts:

**Long-running transactions → old snapshots → delayed tuple cleanup → potential table bloat.**

I also learned that normal VACUUM generally makes space reusable within PostgreSQL rather than immediately shrinking the table file.

`VACUUM FULL` can reclaim disk space by rewriting a table, but it requires an exclusive lock and is not something to run casually in production.

## 6. Operating the PXC Cluster Safely

My three-node Percona XtraDB Cluster taught me that **database containers need database-aware operational procedures.** That's why startup and shutdown are built into the Compose file rather than left to chance.

Early on, I ran into certificate problems, donor timeouts, cluster membership issues, and shutdowns that ended with exit code 137 (the container being killed before MySQL finished). The shared certificate directory, the healthcheck on `pxc1`, and `stop_grace_period` address those directly.

The shutdown procedure is simply:

```bash
docker compose stop pxc3 pxc2 pxc1
```

If you use Option B, do the same thing explicitly, one node at a time, with a long timeout:

```bash
docker stop -t 120 pxc3
docker stop -t 120 pxc2
docker stop -t 120 pxc1
```

To start the cluster again, check `grastate.dat` on each node and understand the meaning of `safe_to_bootstrap`:

```bash
docker run --rm -v pxc1_data:/data alpine cat /data/grastate.dat
```

After a clean shutdown, the last node to leave the cluster (here, `pxc1`) will have `safe_to_bootstrap: 1` and is the right node to start first.

After an unclean shutdown, selecting the correct bootstrap node requires recovery checks. Compare the recovered sequence numbers across nodes and bootstrap from the most advanced one. Simply changing `safe_to_bootstrap` to `1` without verifying that can lose data.

## 7. My Most Useful Commands

I kept a command cheat sheet from the start of the project, and it has become one of the most useful outcomes. It captures the commands I actually needed while learning and troubleshooting. I recommend starting one on day one.

For Docker:

```bash
# Running containers
docker ps

# All containers
docker ps -a

# Status of the Compose-managed lab
docker compose ps

# Follow logs
docker logs -f postgres-server

# Inspect network configuration
docker inspect postgres-server \
  --format '{{json .NetworkSettings.Networks}}'

# Resource usage
docker stats

# List Docker volumes
docker volume ls

# Check PMM services
docker exec pmm-client pmm-admin list
```

These commands are my first line of investigation whenever something isn't behaving as expected.

For PostgreSQL, my daily reference includes:

```sql
-- Current sessions
SELECT pid, usename, state, query
FROM pg_stat_activity;

-- Long-running transactions
SELECT
    pid,
    state,
    now() - xact_start AS transaction_age,
    query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL;

-- Dead tuples
SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Blocking sessions
SELECT
    pid,
    pg_blocking_pids(pid) AS blocked_by
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;
```

These are simple queries, but they form a useful starting point for troubleshooting.

## 8. Design Principles Behind the Lab

To summarize, these are the principles the setup above is built on:

1. **Define the whole lab in Docker Compose**, rather than mixing `docker run` commands with Compose-managed containers.
2. **Declare persistent volumes and network attachments before creating any databases.**
3. **Treat startup and shutdown as part of the design**, especially for PXC.
4. **Make PMM registration reproducible** with a persistent client volume and an idempotent script, and keep credentials out of scripts and command history.
5. **Keep a command cheat sheet from the beginning.**

## Final Thoughts

What began as an effort to build a small local database environment turned into a practical DBA learning experience.

I now have a place to explore PostgreSQL performance, MVCC, autovacuum, MySQL replication concepts, PXC clustering, and database monitoring without risking a production system.

Perhaps the biggest lesson is that the most valuable learning moments often happen when something breaks.

A Docker DNS failure teaches networking. A missing PMM registration teaches persistence and identity. A PXC bootstrap problem teaches cluster recovery. A growing dead tuple count teaches PostgreSQL MVCC.

And once you understand why something broke, you're much better prepared to troubleshoot it the next time.

**My next goal is to continue expanding the lab with PostgreSQL replication, backup and recovery, and more deliberate performance troubleshooting exercises.**

---

*This article describes a local learning environment. The commands and configurations are intended for experimentation and should be reviewed and adapted before use in production.*
