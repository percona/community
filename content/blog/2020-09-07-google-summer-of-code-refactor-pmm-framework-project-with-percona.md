---
title: 'Google Summer of Code Refactor PMM Framework Project with Percona'
date: Mon, 07 Sep 2020 11:08:19 +0000
draft: false
tags: ['author_patel', 'Entry Level', 'Google Summer of Code', 'GSoC', 'MySQL', 'MySQL', 'Open Source Databases', 'PMM', 'Tools']
authors:
  - meet_patel
images:
  - blog/2020/09/Screenshot-2020-09-07-at-14.46.59.png
slug: google-summer-of-code-refactor-pmm-framework-project-with-percona
---

I am **Meet Patel**, 2nd year undergraduate at DAIICT, Gandhinagar, India; pursuing a bachelor’s degree in Information and Communication Technology with a minor in Computational Science. 

I am proud to be selected for the **Google Summer of Code** program under an open source organization as big and impactful as **Percona**. As we head towards the end of this amazing program, I’ll try to share a general overview of what and how all of it has been implemented.

About the project
-----------------

PMM-Framework is a shell based tool to quickly deploy Percona Monitoring and Management, add different database clients to it and load test them; all fully automated. It can automatically download and install through Tarball installers and Docker images for the specific version provided. It incorporates usage of tools like DB Deployer to deploy MySQL databases. Other supported DBs by PMM-Framework include Percona Server, MongoDB, Percona Server for MongoDB, PostgreSQL, MariaDB and PXC. It can also be used to wipe all the PMM configuration after tests are done. 

The main objective of the project was to make bug fixes, refactor the framework, add stability to it and make it more robust and useful. In the first half of the project timeline, I worked on implementing the above tasks and tested PMM using the PMM-Framework. Being a shell based tool, PMM-Framework had a slightly steep learning curve for newcomers. So given the mentors’ suggestions, I made a user friendly CLI tool from scratch, namely PMM-Framework-CLI, that would query the user and execute PMM-Framework on the machine, or inside a VagrantBox. 

You can check out the quick demo here:  [https://youtu.be/qPXlTMrsBcU](https://youtu.be/qPXlTMrsBcU) You can check out my contributions to PMM-Framework at [GSoC Project Branch](https://github.com/percona/pmm-qa/tree/GSOC-2020). The source code to the PMM-Framework-CLI tool can be found [here](https://github.com/Percona-Lab/pmm-framework-cli). This tool is soon to be published on NPM so that everyone can quickly start using it through the NPM repository.

Challenges faced
----------------

There would be many unforeseen challenges regardless of the project, overcoming them teaches you a lot. The first challenge that I faced in this project was to understand how everything was working in PMM. I went through every documentation that I could find to understand PMM architecture. Working with shell scripts of this size and debugging them was also a challenge. Due to Covid-19 my university exams timelines were uncertain, mentors also helped me manage that. I didn’t have a lot of prior knowledge about many Linux, Database and Networking concepts, learning which only has added to my skills.

Experiences
-----------

It has been a great learning experience as well. I have got a really great opportunity to experiment and work hands on numerous tools and technologies in such a short timespan. To list some of them:

*   Docker
*   Bash Scripting
*   NodeJS (and publishing package to NPM)
*   Linux, Networking, Databases
*   Ansible
*   SSH
*   Jenkins Pipelines
*   Percona Monitoring and Management (of course!)

Apart from these, the common and biggest advantage of any Google Summer of Code project is that you get to understand a huge codebase that you wouldn’t otherwise. You also get exposed to the best coding practices, development workflows, issues management, time management to name a few. Apart from this, although not part of GSoC but related to the work, I wrote an article about Encryption in SSH/HTTPS that has been trending on the Cybersecurity domain of Medium. The article can be read here: [https://medium.com/code-dementia/demystifying-secure-in-ssh-tls-https-ad7473106c6a](https://medium.com/code-dementia/demystifying-secure-in-ssh-tls-https-ad7473106c6a) 

The part I loved most is the exposure that I got, let alone the learning. The mentors have been extremely friendly and supportive about everything. I also got to improve on my communication skills because of my regular interaction with the mentors. This project has for sure been a great addition to my résumé. I’m happy to announce that this also helped me secure a summer internship at Goldman Sachs for the next summer!  Being a student, learning directly from people having 10x the experience you have not only teaches you well but also prepares for how the team work really happens. 

Overall, it has been an absolutely amazing experience working with Percona and a special thanks to the mentors **Puneet Kala, Nailya Kutlubaeva, Vasyl Yurkovych** of Percona for guiding me throughout.