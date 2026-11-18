# PostgreSQL restore-permissions source notes

Consulted: 13 October 2026. Official sources only. These notes describe documentation and proposed checks; they are not execution evidence. The selected lab release is PostgreSQL **18.4**, subject to confirmation by its recorded server/client output. The `/docs/18/` URLs are the major-version manual, not a frozen copy of the 18.4 manual. Critical semantics were also checked against the exact **`REL_18_4` release tag** in the official `postgres/postgres` source mirror, as detailed below. Do not describe 18.4 as the latest release.

## Exact-release documentation verification

The following source documents were consulted through the browser at tag `REL_18_4`. These are release-tag references, not the moving `REL_18_STABLE` branch. Summaries below are paraphrases, with no verbatim excerpts. The tag establishes the source version; the independent lab evidence establishes the executed binary and image.

| Verified semantics at `REL_18_4` | Exact-release official source |
| --- | --- |
| `--no-owner` suppresses original ownership commands; `--no-acl` suppresses access-privilege restoration; `--role` issues `SET ROLE` after connecting; `--single-transaction` implies exit-on-error. | [pg_restore.sgml](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/pg_restore.sgml) |
| `pg_dump --no-owner` is ignored for archive output; use the restore option instead. | [pg_dump.sgml](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/pg_dump.sgml) |
| Defaults change future objects, not existing objects. The current creator's defaults apply at creation, without inheritance from role memberships. `FOR ROLE` identifies the creator; schema-local defaults add to global defaults. | [alter_default_privileges.sgml](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/alter_default_privileges.sgml) |
| Sequence `nextval` requires `USAGE` or `UPDATE`, `currval` needs `USAGE` or `SELECT`, and `setval` requires `UPDATE`. Sequence allocations need not be gapless. | [func.sgml, sequence-functions section](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/func.sgml) |
| `RETURNING` requires `SELECT` on the columns it references. | [insert.sgml](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/insert.sgml) |

No semantic discrepancy relevant to this lab was found between these tagged passages and the cited version 18 HTML pages. Prefer the tagged links when substantiating exact-18.4 claims, and the rendered manual links for convenient reading. Source line locations observed in the tagged files: pg_restore ownership 333–349, ACL 480–488, transaction 490–500, role 934–948; default privileges 95–107 and 145–158; sequence functions 18690–18775; INSERT 113–118 (browser line indices; source viewers may offset by one).

Supplementary implementation confirmation: [pg_backup_archiver.c at `REL_18_4`](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/src/bin/pg_dump/pg_backup_archiver.c) treats both ordinary ACL and DEFAULT ACL entries as ACL entries; its skip-ACL path excludes them. This supports the default-ACL omission test but does not replace the real restore checks.

## Restore flags and database scope

[PostgreSQL 18: pg_restore](https://www.postgresql.org/docs/18/app-pgrestore.html)

`--no-owner` suppresses commands restoring original ownership. It does not request translation of role names in grants. `--no-acl` (also `--no-privileges`, `-x`) suppresses access-privilege restoration. `--role=role_name` causes `SET ROLE` after connection; it determines the effective role performing the restore, rather than rewriting every role reference. `--single-transaction` implies `--exit-on-error` and makes a failed restore atomic. Without exit-on-error, restoration normally continues and reports an error count. Start with a database cloned from `template0` to avoid local `template1` additions. Pre-created target database ownership is a separate choice when not using `--create`.

[PostgreSQL 18: pg_dump](https://www.postgresql.org/docs/18/app-pgdump.html)

`pg_dump` dumps one database; it does not define cluster-global roles or tablespaces. Provision the lab's synthetic roles explicitly. Custom archives are restored through `pg_restore` and allow inspection of their contents. Preserve a full archive for both comparison branches. At dump time, `pg_dump --no-owner` is ignored for non-text archives: choose the ownership policy with `pg_restore`. Dumping with `--no-acl` removes privilege information from the archive, so it would prevent a later comparison against preserved ACLs.

## Existing permissions and future permissions

[PostgreSQL 18: ALTER DEFAULT PRIVILEGES](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html)

Defaults affect future objects, never objects already present. `FOR ROLE owner_role` identifies the role whose subsequently created objects receive the defaults; `IN SCHEMA app` limits the relevant schema in the current database. At creation, only the current creator role's defaults apply. They are not inherited from roles of which that creator is a member. Therefore migrations that log in as a separate role must either use their own defaults or `SET ROLE` to the intended owner before DDL. Per-schema defaults add to global defaults and cannot cancel global grants. Inspect defaults using `\ddp` or `pg_default_acl`.

[PostgreSQL 18: Privileges](https://www.postgresql.org/docs/18/ddl-priv.html)

Schema `USAGE` allows object lookup, subject to the objects' own permissions. Table `SELECT` and `INSERT` are distinct privileges. Schema `CREATE` permits creating objects and need not be granted to the application. Owner powers are broader than application grants. Table and sequence ACLs should both be inspected. An empty `\dp` privilege cell means built-in defaults, including the owner's privileges; it does not prove that nobody has access. `CONNECT` is checked on connection startup, which an in-session `SET ROLE` test does not exercise.

## Sequence and INSERT checks

[PostgreSQL 18: Sequence manipulation functions](https://www.postgresql.org/docs/18/functions-sequence.html)

`nextval` requires sequence `USAGE` or `UPDATE`; `currval` requires `USAGE` or `SELECT`; `setval` requires `UPDATE`. `USAGE` is sufficient for ordinary ID allocation and avoids granting `setval`. `currval` is session-local, so exercise it in the same session as `nextval` or an insert using that sequence. Sequence allocations can leave gaps after failed transactions; do not treat gapless IDs as a correctness requirement.

[PostgreSQL 18: GRANT](https://www.postgresql.org/docs/18/sql-grant.html)

Table grants and sequence grants are separate commands. Use named schema, table and sequence grants for repairs; avoid `ALL PRIVILEGES`. A narrowly scoped `ALTER DEFAULT PRIVILEGES ... GRANT SELECT, INSERT ON TABLES` is still a policy covering all future tables made by that creator in that schema, so describe that deliberate scope.

[PostgreSQL 18: INSERT](https://www.postgresql.org/docs/18/sql-insert.html)

An `INSERT` requires table/column `INSERT`. `RETURNING` additionally needs `SELECT` on referenced columns. A plain insert without `RETURNING` can isolate the expected sequence-permission failure. Once SELECT and INSERT are granted together, returning the generated ID is a useful positive check.

[PostgreSQL 18.4 release notes](https://www.postgresql.org/docs/18/release-18-4.html)

The release-specific page identifies the chosen minor release. Runtime version output and the pinned image digest, rather than the mutable image tag alone, must establish the exact executed build.

## Lab design implications to verify experimentally

These are test requirements, not claimed results:

- The preserving branch should require original synthetic roles, restore owners, existing ACLs and creator-scoped default ACLs, and permit the intended app operations.
- The remapping branch should restore with `--no-owner --no-acl --role=new_owner`, prove ownership, demonstrate absent app rights, then apply only the named schema/table/sequence grants required.
- A separate `--no-owner`-only inspection or restore should expose unchanged grantee names and original `ALTER DEFAULT PRIVILEGES FOR ROLE` references. Do not call this complete remapping.
- Use a sequence-backed `DEFAULT nextval(...)` or `bigserial` for the sequence-permission demonstration. Avoid inferring that the same permission path applies to identity columns.
- Test SELECT and INSERT as a non-superuser effective application role. Assert `current_user`, role flags and lack of owner membership. Explicitly say if `SET ROLE` is used and connection authentication is outside scope.
- Create a new table as the owner/migration role after configuring its defaults. Separately show that defaults do not repair an already-created table.
- Include negative checks that the app cannot CREATE in the schema, UPDATE/DELETE the table, or call `setval` when those powers were not granted.
- Check exit status **and expected error text/SQLSTATE** for expected failures, then demand a clean fresh disposable run. Record raw commands and outputs without fabricating examples as observed results.


## Additional technical references

Official `REL_18_4` references for the tested permission and restore semantics:

- [psql exit status and ON_ERROR_STOP](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/psql-ref.sgml)
- [Sequence allocations and transaction rollback](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/func.sgml)
- [Database creation and ACL scope](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/pg_restore.sgml)
- [Role membership options](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/grant.sgml)
- [Role INHERIT defaults](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/create_role.sgml)
- [Session user and SET ROLE prerequisites](https://raw.githubusercontent.com/postgres/postgres/REL_18_4/doc/src/sgml/ref/set_role.sgml)
