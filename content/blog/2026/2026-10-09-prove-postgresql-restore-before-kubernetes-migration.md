---
title: "Prove your PostgreSQL restore before a Kubernetes migration"
date: "2026-10-09T12:00:00+02:00"
draft: false
tags: ['PostgreSQL', 'Kubernetes', 'Backup', 'Recovery', 'Community']
categories: ['Community']
authors:
  - timothy_olaleke
slug: prove-postgresql-restore-before-kubernetes-migration
---

A migration plan can name every component and still leave the useful question unanswered: if the move fails, can the application work again? A dump file is not that answer. A restore into a new database, followed by the checks the application actually needs, is.

## Define what recovered means

For this lab I treated the application as a small order service. Recovered meant four checks, and nothing else:

- The login role app_orders can connect to the restored database.
- The known order lab-customer-1001 is present and still has two line items.
- That role can insert a new order and one line item.
- The insert uses the restored sequence and the foreign key, so the new line points at the new order.

I did not treat "pg_restore exited 0" as recovered. I also did not treat a connection as the postgres superuser as recovered.

The backup was taken in the same session, so this lab does not measure how much data an older dump would miss. The restore times below are for a 64 kB example. They are not a production recovery-time objective.

## One example, two clusters

I built this localhost lab for the article using synthetic data and two throwaway PostgreSQL instances. Both were PostgreSQL 16.14 from Homebrew, with client tools of the same version. The exercise did not use a production host, password, or customer record.

The source database, orders_src, had the pgcrypto extension, an orders table, an order_items table, and grants for app_orders. The role was created in the source cluster. It was not created inside the database dump.

```sql
-- Selected setup statements; full example in the appendix.
CREATE ROLE app_orders LOGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- orders.id defaults to gen_random_uuid()
-- order_items.order_id references orders(id)
GRANT USAGE ON SCHEMA public TO app_orders;
GRANT SELECT, INSERT ON orders, order_items TO app_orders;
```

I dumped only that database:

```sh
pg_dump --host=127.0.0.1 --port=55432 --username=postgres \
  --dbname=orders_src --format=custom --file=article-lab.dump
```

That command exited 0 in 0.07 seconds. The custom-format file was 5,170 bytes. The archive header said it was created at 2026-10-01 10:57:05 CAT from database version 16.14. pg_restore --list showed tables, data, grants, the pgcrypto extension, and a default privilege. It had no ROLE entry for app_orders.

The public table data was 64 kB. I am not using the size of the whole database directory as the size of the example.

## The finding

The first useful failure did not appear when I restored into another database on the source cluster. That restore exited 0, but it was insufficient for validating recovery into a fresh cluster. app_orders was already a cluster role, so the grants had something to attach to. A same-cluster restore can test other recovery scenarios; it does not test whether a new cluster has the required roles.

I then created a second instance on port 55433. Its only role was postgres. I created an empty orders_dst from template0 and restored the same file:

```sh
pg_restore --host=127.0.0.1 --port=55433 --username=postgres \
  --dbname=orders_dst --exit-on-error --single-transaction \
  article-lab.dump
```

That command exited 1 in 0.04 seconds. The error was:

```text
pg_restore: error: could not execute query: ERROR:  role "app_orders" does not exist
Command was: GRANT USAGE ON SCHEMA public TO app_orders;
```

Because the restore used --single-transaction, the failed grant rolled the load back. \dt on orders_dst reported no relations. A dump that listed tables, data, and grants was still not a complete recovery plan. The missing piece was cluster state: the login role.

I created only that role on the second instance and ran the same pg_restore again. It exited 0 in 0.05 seconds. pgcrypto 1.3 was present after the restore, because this target server shipped that extension. Connecting as app_orders, the known order still had two items. An insert of lab-customer-restore-check with line SKU-C and quantity 1 succeeded, and the foreign key held.

A custom dump can contain the tables, data, and grants needed by an application yet omit a role those grants depend on. A same-cluster restore can therefore succeed while a fresh-cluster restore fails.

## What changes when you repeat this in Kubernetes

The dump file does not change. The target does.

In this lab, "a new instance" was a second PostgreSQL cluster on another port. The equivalent Kubernetes target is a freshly initialized PostgreSQL cluster with new storage, whether created manually or by an operator. A replacement pod that mounts the existing data volume retains the database state, including roles; restarting a pod alone does not reproduce this test. Bootstrap credentials may be supplied through a Secret, but PostgreSQL roles are cluster state, not contents of article-lab.dump. If app_orders is absent in the fresh target, replaying this dump produces the same failed grant. Create the required application role before restoring. Do not assume the operator's bootstrap role is the role your application uses.

The connection settings also need validation. This lab used 127.0.0.1 and a local role. For Kubernetes, check that the application's Service endpoint, Secret, database name, and login role match the intended target; a migration may change some of them. pg_restore does not edit DATABASE_URL or Kubernetes resources. Run the same checks from the application process: read lab-customer-1001, then insert one disposable order and its line item. A laptop or port-forward check does not exercise the same network path as the application pod and can pass while that pod still cannot connect.

The server package can change too. Both instances here were PostgreSQL 16.14 from the same Homebrew install, so pgcrypto 1.3 restored cleanly. A Kubernetes image can omit that extension or ship another version. After restore, check pg_extension inside the target, then run the application checks. Do not infer the extension from the source cluster.

## What this lab does not prove

It does not prove operator backup, volume snapshots, failover, or point-in-time recovery. Those are different mechanisms. A logical dump does not include the write-ahead log or the persistent volume.

It does not prove a production recovery time. The successful restore took 0.05 seconds for this 64 kB example. Larger datasets and different storage, hardware, and validation work can change that substantially. The backup being seconds old limits what this exercise says about potential data loss; it does not explain the restore speed.

It does not prove rollback. I took no writes on the source after the dump. During a migration, those writes exist. Before the cutover, decide who stops writes, and do not point the application back at the old database unless you have a plan for writes that happened after the dump. This lab did not test that plan.

The decision from the exercise is narrow. Before calling a Kubernetes migration recoverable, initialize a fresh PostgreSQL cluster, provision the roles and extension packages the restore requires, restore the dump, and run the application checks from the workload that will connect. Then test the backup method production will actually use. A green restore on the source cluster alone does not establish fresh-cluster recovery.

## Sources

[PostgreSQL 16 SQL dump guidance](https://www.postgresql.org/docs/16/backup-dump.html)

[PostgreSQL 16 pg_restore reference](https://www.postgresql.org/docs/16/app-pgrestore.html)


## Appendix: Reproduce the missing-role failure

This script reconstructs a minimal example of the finding; it is not the source of the original 64 kB size, archive size, or timings above. It was separately executed with PostgreSQL 16.14: the same-cluster restore succeeded, the fresh-cluster restore failed on the missing role, no public tables remained after rollback, and creating the role allowed restore and application-role checks to pass. Both companion instances were stopped afterward.
Save the script as reproduce.sh and run it with sh reproduce.sh. It defaults to the Homebrew PostgreSQL 16 tools; set PG_BINDIR to your PostgreSQL 16 bin directory if needed. It creates private temporary data directories and Unix sockets, listens on no TCP interface, and retains logs and the archive in the evidence directory it prints. The source and target use local trust authentication only for this disposable exercise. Do not reuse that authentication setup for a deployed database.

```sh
#!/bin/sh
set -eu
umask 077
PG_BINDIR=${PG_BINDIR:-/opt/homebrew/opt/postgresql@16/bin}
TASK_LAB=$(mktemp -d /tmp/pg-restore-companion.XXXXXX)
cleanup() {
 "$PG_BINDIR/pg_ctl" -D "$TASK_LAB/target" -m fast -w stop >/dev/null 2>&1 || true
 "$PG_BINDIR/pg_ctl" -D "$TASK_LAB/source" -m fast -w stop >/dev/null 2>&1 || true
}
trap cleanup EXIT HUP INT TERM
mkdir "$TASK_LAB/socket"
printf 'Evidence directory: %s\n' "$TASK_LAB"
"$PG_BINDIR/postgres" --version
for instance in source target; do
 "$PG_BINDIR/initdb" -D "$TASK_LAB/$instance" -U postgres --auth=trust --no-locale >"$TASK_LAB/$instance-init.log"
done
"$PG_BINDIR/pg_ctl" -D "$TASK_LAB/source" -l "$TASK_LAB/source.log" -o "-k $TASK_LAB/socket -p 55442 -c listen_addresses=''" -w start >/dev/null
"$PG_BINDIR/pg_ctl" -D "$TASK_LAB/target" -l "$TASK_LAB/target.log" -o "-k $TASK_LAB/socket -p 55443 -c listen_addresses=''" -w start >/dev/null
export PGHOST="$TASK_LAB/socket" PGUSER=postgres
"$PG_BINDIR/createdb" -p 55442 -T template0 orders_src
"$PG_BINDIR/psql" -X -v ON_ERROR_STOP=1 -p 55442 -d orders_src <<'SQL'
CREATE ROLE app_orders LOGIN;
CREATE EXTENSION pgcrypto;
CREATE TABLE orders (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 customer_ref text NOT NULL UNIQUE
);
CREATE TABLE order_items (
 id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
 order_id uuid NOT NULL REFERENCES orders(id),
 sku text NOT NULL,
 quantity integer NOT NULL CHECK (quantity > 0)
);
INSERT INTO orders(customer_ref) VALUES ('lab-customer-1001');
INSERT INTO order_items(order_id,sku,quantity)
 SELECT id,'SKU-A',1 FROM orders WHERE customer_ref='lab-customer-1001';
INSERT INTO order_items(order_id,sku,quantity)
 SELECT id,'SKU-B',2 FROM orders WHERE customer_ref='lab-customer-1001';
GRANT USAGE ON SCHEMA public TO app_orders;
GRANT SELECT,INSERT ON orders,order_items TO app_orders;
GRANT USAGE,SELECT ON SEQUENCE order_items_id_seq TO app_orders;
SQL
"$PG_BINDIR/pg_dump" -p 55442 -d orders_src -Fc -f "$TASK_LAB/article-lab.dump"
"$PG_BINDIR/pg_restore" --list "$TASK_LAB/article-lab.dump" >"$TASK_LAB/archive-list.txt"
"$PG_BINDIR/createdb" -p 55442 -T template0 orders_same_cluster
"$PG_BINDIR/pg_restore" -p 55442 -d orders_same_cluster --exit-on-error --single-transaction "$TASK_LAB/article-lab.dump"
printf 'same_cluster_restore_exit=0\n'
"$PG_BINDIR/createdb" -p 55443 -T template0 orders_dst
set +e
"$PG_BINDIR/pg_restore" -p 55443 -d orders_dst --exit-on-error --single-transaction "$TASK_LAB/article-lab.dump" >"$TASK_LAB/first-restore.out" 2>"$TASK_LAB/first-restore.err"
TASK_FIRST_STATUS=$?
set -e
printf 'fresh_cluster_restore_exit=%s\n' "$TASK_FIRST_STATUS"
[ "$TASK_FIRST_STATUS" -eq 1 ]
cat "$TASK_LAB/first-restore.err"
TASK_TABLE_COUNT=$("$PG_BINDIR/psql" -XAt -p 55443 -d orders_dst -c "SELECT count(*) FROM pg_tables WHERE schemaname='public'")
printf 'tables_after_failed_restore=%s\n' "$TASK_TABLE_COUNT"
[ "$TASK_TABLE_COUNT" -eq 0 ]
"$PG_BINDIR/psql" -X -v ON_ERROR_STOP=1 -p 55443 -d postgres -c 'CREATE ROLE app_orders LOGIN;'
"$PG_BINDIR/pg_restore" -p 55443 -d orders_dst --exit-on-error --single-transaction "$TASK_LAB/article-lab.dump"
printf 'restore_after_role_creation_exit=0\n'
"$PG_BINDIR/psql" -X -v ON_ERROR_STOP=1 -p 55443 -U app_orders -d orders_dst <<'SQL'
SELECT current_user;
SELECT customer_ref,count(*) AS line_count FROM orders
 JOIN order_items ON order_items.order_id=orders.id
 WHERE customer_ref='lab-customer-1001' GROUP BY customer_ref;
DO $$ BEGIN
 IF (SELECT count(*) FROM orders JOIN order_items ON order_items.order_id=orders.id
     WHERE customer_ref='lab-customer-1001') <> 2 THEN
  RAISE EXCEPTION 'Known order did not retain two items';
 END IF;
END $$;
WITH new_order AS (
 INSERT INTO orders(customer_ref) VALUES ('lab-customer-restore-check') RETURNING id
)
INSERT INTO order_items(order_id,sku,quantity)
 SELECT id,'SKU-C',1 FROM new_order RETURNING id,order_id,sku,quantity;
DO $$ BEGIN
 IF (SELECT count(*) FROM orders JOIN order_items ON order_items.order_id=orders.id
     WHERE customer_ref='lab-customer-restore-check' AND sku='SKU-C' AND quantity=1) <> 1 THEN
  RAISE EXCEPTION 'New order validation failed';
 END IF;
END $$;
SQL
"$PG_BINDIR/psql" -X -p 55443 -d orders_dst -c "SELECT extname,extversion FROM pg_extension WHERE extname='pgcrypto'"
printf 'companion_checks=PASS\n'
cleanup
trap - EXIT HUP INT TERM
printf 'Both throwaway instances stopped; evidence retained at %s\n' "$TASK_LAB"
```

## Disclosure

AI assisted initial drafting, editing, and companion-script preparation and testing. I edited the article and supplied the original lab results. This is a synthetic-data lab, not a customer incident or a Percona Operator recovery test.
