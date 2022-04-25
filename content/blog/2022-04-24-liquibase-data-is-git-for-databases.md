---
title: "Liquibase Data is Git for Databases"
date: "2022-04-25T00:00:00+00:00"
draft: false
tags: ['blog', 'PerconaLive', 'PerconaLive2022', 'DevOps']
images:
  - blog/2022/4/liquibase-data-gitflow-580x296.png
authors:
  - robert_reeves
slug: 'liquibase-data-is-git-for-databases'
---

*Author's Note: Robert will be demoing Liquibase Data at Percona Live 2022 on Wednesday, May 18 at 11:50am. [Add this presentation to your schedule.](https://sched.co/10JOM)*

Git is an amazing tool for collaboration — developers can work together to build better software faster. However, the usual Git workflow neglects the database. With [Liquibase Data](https://github.com/liquibase/liquibase-data) we’re bringing git to the database so you can easily version containerized databases, share changes with team members, store versions in remote locations, and tag versions.

## The Vanilla Git Workflow
The standard Git workflow is simple. A developer can `git init` to create a local repository. Next, after making changes, `git commit` creates a local version. Then, the developer pushes to a remote branch using `git push`. Finally, another developer can `git pull` to see the new code updates.

## Liquibase Data Workflow
We created the same Git workflow in Liquibase Data. Using the [Liquibase Data extension](https://github.com/liquibase/liquibase-data), Liquibase users can initialize a new database in a Docker container using `liquibase data run`. Which databases? ALL of them. All it requires is a database Docker image that has a volume mount for the data. Liquibase takes it from there. If you already run your development databases via Docker, you will find that Liquibase Data parallels the `docker run` command. 

Here’s what you’ll be able to do:

* Clone from remote repositories
* Make changes to the database
* Commit and push your changes to share with team members
* Tag commits
* Easily view the difference between two database commits to identify changes

Our team thinks this will be useful for test data management and supporting developer database workflows.

Just like you commit after changing your code, you can do the same with Liquibase Data. After you add data to your database or change the schema, run `liquibase data commit`. Commands such as `push`, `remote`, and `log` are also available. 

## Easily Compare Databases
Determining what has changed in your database schema can be very difficult. Liquibase Data makes it simple to find schema differences between commits using the `diff` command. With Liquibase Data, the required database starts automatically for you to create the diff.

## Watch Liquibase Data Demos
Robert Reeves, CTO of Liquibase, [demonstrates how to quickly provision a developer instance of MongoDB](https://www.youtube.com/watch?v=k4m2UCqddHo), make changes to MongoDB, and then commit the change. You’ll see how easy it is to roll your changes backward and forward.


Check out our other Liquibase Data demos for [Oracle](https://www.youtube.com/watch?v=AByPvVoWIXM) and [SQL Server](https://www.youtube.com/watch?v=gLub_7Fcnh4)! Liquibase Data works with ANY database in a Docker Container.

Try Liquibase Data
We think Liquibase Data will be helpful for developers sharing databases among team members. Just imagine — you’ll be able to share datasets you’re working on early in the process and share a separate one later in the process. The distribution of valid test data amongst Dev and QA will speed testing cycles and help find bugs sooner. 

Of course, we want to hear from you! Tell us what you would like to see in Liquibase Data and share with us how you are using it. Our [Open Beta program](https://github.com/liquibase/liquibase-data/tree/main/beta) is a great way to experience the benefits and give us input to make it work even better. We have a tutorial that will walk you through, step by step, how to use Liquibase Data. Along the way, you will have an opportunity to provide your thoughts.

Finally, all of us at Liquibase thank you for your support over the past 15 years of open source greatness. We could not have done it with you. And, the best is yet to come!