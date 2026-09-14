---
title: "Prove the Backup: A Percona Distribution for PostgreSQL Restore Drill on Windows"
date: "2026-09-14"
draft: true
tags: ['PostgreSQL', 'Docker', 'Backup', 'PowerShell', 'Windows']
categories: ['PostgreSQL', 'Community']
authors:
  - jack_vansickle
images:
  - hub/home/cover.jpg
slug: percona-postgresql-restore-drill-on-windows
---

A backup is only useful if it can be restored. This lab seeds a source database, takes a logical archive, deliberately deletes the source database, restores into a clean target, and checks the recovered state. Percona Distribution for PostgreSQL does not provide a native Windows package. Windows is only the Docker Desktop host; PostgreSQL and its utilities run in Linux containers.

The current Percona 17 Docker documentation uses `percona/percona-distribution-postgresql:17.11`, requires `POSTGRES_PASSWORD`, and exposes PostgreSQL on container port 5432. Docker Desktop is the recommended way to obtain Docker Engine, the CLI, and Compose on Windows. [Percona Docker guide](https://docs.percona.com/postgresql/17/docker.html) · [Docker Compose installation](https://docs.docker.com/compose/install/)

## 1. Create the Compose project

Start Docker Desktop, open PowerShell, and make a uniquely named lab directory. The timestamp gives Compose a new project name, so an old named volume cannot silently turn a rerun into a test of stale data.

```powershell
$ErrorActionPreference = "Stop"

docker version
if ($LASTEXITCODE -ne 0) { throw "Docker Engine is unavailable." }

docker compose version
if ($LASTEXITCODE -ne 0) { throw "Docker Compose is unavailable." }

$lab = "percona-restore-lab-{0}" -f (Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Path $lab | Out-Null
Set-Location $lab
New-Item -ItemType Directory -Path backups | Out-Null
```

Save this as `compose.yaml`. Separate named volumes prevent the recovery target from sharing source data; the archive will be copied through the Windows filesystem.

```yaml
services:
  source:
    image: percona/percona-distribution-postgresql:17.11
    environment:
      POSTGRES_USER: drill
      POSTGRES_PASSWORD: lab-only-change-me
      POSTGRES_DB: drill
    ports:
      - "127.0.0.1:55432:5432"
    volumes:
      - source-data:/data/db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -q -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 12
      start_period: 10s

  target:
    image: percona/percona-distribution-postgresql:17.11
    environment:
      POSTGRES_USER: drill
      POSTGRES_PASSWORD: lab-only-change-me
      POSTGRES_DB: restore_drill
    ports:
      - "127.0.0.1:55433:5432"
    volumes:
      - target-data:/data/db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -q -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 12
      start_period: 10s

volumes:
  source-data:
  target-data:
```

This password is disposable; use proper secret handling outside a lab. Percona’s v17 Dockerfile sets `/data/db` as `PGDATA`. Compose does not otherwise equate “running” with “ready,” so health checks matter. [Percona v17 Dockerfile](https://github.com/percona/percona-docker/blob/main/percona-distribution-postgresql-17/Dockerfile) · [Docker startup-order guidance](https://docs.docker.com/compose/how-tos/startup-order/)

```powershell
docker compose config --quiet
if ($LASTEXITCODE -ne 0) { throw "Compose validation failed." }

docker compose pull
if ($LASTEXITCODE -ne 0) { throw "Image pull failed." }

docker compose up -d --wait --wait-timeout 60 source
if ($LASTEXITCODE -ne 0) { throw "Source failed to become healthy." }

$serverVersion = docker compose exec -T source psql -U drill -d drill -Atc "SELECT version();"
if ($LASTEXITCODE -ne 0) { throw "Version query failed." }
$serverVersion
```

Record the actual version string. Do not infer it from the tag alone.

## 2. Seed known data and prove the baseline

```powershell
@'
CREATE TABLE orders (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer text NOT NULL,
  amount numeric(10,2) NOT NULL CHECK (amount >= 0)
);
INSERT INTO orders (customer, amount)
VALUES ('Ada', 10.25), ('Grace', 20.00), ('Linus', 30.00);
'@ | docker compose exec -T source psql -U drill -d drill -v ON_ERROR_STOP=1
if ($LASTEXITCODE -ne 0) { throw "Seed step failed." }

$baseline = docker compose exec -T source psql -U drill -d drill -Atc "SELECT count(*) || '|' || sum(amount) FROM orders;"
if ($LASTEXITCODE -ne 0 -or $baseline.Trim() -ne "3|60.25") {
  throw "Baseline check failed: $baseline"
}
```

**Pass:** the command returns `3|60.25`. Anything else is a stop condition.

## 3. Create and export the archive

`pg_dump -Fc` creates a custom-format archive for `pg_restore`; PostgreSQL describes this format as flexible and compressed by default. Write it inside the Linux container, inspect its table of contents, and copy it to Windows:

```powershell
docker compose exec -T source pg_dump -U drill -d drill -Fc -f /tmp/drill.dump
if ($LASTEXITCODE -ne 0) { throw "pg_dump failed." }

docker compose exec -T source pg_restore --list /tmp/drill.dump
if ($LASTEXITCODE -ne 0) { throw "Archive inspection failed." }

docker compose cp source:/tmp/drill.dump .\backups\drill.dump
if ($LASTEXITCODE -ne 0) { throw "Archive export failed." }

$backup = Get-Item .\backups\drill.dump -ErrorAction Stop
if ($backup.Length -le 0) { throw "Backup file is empty." }
$backup | Select-Object FullName, Length, LastWriteTime
Get-FileHash .\backups\drill.dump -Algorithm SHA256
```

Copying avoids routing a binary archive through PowerShell’s output pipeline. `docker compose cp` transfers files between a service container and the local filesystem. The hash identifies this particular file; it is not a universal expected value. Two clean image-side validation runs each produced a 2,360-byte archive but different SHA-256 hashes because the archives contain run-specific metadata. Record the hash so the same file can be checked after another transfer. [PostgreSQL `pg_dump`](https://www.postgresql.org/docs/17/app-pgdump.html) · [Docker Compose `cp`](https://docs.docker.com/reference/cli/docker/compose/cp/)

## 4. Inject failure, then recover

This is the destructive step. Confirm that the current timestamped lab directory is disposable before continuing.

```powershell
docker compose exec -T source psql -U drill -d postgres -v ON_ERROR_STOP=1 -c "DROP DATABASE drill;"
if ($LASTEXITCODE -ne 0) { throw "Failure injection command failed." }

# Windows PowerShell 5.1 treats redirected native stderr as an error record.
# This one command is expected to fail; capture it, then restore strict handling.
$previousErrorActionPreference = $ErrorActionPreference
try {
  $ErrorActionPreference = "Continue"
  $missingDb = docker compose exec -T source psql -U drill -d drill -c "SELECT 1;" 2>&1 | Out-String
  $missingDbExit = $LASTEXITCODE
} finally {
  $ErrorActionPreference = $previousErrorActionPreference
}
$missingDb.Trim()
if ($missingDbExit -eq 0 -or $missingDb -notmatch 'database\s+"drill"\s+does\s+not\s+exist') {
  throw "Unexpected failure probe result: $missingDb"
}

docker compose stop source
if ($LASTEXITCODE -ne 0) { throw "Could not stop the failed source." }

docker compose up -d --wait --wait-timeout 60 target
if ($LASTEXITCODE -ne 0) { throw "Target failed to become healthy." }

docker compose cp .\backups\drill.dump target:/tmp/drill.dump
if ($LASTEXITCODE -ne 0) { throw "Archive import failed." }

docker compose exec -T target pg_restore -U drill --dbname=restore_drill --clean --if-exists --single-transaction /tmp/drill.dump
if ($LASTEXITCODE -ne 0) { throw "Restore failed." }
```

**Failure check passes** only when the post-drop connection fails specifically because `drill` does not exist. The regular expression tolerates whitespace because Windows PowerShell 5.1 can wrap native error text across lines. Stopping the now-unhealthy source keeps it out of the target’s readiness check. The target has a deliberately different database name, so the restore omits `--create` and loads directly into `restore_drill`. `--clean --if-exists` makes replacement explicit without missing-object noise. For this small lab, `--single-transaction` makes the restore all-or-nothing and implies exit-on-error. [PostgreSQL `pg_restore`](https://www.postgresql.org/docs/17/app-pgrestore.html)

## 5. Verify the recovered state

```powershell
$verifySql = @'
SELECT concat_ws('|',
  (SELECT string_agg(id::text || ':' || customer || ':' || amount::text, ',' ORDER BY id) FROM orders),
  (SELECT count(*) FROM pg_constraint WHERE conrelid = 'public.orders'::regclass),
  (SELECT is_identity FROM information_schema.columns
     WHERE table_schema = 'public' AND table_name = 'orders' AND column_name = 'id'),
  (SELECT last_value || ':' || is_called FROM public.orders_id_seq)
);
'@

$restored = $verifySql | docker compose exec -T target psql -U drill -d restore_drill -At -v ON_ERROR_STOP=1
$expected = "1:Ada:10.25,2:Grace:20.00,3:Linus:30.00|2|YES|3:true"

if ($LASTEXITCODE -ne 0 -or $restored.Trim() -ne $expected) {
  throw "Restore verification failed: $restored"
}
"PASS: rows, constraints, identity definition, and sequence state recovered."
```

The drill passes only if readiness succeeds, the baseline matches, the archive is nonempty and parseable, the expected missing-database error is observed, `pg_restore` exits zero, and the final row, constraint, identity, and sequence signature matches exactly.

## When a check fails

Treat a thrown error as evidence, not an invitation to skip ahead. If the source never becomes healthy, run `docker compose ps` and `docker compose logs --no-color source`; initialization and permission errors normally appear there. A “port is already allocated” error concerns the host side of 55432 or 55433, not container port 5432. If `pg_restore --list` fails, discard the archive and create a new one rather than attempting a hopeful restore.

Ownership errors usually mean that source and target roles differ. This lab intentionally creates the `drill` superuser in both containers, avoiding that variable; a production restore needs an explicit role and privilege plan. A final signature mismatch is also a failed restore even when `pg_restore` returned zero. Preserve the logs and archive, identify the difference, fix the procedure, and repeat from a new timestamped project. Do not label the backup usable until every check passes.

## PowerShell and Docker Desktop gotchas

- Use `docker compose`, not the legacy `docker-compose` executable.
- Run from the directory containing `compose.yaml`. Keep Windows paths such as `.\backups` separate from container paths such as `/tmp`.
- Keep `$LASTEXITCODE` checks immediately after native commands. `-T` disables pseudo-TTY allocation for noninteractive execution.
- Avoid PowerShell backtick line continuations: an invisible trailing space can break them.
- If host port 55432 or 55433 is occupied, change only the left side of that mapping. The container port remains 5432.
- `docker compose down` preserves named volumes. For this lab only, `docker compose down -v` deletes both disposable data volumes; never apply `-v` casually elsewhere. [Docker Compose `down`](https://docs.docker.com/reference/cli/docker/compose/down/)

## What this drill does not prove

This is a logical, single-database restore—not physical backup, point-in-time recovery, replication, failover, or a performance test. `pg_dump` does not capture cluster-wide roles and tablespaces; PostgreSQL directs those cases to `pg_dumpall`. A backup kept on the same laptop is not disaster-resilient. The lab also does not exercise application reconnects, large datasets, extensions, encryption, or remote object storage. Restore only archives from trusted sources: PostgreSQL warns that restoring can execute code chosen by source superusers. [PostgreSQL `pg_dump` limitations and warning](https://www.postgresql.org/docs/17/app-pgdump.html)

## Validation scope

On September 5, 2026, this workflow completed one clean, AI-assisted automated run on the author's Windows 11 Pro 25H2 laptop (build 26200.9168), using Docker Desktop 4.89.0, Docker Engine 29.7.2, Compose 5.5.0, and Windows PowerShell 5.1.26100.9168. The run used a fresh Compose project and separate new source and target data volumes. Linux amd64 containers from `percona/percona-distribution-postgresql:17.11` reported PostgreSQL 17.11 — Percona Server for PostgreSQL 17.11.1.

Plain `docker compose pull` succeeded. Both services became healthy within the article's 60-second timeout. The source returned the `3|60.25` baseline, and `pg_restore --list` parsed the exported 2,360-byte archive. Both `docker compose cp` transfers passed through the Windows filesystem. The Windows archive and imported target copy had the same SHA-256: `bb521cadcca1547c39d3d3a161a65228300a68f0905badf09b79011236c5311d`.

After the source database was dropped, its connection probe returned exit 2 with the expected missing-database error. The source was stopped, `pg_restore` into the clean target exited zero, and the recovered signature matched exactly: `1:Ada:10.25,2:Grace:20.00,3:Linus:30.00|2|YES|3:true`.

Execution used a PowerShell evidence wrapper around the article's Compose layout and database commands, adding explicit project scoping, container ownership checks, command-output capture, and the imported-archive hash comparison. The expected-error probe was corrected for Windows PowerShell 5.1: temporary `Continue` handling preserves the native error and exit code, and a whitespace-tolerant pattern accepts line-wrapped error text. The saved transcript, command outputs, status record, and backup support these results. This was automated execution on the author's Windows laptop; no manual command-by-command execution is claimed.

## AI-assistance disclosure

AI assistance was used to structure this lab, cross-check commands against official documentation, edit the prose, and prepare and execute the automated PowerShell validation on the author's Windows laptop. The author remains responsible for reviewing the evidence, correcting the article, and approving it for publication.
