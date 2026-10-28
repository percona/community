---
title: "PostgreSQL restores: preserve ownership and grants, or remap them deliberately"
date: 2026-10-13
draft: true
# The retained manuscript date is not a publication slot; editors will schedule this draft.
categories: [PostgreSQL, Community]
images: [blog/2026/10/postgresql-restore-permissions-cover.png]
tags: [PostgreSQL, Backups, Security]
authors: [haifeng_cheng]
slug: postgresql-restore-ownership-acls-default-privileges
---

A PostgreSQL restore can recover every row and still leave the application unable to insert the next one. To understand why, we need to look at ownership, table permissions and sequence permissions separately. Default privileges add a further question: who will create the next table?

This article follows two ways of restoring the same custom-format backup. The first preserves the source ownership and access control lists (ACLs), which record grants to roles. The second gives restored objects a new owner and explicitly grants the intended application permissions. The distinction matters because `pg_restore --no-owner` does not translate all references to old roles into new ones.

The examples use synthetic data in disposable local containers. AI/model assistance was used to develop the text and lab scripts; execution and checks were performed through automated tools. This is a lab exercise, not a production case study.

## Choose the restore policy

### Preserve ownership and ACLs

- **Restored objects:** Keep the source owners; create the required roles first.
- **Existing application access:** Replay the source grants.
- **Future objects:** Check the original creator’s default privileges.

### Remap deliberately

- **Restored objects:** Use `--no-owner --no-acl --role=target_owner`.
- **Existing application access:** Grant the target application’s schema, table and sequence privileges explicitly.
- **Future objects:** Set defaults for the role that actually creates the objects.

`--no-owner` alone is not the second policy: it changes ownership without translating role names in the archived grants. The diagnostic branch below shows the difference.

## What the lab controls

The lab pins PostgreSQL **18.4**, using the `linux/amd64` image:

```text
postgres:18.4-bookworm@sha256:882236b897e39051d2368c5ccc6cda944904723506b2dfc97f2a8f5bc9afa382
```

Docker is version **28.4.0**. The server and tools reported **18.4 (Debian 18.4-1.pgdg12+1)**. The digest identifies the tested image so that the environment can be reproduced; it is not a claim that 18.4 is the latest release.

The version-specific references are PostgreSQL's `REL_18_4` documentation for [restore options](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/pg_restore.sgml) and [default privileges](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/alter_default_privileges.sgml). Further references are listed in the [source notes](/blog/2026/10/postgresql-restore-permissions/references/source-notes.md).

The recorded verification run completed on **13 October 2026 at 08:10:20 UTC: PASS, 70 checks, no unexpected failures**. The 70 comprise **57 positive/state checks**, **12 expected permission failures with SQLSTATE 42501**, and **one expected missing-role restore failure**. Its [results](/blog/2026/10/postgresql-restore-permissions/outputs/run-03/results.json), [transcript](/blog/2026/10/postgresql-restore-permissions/outputs/run-03/transcript.log) and [checklist](/blog/2026/10/postgresql-restore-permissions/outputs/run-03/checklist.tsv) include the expected failures and cleanup.

Download and extract the [original reproducibility bundle](/blog/2026/10/postgresql-restore-permissions/haifeng-cheng-postgresql-restore-permissions-reproducibility.zip). It contains the unchanged scripts, raw outputs, checksums and limitations from the recorded lab. The [bundle SHA-256](/blog/2026/10/postgresql-restore-permissions/SHA256SUMS) identifies the download. The results below refer to the recorded 13 October run.

Use a local Docker engine for this disposable lab, not a production or shared remote daemon. Restore only archives from trusted sources: a restore can execute code chosen by the source superusers.

To reproduce from the companion directory, with Python 3, Docker and the pinned image available, choose a new output directory:

```sh
python3 scripts/run_lab.py --output outputs/my-fresh-run
```

The source and target are separate disposable PostgreSQL instances, with their data held in temporary memory-backed filesystems. Containers use no network and publish no ports; PostgreSQL accepts only local socket connections.

The owner, application and migration roles are synthetic and `NOLOGIN`. Checks connect locally as the bootstrap administrator, then use `SET ROLE` to exercise a non-superuser application's effective privileges. The remapped application is also checked for owner-role membership and elevated attributes. This tests what the role can do after the switch. It does not test application authentication, passwords, connection pooling or connection-time `CONNECT` permission.

The source database contains an `app` schema owned by `legacy_owner`, an application role called `legacy_app`, and a small table:

```sql
SET ROLE legacy_owner;

CREATE TABLE app.widgets (
    id bigserial PRIMARY KEY,
    payload text NOT NULL
);

GRANT USAGE ON SCHEMA app TO legacy_app;
GRANT SELECT, INSERT ON TABLE app.widgets TO legacy_app;
GRANT USAGE ON SEQUENCE app.widgets_id_seq TO legacy_app;

ALTER DEFAULT PRIVILEGES FOR ROLE legacy_owner IN SCHEMA app
    GRANT SELECT, INSERT ON TABLES TO legacy_app;
ALTER DEFAULT PRIVILEGES FOR ROLE legacy_owner IN SCHEMA app
    GRANT USAGE ON SEQUENCES TO legacy_app;
```

The explicit grants cover the existing table and sequence. The defaults set the policy for subsequent objects created by `legacy_owner` in this schema. We need both: default privileges do not change existing objects. [PostgreSQL documents that separation explicitly.](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html)

`bigserial` supplies a sequence-backed default, so an insert can expose a missing sequence permission. Table `INSERT` alone does not grant the right to call that sequence's `nextval`. Sequence `USAGE` is sufficient for ordinary ID allocation; the application does not need sequence `UPDATE`, which would also allow `setval`. [See sequence manipulation functions.](https://www.postgresql.org/docs/18/functions-sequence.html)

## Keep one complete archive

The source is dumped once using `pg_dump --format=custom`. Both policies use that same archive, and its transfer to the target is verified by SHA-256. Below are the PostgreSQL portions of the commands, executed inside the relevant container. The companion runner records the complete `docker exec` commands:

```sh
pg_dump -h /lab/socket -U postgres --format=custom \
    --file=/lab/source.dump lab_source
pg_restore --list /lab/source.dump
```

Keep the ACLs in the dump so that you can choose whether to preserve or replace them later. For ownership, `pg_dump --no-owner` is ignored for non-text archives: with a custom archive, you make that choice at restore time. [The `pg_dump` manual describes this behaviour.](https://www.postgresql.org/docs/18/app-pgdump.html)

The archive also has a clear limit: `pg_dump` exports one database, not definitions of cluster-wide roles. Our script creates the required synthetic roles separately. A real migration needs a reviewed policy for those roles, their memberships and any authentication configuration. The database archive does not provision them. [See the scope of `pg_dump`.](https://www.postgresql.org/docs/18/app-pgdump.html)

Each target database starts from `template0`. Restores use `--single-transaction`, which also implies exit-on-error, so a failed restore does not leave half of the archive installed.

These commands do not use `--create`: target database creation and ownership are chosen separately, and restoring the source database creation, ownership and database-level ACL policy is outside this comparison. Database privileges need a separate review. [These restore options are documented here.](https://www.postgresql.org/docs/18/app-pgrestore.html)

## Policy 1: preserve the source identities

The preserving command has no ownership or ACL suppression flags:

```sh
pg_restore -h /lab/socket -U postgres --dbname lab_preserved \
    --single-transaction --exit-on-error /lab/source.dump
```

First, try the restore on a target that has neither `legacy_owner` nor `legacy_app`. The lab captures this expected failure with its exit status and PostgreSQL error, then checks that the single transaction left no restored schema behind. To preserve the original ownership and grants, create the original roles and repeat the restore:

```sql
CREATE ROLE legacy_owner NOLOGIN;
CREATE ROLE legacy_app NOLOGIN;
```

These role definitions are enough for this synthetic test; they are not a recipe for copying a production role hierarchy.

The first restore exited **1**, with this recorded error:

```text
pg_restore: error: could not execute query: ERROR:  role "legacy_owner" does not exist
Command was: ALTER SCHEMA app OWNER TO legacy_owner;
```

The schema-absence assertion returned `t`, confirming rollback. After role creation, the restore exited **0**; the ownership, default-ACL and application-operation checks passed.

After the successful restore, inspect object ownership, ACLs and `pg_default_acl`. A row count alone cannot show whether the application has the access it needs. `legacy_owner` should own the restored schema, table and sequence; `legacy_app` should have the source grants. Test both reads and generated-ID inserts under the application role:

```sql
SET ROLE legacy_app;
SELECT count(*) >= 0 FROM app.widgets;
BEGIN;
INSERT INTO app.widgets (payload)
    VALUES ('synthetic-probe') RETURNING id > 0;
ROLLBACK;
RESET ROLE;
```

`RETURNING id > 0` also requires `SELECT` on `id`; our table-level `SELECT` grant covers that requirement. Successful insert probes are rolled back, and the runner checks that the original two synthetic rows remain unchanged. Rollback does not reclaim the sequence values consumed by those successful inserts.

When isolating a missing sequence permission, use a plain insert first. Otherwise, a missing `RETURNING` privilege could confuse the result. [See `INSERT` privileges.](https://www.postgresql.org/docs/18/sql-insert.html)

Next, create a new sequence-backed table while the effective role is `legacy_owner`. The restored default privileges should give `legacy_app` the intended access to the new table and its sequence. This checks the source's future-object policy, which a test of the restored table alone cannot establish.

## Why `--no-owner` alone is not a role map

For a diagnostic restore, keep the source roles available and change only the ownership policy:

```sh
pg_restore -h /lab/socket -U postgres --dbname lab_owner_only \
    --single-transaction --exit-on-error --no-owner /lab/source.dump
```

In this branch, the restore runs as the bootstrap administrator. Suppressing ownership commands makes the restoring role own newly created objects. It does not replace the archive's `legacy_app` grantee with `target_app`.

The same limit applies to default privileges. An entry belonging to `legacy_owner` does not become an entry for the new object owner. The original ACL statements are still eligible for restoration. [This follows from the separate `--no-owner` and `--no-acl` options.](https://www.postgresql.org/docs/18/app-pgrestore.html)

The catalogue checks found `postgres` ownership, retained `legacy_app` access and two default-ACL entries belonging to `legacy_owner`. `legacy_app` could still read and insert into the restored table; `target_app` failed at schema access.

The future-table check exposed the other consequence. A new `app.owner_only_future` table created as `postgres` gave `legacy_app` neither table access nor sequence `USAGE`: the retained defaults belonged to a different creator.

Ownership has changed, but the old role names remain in the permission policy. On a target lacking those roles, retained ACL statements can also cause restore errors. Treat `--no-owner` as an ownership switch, not a general role-renaming mechanism.

## Policy 2: rebuild the intended permissions

The second policy introduces `target_owner` and `target_app`. It restores into a fresh database owned by `target_owner`:

```sh
pg_restore -h /lab/socket -U postgres --dbname lab_remapped \
    --single-transaction --exit-on-error --no-owner --no-acl \
    --role=target_owner /lab/source.dump
```

Here, `--role` performs `SET ROLE` after connection. Combined with `--no-owner`, that makes `target_owner` the role creating and owning the restored objects.

The separate `--no-acl` option suppresses the archived privilege restoration, including default-privilege grants. It does not revoke built-in defaults or privileges already present on the target. We still need to grant the application its intended access through explicit SQL after the restore. [See `pg_restore`.](https://www.postgresql.org/docs/18/app-pgrestore.html)

Start by attempting a read as `target_app`. It should fail at the schema, before reaching the table. Capture that expected failure, then grant lookup access to the schema:

```sql
GRANT USAGE ON SCHEMA app TO target_app;
```

The next read should reach the table and fail there. Now grant the application the two table privileges it needs:

```sql
GRANT SELECT, INSERT ON TABLE app.widgets TO target_app;
```

The read should now pass, but an insert using the default ID should still fail on `widgets_id_seq`. Grant access to that sequence:

```sql
GRANT USAGE ON SEQUENCE app.widgets_id_seq TO target_app;
```

The recorded failures, in order, were:

```text
ERROR:  42501: permission denied for schema app
ERROR:  42501: permission denied for table widgets
ERROR:  42501: permission denied for sequence widgets_id_seq
```

The runner uses non-interactive SQL execution with `ON_ERROR_STOP=1`, under which these errors returned psql exit **3**; their SQLSTATE was **42501**. After the sequence grant, both application `SELECT` and generated-ID `INSERT ... RETURNING` checks returned `t`, with exit **0**.

Each failure identifies a separate permission: looking up an object in a schema, operating on a table, or allocating an ID from a sequence. Granting `ALL PRIVILEGES` would hide these boundaries and give the application powers it does not need. [PostgreSQL treats these privileges separately.](https://www.postgresql.org/docs/18/ddl-priv.html)

The repair must also leave unrelated operations blocked. The application must still fail to create a table in `app`, update or delete the test rows, and call `setval` on the sequence. These negative checks show that the grants stayed within this example's requirements.

## Default privileges apply only to future objects

Suppose a migration has already created `app.early_widgets` before you install replacement defaults. Configure the intended future policy under `target_owner`:

```sql
ALTER DEFAULT PRIVILEGES FOR ROLE target_owner IN SCHEMA app
    GRANT SELECT, INSERT ON TABLES TO target_app;
ALTER DEFAULT PRIVILEGES FOR ROLE target_owner IN SCHEMA app
    GRANT USAGE ON SEQUENCES TO target_app;
```

The previously created table still needs its own grants:

```sql
GRANT SELECT, INSERT ON TABLE app.early_widgets TO target_app;
GRANT USAGE ON SEQUENCE app.early_widgets_id_seq TO target_app;
```

Check the early table before applying its explicit repair: it should remain inaccessible even after the defaults are installed. Then repair it with the named grants above.

Create `app.future_widgets` *after* the defaults, with `target_owner` as the current role. The application should now be able to read and insert without additional object grants.

This policy covers every future table and sequence created by that owner in `app`. That scope is intentional. If some future tables should remain private, use a different schema or a more selective provisioning policy. Defaults are convenient, but they still grant access. [See schema-specific default privileges.](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html)

Role membership introduces another trap. The lab grants `target_owner` to `migration_role`, then creates `app.migration_widgets` while `current_user` is still `migration_role`. The membership configuration must allow the intended inherited schema privilege for this DDL and the later `SET ROLE target_owner`.

Membership provides schema access in this lab, but the new table belongs to `migration_role`. PostgreSQL applies the current creator's defaults, not defaults inherited from roles of which it is a member. Consequently, `target_owner`'s defaults do not grant `target_app` access to that table. [This creator-role rule is explicit in the manual.](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html)

To follow the lab's ownership policy, the migration changes its effective role before creating subsequent objects. The test first sets the session authorisation to `migration_role`. This means that successful `SET ROLE` depends on that role's membership, rather than the bootstrap administrator's superuser power:

```sql
SET SESSION AUTHORIZATION migration_role;
SET ROLE target_owner;
CREATE TABLE app.migration_fixed_widgets (
    id bigserial PRIMARY KEY,
    payload text NOT NULL
);
RESET ROLE;
```

The resulting table and sequence belong to `target_owner`, so its defaults apply.

The earlier object created as `migration_role` does not change retroactively. The lab repairs its application access with a separate named table-and-sequence grant, while its owner remains `migration_role`. Whether to change that existing object's owner is a separate decision.

The recorded results show both traps: `early_widgets` still produced `permission denied for table early_widgets` after the defaults, and the member-created table produced `permission denied for table migration_widgets`. Both had SQLSTATE **42501**.

The explicitly repaired early table, the future owner-created table and `migration_fixed_widgets` all passed their application `SELECT`, generated-ID `INSERT` and privilege checks.

## A restore is complete when the chosen policy passes

The companion checklist records the required result for each operation, the actual exit status and the associated log. An expected failure must match the intended PostgreSQL error as well as return a non-zero status. An unrelated connection error does not count as a passing permissions test. The recorded final run recreated both disposable instances from scratch and repeated the checks.

For preservation, check that the source owners, existing ACLs and original creator's future-object defaults all work.

For remapping, verify the new owner, grant the intended application permissions explicitly, repair existing objects separately from future defaults, and run migration DDL as the intended creator. In either policy, test both the application operation and the powers it must not have.

The scope is deliberately small: ordinary tables, `bigserial` sequences, one application schema and synthetic roles. It does not establish behaviour for identity columns, extensions, row-level security, large objects, security-definer functions, partitioning, tablespaces, production authentication or cross-version migrations.

Sequence values may have gaps after failed statements and after successful inserts whose transactions are rolled back, so the checks do not demand consecutive IDs.

*This post is part of the [Percona Community Writers Program](/blog/write-for-percona-community/).*
