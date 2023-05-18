---
title: "Easy Way to Start Contributing to Open Source With PMM Documentation"
date: "2023-05-18T00:00:00+00:00"
draft: false
tags: ["opensource", "documentation", "percona"]
authors:
  - aleksandra_abramova
images:
  - blog/2023/05/PMM-Doc-Contribute.jpg
---

If you are a user of Percona Monitoring and Management and noticed any typo or inaccurate information in its [documentation](https://docs.percona.com/percona-monitoring-and-management/index.html), you can easily correct it yourself in the [repository](https://github.com/percona/pmm-doc) following detailed instructions in [README.md](https://github.com/percona/pmm-doc#readme). But if you are not experienced in open source contributions, you may still feel uneasy about following those steps. This post is for you! We will walk through the main steps with pictures and explanations.

## Create a Fork

First, you need to create a fork from the main repository to your account. In the top-right corner of the page, click **Fork - Create a new fork**. 

![Contribution](blog/2023/05/contribution2.jpg)

## Build Documentation With Docker
The easiest way is to build documentation with Docker. If you don’t have it installed, download it from the Docker official website and follow the instructions. The process of installation is quick, and it is no more difficult than the installation of any other app.

Open your fork on GitHub and clone that repository to your local environment. 

`git clone git@github.com:{user-name}/pmm-doc.git`

![Contribution](blog/2023/05/contribution1.jpg)

Change directory to **pmm-doc**. 

`cd pmm-doc`

To check how our edits will look like, we need to build documentation for live previewing. Run: 

`docker run --rm -v $(pwd):/docs -p 8000:8000 perconalab/pmm-doc-md mkdocs serve --dev-addr=0.0.0.0:8000`

Wait until you see `INFO    -  Start detecting changes`. When the documentation is ready to work with, it will be available at [http://0.0.0.0:8000](http://0.0.0.0:8000/) in your browser, and it will reflect all changes that you make locally.

## Make Changes

In a new Terminal tab, create a new branch and make your changes. Save them, create a commit, and push it to your fork. 

Create a pull request to the main repository. You will also need to sign the CLA, so we could merge your changes. 

You did it! Congratulations! Now wait for the feedback from the Percona team. If there is no problem with your PR, it will be merged into the main repository.

## Next Steps

To make further changes, you need to keep your repository up-to-date with the upstream one. There are several ways to do it. You can find the information [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork). The simplest way is to do it using the GitHub interface. Just click on **Sync fork** and then **Update branch**.

![Contribution](blog/2023/05/contribution3.jpg)

After that, you will be able to update your local repository with `git pull` command. 

If you face any problems with contributions to Percona repositories, don’t hesitate to contact us at community-team@percona.com or ask your question on the [Percona Forum](https://forums.percona.com/). 
