---
title: 'How a Database Monitoring Tool Can Help a Developer. The Story of One Mistake.'
date: "2023-04-07T00:00:00+00:00"
draft: false
tags: ['PMM', 'Monitoring']
categories: ['PMM']
authors:
  - daniil_bazhenov
images:
  - blog/2023/04/start-new-feature.jpg
---

I will tell you the real story of using database monitoring tools when developing an application. I will show you an example of how I managed to detect and fix a problem in the application.

_A small clarification, the real story from my development practice happened a little more than a week ago, but for the article I took graphs of final debugging, so that the graphs show the correct sequence and fit into the available for explanation and demonstration. It's just that in reality, I went out for coffee several times and thought for a long time about what was reflected in the graphs of monitoring:)_

![How a Database Monitoring Tool Can Help a Developer](/blog/2023/04/start-new-feature.jpg)

![How a Database Monitoring Tool Can Help a Developer](/blog/2023/04/pmm-image-1.jpg)

## About the app and the process

I am developing a PHP application using MongoDB as a database. The application is lightweight, and most load falls on the database. I have implemented functions at the application level to adjust the number of queries, as the application can quickly load the database to 100%. 

For development, I use several small dev instances in AWS, use Percona Server for MongoDB with three nodes as a database, and have Percona Monitoring and Management (PMM) installed for monitoring the databases. 

My development process consists of the following steps:

1. I developed a new feature and ran it on the dev server for testing.
2. I check the prefiling on the PHP side, and there is no memory leak, and I am happy with the speed.
3. I check the database monitoring to ensure everything works fine. 
4. I debug the feature, setting the number and types of queries in the function to balance the number of queries and the load on the database, if necessary. 

## Adding new functionality to the application

So I started the application and got ready to run the new feature. The feature was getting information from open sources, processing it, and saving it to the database. The second part of the functionality went through all the saved documents and did some additional processing. 

At this point, the application already had a lot of features that loaded the CPU of the Primary Node by 25-40%, and everything was running stably. I decided to have a performance reserve, as I planned to add new features.

I checked several dashboards, and there were no anomalies or changes. PMM has many dashboards and charts, and I will only show a few, just some.

![Adding new functionality to the application](/blog/2023/04/pmm-image-2.jpg)

I saved the changes with the new feature and pushed it to the dev server to make it work. Then I checked that the function started without errors, and the result was visible in the database. I use MongoDB Compass to check the result of a database entry.

## Something has gone differently than planned.

I waited a few minutes and rechecked the dashboard. At first glance, the main screen was fine. However, I was alarmed by the speed of processing. The number of operations has mostly stayed the same.

I scrolled down through the various charts on the dashboard and saw an anomaly.

The latency increased, and the app loaded the instance to 100% CPU.

![Something has gone differently than planned](/blog/2023/04/pmm-image-3.jpg)

![Something has gone differently than planned](/blog/2023/04/pmm-image-4.jpg)

I have made a test run on the application side and checked the profiler there, too. The app worked poorly, and queries were slow.

## Finding the cause of the problem

I knew the reason was the new feature and immediately rolled back the last changes.

I had a rough idea of where the problem might be, made a few changes, and started again.

I did it several times, but the result was the same (the CPU was loaded at 100%).

I selected a period with a load and used the Query Analytics function built into the monitoring.
Query Analytics shows a list of queries sorted by load or execution speed. Some of the queries to the Pages collection gave 90% load, and the Query Time was more than 3 minutes.

![Percona Monitoring and Management PMM - MongoDB - QAN](/blog/2023/04/pmm-qan.jpg)

In Query Analytics, you can find slow queries, see their details, and then debug them in the application.

## Fixing the problem

I made a few changes that fixed the problem. 

The first problem was the indexes. I create indexes from within the application using the command. 
```
$app['db']->CollectionName->createIndex(['index_key' => 1]);
```

Since the application uses many different collections and queries with conditions on various fields and with or without sorting, I have a lot of indexes.

I made a typo in this case, and the index was not created correctly.

After the indexes were created correctly, I needed quick runs to debug the number of queries to adjust the CPU load to around 50%.

You can see the final chart after debugging and fixing the problem.

![Percona Monitoring and Management PMM - Fixing the problem](/blog/2023/04/pmm-image-5.jpg)

![Percona Monitoring and Management PMM - Fixing the problem](/blog/2023/04/pmm-image-6.jpg)

## Conclusion

Don't forget to add indexes and make sure they work.

I am a simple developer who can make mistakes and do different experiments. Installing the monitoring was one of the experiments, and previously I just focused on the speed of the PHP script. From time to time, I have looked at the monitoring dashboard in the AWS control panel, but it gives less information, only about the instance itself, without being able to investigate in detail.

So, [PMM](https://www.percona.com/software/database-tools/percona-monitoring-and-management) have a great tools for debugging and searching “bottlenecks” in the databases. And I recommend installing and trying database monitoring with PMM if your application uses MySQL, PostgreSQL, or MongoDB.






