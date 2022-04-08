---
title: "Percona Podcast Russian Edition Ep 1 - Andrey Borodin (Yandex)"
description: "Andrey Borodin, Teamlead of Open Source RDBMS Development at Yandex, sat down with Daniil Bazhenov, Community manager at Percona, to talk over machine learning in databases, WAL-G disaster recovery tool, #database naming, testing, fixing rare reproducible bugs, and more."
short_text: "Andrey Borodin, Teamlead of Open Source RDBMS Development at Yandex, sat down with Daniil Bazhenov, Community manager at Percona, to talk over machine learning in databases, WAL-G disaster recovery tool, #database naming, testing, fixing rare reproducible bugs, and more. Andrey is a software engineer, computer scientist, developer at Yandex, Ph.D., associated professor  at Ural Federal University, co-founder of Octonica company. He is interested in backup technologies and data indexing. His recent talk at Percona Live featured the architecture of point in time recovery with WAL-G in the cloud."
date: "2021-08-10"
podbean_link: ""
youtube_id: "BYt9T4J1aYs"
speakers:
  - andrey_brodin
  - daniil_bazhenov
---

## Transcript

**Daniil Bazhenov:**
Hello! My name is Daniel, I'm from Percona. I welcome you on the Percona podcast, where we invite engineers, opinion leaders, tech leads and talk about databases, about open source. Andrey Borodin from Yandex is with us today. Hi Andrew! Tell us a little about yourself, what you are doing, what you are doing now, about yourself.
 
**Andrey Borodin:**
I'm fixing Postgres for Yandex, sometimes something doesn't work there or something can be done better. My team and I fix bugs, make features, watch the bases fly, how the bytes are written there so that none of them disappear ... All simple work.
 
**Daniil Bazhenov:**
Tell us a little more, maybe about what you are working with. Yes, I see, Postgres, everything breaks ... What breaks? I also have a website, there is also Postgres, something is probably breaking.
 
**Andrey Borodin:**
No, Postgres is certainly a reliable database. In general, we make a managed database, that is, if Yandex services want a database, they press a button and virtual machines are created, poured, combined into a cluster, backups are made, monitors are installed, upgrades are done, all sorts of things. My unit, the unit in which I work, is engaged in the development of transactional databases, these are MySQL, Postres, Greenplum and MS SQL. Already my division, which I manage, is engaged in the development of open databases. Well, that is, it is obvious that we cannot develop MS SQL, because it is developed by Microsoft. We put our hand to everything else whenever possible. All these are reliable bases, but on a large scale various exceptional situations arise that are difficult to step on. But when you have several thousand bases, they still happen.
 
**Daniil Bazhenov:**
It's clear. You recently spoke at Percona Live, our big online conference, and it was very interesting, thank you. We will try not to repeat this talk, I just would like to ask you to tell us what it is about. What was there and, perhaps, if someone is interested, they can find the report on YouTube, listen.
 
**Andrey Borodin:**
The talk at Percona Live was that we are developing a backup system. When we were building managed databases in Yandex.Cloud, there was a wal-e system, with which everything was fine, but something was not right. It was replaced by the WAL-G system, which was rewritten almost from scratch. We began to help her develop, and at some point I suddenly discovered that I became the main maintainer of this database. It seems like I just brought pull requests and fixed bugs ... But somehow it happened that it spilled over to us, and now about half, slightly less than half of the WAL-G developers from Yandex. And at some point we supported MySQL,
then we supported MongoDB on the same system, and we created a backup management system with a single interface for many transactional databases. That is, if you administer MySQL, Postgres, Microsoft SQL Server, Greenplum, and FoundationDB at the same time, and you want you to consistently make backups, you configure WAL-G everywhere and only monitor it. You have fewer entities to observe. Well, we tried to make it effective. Here is a report on how to make sure that not a single extra byte is sent over the network, not compressed, there is such a thing, here.
 
**Daniil Bazhenov:**
It's clear. You said that you are faced with some kind of errors, problems, something falls, something has to be fixed. It is interesting what happened now, perhaps today, yesterday, the day before yesterday, or some typical things. What problems do you face?
 
**Andrey Borodin:**
I can tell you about the example of fixing the error about reindex concurrently. I will try not to make it a lecture for an hour and a half. In Postgres, it is possible to rebuild the index under load. Well, that is, for example, bloat has accumulated there, or you just want to create a new index under load. The plate is changing, you don't want to have a lot of logs. Well, you don't run create index, but create index concurrently. The minimum number of logs is taken, but the table needs to be scanned twice. Read once to build the primary index, then the index starts updating, and the second time reads the table to download the changes that were missed during the first index run. So, three years ago, on one of the installations, a message appeared that one line was not included in the index after the index was built competitively. Then two years ago this message appeared again. A year ago people came from one big service, I think it was S3 Metadata, and they say that we have a replay, but it's once a quarter. Okay, okay, I'm waiting 3 months. Finally, I was able to catch this error in December. I realized that there was an error in the logs. I wrote a patch and it came out with update 12.7, I think, or 12.6. And in the summer, people from S3 came back and said: “And there is still a bug, we have a replay again, only now it is less frequent than once a quarter. And yesterday we also discussed Postgres with the developer and realized what the problem was. And now today I wrote a patch all day to fix this problem. I hope that we will fix this problem for the last time.
 
**Daniil Bazhenov:**
It is very interesting to debug a problem that is reproduced quarterly.
 
**Andrey Borodin:**
And most importantly, our tickets are evaluated by story points, that is, development days, and there are two days of development on this ticket, it was created 3 years ago during the first reproduction, I sometimes transfer it to work, sometimes I forget, so it accumulated in total , I don’t know, several months of development on this ticket, but it is estimated in two days. I think this happens in other areas too.
 
**Daniil Bazhenov:**
Yes of course. A little about the tools. What are your favorite tools that you use now for debugging, finding problems? Well, exactly what is in the current use.
 
**Andrey Borodin:**
In general, before I got to Postgres, I was doing Windows development for 10 years, and Visual Studio was close to me. In the Posgres world, I had to move to unix-like systems, so I've been doing this for 4-5 years, I still feel like a cardboard, fake Linux developer. I can use GDB, but I can look at variables like that, put breakpoints, but I don’t know how to use wise scripts. My main code editor is Visual Studio code, but it's just there to correct the text, nothing else happens, you type letters, press the keys ... Here.
 
**Daniil Bazhenov:**
Use the keyboard, right? Class.
 
**Andrey Borodin:**
Yes, I have two of them.
 
**Daniil Bazhenov:**
Why the second?
 
**Andrey Borodin:**
This one, and also on a laptop, to fix bugs with two hands. And I have been using the code server lately. This is Visual Studio Code, only on remote virtual machines. Recently, I like to debug on virtual machines, not in containers on a laptop.
 
**Daniil Bazhenov:**
It's clear. If we talk about some new tools, tools that you might have tried or want to try, or heard somewhere at rallies, or one of the guys directly said that this is a cool thing.
 
**Andrey Borodin:**
I am writing a database that is older than me. It is written in S89, the ANSI the C , I was still in kindergarten did not go when the standard has been adopted. I use utilities that existed when I started school.
 
**Daniil Bazhenov:**
Let's talk about management then.
 
**Andrey Borodin:**
No, there is one thing where I like new things. These are algorithms. B olshe of all, I want to pull in Postgres ... Last year, '20 many people do not like it, but nevertheless invented Piecewise Geometric Model. 3 years ago Google came up with such an interesting initiative as learned indexes: let's bring some machine learning to databases. In databases, everything is tight with machine learning, because classical algorithms in deterministic problems, well-posed, yes, classical algorithms outperform these machine learning. But finally there was a case of cutting edge, so to speak, progress to apply in databases. But, unfortunately, learned indexes did not support the concurrent access model, did not support updates, and in general it was such a proof of concept that, yes, it looks like a database, but you are not a database. In the twentieth year, several Italian researchers came up with the idea of the Piecewise Geometric Model, which is bringing the idea of learned indexes to reality: let's make an associative search container that uses interpolation search, which is like statistically trained trees. And this is the kind of thing I use all the time. That is, I'm reading about some new Bloom filters out there, which Facebook also recently suggested, new algorithms and data structures, and it's really cool. I'm excited about a new way to stuff bytes into processors.
 
**Daniil Bazhenov:**
Good. In simpler terms, what is the most common mistake people make when they work or do something with databases?
 
**Andrey Borodin:**
The worst mistake that users make ... We are writing a cloud service, it is easy to create a database there, it is easy to monitor the database, it is easy to backup the database, and it is very easy to delete the database there. Once a month I see an incident where a person named his cluster something like "well, some data." Another person came, there is not enough quota, there is not enough money, or for some reason this is: "Unnecessary base, terabyte, oops, delete!" The clouds are removing the bases very quickly. It's not really about exploitation. But here I am participating in these incidents. because I look at how the system, my backup system is good at restoring the database back. The most important point of the cloud service is that we will not allow the user to lose data, we do not give the opportunity to turn off VSyns there, we do not give the opportunity to disable point-in-time recovery, the user must not only delete his data, he must wait for the recovery window to end. Well, here's a mistake that is common, and we somehow prevent it.
 
**Daniil Bazhenov:**
I haven't used Yandex.Cloud for a long time. And yesterday I literally ran into it on GitHub. I have not deleted the repositories for a long time, I went in, I had to delete, and they highlighted such a danger zone, everything that is connected with deletion is there: think three times if you should do it. Is it the same for you?

**Andrey Borodin:**
Yes, the request per second graph is shown, and you must type the name of the database and not make a mistake in any character. You cannot paste it from the clipboard. But this is a rake that is laid in advance. When you create a database, you need to give it a meaningful name. Usually creators, developers, do not know the service they are writing, they create the future, it is difficult to see the future. And they don't know what the database will be called, they call it Database_1. And then you don't remember what Database_1 is. It is not enough to show 1000 RPS or 10,000 RPS on the host. By the way, another feature of Yandex. A very large part of the load in Yandex is created by tests, something is constantly being tested somewhere. The test base is usually loaded like this into the shelf, because you want to know when they will break, they are test ones, what load will beat them. Therefore, the load schedule does not always scare a person. Well, yes, here it is 10 kilo RPS, but in testing it is always like that, it’s on sale we have there just barely zero recycling breaks away. But if you have any ideas on how to distinguish a well-needed base from an unnecessary one, then be sure to write to me. I will be glad to hear it.
 
**Daniil Bazhenov:**
It seems to me that you yourself suggested the idea, this is just a name validator. If someone tries to create something with the word test, then he should be told: “Ok, is this really a test? We'll kill it in a week. ” So, everything else should be checked against the Yandex dictionary, that this is something that will work.
 
**Andrey Borodin:**
Some service had a database of testers, whom they considered the most loyal users, and they named it ... That is, the word test appeared in the name.
 
**Daniil Bazhenov:**
By the way, I saw somewhere in which service, he just did not allow this crazy name to be created, he said write something humanoid. OK. We talked about mistakes. There are just databases. You work with relational databases. Even in relational databases, many variations are emerging now. And forks of MySQL, and forks of PostgreSQL, and just some new databases, and many, many databases, you probably notice this too. What do you think is connected with it, what makes people try new things?
 
**Andrey Borodin:**
My answer here is that the database is an unsolved problem. Unfortunately, so far the databases are failing. Everything that we have done, we as humanity, is still not even close to perfect. Look, the cars are the same, the history of the car is constantly new, they have some new safety systems. 20 years ago, no one knew what a system of exchange rate stability was. Now in Russia it is forbidden to sell new cars without a system of exchange rate stability. The cars are still imperfect, people still suffer from exploitation, the nuts still fall off, all the gasoline runs out, and the user is like, “Why isn't she driving? Start up! ” And she's not going. It's the same story with databases. There is no service that simply works, in clear idioms, with clear guarantees. The database is still a black box with 1000 pens. Even if you have a Kuber operator there or there is a magic DBA, some magic happens somewhere, someone has to pull the strings so that everything will fly correctly. The database will be better. Examples include electricity. Previously, it was possible to get electricity from different providers, it could be direct current, it could be alternating current, it could be multiphase electricity. Now you have an outlet, you stick what you want into it and don't think about the need to renew any contracts, any kind of service. Electricity is a resolved problem, there is no database yet. The database will develop, unfortunately, for quite a long time.
 
**Daniil Bazhenov:**
Excellent. Fortunately, I guess. If we work with databases, then probably to our happiness.
 
**Andrey Borodin:**
We would have found another job. But this is really the place where you can put in the effort and move humanity in the right direction. Or wrong. But it depends on the effort.
 
**Daniil Bazhenov:**
I’m from my bell tower, for example ... Okay, I, for example, have been working MySQL for a long time, then okay, I'm tired, you can try a new project there PostreSQL, you can put a small project there Mongo, and just write in a row, and everything is fine working. When the database appeared a year ago, you go there and see that it has top clients, its implementation ... I just don't quite understand how it comes about, so I ask. No, I may understand how this appears, because I observe it often, but it’s just interesting not from the outside. What would make you, here you are creating a new project, I clean up such a top 5 databases, I want it on this one.
 
**Andrey Borodin:**
Because there are known limitations in older databases. The limitation, for example, of the same Postgres or MySQL, is quite understandable, it is, firstly, the incomplete serializability of transactions, which are cosmically expensive there. That is, serializable or higher levels of strick serializable, they really do drop performance in Postgres or MySQL. Here, and another, more real problem, is that the service cannot grow for, say, 10 terabytes. Postgres or MySQL for 10 terabytes does not work. These two problems need to be solved. Whoever decides first is a fine fellow.
 
**Daniil Bazhenov:**
You contribute a lot to the open source, there were many examples of your presentation at Percona Live. I faced a problem at work, when, for example, a person wants to contribute to open source, he is not allowed to do it somehow with an organizational plan. I would like to know how your process is organized here, that is, but you write your own patches for yourself, and here, for example, you need to make a contribution to some side project, WAL-G, yes, that is, you are right here everything is smoothly organized at the company level.
 
**Andrey Borodin:**
No, we have anarchy.
 
**Daniil Bazhenov:**
Well, just tell me how it happens. For me, for example, when I was engaged in development, if I came to the manager and said, instead of writing some feature from our backlog, I want to fix a bug in a third-party product instead of plugging their manager, I would be told: "Let's wait".
 
**Andrey Borodin:**
There are many cases when besides us it seems that no one will develop. Well, that is, for example, now compression in the Postgres protocol is being developed by Yandex developers and one of the Postgres Professional developers. And it seems that there are 2 more people in the world there, Justin Freesby, I don't remember where he works, and someone else also showed interest. And so four people gathered and what are you doing. And it is obvious that Yandex definitely needs it. The cost of operation for us consists of interdata-center traffic, we definitely need to compress the traffic, and on the other hand, there is an understanding that one person who needs to work there from our side, he will definitely be useful there, he will not stomp there, he is something will move forward. Therefore, Daniel is doing this. We do not have a decision-making process, because, in fact, all cases are exceptional. In Yandex, they often say: “Use your head”. This is a general recommendation that does not say anything about what exactly needs to be done, that is, how to use it: by keyboard or thinking. First of all, we of course investigate incidents and there is a policy, not a policy, that everything related to incidents, everything that
affected users, we must fix it. If someone could not send an email due to the fact that we have an error in the connection pooler, we must fix it. That is, how this error still gets into our backlog. And here are the two main ways to get into the backlog, this is something that will save us a lot of money, or something that led to the downtime, that some service was down. Then just a standard process, we choose the most critical - we do it.
 
**Daniil Bazhenov:**
Understood thanks. In principle, this is the norm for you, this is good, very cool.
 
**Andrey Borodin:**
My department is called Development of open databases, that is, we do almost nothing else.
 
**Daniil Bazhenov:**
Do you have a big team?
 
**Andrey Borodin:**
With 6 people, including me, and Yuri Frolov, we now have a trainee engineer, who full-time to Postgres, Greenplum, and elsewhere. There is a person in Moscow who is working on minor problems related to MySQL 5.7, but he is not in my department, he is in Dima's department. There, certificates are not updated. MySQL 5.7 does not know how to renew TLS certificates, and on each class it does this once a year, but we have several thousand clusters, a dozen hosts are added every day, which need to renew TLS certificates. The monitoring lights up once every 2 weeks, and once every 2 weeks the attendants suffer with the need to notify all users that MySQL 5.7 will be restarted. Therefore, we need to do this now ... The code has already been written, we only need to roll out the assembly with reloading the TLS certificate without breaking existing connections. I don’t remember why I told it ... And, how many of us, that there are not only developers in my department. Yes.
 
**Daniil Bazhenov:**
We talked about what you do, what you would like to see in the future, machine learning. And it’s also interesting, again, what will happen next, what will change exactly in what you are working with? What interesting things, technologies will appear in the next couple of years, what to expect?
 
**Andrey Borodin:**
One of the growth points of such data management technologies in the world today is the idea that databases used to be written to disk. One of my favorite MangaDB databases, not MongoDB, writes to pipe at all, but that's another story. The idea of being able to write to a scalable network service actually originated in Amazon Aurora, and many developers recently realized that Amazon Aurora was hitting billions of dollars a year in revenue. Now they began to create data management systems that are not based on what we write to a local hard disk (well, not on a local NVMe disk, not on a local SSD disk), but we are writing some service that provides an API for data management. Not SQL-ness, but a simpler protocol like storing a page of data, and I think that in the next two years we will see Amazon Aurora in open source. We will see databases that live on top, that separate compute and storage, separate compute and storage. Now Zenith is probably such an advanced startup on this topic, they write for Postgres. I'm sure there are analogues in the MySQL world too. I sometimes look, they are being developed on GitHub, I signed their commit log, and I see that their engineering thought sometimes rushes in one direction, sometimes rushes in the other direction, but in general they follow the path of refusing the guarantee of disks, these here are the file systems, yes, that our data is sent to some service that is already sharded, which is already cheap, which is already effective, and latency is provided due to good caching of the local in the buffer, but not on the disk. 
 
**Daniil Bazhenov:**
Cool. I propose to finish, we talked cool in my opinion. Thank you very much for this meeting, for this entry. I invite everyone to our community website percona.community, where you can find all podcasts, recordings, we also have a Percona Youtube channel, where you can find, among other things, Andrey's report on Percona Live and this podcast will be published. Thanks to all! Thank you very much, Andrey.

## Transcript RU

**Даниил Баженов:**
Всем привет! Меня зовут Даниил, я из Percona, приветствую вас на подкасте Percona, куда мы приглашаем инженеров, лидеров мнений, техлидов и говорим о базах данных, об opensource. Сегодня с нами Андрей Бородин из Яндекса. Привет, Андрей! Расскажи немножко о себе, о том, чем занимаешься, что сейчас делаешь, о себе.

**Андрей Бородин:**
Я чиню Postgres для Яндекса, там иногда что-нибудь не работает или что-нибудь можно сделать лучше. Я и моя команда фиксим баги, делаем фичи, смотрим как летят базы, как там пишутся байты, чтобы ни один не пропал... Вся нехитрая работа.

**Даниил Баженов:**
Расскажи немножко больше, возможно о том, с чем работаешь. Да, понятно, Postgres, всё ломается... Что ломается? У меня вот тоже есть веб-сайт, там тоже Postgres, наверное что-то ломается. 

**Андрей Бородин:**
Нет, Postgres конечно надежная база данных. Вообще мы делаем управляемую база данных, то есть сервисы Яндекса если хотят базу, они нажимают кнопку и создаются виртуальные машины, наливаются, объединяются в кластер, делаются бэкапы, навешиваются мониторинги, апгрейды делаются, всякие такие вещи. Моё подразделение, подразделение, в котором я работаю, занимается разработкой транзакционных баз данных, это MySQL, Postres, Greenplum и MS SQL. Вот уже моё подразделение, которым я руковожу, занимается разработкой открытых баз данных. Ну то есть очевидно, что MS SQL мы не можем развивать, потому что его развивает компания Microsoft. Ко всему остальному мы прикладываем руку по возможности. Всё это надежные базы, но в большом масштабе возникают разные исключительные ситуации, на которые сложно наступить. Но когда у тебя несколько тысяч баз, то они все равно случаются.

**Даниил Баженов:**
Понятно. Недавно вы выступали на Percona Live, нашей большой онлайн-конференции, и это было очень интересно, спасибо. Мы постараемся не повторять этот доклад, просто я бы хотел попросить, чтобы вы рассказали о том, о чём это. Что там было и, возможно, если кого-то заинтересует, они могут найти доклад на YouTube, послушать.

**Андрей Бородин:**
Доклад на Percona Live был о том, что мы развиваем систему резервного копирования. Когда мы строили управляемые базы данных в Яндекс.Облаке, существовала система wal-e, с которой было всё нормально, но что-то всё было не так. Её заменила система WAL-G, которая была переписана почти с нуля. Мы стали помогать ей развиваться, и в какой-то момент я вдруг обнаружил, что я стал главным майнтейнером этой базы данных. Я вроде просто пулл реквесты приносил и баги чинил... Но вот как-то так случилось, что она перетекла к нам, и сейчас около половины, чуть меньше половины разработчиков WAL-G из Яндекса. И в какой-то момент мы поддержали MySQL, потом поддержали MongoDB в той же системе, и мы создали систему управления бэкапами с единым интерфейсом для очень многих транзакционных баз данных. То есть если вы администрируете одновременно и MySQL, и Postgres, и Microsoft SQL Server, и Greenplum, и FoundationDB, и вы хотите, чтобы вы единообразно делали резервные копии, вы настраиваете везде WAL-G и вот только его мониторите. У вас становится меньше сущностей, которые нужно наблюдать. Ну и мы постарались сделать его эффективным. Вот доклад о том, как сделать так, чтобы ни одного лишнего байта не отправлять через сеть, не сжимать, там такое всякое, вот. 

**Даниил Баженов:**
Понятно. Вы говорили о том, что сталкиваетесь с каким-то ошибками, проблемами, что-то падает, что-то приходится фиксить. Интересно, что сейчас, возможно сегодня, вчера, позавчера произошло, или какие-то типовые вещи. С какими проблемами вы всё-таки сталкиваетесь?

**Андрей Бородин:**
Я могу рассказать рассказать на примере исправление ошибки про reindex concurrently. Я постараюсь, чтобы это не стало лекцией на полтора часа. В Postgres можно перестроить индекс под нагрузкой. Ну то есть например там скопился bloat или просто вы хотите создать новый индекс под нагрузкой. Табличка меняется, вы не хотите, чтобы было много логов. Ну вы запускаете не create index, a create index concurrently. Берутся минимальное количество логов, но таблицу нужно просканировать два раза. Один раз прочитать, чтобы построить первичный индекс, потом индекс начинает обновляться, и второй раз прочитать таблицу, чтобы закачать изменения, которые пропустили в момент первого прогона индекса. Вот, и три года назад на одной из инсталляций появилось сообщение о том, что одна строчка не попал в индекс после построения индекса конкурентно. Потом два года назад снова появилось это сообщение. Год назад пришли люди из одного крупного сервиса, кажется это были Метаданные S3, и говорят, что у нас есть воспроизведение, но оно раз в квартал. Ну ладно, хорошо, я жду 3 месяца. И наконец, я смог поймать эту ошибку в декабре. Я понял, что там ошибка в логах. Я написал патч, и он вышел с обновлением 12.7, кажется, или 12.6. И летом люди из S3 снова пришли и сказали: “А там всё ещё есть баг, у нас есть снова воспроизведение, только теперь оно пореже, чем раз в квартал. И вот вчера мы обсуждали вместе c разработчиком тоже Postgres’a и поняли, в чём проблема. И вот сейчас сегодня писал весь день патч, чтобы эту проблему починить. Я надеюсь, что мы последний раз фиским эту проблему. 

**Даниил Баженов:**
Очень интересно отлаживать проблему, которая воспроизводится раз в квартал. 

**Андрей Бородин:**
И главное, у нас же тикеты оцениваются по стори пойнтам, то есть дни разработки, и там стоит два дня разработки на этом тикете,он создан 3 года назад при первом воспроизведении, я его иногда переношу в работу, иногда забываю, поэтому там суммарно аккумулировалось, не знаю, несколько месяцев разработки по этому тикету, а он оценен в два дня. Я думаю, что такое в других сферах тоже случается. 

**Даниил Баженов:**
Ну да, конечно. Немножко про инструменты. Какие любимые инструменты, что используете сейчас для отладки, поиска проблем? Ну именно о том, что в текущем именно использовании. 

**Андрей Бородин:**
Вообще до того, как я оказался в Postgres, я 10 лет занимался виндовой разработкой, и мне была близка Visual Studio. В Posgres’ном мире пришлось переехать на unix-like системы, поэтому я вот до сих пор 4года-5лет этим занимаюсь, до сих пор чувствую себя картонным, ненастоящим разработчиком-линуксоидом. Я умею пользоваться GDB, но так типа там посмотреть переменные, брейкпоинты поставить, но мудрых скриптов я не умею. Основной редактор кода у меня Visual Studio code, но просто там текст поправить,  больше ничего не случается, буквы набираешь, клавиши нажимешь... Вот. 

**Даниил Баженов:**
Клавиатуру используйте, да? Класс.

**Андрей Бородин:**
Да, у меня их две. 

**Даниил Баженов:**
Зачем вторая?

**Андрей Бородин:**
Вот такая, и еще на ноутбуке, чтобы с двух рук баги фиксить. И ещё я использую в последнее время code server. Это Visual Studio Code, только на удалённых виртуальных машинах. В последнее время мне нравится дебажить на виртуалках, не в контейнерах на ноутбуке. 

**Даниил Баженов:**
Понятно. Если говорить о каких-то новых тулзах, инструментах, которые может быть пробовали или хотите попробовать, или слышали где-то на митингах, или кто-то из ребят прям рассказал, что крутая штука.

**Андрей Бородин:**
Я пишу базу данных, которая старше меня. Она написана на языке С89, ANSI C, я тогда еще в садик не пошёл, когда этот стандарт был принят. Я использую утилиты, которые существовали тогда, когда я пошёл в школу. 

**Даниил Баженов:**
Поговорим о менеджменте тогда.

**Андрей Бородин:**
Не, есть одна вещь, где я люблю новые штуки. Это алгоритмы. Больше всего я хочу затащить в Postgres... В прошлом году, 20 год многим не понравился, но тем не менее изобрели Piecewise Geometric Model. 3 года назад Google выступил с такой интересной инициативой как learned indexes: давайте принесем немножко machine learning в базы данных. В базах данных все туго с machine learning, потому что классические алгоритмы в детерминированных задачах, хорошо поставленных, да, классические алгоритмы выигрывают у вот этих machine learning. Но наконец появился случай острие, так сказать, прогресса применить в базах данных. Но, к сожалению, learned indexes не поддерживали модель конкурентного доступа, не поддерживали обновления, и вообще это такой proof of concept был который, да, напоминает базу данных, но ты не база данных. В двадцатом году несколько итальянских исследователей выступили с идеей Piecewise Geometric Model, это приближение идеи learned indexes к реальности: давайте сделаем контейнер с ассоциативным поиском, который использует интерполяционный поиск, который похож на статистически обученные деревья. И вот такого плана вещи я постоянно использую. То есть я читаю про какие-нибудь там знаю новые Bloom фильтры, тоже недавно Facebook предложил, новые алгоритмы и структуры данных и прям прикольно. Я рад новому способу уложить байты в процессоры.

**Даниил Баженов:**
Хорошо. Если говорить о более простых вещах, какая самая распространенная ошибка,  которую совершают люди, которые работают или делать что-либо с базами данных?

**Андрей Бородин:**
Самая страшная ошибка, которую делают пользователи… Мы пишем облачный сервис, там легко создать базу, легко мониторить базу, легко бэкапить базу и  там очень легко базу удалить. Раз в месяц я наблюдаю инцидент, когда человек назвал свой кластер как-нибудь “ну какие-то данные”. Другой человек пришёл, что-то не хватает квоты, не хватает денег, ну или или по какой-то причине такой: “Ненужная база, терабайт, опа, delete!” Облака очень быстро удаляют базы. Это не совсем про эксплуатацию. Но вот я участвую в этих инцидентах. потому что я смотрю на то как система, моя система резервного копирования хорошо восстанавливает базу данных обратно. Самый главный смысл облачного сервиса, что мы не дадим пользователю потерять данные, мы не даем возможность там выключить VSyns, мы не даем возможность отключить point-in-time recovery, пользователь должен не просто удалить свои данные, он должен дождаться окончания окна восстановления. Ну вот такая ошибка, которая частая, и мы как-то её предотвращаем.

**Даниил Баженов:**
Я давно не пользовался Yandex.Cloud. И вчера буквально столкнулся на GitHub. Я не удалял репозитории давно, зашёл, надо было удалить, и они такие выделили ярко danger zone, там всё всё что связано с удалением: подумай три раза, стоит ли это тебе делать. У вас так же?
**Андрей Бородин:**
Да, показывается график request per second, и ты должен набрать название базы данных и ни в одном символе не ошибиться. Ты не можешь вставить его из clipboard. Но это грабли, которые закладываются заранее. Когда ты создаёшь базу данных, тебе надо дать ей осмысленное имя. Обычно творцы, разработчики, не знают сервиса, который они пишут, они создают будущее, сложно видеть будущее. И они не знают, как база данных будет называться, они называют ее База_данных_1. А потом не помнишь, что такое  База_данных_1. Недостаточно показывать 1000 RPS или 10 000 RPS на хосте. Кстати, еще одна особенность Яндекса. Очень большая часть нагрузки в Яндексе создаётся тестами, постоянно что-то где-то тестируется. Тестовой базы обычно нагружена вот так вот в полку, потому что хочешь знать когда они сломаются, они же тестовые, какая нагрузка их прибьет. Поэтому график нагрузки не всегда человека пугает Ну да, тут 10 kilo RPS, но в тестинге всегда так, это вот на проде у нас там еле-еле от нуля утилизация отрывается. Но если есть какие-то идеи, как отличить хорошо нужную базу от ненужной, то обязательно мне пишите. Я буду рад услышать это. 

**Даниил Баженов:**
Мне кажется, Вы сами предложили идею, это просто валидатор названий. Если кто-то что-то пытается создать со словом test, то ему надо говорить: “О'кей, это точно тест? Мы это убьём через неделю”. Вот, и всё остальное должна сверяться сверять со словарём Яндекса, что это что-то, что будет работать. 

**Андрей Бородин:**
В каком-то сервисе была база данных тестировщиков, которых они считали самыми лояльными пользователями, и они назвали ее... То есть там появилось слово testв названии. 

**Даниил Баженов:**
Я где-то кстати видел, в каком сервисе, он как раз не давал создавать вот этот бредовое название, говорил напиши что-то человекоподобное. Ладно. Об ошибках поговорили. Есть вот именно базы данных. Ты работаешь с реляционными базами данных. Даже в реляционных базах данных сейчас множество вариаций появляется. И форки MySQL, и форки PostgreSQL, и просто какие-то новые базы данных, и множество-множество баз данных, наверное замечаете это тоже. С чем, как думаешь, это связано, что заставляет людей пробовать новое?

**Андрей Бородин:**
Мой ответ здесь такой, что база данных - это нерешенная проблема. К сожалению, пока что базы данных не справляются. Все, что мы сделали, мы как человечество, до до сих пор даже близко не идеально. Смотрите, с машинами та же, история машины появляются постоянно новые, у них появляются какие-то новые системы безопасности. 20 лет назад никто не знал, что такое система курсовой устойчивости. Сейчас в России запрещено продавать новые автомобили без системы курсовой устойчивости. Автомобили по-прежнему неидеальные, по-прежнему люди страдают от эксплуатации, по-прежнему гайки отваливаются, вытекает весь бензин, и пользователь такой: “Почему она не едет? Заводись!” А она не едет. Вот с базами данных та же самая история. Нет просто сервиса, который просто бы работал, в понятных идиомах, с понятными гарантиями. База данных по-прежнему черный ящик с 1000 ручек. Даже если у вас там Kuber оператор или есть волшебный DBA, где-то происходит какая-то магия, кто-то должен дёргать за ниточки, чтобы вот всё правильно летело. База данных будут лучше. Можно привести примеры, как электричество. Раньше можно было получать электричество у разных провайдеров, это мог быть постоянный ток, это мог быть переменный ток, это могло быть многофазное электричество. Сейчас у вас есть розетка, вы в нее втыкаете что хотите и не думаете о том, что надо какие-то контракты продлить, какое-то сервисное обслуживание. Электричество - решённая проблема, базы данных пока нет. База данных будут развиваться, к сожалению, еще довольно долго. 

**Даниил Баженов:**
Отлично. К счастью, наверное. Если мы работаем с базами данных, то наверное к нашему счастью. 

**Андрей Бородин:**
Мы бы нашли  другую работу. Но это действительно то место, где можно приложить усилия и сдвинуть человечество в правильном направлении. Или в неправильном. Но тут зависит от усилия.

**Даниил Баженов:**
Я вот со своей например колокольни... О'кей, я, например, долго работаю MySQL, потом ладно, устал, новый проект можно попробовать там PostreSQL, маленький совсем проект можно там поставить Mongo, и просто писать в ряд, и всё прекрасно работает. Когда база данных появилась год назад, там заходишь смотришь, что у неё топовые клиенты, реализация... Я просто не совсем понимаю, как это появляется, поэтому спрашиваю. Нет, я возможно понимаю, как это появляется, потому что наблюдаю это часто, но просто интересно ещё не со стороны. Что бы тебя заставило, вот ты создаешь новый проект, такой вот топ 5 баз данных убираю, хочу вот на вот этом.

**Андрей Бородин:**
Потому что в старых базах данных есть известные ограничения. Ограничение, например, того же Postres или MySQL, довольно понятное, это, во-первых, неполная сереализуемость транзакций, которые стоят там космически дорого. То есть serializable или более высокие уровни strick serializable, они действительно роняют производительность в Postres или MySQL. Вот, и другая, более реальная проблема, это то, что сервис не может вырасти за, условно, 10 терабайт. Не работает Postres или MySQL за 10 терабайт. Вот эти две проблемы надо решить. Кто первый решит, тот молодец.

**Даниил Баженов:**
Вы делаете очень много вклада в оpen source, было много примеров вашей презентации на Percona Live. Я сталкивался с проблемой на работе, когда, например, человек хочет делать вклад в оpen source, ему не позволяют это делать как-то с организационным планом. Я бы хотел узнать, как у вас тут организован процесс, то есть но вы пишите свои какие-то патчи для себя, а тут надо например сделать вклад в какой-то сторонний проект, WAL-G, да, то есть вас это прямо вот всё гладко организовано на уровне компании. 

**Андрей Бородин:**
Не, у нас анархия.

**Даниил Баженов:**
Ну просто расскажи, как это происходит. У меня, например, когда я занимался разработкой, если я пришёл бы к менеджеру и сказал, я тут вместо того чтобы написать какую-то фичу из нашего бэклога, хочу баг пофиксить в стороннем продукте вместо того чтобы затыркать их менеджера, мне бы сказали: “Давай подождём”. 

**Андрей Бородин:**
Есть много случаев, когда кроме нас кажется, что никто не будет развивать. Ну то есть, например, сейчас сжатие в протоколе Postgres развивается разработчикам Яндекса и одним из разработчиков Postgres Professional. И кажется, что есть ещё там 2 человек в мире, Justin Freesby, не помню, где он работает, и ещё кто-то тоже проявлял интерес. И вот четыре человека собрались и что ты делают. И очевидно, что Яндексу это точно надо.  Стоимость эксплуатации у нас складывается из междудатацентрового трафика, нам точно надо трафик сжимать, и с другой стороны есть понимание, что один человек, который надо там работает с нашей стороны, он точно будет там полезен, он не будет там топтаться, он что-то будет продвигать вперед. Поэтому вот Даниил этим занимается. Процесса принятия решений у нас нет, потому что, на самом деле, все случаи исключительные. В Яндексе часто говорят: “Используйте голову”. Это такая общая рекомендация, которая ничего не говорит, что конкретно надо делать, то есть как использовать: по клавиатуре или думать. В первую очередь, мы конечно расследуем инциденты и есть политика не политика, что всё что связано с инцидентами, всё что аффектило пользователей, мы должны починить. Если кто-то не смог отправить письмо по причине того, что у нас есть ошибка в connection pooler, мы должны её починить. То есть как это ошибка всё равно попадает в наш бэклог. И вот два основных пути попадания в бэклог, это что-то, что сэкономит нам много денег, либо что-то, что привело downtime, что какой-то сервис полежал. Дальше просто стандартный процесс, выбираем самое критичное - делаем. 

**Даниил Баженов:**
Понял, спасибо. У вас в принципе это норма, это хорошо, очень круто. 

**Андрей Бородин:**
У меня подразделение называется Pазработка открытых баз данных, то есть мы ничего другого почти не делаем.

**Даниил Баженов:**
У вас большая команда?

**Андрей Бородин:**
Сейчас 6 человек, включая меня, и Юра Фролов у нас сейчас стажер, еще 4 инженера которые full-time контрибьютят в Postgres, Greenplum, куда-то ещё. Есть в Москве человек который дорабатывает небольшие проблемы, связанные с MySQL 5.7, но он не в моём подразделении, он в подразделении Димы. Там сертификаты не обновляются. MySQL 5.7 не умеет обновлять TLS-сертификаты, и на каждом классе этого делать раз в год, но у нас несколько тысяч кластеров, каждый день добавляется десяток хостов, которым нужно обновить TLS-сертификаты. Мониторинг загорается раз в 2 недели, и вот раз в 2 недели дежурные страдают с тем, что нужно оповестить всех пользователей, о том что MySQL 5.7 будет перезапущен. Поэтому нам нужно сейчас вот сделать… Код уже написали, нужно выкатить только сборку с перезагрузкой TLS-сертификата без обрыва существующих соединений. Не помню, почему это рассказывал... А, сколько нас, что есть не только в моем подразделении разработчики. Да. 

**Даниил Баженов:**
Мы поговорили о том чем ты занимаешься, что бы хотел увидеть в будущем, machine learning. И тоже интересно опять же, что будет дальше, что изменится именно в том, с чём работаете? Какие интересные штуки, технологии появятся в ближайшие пару лет, что ожидать?

**Андрей Бородин:**
Одной из точек роста таких технологий управления данными в мире сейчас является идея того, что раньше базы данных писали на диск. Одна из моих любимых баз данных MangaDB, не MongoDB, пишет вообще в pipe, но это отдельная история. Идея того, что можно писать в масштабируемый сетевой сервис фактически была создана в в продукте Amazon Aurora, и очень многие разработчики недавно осознали, что Amazon Aurora вышла на revenue в несколько миллиардов долларов в год. Сейчас стали создавать системы управления данными, которые основаны не на том, что  мы пишем на локальный жёсткий диск (ну не на локальная NVMe диск, не на локальный SSD диск), а пишем некоторый сервис, который предоставляет API по управлению данными. Не SQL-ныц, а более простой протокол типа хранение страницы данных, и я думаю, что в ближайшие два года мы увидим Amazon Aurora в open source. Мы увидим базы данных, которые живут поверх, которые разделяют compute и storage, разделяют вычислительную часть и хранение данных. Сейчас наверное таким передовым стартапом на эту тему является Зенит, они пишут для Postgres. Я уверен, что есть аналоги и в мире MySQL тоже. Я иногда смотрю, они разрабатываются на GitHub, я подписана их лог коммитов, и я смотрю, что у них инженерная мысль иногда метается в одну сторону, иногда метается в другую сторону, но в целом они идут по пути отказа от гарантии дисков, вот этих вот файловых систем, да, что у нас данные отправляются в некоторый сервис который уже шардированный, которые уже дешёвый, которые уже эффективный, и latency обеспечивается за счет хорошего кеширования локального в буфере, но не на диске.

**Даниил Баженов:**
Круто. Предлагаю заканчивать, мы круто по-моему поговорили. Большое спасибо за эту встречу, за эту запись. Всех приглашаю на наш коммьюнити веб-сайт percona.community, где можно найти все подкасты, записи, также у нас есть Youtube канал Percona, где можно найти в том числе доклад Андрея на Percona Live и будет опубликован этот подкаст. Всем спасибо! Большое спасибо, Андрей.

