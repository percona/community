---
title: 'How to contribute Dashboards to PMM'
date: Mon, 04 May 2020 14:54:56 +0000
draft: false
tags: ['daniil.bazhenov', 'Entry Level', 'Information', 'Intermediate Level', 'Open Source Databases', 'Tools']
authors:
  - daniil_bazhenov
images:
  - blog/2020/05/Contribute_to_dashboards_1.png
slug: how-to-contribute-dashboards-to-pmm
---

Have you already contributed to Percona’s open-source products or perhaps you wanted to try doing so? 

I will tell you how to become a contributor to the popular open-source product from Percona in just a few hours. You don't need any serious developer skills. 

We earlier explained how to contribute to PMM documentation in [our last post](https://www.percona.com/community-blog/2020/01/28/how-to-contribute-to-pmm-documentation/). Now we will contribute to PMM itself, namely to Dashboards. Dashboards are an important part of PMM, they are seen and used by thousands of users, so your contribution may be of benefit to many others. 

You can view the latest version of our demo at [https://pmmdemo.percona.com/graph/](https://pmmdemo.percona.com/graph/). 

The purpose of this latest article is to introduce you to the process of making changes to Dashboards in PMM, such as creating a new dashboard or improving an existing one. If you want to become a contributor, you will need to repeat the steps from [my earlier post](https://www.percona.com/community-blog/2020/01/28/how-to-contribute-to-pmm-documentation/). 

You need to:

1.  Have PMM installed on your server. PMM is easy to install via Docker.
2.  Have a GitHub account and install Git on your computer.

![How to contribute Dashboards to PMM](blog/2020/05/Contribute_to_dashboards_1.png)

What kind of contribution should I make?
----------------------------------------

Of course, this is the first question to decide. PMM is a great product that many developers are working on. PMM uses [JIRA](https://jira.percona.com/projects/PMM/issues/PMM-4923?filter=allopenissues) to track development tasks. You can:

1.  Explore the tasks and choose an interesting one
2.  Create your own task from scratch

When I used PMM, I noticed that many charts have useful tooltips.  Although you can make any sort of contribution, in this article I will use the simplest type of contribution, a tooltip. 

Here’s the value of tooltips:

> Tooltips - they are written by experts, for consumption by non-experts.  One of Percona's value-add is to write good tooltips that are useful. We (Perconians) know the technologies and we have people who are used to simplifying complex topics.

![Tooltips](blog/2020/05/Contribute_to_dashboards_2.png) 

There are a lot of widgets that haven't been described yet, so tooltips would hugely increase user experience here. You can open the widget settings and do the following:

1.  See settings, functions and parameters on which the chart is built.
2.  Study the documentation for these parameters
3.  Write a tooltip.

![PMM Dashboard Settings](blog/2020/05/Contribute_to_dashboards_3.png) 

Now that we have defined what we’re about to do, let’s make a tooltip for one of the charts. 

I opened JIRA and created a task where I described what I would do: 

**Tooltips: Prometheus dashboards: Head Block: Update graph panel description** 

[https://jira.percona.com/browse/PMM-5053](https://jira.percona.com/browse/PMM-5053) 

![PMM Dashboards Jira Issue](blog/2020/05/Contribute_to_dashboards_4.png)

We'll find a repository for the Dashboards
------------------------------------------

We'll make changes to the code. 

PMM is big, for convenience it has a lot of GitHub repositories which can be found in the main repository [https://github.com/percona/pmm/tree/PMM-2.0](https://github.com/percona/pmm/tree/PMM-2.0). 

Since I will be contributing to Dashboards, I will need a Grafana Dashboard repository: [https://github.com/percona/grafana-dashboards](https://github.com/percona/grafana-dashboards) 

Next I make a fork of this repository in my GitHub account. A fork is needed to check my changes before sending them to the main repository. 

By the way, more than 600 people have already done it. You can do it, too! :) ![PHH Dashboards Contribution GitHub ](blog/2020/05/Contribute_to_dashboards_5.png)

Let's study the structure of the Dashboard
------------------------------------------

All Dashboards are located in the "dashboards" folder and each dashboard is a JSON file. 

An example can be found here: [https://github.com/percona/grafana-dashboards/tree/master/dashboards](https://github.com/percona/grafana-dashboards/tree/master/dashboards) 

Next I have to:

1.  Find the JSON file I need
2.  Understand what needs to be changed
3.  Change it
4.  Commit and send a Pull Request for review
5.  Celebrate

It is important that all contributions are carefully reviewed. When I wrote this article, I changed only a few lines, but even this was in review for several days by different expert advisors.

Changing the Dashboard is easy
------------------------------

I don't have to know JSON. You can change Dashboards directly in the PMM interface. All settings are saved in JSON. Each chart has a button "Panel JSON", which allows you to display JSON code. ![Changing the Dashboard is easy](blog/2020/05/Contribute_to_dashboards_6.png) That way, I can:

1.  View the chart settings
2.  Make the necessary changes
3.  Save and get the necessary JSON file

If you look at the chart settings, you can understand what functions and arguments they use and check out the documentation: 

*   [https://prometheus.io/docs/prometheus/latest/querying/functions/](https://prometheus.io/docs/prometheus/latest/querying/functions/) 
*   [https://prometheus.io/docs/prometheus/latest/querying/operators/](https://prometheus.io/docs/prometheus/latest/querying/operators/) 

Review the documentation to make the correct description for the chart or make other improvements to the chart. 

As a next step, I need to add value to the Description field. As soon as I add it, I immediately get the tooltip for the chart. 

![ Description field](blog/2020/05/Contribute_to_dashboards_7.png)

Save the result
---------------

I add the Description and save the chart. Then I open the JSON widget and find my value in the "description" field. It's simple. I need to move the changes to the git repository. 

If I had created a new Dashboard or a chart, it would have been easier for me to transfer the entire file to the repository. But since I only have one line changed, I will only move it. 

![JSON](blog/2020/05/Contribute_to_dashboards_8.png) 

I made my fork repository's git clone to a computer beforehand.

1.  I open the dashboards/Prometheus.json file
2.  I find the "title" block: "Head Block"
3.  I add a line with "description" and save the file

Working with the PMM repository
-------------------------------

I have already described in detail the work with the repository in the previous article (link), and you can also use the instructions in the repository itself: 

[https://github.com/percona/grafana-dashboards/blob/master/CONTRIBUTING.md](https://github.com/percona/grafana-dashboards/blob/master/CONTRIBUTING.md) 

I created a separate branch, named the commit correctly and sent it to my repository. 

I then made a Pull Request to the main grafana-dashboards repository. 

I really liked the process of testing the repository. I'll tell you the steps.

### Contributor License Agreement

The first step is to sign the license/cla Contributor License Agreement. This is done with your GitHub account and one button. Simply read and agree. 

![Contributor License Agreement](blog/2020/05/Contribute_to_dashboards_9.png)

### Automated code review

Your branch will pass an automated code check using the [Codecov](https://codecov.io/) service. 

You will be able to see the process and you will see the result: Codacy/PR Quality Review Up to standards. 

A positive pull request. ![Codecov](blog/2020/05/Codecov.png)

### Continuous integration (CI)

After each commit, Jenkins CI will try to build a PMM to:

1.  Make sure that your changes do not break the PMM
2.  Run auto testing

It takes a few minutes. 

I'm sure you'll pass all the automatic checks. 

You can try to start the build yourself using the instructions in the repository. 

If you are interested in these processes, please let me know in the comments. ![Jenkins](blog/2020/05/Jenkins-1.png)

Expert review and code review
-----------------------------

Percona experts check all code changes. The more changes, the more experts will be involved. 

While I was writing this article, I made several contributions to Dashboards PMM.

1.  When I changed one line to add a tooltip, my code was reviewed by 2 people: the person responsible for Dashboards and those leaders.
2.  When I added a 50 line instruction, it already needed to be reviewed by 4 people.

After each task is completed in JIRA, they will be checked by the QA department. 

You should not worry about the review process. Percona experts are very friendly, they will write recommendations directly to GitHub. They can even correct some lines at once. 

If you have any questions, just text me, I'll try to help. 

I received a few recommendations, made some changes and my contribution was accepted. ![](blog/2020/05/Contribute_to_dashboards_14.png)

Results
-------

I became a PMM contributor by improving one of the Dashboards. I spent about 30-60 minutes a day and it took me less than a week. 

![Result](blog/2020/05/Contribute_to_dashboards_15.png) 

In the process, I was able to add instructions for future contributors (link). You can improve this manual, too. 

I urge you to become a contributor. If you need help, just email me. 

More ideas for contributions can be found here: [Link](https://www.percona.com/community/contributions/pmm)

My references
-------------

Home page of the PMM contributor: [https://www.percona.com/community/contributions/pmm](https://www.percona.com/community/contributions/pmm) 

An article on how to become a documentation contributor: 
*  Instructions for Contributors: Issue at JIRA: [https://jira.percona.com/browse/PMM-5053](https://jira.percona.com/browse/PMM-5053) 
* A branch in my repository: [https://github.com/dbazhenov/grafana-dashboards/tree/PMM-5053_dbazhenov_tooltip](https://github.com/dbazhenov/grafana-dashboards/tree/PMM-5053_dbazhenov_tooltip) 
* Pull Request to PMM repository [https://github.com/percona/grafana-dashboards/pull/524](https://github.com/percona/grafana-dashboards/pull/524) 
* Confirmed by CLA: [https://cla-assistant.percona.com/percona/grafana-dashboards?pullRequest=524](https://cla-assistant.percona.com/percona/grafana-dashboards?pullRequest=524)