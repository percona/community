---
title: 'Zero downtime schema change with Liquibase & Percona'
date: Mon, 26 Oct 2020 14:14:50 +0000
draft: false
tags: ['ronak.rahman', 'Liquibase', 'MySQL', 'MySQL', 'mysql-and-variants', 'Tools', 'Toolkit']
authors:
  - ronak_rahman
images:
  - blog/2020/10/image1-1.png
slug: zero-downtime-schema-change-with-liquibase-percona
---

I am always surprised to learn something new whenever I talk to a member of the open-source community. No matter how much I think I have heard of every use case there is for [Liquibase](https://www.liquibase.org) (and database change management in general), I always hear something that makes this space still feel new. There’s always something left to discover. 

Today, that new something is the problem of how to perform large batches of changes with SQL ALTER TABLE statements. No problem you say? Okay, but this ALTER needs to happen in production. Still not worried? Well, let’s say you have millions of rows, and because you’re so successful, you have many transactions happening per minute (maybe even per second). Yeah…now we are talking. You can’t alter the table because you can’t afford to [lock that table](https://dev.mysql.com/doc/refman/5.7/en/alter-table.html) for the 30 minutes (or more) it may take to execute the ALTER command. 

Well, what do you do? A Liquibase user just spoke to me about this very use case, and that they use [Percona](https://www.percona.com/doc/percona-toolkit/LATEST/index.html) with MySQL to solve this problem. (Thanks Erin Kolp!) In particular, [pt-online-schema-change](https://www.percona.com/doc/percona-toolkit/LATEST/pt-online-schema-change.html) (which is a part of the [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit)) that allows you to perform the ALTER to a table without interrupting table access. Under the covers it makes a temporary table from the actual table being altered, makes the DDL change, then copies the data over, and swaps out the tables. 

Great! No more writing one-off scripts as a DBA to manage this problem! The advantage of using Percona may be obvious, but I think Percona said it best: 

“These tools are ideal alternatives to private or ‘one-off’ scripts, because they are professionally developed, formally tested, and fully documented. They are also fully self-contained, so installation is quick and easy, and no libraries are installed.” 
Percona and Liquibase are kindred spirits. I’ve seen folks rip out their old school CI/CD setup for the database and replace it with Liquibase for the same reason. It was made and tested by a community so you can have confidence it works and you can concentrate on delivery. 

So now I have solved production interruption due to changes like alters that can cause tables to become unavailable, how do I automate this? By combining Liquibase with a [Liquibase/Percona extension](https://github.com/adangel/liquibase-percona) written by [Andreas Dangle](https://github.com/adangel). 
Here are the basic steps:

*   [Download and install Liquibase](https://www.liquibase.org/download)
*   Install [Percona Toolkit](https://www.percona.com/doc/percona-toolkit/LATEST/installation.html)
*   [Download the Percona Liquibase extension](https://github.com/adangel/liquibase-percona)
*   Place the jar file in your “lib” directory in your Liquibase install directory.
*   ![Zero downtime schema change with Liquibase & Percona](blog/2020/10/image1-1.png)
*   Update any changeset that needs to use Percona to include \`usePercona:true\` (see example below)
*   Profit

Example
-------

Here, we want to add a column: Example:
```
<changeSet id="2" author="Alice">

    <addColumn tableName="person">

        <column name="address" type="varchar(255)"/>

    </addColumn>

</changeSet>
```
Corresponding command that Liqubase would run: pt-online-schema-change --alter="ADD COLUMN address VARCHAR(255)" ... Enjoy all the PTO you get because your deployments happen super fast with no downtime. Hey in the meantime, why don’t you smack talk and shit post on social media? I’m available, I’ve got thick skin, and I’m online a bunch: 
* Twitter: [@ronakrahman](https://twitter.com/RonakRahman) 
* LinkedIn: [https://www.linkedin.com/in/ronak/](https://www.linkedin.com/in/ronak/) 
* Discord: [https://discord.gg/9yBwMtj](https://discord.gg/9yBwMtj) (ronak#8065) 
* Github: [https://github.com/ro-rah](https://github.com/ro-rah)