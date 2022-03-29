---
title: "MySQL Backups and Database Recovery Best Practices - Percona Podcast 02"
description: "We cover details about Walter's latest blog outlining MySQL Backup best practices."
short_text: "The Hoss talks with Walter Garcia remote dba expert for Percona about how to ensure you are getting good and consistent MySQL backups. We cover details about Walter's latest blog outlining MySQL Backup best practices."
date: "2021-02-16"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep02-talking-mysql-backup-best-practices-with-walter-garcia/"
youtube_id: "AJaze6ehqm0"
speakers:
  - walter_garcia
  - matt_yonkovit
aliases:
    - "/podcasts/2/"
url: "/podcasts/2-mysql-backups-database-recovery-best-practices"
---


## Transcript

**Matt Yonkovit:**  
Hi everybody. **Matt Yonkovit**, The HOSS, Head of Percona Strategy at Percona, I welcome you to another Percona Tech Talk, where we're gonna bring you the best in the open source space, and give you the most interesting fun speakers ever. We hope you enjoy the show. Walter, thank you for sitting down and talking with me today. I really appreciate it. We're going to be talking a little bit about your recent blog MySQL, backup, and recovery best practices. But I'd like to get you introduced to those who are watching or listening. So Walter maybe gives us a little bit of detail on who you are.

**Walter Garcia:**  
Yes, sir. Thank you, Matt, for the invitation. I am from Argentina. I Live in Mendoza city. This is a little city near Chili. I am working in the managed service team. DBA, remote DBA. This is great to work in Percona.

**Matt Yonkovit:**  
Great, great. Well, we're very happy to have you. I know we have a very large group of database administrators supporting people in Argentina and Uruguay and Brazil, we have Percona South America down there. And there are some just wonderful folks that we've been able to find in those areas. So we're really excited to have you. Well, I think reading your article it reminded me of all of the things that I did when I was doing DBA work and all the things that I saw people do that were problems. And back when I was a DBA, which was I think when dinosaurs were alive because it was so long ago, it was very, very, very, very long. I always ran into people who made really similar mistakes over and over again, and I'm wondering, what are the biggest mistakes that you see currently with people in their backup setups?

**Walter Garcia:**  
Well, the biggest mistake is to save the backups in the same machine where my sequel is running, this is the fields one. So you need to see if the machine is unreachable, or you have some hardware problem, most probably, you will lose all the backups. So this is high, recommended to keep all the copies in different locations, for example, Amazon s3, or maybe you have a file server in different locations. So at least you can keep a copy in the same machine where MySQL is running. But you can copy or keep a copy in different locations. So if you lose this machine, you can restore it from the other side.

**Matt Yonkovit:**  
Yeah, that's, that's great advice. Because I know personally, I've seen companies that have had that type of issue. It's easy. Most people will backup locally first anyways. So it's that next step of copying them somewhere else. I've actually seen this where people have had to failover to another data center and haven't had their backups. And that caused an issue as well. So you've got to be mindful of having your backups available. Because when you need them, it's a really bad time to figure out you don't have them. Yes, exactly. Yes. So you talked a little bit about restore testing, and I have found that 90% of DBAs that I talked to have never tested a restore. Why is that so important? Why is that so critical?

**Walter Garcia:**  
This is a very important task, at least to run one per month to check and test your previous backup. At least you can take the last backup and run the restore testing on different servers as  well. Why do you need to test your backups? Maybe in the backup process, some files are corrupted. So, in case you need to restore fast or you need to restore the backup in production, you will lose time because there were some problems in the process. So this is a very important task to test all the procedures uncommon in the restore process. For example, the copy the backup from the external location to restore a testing server, also, to test the grip, and uncompress backups. And if you are using XtraBackup, you will test the apply log procedures as well. So the last option is to start with a MySQL service. And check that all this runs and that MySQL is running. Okay, without a problem. So you can test some select if you want, or some insert as well, just to check there is no problem in the previous restore. Also, this is a file recommendation option to write documentation about all the previous steps why? Because maybe there are other guys in the team who will need to restart the server. So the guy or the team can check all the steps and just maybe read and paste some comment. This is great to avoid wasting time to do the same process again.

**Matt Yonkovit:**  
You don't want your boss staring over your shoulder. And you don't remember the commands. That's a very bad thing.

**Walter Garcia:**  
Yes, exactly. Some customers need to restore a Replication Server in production. So we have all the documentation. So me or the other guy in the team, just copy the process. And this is fast, so we can not lose time thinking about the comments.

**Matt Yonkovit:**  
Okay, great. Great. Yeah. And I think that restore testing is one of those things that nobody likes to do, because it takes a lot of time, especially in our bigger databases,

**Walter Garcia:**  
Yes! For example, if you have 10 terabytes of backups, it will take a few days to test the restore process. But you need to do this at least one time to create the documentation. So maybe the next time in the restore process, you will need a little less time to to to run the restart, because you have all the documentation. Also, this is very important. After the restore after the start MySQL process, I recommend to configure this restart server as replication from the master so and keeping the replication running at least for one or two days to check the Restore is perfect if there are no problems in the replication process. You are very good to check. So all the processes and the backup are correct.

**Matt Yonkovit:**  
Yeah, I can imagine. I mean, like there's a lot there where somebody goes in the database starts up, okay, I'm done. But then if you go in and select things or do operations, everything fails.

**Walter Garcia:**  
Yes, sometime after the restore. If you configure the replication, you can check if there are maybe duplicated entries or maybe some update in their application process failed. So if you get this fail the application may fail, maybe the backup will not work. And you need to take a new backup and check again.

**Matt Yonkovit:**  
Yeah, yeah. And I mean, there's nothing worse than getting it all restored and taking 48 hours or 72 hours on a big database and then finding it doesn't work. That's horrible. So you want to make sure that you know you're protected there as possible and speaking of protected, um there's a lot of people who run a logical backup or a physical backup, but sometimes they don't run both sometimes they do. Do you need both? Is that something that you think you should do? You should definitely do both?

**Walter Garcia:**  
Yes, exactly. So this is good. If you are encrypting the backup, to check the key, if this is working, sometimes the customer is running backups very well. And the encryption key is different. So in case you need to restore it, this will fail. So this is good to test the key as well.

**Matt Yonkovit:**  
Okay, so I'm Walter. So logical and physical backups. Yes. Tell me a little bit about whether you need both of those.

**Walter Garcia:**  
I recommend both. Because from the previous restore testing, you can use physical backup to restore a fast server? Well, I mean, fast. If you have any small backup, right, but this is a fast procedure, if you compare it with the logical backups. I recommend that because a physical backup is fast to restore the full backup, but then you can use logical backup to restore maybe one or a couple of tables and nothing is because if you need to restore a full backup from the logical backup, this will take a lot of time. Because you need to run million insert

**Matt Yonkovit:**  
Right. And a lot of times you know somebody does something like drop a table, delete records from a table, just need those little tiny things. So it's really important to have both those logical and physicals

**Walter Garcia:**  
Yes, exactly. You can restore maybe one table and copy one or two or more rows from the previous day. That is what I recommend taking both.

**Matt Yonkovit:**  
Okay. Well, Walter, thank you for writing that blog. He was great. If you haven't read the blog, I would encourage you. I'm going to go ahead and put it in the links here. It's a wonderful kind of recap of all the things around backups that you should be looking at doing. And Walter, thank you for sharing your knowledge today. We really appreciate you spending a few minutes this morning talking with us.

**Walter Garcia:**  
Thank you and you're welcome, Matt.

