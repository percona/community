---
title: "Automating Percona's XtraBackup"
date: "2023-01-04T00:00:00+00:00"
draft: false
tags: ['XtraBackup', 'automation', 'xtrabackupautomator']
authors:
  - phil_plachta
images:
  - blog/2023/01/automate_xtrabackup.png
---

[Percona's XtraBackup](https://www.percona.com/software/mysql-database/percona-xtrabackup) is a beautiful tool that allows for the backup and restoration of MySQL databases. 

From the documentation:

> The Percona XtraBackup tools provide a method of performing a hot backup of your MySQL data while the system is running. Percona XtraBackup is a free, online, open source, complete database backups solution for all versions of Percona Server for MySQL and MySQL®. Percona XtraBackup performs online non-blocking, tightly compressed, highly secure full backups on transactional systems so that applications remain fully available during planned maintenance windows.

 It is great but it quickly becomes difficult to wield when using it multiple times per day across multiple environments. [XtraBackup Automator](https://github.com/phildoesdev/xtrabackupautomator) attempts to make this easier by providing the ability to:

* Schedule when we should create backups
    - Times of day, when to make a base backup vs incremental
* Archive old backups
    - Decide what to do with the base backup and its increments when we are ready to create a new base
* Maintain x days of archives
    - Define how many archived backup groups should we keep before removing them from the file system

[XtraBackup Automator](https://github.com/phildoesdev/xtrabackupautomator) automates away the management of MySQL backups.



## Considerations Before Installing

I strongly recommend testing this on some sort of preproduction environment first. The thing I've seen most likely to cause trouble is the archival process. By default, this tool uses the gztar 'tarball' as its compression method, which can be resource intensive if you are working on a large database backup. For instance, one of our servers (a Google Cloud Platform virtual machine with 8 vCPU, 32gb RAM, 1000GB SSD persistent disk, running Debian 10) with a ~140GB base backup currently jumps in CPU usage by ~13% for 4 hours, with a handful of 5%-15% jumps in RAM usage, while creating this archive. Another downside of this compression method is that it can take 10-20 minutes to unzip, depending on settings. The benefit of the tarball is that we are able to take these large backups from 140GB to < 10GB and this is worth all that other trouble for us as we want to have two weeks of daily backups. If these down sides are not acceptable, I recommend playing with the archive type as described in the config. I have not personally tested any other methods.

I am assuming that you have administrative access to the server this will run on as installing systemd services and timers requires root access. I see no reason why Cron Jobs could not be used to run this program, but I have never tested that and all documentation references systemd and its tools.



## Info & Requirements

#### Developed On

- **OS:**
  - Debian GNU/Linux 10 (buster)
- **Python Version:**
  - Python 3.10.4
- **Python Packages**
  - **Name:** [pexpect](https://pexpect.readthedocs.io/en/stable/), **Version:** 4.8.0
- **Percona XtraBackup Version:**
  - [XtraBackup](https://www.percona.com/software/mysql-database/percona-xtrabackup) version 8.0.28-21 based on MySQL server 8.0.28 Linux (x86_64)
- **MySQL**
  - MySql  Ver 8.0.28 for Linux on x86_64 (MySQL Community Server - GPL)

#### Required Python Libraries

- [pexpect](https://pexpect.readthedocs.io/en/stable/)

#### Required Files
- [xtrabackupautomator.py](https://github.com/phildoesdev/xtrabackupautomator/blob/main/src/xtrabackupautomator.py)
- [xtrabackupautomator.service](https://github.com/phildoesdev/xtrabackupautomator/blob/main/xtrabackupautomator.service)
- [xtrabackupautomator.timer](https://github.com/phildoesdev/xtrabackupautomator/blob/main/xtrabackupautomator.timer)



## Installing 

Below is a general explanation of how to install and start running this program. I would suggest running the program manually via command line a couple times, in a preproduction environment, to verify things are working as you expect.

___Download The Files___

Download the [Required Files](#required-files) from [https://github.com/phildoesdev/xtrabackupautomator](https://github.com/phildoesdev/xtrabackupautomator)

___Review Your Config Settings___

Review the [Configuration](#configuration) section of this readme and alter these settings to your liking.<br>
Any altered folder paths may affect the create folder instructions below. At minimum you must include database login information, but alter as necessary. I suggest reading through all the config options to see what might be interesting to tweak.

___Edit your systemd service and timer___

If you change the location that the script should run from you must alter the file path in the xtrabackupautomator.service file. I will not explain much else here as there is a lot that might go into these settings. I have given some default settings that hopefully make sense. 

I have also included several links that describe what is possible in the [Sources & Links](#sources--links) section. If there are specific questions in the future I will address them here.

![ServiceTimerExample](/blog/2023/01/automate_xtrabackup_service_timer_example.jpg)

___Install the required dependencies___
```bash
$ python3 -m pip install pexpect
```
___Create the directory for our code to live in___
```bash
$ sudo mkdir /lib/xtrabackupautomator
$ sudo chmod 700 /lib/xtrabackupautomator
```

___Create the directories for our backups to save to___

```bash
$ sudo mkdir -p /data/backups/mysql
$ sudo mkdir -p /data/backups/archive
$ sudo mkdir -p /data/backups/archive/archive_restore

$ sudo chmod 760 /data/backups/mysql
$ sudo chmod 700 /data/backups/archive
$ sudo chmod 700 /data/backups/archive/archive_restore
$ sudo chown -R root:root /data/backups/
```

___Move your downloaded files___

```bash
$ sudo mv xtrabackupautomator.py /lib/xtrabackupautomator/.
$ sudo mv xtrabackupautomator.service /etc/systemd/system/.
$ sudo mv xtrabackupautomator.timer /etc/systemd/system/.
```

___Enable your service and timer___

```bash
$ sudo systemctl daemon-reload

$ sudo systemctl enable xtrabackupautomator.timer

$ sudo systemctl start xtrabackupautomator.timer
$ sudo systemctl status xtrabackupautomator.timer
```

___Congrats, you are now installed!___

You have now installed XtraBackup Automator, it will begin running automatically according to your xtrabackupautomator.timer file. If you wish to run it manually, you can run the python file, or use my preferred method, the  `systemd start` command to start it and `journalctl` to view its output:

```bash
$ systemctl start xtrabackupautomator.service
$ journalctl -f -n 100 -u xtrabackupautomator
```

___Unzipping and Restoring your Backup___

I have included a link in the [Sources & Links](#sources--links) section on [unzipping tar gz files](https://linuxize.com/post/how-to-extract-unzip-tar-gz-file/). 

I strongly suggest reading the [official Percona documentation](https://docs.percona.com/percona-xtrabackup/8.0/backup_scenarios/incremental_backup.html) on restoring backups.

For a point of a reference, I will describe my generic unzip and restore process. I am using the directory `/data/backups/archive/archive_restore/` as a place to unzip and restore from. 

Executing any of the below commands can obviously be very dangerous as we must stop mysql, wipe the current data, and restore with our prepared backup. [Read the documentation](https://docs.percona.com/percona-xtrabackup/8.0/backup_scenarios/incremental_backup.html) and come up with your own plan! The code below is only meant as a reference and may change greatly with time and environments. Always test your plans in a preprod environment!!

![Archives](/blog/2023/01/automate_xtrabackup_archive_pic.png)


```bash
# Always verify our version of Percona's XtraBackup and MySQL match before performing a backup... these differences can make restores fail or behave oddly.
$ sudo mysql --version
$ sudo xtrabackup --version

# Clean our restore folder, just to be safe
$ rm -r /data/backups/archive/archive_restore/*

# Unzip our archived backup to an empty folder. Always verify we have enough disk space to unzip before unzipping
$ sudo tar -xvf database_backup_12_23_2022__06_25_10.tar.gz  -C /data/backups/archive/archive_restore/

# Sanity check, verify we are looking at the backup we think we are (This command checks the base folder, check the latest incremental folder we may have)
$ cd /data/backups/archive/archive_restore/data/backups/mysql/
$ sudo  cat base/xtrabackup_info | grep 'tool_version\|server_version\|start_time\|end_time\|partial\|incremental'

# Prepare the base
$ sudo xtrabackup --prepare --apply-log-only --no-server-version-check  --target-dir=/data/backups/archive/archive_restore/data/backups/mysql/base 

# Prepare each incremental folder. This must be done for each incremental folder we wish to back up to.
$ sudo xtrabackup --prepare --apply-log-only --no-server-version-check --target-dir=/data/backups/archive/archive_restore/data/backups/mysql/base  --incremental-dir=/data/backups/archive/archive_restore/data/backups/mysql/inc_0

# Repeat as necssary....
...

# Stop SQL and our backup script as we do not want it running mid restore
$ sudo systemctl stop mysql
$ sudo systemctl stop xtrabackupautomator.timer

# Wipe bad/corrupted sql data from current instance
$ sudo rm -rv /var/lib/mysql/*

# Verify our mysql data is wiped
$ sudo ls /var/lib/mysql

# I use this method to restore my base backup, there are other options but they did not work correctly in my environment
$ sudo xtrabackup --copy-back --target-dir=/data/backups/archive/archive_restore/data/backups/mysql/base

# Verify the contents are the size we expect as a sanity check and apply the correct ownership to the files
$ du -hs /var/lib/mysql/
$ sudo chown -R mysql:mysql /var/lib/mysql

# Restart mysql and xtrabackupautomator. Verify MySQL's status
$ sudo systemctl start mysql
$ sudo systemctl xtrabackupautomator.timer
$ sudo systemctl status mysql


```


## Configuration

In an attempt to make this a one file, easy to install piece of software, I included the configuration struct in the xtrabackupautomator.py file, in the `__init__` method of the XtraBackupAutomator class, on line ~60 (as of this writing). I will describe that struct, its default values, and other relevant information below. Most of this information can also be found in comments throughout, or in the getter methods for each variable.

```

== db ==
    -un
        [DEFAULT_VALUE: ""]
        XtraBackup user you set up during your initial configuration of Percona's XtraBackup
    
    -pw
        [DEFAULT_VALUE: ""]
        This user's password

    -host
        [DEFAULT_VALUE: "localhost"]
        The IP of your database 

    -port
        [DEFAULT_VALUE: 3306]
        The port to access database 


== folder_names ==
    -base_dir 
        [DEFAULT_VALUE: "/data/backups/"]
        The root directory for all backup related things. Holds current backup and any archived backups.
        This is the default location and is reflected in the setup as we request you create this folder.
        If you change this directory in the config this change must be reflected in the setup.

    -datadir 
        [DEFAULT_VALUE: "mysql/"]
        Folder that current backups will be saved to. This would be the folder that holds the base backup and any 
          incremental backups before they are archived
        If you change this directory in the config this change must be reflected in the setup.
        *** XtraBackupAutomator WILL ARCHIVE AND DELETE ANYTHING IN HERE. THIS SHOULD BE AN EMPTY FOLDER, NOT UTILIZED BY ANYTHING ELSE.

    -archivedir 
        [DEFAULT_VALUE: "archive/"]
        Folder that a group of backups will be archived to. 
        If you change this directory in the config this change must be reflected in the setup.
        *** XtraBackupAutomator COULD POTENTIALLY DELETE ANY NON-DIRECTORY IN HERE.

== file_names ==
    -basefolder_name
        [DEFAULT_VALUE: "base"]
        Foldername for the base backup

    -incrementalfolder_perfix
        [DEFAULT_VALUE: "inc_"]
        Folder name prefix for incremental backups. 
        Suffixed with the current number of incremental backups minus one
        e.g., 'inc_0'

    -archive_name_prefix
        [DEFAULT_VALUE: "database_backup_"]
        Prefix for the archive files. 
        Suffixed by the datetime of the archive
        e.g., 'database_backup_11_28_2022__06_25_03.tar.gz'


== archive_settings ==
    -allow_archive
        [DEFAULT_VALUE: True]
        An override to enable/disable all archive settings.
        Currently, disabling this will cause the program to do a base backup and then incremental backups forever.

    -archive_zip_format
        [DEFAULT_VALUE: "gztar"]
        The default archive file type. I like tarballs because they zip our large database into a manageable file. 
        However, tarballs can take a long time to create and require a fair amount of resources if your DB is large. 
        This setting will depend on your system and the size of your DB. I recommend playing around with this.
        Other zip options: [Shutil Man Page](https://docs.python.org/3/library/shutil.html#shutil.make_archive)

    -archived_bu_count
        [DEFAULT_VALUE: 7]
        Keep x archived backups, once this threshold is reached the oldest archive will be deleted.
        Archiving daily, this is a week of archives.

    -enforce_max_num_bu_before_archive
        [DEFAULT_VALUE: True]
        One of two ways to 'force archive' of backups. 
        This counts the # of incremental backup folders and initiates the archives once that number is reached. 
        A sample use case is that in your systemd timer file is scheduled to do 5 backups throughout the day, so setting this to 
          true and max_num_bu_before_archive_count set to 4 (because we do not count the base) would give you a 'daily archive'

    -max_num_bu_before_archive_count
        [DEFAULT_VALUE: 4]
        The max number of incremental backups to do before we archive (does not count the base). 
        Set to 0 to archive after each base

    -enforce_archive_at_time
        [DEFAULT_VALUE: False]
        One of two ways to 'force archive' of backups. 
        This will archive what ever base or incremental folders exist if a backup is happening within the 
          archive_at_utc_24_hour hour. This is intended to make it easier to schedule when your archive and base backup occur. 
        These can be resource intensive and so it is nice to do at off hours.
        *If this program is scheduled to run more than once during the 'archive_at_utc_24_hour' hour each run will cause an archive.

    -archive_at_utc_24_hour
        [DEFAULT_VALUE: 6]
        If a backup happens within this hour we will archive w/e was previously there and create a new base.
        Matching this with a time setup in your xtrabackupautomator.timer allows you to choose when your backups will 
          occur.
        No explicit consideration for daylight savings time. 
        Defaults to the hour of 1:00am EST, 6:00am UTC.


== general_settings ==
    -backup_command_timeout_seconds
        [DEFAULT_VALUE: 30]
        Give us 'backup_command_timeout_seconds' seconds for the command to respond. 
        This is not the same as saying 'a backup can only take this long'.

    -max_time_between_backups_seconds
        [DEFAULT_VALUE: 60*60*24]
        Max number of seconds between this backup and the last.
        If the last backup is older than this we will archive and create a new base. 
        This is in an attempt to prevent an incremental backup that might span days or weeks due to this service being 
          turned off or some such.
        Defaults (arbitrarily) to 24 hours

    -additional_bu_command_params
        [DEFAULT_VALUE: ["no-server-version-check"]]
        Any additional parameters that you wish to pass along to your backup commands.
        We loop this list, put a '--' before each element and append it to the end of our backup commands.
        This gets applied to the base and incremental backup commands.
        These are params that I have found useful.


== log_settings ==
    -is_enabled
        [DEFAULT_VALUE: True]
        Enables/Disables all logging type settings. This was useful in testing, so I kept it around.

    -log_child_process_to_screen
        [DEFAULT_VALUE: True]
        If this is set to true the child process's output will be dumped to screen but not actually logged anywhere

    -is_log_to_file
        [DEFAULT_VALUE: True]
        If set to True we will try to log to the 'default_log_file' in the 'default_log_path' directory

    -default_log_path
        [DEFAULT_VALUE: "/var/log/"]
        The path that we will try to place our log file ('default_log_file') 

    -default_log_file
        [DEFAULT_VALUE: "xtrabackupautomator.log"]
        The file name we will try to log to

```


## Sources \& Links

- Official Percona XtraBackup Documentation
    - https://docs.percona.com/percona-xtrabackup/8.0/index.html
- Systemctl Overveiw
  - https://fedoramagazine.org/what-is-an-init-system/ 
  - https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
  - https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267
- Systemctl Timers Overview
  - https://linuxconfig.org/how-to-schedule-tasks-with-systemd-timers-in-linux
  - https://opensource.com/article/20/7/systemd-timers
- Systemctl Services Details
  - https://www.freedesktop.org/software/systemd/man/systemd.service.html
- Systemctl Timers Details
  - https://www.freedesktop.org/software/systemd/man/systemd.timer.html
- OnCalendar Expected Formats
  - https://www.freedesktop.org/software/systemd/man/systemd.time.html#
- Archive Zip Options
  - https://docs.python.org/3/library/shutil.html#shutil.make_archive
- How to Extract (Unzip) Tar Gz File
  - https://linuxize.com/post/how-to-extract-unzip-tar-gz-file/
- Restoring Xtrabackup Incremental Backups
  - https://docs.percona.com/percona-xtrabackup/8.0/backup_scenarios/incremental_backup.html

