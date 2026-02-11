---
title: "Running pgBackRest with pg_tde: A Practical Percona Walkthrough"
date: "2026-01-23T00:00:00+00:00"
tags: ["PostgreSQL", "PG_TDE", "Security", "Backups", "Percona", "Opensource"]
categories: ["PostgreSQL"]
authors:
  - shahid_ullah
images:
  - blog/2026/01/pg_tde_pgbackrest.png
---

Not every PostgreSQL installation requires encryption at rest. However, for organizations mandating strict data protection and privacy standards, it is often non-negotiable. When security policies are this rigorous, you need a strategy that protects your data without sacrificing recoverability.

This post details how to combine pgBackRest for reliable backups with Percona's solution for transparent data encryption ([pg_tde](https://docs.percona.com/pg-tde/index.html)), covering setups for Debian/Ubuntu.

## What is pg_tde?

Percona pg_tde is an open source, community driven extension that provides Transparent Data Encryption (TDE) for PostgreSQL. This mechanism allows data to be encrypted at the storage level without affecting application behavior.

Unlike standard disk encryption, which exposes data once the system boots, TDE ensures that the actual database files remain encrypted at the file system level. This protects your data, dumps, and backups even if the operating system is compromised. Currently, it is bundled with Percona Server for PostgreSQL and available in Percona Distribution for PostgreSQL 17+.

Recent Percona releases make this combination more practical than ever. With WAL encryption now ready for production use, we need a backup strategy that respects data security. In this walkthrough, we will demonstrate how to pair it with pgBackRest to ensure fully recoverable, encrypted backups.

## The Use Case

Imagine a team that wants strong security controls without changing application code. They need:

- Data files encrypted at rest (tables and WAL)
- Backups that are consistent, verifiable, and restorable
- A setup that is easy to automate and explain

Percona Distribution for PostgreSQL plus pg_tde and pgBackRest closes the gaps where needed: pg_tde takes care of encryption, pgBackRest provides flexible backup/restore capabilities.

## A Quick Note on Compatibility

At this moment pg_tde cannot be yet used with Community PostgreSQL as pg_tde relies on specific hooks in the PostgreSQL core. Percona Server for PostgreSQL includes these necessary core modifications, which is why we validate this setup using the Percona Distribution for this setup.

While pgBackRest is fully capable of managing TDE enabled clusters, there are specific constraints you must respect to ensure data safety:

- No Asynchronous Archiving: pgBackRest asynchronous archiving is not supported with encrypted WALs. You must configure your archive command to handle WALs synchronously.
- Restore Wrappers: Standard restore commands will not work for encrypted WALs. You must use the pg_tde_restore_encrypt utility to wrap your restore process.

This guide currently focuses on pgBackRest because it is the backup tool that has been tested and validated with pg_tde by the pg_tde community for production backup and restore scenarios at this time.
Other backup tools may also be viable and we are open to collaborating with other tool maintainers and their communities on a shared effort to validate and support pg_tde.

## What You Will Build

By the end of this post you will have:

- Percona Distribution for PostgreSQL installed with pg_tde and pgBackRest
- A key directory and key providers created
- [WAL encryption](https://docs.percona.com/pg-tde/wal-encryption.html) enabled
- A pgBackRest stanza configured and a full backup completed
- Use pg_tde to [encrypt tables and indexes](https://docs.percona.com/pg-tde/test.html)
- A simple verification that encrypted data is not readable on disk

## Prerequisites

- A host (or VM) on Debian/Ubuntu
- Network access to Percona repositories
- Root/Sudo: You need sudo access for installing packages and editing system configuration files in `/etc`
- Postgres User: All database commands (psql, pgbackrest) should be run as the postgres system user
- Postgres user is in the sudoer list to run sudo commands

To switch users:

```bash
sudo -i -u postgres
```

## Step 1: Install Percona Packages

We begin by installing the Percona release repository and enabling the correct PostgreSQL distribution.

### Debian / Ubuntu

```bash
# Install repo helper
sudo apt-get update
sudo apt-get install -y wget gnupg2 lsb-release curl
wget https://repo.percona.com/apt/percona-release_latest.generic_all.deb
sudo dpkg -i percona-release_latest.generic_all.deb

# Enable the repository for the major version selected
sudo percona-release setup ppg-18
sudo apt-get update

# Install the server, tde extension, and pgbackrest
sudo apt-get install -y percona-postgresql-18 percona-postgresql-contrib percona-pg-tde18 percona-pgbackrest
```

### Verify Installation

```bash
psql --version
```

## Step 2: Enable pg_tde and Create Keys

### 2.1 Configure shared_preload_libraries

The pg_tde extension must be loaded at startup. We need to add it to the `shared_preload_libraries` parameter in `postgresql.conf`.

```bash
# Locate the config file
PG_CONF=$(psql -t -P format=unaligned -c "show config_file;")
```

```sql
ALTER SYSTEM SET shared_preload_libraries = 'pg_tde';
```

```bash
# Restart PostgreSQL to load the library
sudo systemctl restart postgresql
```

### 2.2 Create the Key Provider

Now that the extension is loaded, we need to tell pg_tde where to store its encryption keys.

For this tutorial, we will use the File Provider (storing keys in a local file). In production environments, storing encryption keys locally on the PostgreSQL server can introduce security risks. To enhance security, pg_tde supports integration with external Key Management Systems ([KMS](https://docs.percona.com/pg-tde/global-key-provider-configuration/overview.html)) through a Global Key Provider interface.

> Note: While key files may be acceptable for local or testing environments, KMS integration is the recommended approach for production deployments.

```bash
# 1. Create a secure directory for the keys
sudo mkdir -p /etc/postgresql/keys
sudo chown postgres:postgres /etc/postgresql/keys
sudo chmod 700 /etc/postgresql/keys
```

```sql
-- 2. Connect to PostgreSQL to configure TDE
CREATE EXTENSION pg_tde;

-- 1. Define the global key provider
SELECT pg_tde_add_global_key_provider_file('global-file-provider', '/etc/postgresql/keys/tde-global.per');

-- 2. Create and Set the Principal Key
SELECT pg_tde_create_key_using_global_key_provider('global-master-key', 'global-file-provider');
SELECT pg_tde_set_default_key_using_global_key_provider('global-master-key', 'global-file-provider');

-- 3. Enable WAL encryption configuration
ALTER SYSTEM SET pg_tde.wal_encrypt = 'on';
```

```bash
# 4. Restart PostgreSQL to apply the encryption settings fully
sudo systemctl restart postgresql
```

## Step 3: Configure pgBackRest

We need to configure the pgBackRest repository and stanza.

> Note on Compression: Standard pgBackRest setups often enable compression. However, because pg_tde encrypts data (randomizing the bits) before backups occur, standard compression algorithms like gzip are ineffective. We explicitly disable compression to save CPU.

```bash
# Create the configuration file
# /etc/pgbackrest.conf
# In pg1-path use data directory path accordingly
sudo bash -c "cat <<EOF > /etc/pgbackrest.conf
[demo]
pg1-path=/var/lib/postgresql/18/main

[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
log-level-console=info
start-fast=y

# TDE OPTIMIZATION:
# Encrypted data does not compress well. We disabled it to save CPU.
compress-type=none

# TDE REQUIREMENT:
# Asynchronous archiving is NOT supported with pg_tde.
EOF"
```

```bash
# Create the repository directory
mkdir -p /var/lib/pgbackrest
chmod 750 /var/lib/pgbackrest
chown postgres:postgres /var/lib/pgbackrest
```

### Understanding the Settings

- `pg1-path`: The data directory path to be backed up
- `repo1-path`: The directory where backups will be stored
- `repo1-retention-full`: Keep only two full backups
- `start-fast=y`: Forces a checkpoint immediately when a backup starts. Without this, the backup would wait for the next scheduled checkpoint.
- `compress-type=none`: Critical for TDE. Since the WAL and data files are already encrypted (high entropy), compressing them wastes CPU for negligible space savings.

## Step 4: Wire pgBackRest into PostgreSQL Archiving

pg_tde encrypts WAL files on disk. To allow pgBackRest to archive them correctly, we must decrypt them on the fly using the `[pg_tde_archive_decrypt](https://docs.percona.com/pg-tde/command-line-tools/pg-tde-archive-decrypt.html)` wrapper.

Now, configure the `archive_command`. This command tells PostgreSQL to pipe the WAL file through the decryption wrapper before handing it off to pgBackRest.

```sql
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 4;
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = '/var/lib/postgresql/18/bin/pg_tde_archive_decrypt %f %p "pgbackrest --config=/etc/pgbackrest.conf --stanza=demo archive-push %%p"';
```

```bash
# Restart PostgreSQL (adjust service name if needed, e.g., postgresql-18)
sudo systemctl restart postgresql
```

## Step 5: Validate Encryption on Disk

Let’s verify that pg_tde is actually doing its job. We will create two tables — one standard and one encrypted — and then inspect the raw files on disk to see the difference.

```sql
-- 1. Create data: One clear text, one encrypted
CREATE TABLE IF NOT EXISTS clear_table (id INT, secret_info TEXT);
CREATE TABLE IF NOT EXISTS crypt_table (id INT, secret_info TEXT) USING tde_heap;

INSERT INTO clear_table (id, secret_info) VALUES (1, 'FIND_ME_EASILY_123');
INSERT INTO crypt_table (id, secret_info) VALUES (1, 'HIDDEN_FROM_DISK_456');

-- Verify TDE encryption status
-- For non-encrypted tables, this must return 'f' (false)
SELECT pg_tde_is_encrypted('clear_table');

-- For encrypted table, this must return 't' (true)
SELECT pg_tde_is_encrypted('crypt_table');

-- Force data to disk and switch WAL to ensure everything is flushed
CHECKPOINT;
SELECT pg_switch_wal();
```

```bash
# 2. Locate the files on disk
DATA_DIR=$(psql -t -P format=unaligned -c "show data_directory;")
CLEAR_FILE=$(psql -t -P format=unaligned -c "SELECT pg_relation_filepath('clear_table');")
CRYPT_FILE=$(psql -t -P format=unaligned -c "SELECT pg_relation_filepath('crypt_table');")

# 3. Grep for the secret strings
echo "Checking Clear Table (Should Match):"
grep -a "FIND_ME_EASILY_123" "${DATA_DIR}/${CLEAR_FILE}" && echo "  -> FOUND: Clear text is visible!"

echo "Checking Encrypted Table (Should FAIL):"
grep -a "HIDDEN_FROM_DISK_456" "${DATA_DIR}/${CRYPT_FILE}" || echo "  -> CLEAN: Encrypted text was NOT found."
```

## Step 6: Initialize the Stanza and Run a Full Backup

With the archive command configured, we can now initialize the stanza and run our first backup.

```bash
pgbackrest --stanza=demo stanza-create
pgbackrest --stanza=demo --type=full backup
pgbackrest --stanza=demo info
```

### Optional: Test Incremental Backups

```sql
-- Add new data to generate WAL activity
CREATE TABLE test_incr (id serial, data text) USING tde_heap;
INSERT INTO test_incr (data) VALUES ('incremental_change');
```

```bash
pgbackrest --stanza=demo --type=incr backup
pgbackrest --stanza=demo info
```

## Step 7: Run Backup Integrity Tests

pgBackRest has a built-in verify command that checks the integrity of the files in the backup repo.

```bash
pgbackrest --stanza=demo verify
```

## Step 8: Restore (pg_tde-aware)

Restoring an encrypted cluster requires us to reverse the process. Since our backups are stored decrypted by pgBackRest, we use the `[pg_tde_restore_encrypt](https://docs.percona.com/pg-tde/command-line-tools/pg-tde-restore-encrypt.html)` wrapper to re-encrypt the WAL files as they are written back to disk.

### 8.1 Stop the Service

```bash
sudo systemctl stop postgresql
```

### 8.2 Simulate Data Loss

The following command wipes the current data directory clean, ensuring we are restoring into a fresh environment.

```bash
find /var/lib/postgresql/18/main -mindepth 1 -delete
```

### 8.3 Restore from Backup

```bash
pgbackrest --stanza=demo restore
```

### 8.4 Configure the Restore Command

While pgBackRest automatically configures `postgresql.auto.conf` with a default `restore_command`, our setup requires a custom wrapper `pg_tde_restore_encrypt`. Open the configuration file, locate the default `restore_command` entry, and replace it with the pg_tde command below to enable on-the-fly decryption:

```
restore_command = '/usr/lib/postgresql/18/bin/pg_tde_restore_encrypt %f %p "pgbackrest --config=/etc/pgbackrest.conf --stanza=demo archive-get %%f %%p"'
recovery_target_action = 'promote'
```

We set `recovery_target_action = 'promote'` to ensure the database automatically exits recovery mode and accepts read/write traffic as soon as the restore completes.

### 8.5 Start PostgreSQL

```bash
sudo systemctl start postgresql
```

## Step 9: Run Verification Tests

After restoring and starting the PostgreSQL server successfully, verify that the data was restored properly and also make sure that encrypted data can be retrieved.

```sql
-- Verify data integrity (sample rows)
SELECT * FROM clear_table LIMIT 5;
SELECT * FROM crypt_table LIMIT 5;

-- Check data from before the incremental backup
SELECT * FROM test_incr LIMIT 5;

-- Verify TDE encryption status
-- For non-encrypted tables, this must return 'f' (false)
SELECT pg_tde_is_encrypted('clear_table');

-- For encrypted table, this must return 't' (true)
SELECT pg_tde_is_encrypted('crypt_table');
```

## Wrap-up

Security often comes at the cost of operational complexity, but it doesn’t have to compromise recoverability. By pairing Percona's solution for transparent data encryption (pg_tde) with pgBackRest, you can established a strategy that satisfies both security auditors and operations teams: your data is transparently encrypted on disk to meet strict compliance standards, while your backups remain consistent, verifiable, and easy to restore.

While this walkthrough used a local file provider for simplicity it is highly discouraged to do so for any production or otherwise serious use cases. For this particular scenario, the focus was supposed to be on backup, please let us know if some similar articles about Key Management System (KMS) configuration is what you would be interested in.

As you progress from this blog post to a production deployment, we recommend exploring a dedicated [KMS](https://docs.percona.com/pg-tde/global-key-provider-configuration/overview.html) solution to further harden your architecture against unauthorized access.

Finally, be aware that to support archiving, the pg_tde wrapper decrypts WAL files before sending them to the repository. This means your backup repository currently holds unencrypted data. To close this security gap in production, you must ensure that encryption is enabled at the backup repository level so that your backups remain just as secure as your live database.

Remember: While backup is running you should not change any configurations of WAL encryption including:
global key providers operations (creating or changing)
keys for WAL encryption (creating or changing)
changing the pg_tde.wal_encrypt setting
The reason is that standbys or standalone clusters created from backups done while such changes occurred may fail to start during WAL replay and may also lead to the corruption of encrypted data (tables, indexes, and other relations).
