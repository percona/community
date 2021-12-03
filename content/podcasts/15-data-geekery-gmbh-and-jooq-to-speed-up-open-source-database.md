---
title: "Data Geekery GmbH and JooQ to speed up open source database - Percona Podcast 15"
description: "The HOSS (Matt Yonkovit) sat down with Lukas to discuss ORM’s like Hibernate and how JooQ is different."
short_text: "Lukas Eder is the CEO and founder of Data Geekery GmbH, the company behind JooQ an open source Java framework that gives you an API that allows you to write SQL statements through natural Java api calls. The HOSS (Matt Yonkovit) sat down with Lukas to discuss ORM’s like Hibernate and how JooQ is different. We also talk about how speed is important and how JooQ can help speed up database applications."
date: "2021-03-30"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-_-ep-15-with-lukas-eder-ceo-and-founder-of-data-geekery-gmbh/"
youtube_id: "hPAJ92DGfNk"
speakers:
  - lukas_eder
aliases:
    - "/podcasts/15/"
url: "/podcasts/15-data-geekery-gmbh-and-jooq-to-speed-up-open-source-database"
---

 ## Transcript
 
**Matt Yonkovit:**  
Everybody, Matt, you're going to head over to our strategy here at Percona with another episode of The HOSS (that's me) Talks FOSS, yes, we're here to give you the best in the open-source space. Today, we've got an extra special episode. So we love it that you've tuned in to watch. So I'm here with Lucas Eder, the founder and CEO of JooQ. Hi, Lucas, how are you doing today?

**Lucas Eder:**
Great, how are you doing? 

**Matt Yonkovit:**  
Great, wonderful. So I saw your framework out there and was really intrigued. And I know that as a DBA, as someone who's come from the database background, I always had to deal with problem queries, I always had to deal with applications that were of concern. And a lot of times the problem ended up being the ORM. And a lot of times, it ended up being hibernate. And so I'm sure that you've experienced that as well. Because what can I do, you can quote me on that all you want. You know, it's so I've noticed that hibernate and RMS like Ruby and Rails and other ORM tend to have problems generating an efficient query. And so that's why JooQ was so interesting. So maybe you can tell us a little bit about JooQ, I'm sure that a lot of people that I work with, that I deal with would be very interested in what JooQ is and how it works.

**Lucas Eder:**
Yeah, excellent. So a JooQ is an alternative. So essentially, what it really does is, it's an internal domain-specific language that models the SQL language As a language inside of Java. So you can use the Java compiler to type-check your SQL queries, instead of having it externally to Java. So alternatives that used to exist before were like JDBC. With JDBC, you have just strings, you can pass around. There are other utilities like my bat is and other libraries, but JooQ really models the entire SQL language as a Java API, and it has a code generator that generates your database schema. So that means whenever you rename something, your new queries won't compile. Just like when you have us inside of your database, you have dynamic SQL in JooQ, that's what JooQ does. It's not really rocket science, it's just merely an internal diesel, which exists in a lot of languages, but I think Job is the most sophisticated that has ever been created and of this kind. So JooQ is been around for 12 years now, and now supports about 25, relational database, dialects, and a lot of features of all the different vendors. 

**Matt Yonkovit:**  
And what I really saw interesting was, you have the capability to really refine the SQL code itself. You know, with Hibernate, there's, there's a limited amount of options that you have. And it looks like you have a lot more capabilities to build deeper, richer SQL statements and really get into a lot more fine-grained detail.

**Lucas Eder:**
So the idea of JooQ is you actually want to write SQL, but you want to write SQL in Java. And you don't want to have it external to Java, but internal to Java. So but you want to write exactly what do you know, what do you like, an inner join, outer join, whatever kind of union, whatever kind of operator lateral join, or something really fancy like JSON or XML nested in SQL, and you want to write exactly that. And JooQ will help you write exactly that. But by removing all the, I'd say, ugly parts of SQL, so don't the ugly parts of SQL are the syntax is kind of weird. So it's not a very modern syntax. It's not very composable. So if you want to have dynamic SQL, for instance, and it's a frequent requirement, where you have a subquery that you only want to join under certain conditions, this is super easy with JooQ, you will never run into any syntax errors. Because you forgot that in this database product, you have to add parentheses around this subquery or you have to name your derive table x or y or whatever, JooQ handle all of these little things but give you all the strength of SQL at the same time without hiding it. So that's the main difference. 

**Matt Yonkovit:** 
Yeah, that's fair. 

**Lucas Eder:**
Yeah, thanks. Oh, he said hibernate generates bad SQL at times. I don't think that hibernate actually does that. Hibernate generates good SQL. But the difficulty is, it doesn't give you the control, JooQ does, for instance, so if you will know exactly, I want to have this kind of query and I need these five tables here. And it was hibernated, sometimes it's difficult to foresee what kind of joins are going to be produced. Obviously, with experience you can foresee that. But let's say a junior developer might not know this, and maybe the code already shipped to production, you haven't noticed that you're joining too much, or too little or whatever. And the queries will do the correct thing but maybe not efficient, and will JooQ from the beginning you actually have to design your queries. 

**Matt Yonkovit:** 
Right and with JooQ and the difference between hibernate and JooQ some programmes a lot of RMS, you'll define the schema as the classes and then it will build the database and the schema in the back end. For you. Yeah, it's bring your schema to JooQ, right?

**Lucas Eder:**
Exactly. So the idea of JooQ is, the fact that you're using Java is maybe temporary even. So maybe tomorrow or in a year or two, you want to use JavaScript or whatever, but your database will state. So I'm with this background, I'm a very SQL-oriented person, a very relational oriented person, as they used to have a lot of people in the 90s. But as it's a bit rarer today, um, but from experience, I really think data has mass. So I'm quoting.. I forgot who said by Oracle, but data has mass. So data actually sits there and is inert. And your application can move very quickly, you can redesign your application very quickly, but you're not going to redesign the database very quickly. So chances are that a legacy system has a schema that will not change easily. And you want to have the schema as the source of truth, not your Java code. So it's a different mindset. For instance, when you want to prototype stuff, having Java code as the source of truth or whatever in the client, might be faster in the prototyping phase. But even when you're using JPA, I think you want to switch to the database first approach at some point, because that stuff is going to stay and maybe or your client design might change. Nothing would happen frequently in my jobs is maybe you have a Java client and the Python client or whatever, for some scripting. And you don't want to you don't want to work with a schema that is not nicely designed with DDL. 

**Matt Yonkovit:** 
Yeah, and I think that the query design and schema design is actually becoming more and more a lost art, which is a shame because that's where you can get a lot more performance and scalability with your application. 

**Lucas Eder:**
Absolutely. It's absolutely. And so I've noticed this when I did SQL training, so I used to have only training about SQL language features like window functions and performance. And then I added a third day of training about normalisation, I thought no one was gonna buy that, because everyone already knows, right? This is old stuff, maybe some junior developers might be interested. But you'd be surprised how many people actually wanted to learn or relearn how to properly normalise schema, how to get the third normal form. This is, as you say, it's the last art. 

**Matt Yonkovit:** 
And that's a shame because where I have seen the most performance benefit, the most scalability, the most security actually, is in that designing of the schema and designing of the actual database architecture. But now we've moved into this phase where everything is cloud-oriented database, as a service, everybody wants it easy, as easy as they can get it. And that's great, except people start to lose those skills. And the funny thing is when you start to lose those skills, your databases become bigger, they become less flexible. And as that happens, you spend more money because now all of a sudden, like your tables are 10 times the size. And in the cloud, you pay per gigabyte and everything else. 

**Lucas Eder:**
So it's kind of a crazy time you have to migrate your data, you have a lot more complex migrations, instead of just adding and dropping a little bit of data. Yeah, so you have even, right, yeah, more data transfer as well. 

**Matt Yonkovit:** 
Yeah, it's it's a slippery slope there. It really is. Now, now JooQ you know, it is a fully supported product, it's open-source, so anybody can go download it today. And if they need help like you, you have a model that offers support for folks who are looking for help as well, correct?

**Lucas Eder:**
Yeah, so there's community support on Stack Overflow, or GitHub, which is free of charge. But, of course, no guarantees. And paying customers, regardless of the database product they're using, if they're paying customers to get premium support, by email directly. So usually, people don't actually need support for JooQ because it's just SQL. So it's kind of a goal is it's really straightforward. If you know SQL do but obviously we help people get their SQL queries right all the time. So that still happens. So you do like a lot of the support, you get SQL help. Yeah, but it's not a very support intensive product. I'd say. From the beginning, I've tried to focus my marketing on people who actually appreciate SQL. So I never, I did some some ranting about JPA in the past, how JooQ is better and blah, blah, but I think I've grown past kind of marketing and I'm not marketing JooQ for an advertising job as a good product for people who like an ORM I mean if you want to work with your objects and your object graph, then please use an ORM. But if you want to work with SQL, I think then JooQ is going to be a good solution. And those people already know a lot of SQL and they will find JooQ just perfect for them because it listens to exactly what they want. But an in a more type-safe way. So it's not really a support business, like other open-source businesses, which is kind of mean right? So to make money, we actually have to have commercial licences, I think because it's such a great product.

**Matt Yonkovit:** 
Okay. And what licence is this released under right now?

**Lucas Eder:**
So the open-source edition is Apache 2.0. 

**Matt Yonkovit:** 
Okay, so it's very permissive. I know a lot of people right now are moving, exploring the different licences. So having a permissive licence, in my opinion, works out in your favour, because you'll get more people to adopt. Are you seeing a lot of adoption so far in a lot of enterprises? Is that is that a space that has started to take notice?

**Lucas Eder:** 
Yes, of course, I don't know who is using the open-source edition. They obviously don't tell me but the paying customers, they're from all sorts of companies, including fortune hundreds. And I think JooQ is being used everywhere. But now. So I've seen different, different surveys in the past, like five years ago, I think JooQ had about between four and 6% market share compared to Hibernate, which has maybe 40 or 50, some market share for JDBC, pure JDBC applications. And from my download and customer statistics that has grown, I haven't seen another survey that actually checked on SQL frameworks, because it's done a bit out of fashion to ask about that. So these surveys typically ask about cloud and this kind, but I think the market share should be around seven 8%. Now, so it's quite big. Everyone who is really into this topic is using JooQ. There's hardly any alternative in this domain. So in this niche. 

**Matt Yonkovit:** 
So in your experience, and you've done SQL coding for a long time, and you've helped people design things you've given training, what would you say is the number one problem that developers continually fall into, when trying to build their databases and design their applications when it comes to SQL?

**Lucas Eder:** 
I think the number one problem is to not version control their database from the beginning. So they want to just try around a little bit and add some table here and some table there. And before they know it, they go live was with some great table scripts. And it's a complete mess. So they don't think about how to increment their database schema. So if you have to do that, after the fact, it's much harder to get it right. So I think number one problem for developers is to from the beginning, use something like Liquibase, or Flyway or whatever tool helps you be very diligent and very careful about your database schema design, of course, as we discussed earlier, but also evolution. So the database schema evolution is one of the still, I think, unsolved problems. So flyway offers a lot of simple tooling to just get the database increment scripts in the right order, but it's just very script-based. So you can do everything the database can do. But it's script based, you have to do everything manually. Liquibase offers a little bit more help with the XML or YAML, or JSON format, I think, what they're doing, and so you have some abstraction over the dialect and syntax and maybe a little bit easier to manage. But you have to do a lot of stuff manually. I think there's still room for a new vendor to solve problems in this area. But even if that if that's not available yet, you should, you should think about how to properly increment your database changes and version control them. So it's really weird that we were using version control for all languages, but not for SQL. That I kind of don't understand that right? 

**Matt Yonkovit:** 
Yeah, this is true. And I think this has driven a lot of people over to the no SQL camp where their claim is, oh, it's schema less. Until you run into performance problems and scalability issues, then all of a sudden, the first thing is, oh, well, you didn't design the schema properly.

**Lucas Eder:** 
Yeah, and it's not schema less at all. I mean, I tend to not use that term. It's very misleading. I tend to distinguish between the schema on write which is like relational databases, where you have schema enforcement when you write to the database, whereas no SQL databases are often schema on read, you have a schema? It's just discovered when you read the database, right? But there it is, you get the schema, and they discovered it on the fly. So I think it's better to to enforce it when you write so you know exactly what's in the database. But yeah, that's just us, right? Yeah, we know these things. We have to share these things. But of course, again, it makes it harder to prototype and to, I mean, if you want to move fast at the beginning of a project, getting this part, right is the hardest part, because you have to do a lot more upfront work, then if you have something like a NoSQL database, we can just dump everything into a box and then throw it away, and then dump it into the next box as you evolve your product before you go live. But again, if you start planning for your schema evolution from the beginning, then this is not going to be a problem in the long run. 

**Matt Yonkovit:** 
Okay, great. And if people want to help with JooQ, and they want to either contribute, provide open up bugs how do they get involved in the community?

**Lucas Eder:** 
The best way is on GitHub for box or the mailing list for questions. So it's not much of an open source project in the classical sense, where there's a lot of contributors. So contributors are usually people who report bugs, of course, we always appreciate that. But for instance, the tests are not open source. So you can't just make a pull request and run our integration test and see if you're still doing it right. That's part of the business model to not open source the test, kind of like SQLite does, I don't know, have you seen that. But SQLite has some tests open and some tests closed, which helps wretchedly keep control over the intellectual property. So we don't have to test open-source. So this is this means a lot of people don't actually contribute code. The other reason is, I actively discouraged contributing code because I think the way GitHub handles this is hardly ever the right way. Everyone could just dump some code on GitHub and ask the maintainers to please merge that. And it's a lot of work. And contributors usually don't actually know the roadmap, don't know how feature x interacts with feature y. And they're actually not skilled enough to to do that work. And that's the best way usually not to contribute code, but you can contribute ideas to contribute use cases, to documents have to say, Okay, this is a cloche, how can I do this better? Actually, just ordinary customer support cases are the way we like to receive contributions in the best way. I think that's the best way to interact. 

**Matt Yonkovit:** 
Honestly, what I've seen is the best contributions to most open source projects end up being feedback like the testing the documentation on how to use it, educational materials, things like that.

**Lucas Eder:** 
Absolutely. And you can even host that yourself. I mean, if you write blog posts, I mean, that's very helpful. It's your point of view. It's your different angle and a different perspective on the product that a vendor would never write this way, and maybe very helpful for someone else. 

**Matt Yonkovit:** 
Well, Lucas, thank you for joining me today. I appreciate your taking a little bit of your time to explain JooQ and where it's at. I really enjoyed our conversation here. And I appreciate you coming on.

Wow, what a great episode that was! We really appreciate you coming in and checking it out. We hope that you love open source as much as we do. If you like this video, go ahead and subscribe to us on the YouTube channel. Follow us on Facebook, Twitter, Instagram and LinkedIn. And of course, tune into next week's episode. We really appreciate you coming and talking open-source with us.



