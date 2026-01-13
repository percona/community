---
title: "Configuring the Component Keyring in Percona Server and PXC 8.4"
date: "2026-01-13T00:00:00+00:00"
tags: ["Opensource", "Percona", "key ring", "MySQL", "Community", "Percona Server", "PXC", "Security"]
categories: ["MySQL"]
authors:
  - wayne
  - stan_lipinski
images:
  - blog/2026/01/keyring-component.png
---

# Configuring the Component Keyring in Percona Server and PXC 8.4  
*(Or: how to make MySQL encryption boring, which is the goal)*

Encryption is one of those things everyone agrees is important, right up until MySQL refuses to start and you’re staring at a JSON file wondering which brace ruined your evening.

With **MySQL 8.4**, encryption has firmly moved into the **component world**, and if you’re running **Percona Server 8.4** or **Percona XtraDB Cluster (PXC) 8.4**, the supported path forward is the `component_keyring_file` component.

The good news: the setup is mostly identical for Percona Server and PXC.  
The bad news: PXC 8.4.4 and 8.4.5 shipped with a bug that makes this less fun than it should be.

Let’s walk through a setup that works, keeps your keys locked down, and avoids the usual landmines.

---

## Step 1: Tell MySQL Which Component to Load

Components are registered using **JSON**, not traditional MySQL configuration syntax. This is important, because MySQL will not politely warn you if you get it wrong. It will simply refuse to start.

Create the file:

```bash
sudo vi /usr/sbin/mysqld.my
```

Add:

```json
{
  "components": "file://component_keyring_file"
}
```

Take a second to double-check the formatting. One missing quote here will cost you more time than you want to admit.

Now lock it down:

```bash
sudo chown root:root /usr/sbin/mysqld.my
sudo chmod 644 /usr/sbin/mysqld.my
```

This is configuration, not data. MySQL only needs to read it.

---

## Step 2: Prepare the Keyring Directory (Handle With Care)

This directory will hold encryption keys. Treat it accordingly.

```bash
cd /var/lib
sudo mkdir mysql-keyring
sudo chown root:root mysql-keyring
sudo chmod 750 mysql-keyring
```

A simple rule that saves headaches:

- **Root owns the keys**
- **MySQL is allowed to access them**
- **Nobody else gets any ideas**

---

## Step 3: Configure the Keyring Component Itself

Next, move to the plugin directory:

```bash
cd /usr/lib64/mysql/plugin
```

Create the component configuration file:

```bash
sudo vi component_keyring_file.cnf
```

Add:

```json
{
  "path": "/var/lib/mysql-keyring/component_keyring_file",
  "read_only": true
}
```

This file tells MySQL where the keyring lives and ensures it can’t be casually modified at runtime.

Set ownership and permissions:

```bash
sudo chown root:root component_keyring_file.cnf
sudo chmod 640 component_keyring_file.cnf
```

Again: configuration belongs to root. MySQL just reads it.

---

## Step 4: The PXC 8.4.4 / 8.4.5 Bug (Yes, There’s One)

If you’re running **Percona Server**, you can skip this entire section and enjoy your day.

If you’re running **Percona XtraDB Cluster 8.4.4 or 8.4.5**, there is a known issue with plugin paths that prevents the component keyring from loading correctly. This was fixed in **PXC 8.4.6**.

If upgrading isn’t an option yet, you’ll need one of the following workarounds.

### Option A: Create a Symlink (Preferred)

```bash
sudo ln -s \
/usr/bin/pxc_extra/pxb-8.4/lib/lib64/xtrabackup/plugin \
/usr/bin/pxc_extra/pxb-8.4/lib/plugin
```

### Option B: Copy the Plugin Directory

```bash
sudo cp -ar \
/usr/bin/pxc_extra/pxb-8.4/lib/lib64/xtrabackup/plugin \
/usr/bin/pxc_extra/pxb-8.4/lib
```

If you’re on **PXC 8.4.6 or newer**, this problem is already behind you and you can safely pretend it never existed.

---

## Step 5: Restart MySQL

Time for the moment of truth:

```bash
sudo systemctl restart mysql
```

Or `mysqld`, depending on your system.

If MySQL starts cleanly, you’re doing well. If not, go back and check your JSON files. It’s almost always the JSON.

---

## Step 6: Verify the Keyring Is Actually Loaded

Never assume. Always verify.

```sql
SELECT *
FROM performance_schema.keyring_component_status;
```

You should see the `component_keyring_file` listed and active. If it’s there, the keyring is live.

---

## A Note for Percona Server Users

Percona Server may still include **legacy keyring plugins** such as:

- `keyring_file`
- `keyring_vault`

Do not mix legacy keyring plugins with component keyrings. They come from different eras of MySQL design and do not coexist peacefully.

Choose one model. For MySQL 8.4 and forward, **components are the future**.

---

## Final Thoughts

This setup works reliably for:

- Percona Server 8.4
- Percona XtraDB Cluster 8.4  
  (with the known exception of 8.4.4–8.4.5)

Most failures come down to:

- Treating JSON like a `.cnf` file
- Loose ownership on sensitive files
- Forgetting the PXC-specific workaround

Once those are handled, the component keyring fades into the background where it belongs. And when it comes to encryption, boring, quiet, and uneventful is exactly the outcome you want.
