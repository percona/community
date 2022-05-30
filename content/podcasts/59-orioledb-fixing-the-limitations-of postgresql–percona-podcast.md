---
title: "OrioleDB: Fixing the Limitations of PostgreSQL - Percona Podcast #59 /w Alexander Korotkov, Founder & CEO at OrioleDB"
description: "Alexander Korotkov walks us through the evolution of some of contributions before talking about his work to re-architect some of the PostgreSQL core. Learn more about OrioleDB and what makes it different"
short_text: "The HOSS Talks FOSS podcast welcomes Alexander Korotkov, Founder & CEO at OrioleDB. Alexander is a major contributor and committer in the PostgreSQL Global Development Group. With more than 10 years of experience and a ton of features under his belt he knows more about the early days in Postgres then most.  He walks us through the evolution of some of contributions before talking about his work to re-architect some of the PostgreSQL core. Learn more about OrioleDB and what makes it different. Those interested in learning more about the work, check out OrioleDB’s Github webpage https://github.com/orioledb"
date: "2022-04-28"
podbean_link: "https://percona.podbean.com/e/orioledb-fixing-the-limitations-of-postgresql-percona-podcast-58-w-alexander-korotkov-founder-ceo-at-orioledb/"
youtube_id: "wu3YRhJ8U0s"
speakers:
  - alexander_korotkov
  - matt_yonkovit
aliases:
    - "/podcasts/orioledb-fixing-the-limitations-of-postgresqlpercona-podcast58/"
---

## Transcript
**Matt Yonkovit:**  
Hi everybody, welcome to another HOSS talks FOSS. I'm the HOSS, the head of open source strategy at Percona Matt Yonkovit. Today, I am joined by Alexander Korotkov. And we're here to talk about some of the things that he's done in the PostgreSQL space and in his career, how are you this morning, Alexander?

**Alexander Korotkov:**  
I'm good. How are you?

**Matt Yonkovit**
I'm very well; I'm very well. So you have a long history in Postgres in the open-source space? How did you get started in open source and, and Postgres specifically?

**Alexander Korotkov:**  
Yes, I started with Postgres more than ten years ago. I have explored the functionality of Postgres. And there is a country model, which provides Levenshtein distance or function, which is a number of edits in operation to transform one stink into another. And that time is that version; the implementation was gonna didn't support multibyte encodings properly. So it just compares strings, wide per byte. Right. And that didn't work well, are all the characters. And I explored the code, and I found this is quite easy to fix. And that was my first patch to the hacker's mailing list. And then I also found that we can do some optimizations for this function. And that's as it was, basically my second patch, and starting from my first contribution. I have faced it with high requirements, a high level of requirements the coding from the community. So, I remember my patch was to be reviewed by Tahira, and Robert Hass and these have to do any analysis of the performance of good support of multibyte encoding, make the function slower, and so on. Yes, this is how I get involved. And then I get involved in indexing stuff because that was my field of interest during my Ph.D. studentship. And I wrote some patches to improve split functions for geospatial indexes and so on. This is how I did involve in Postgres.

**Matt Yonkovit:**  
Yeah. And so your early work was still on performance. And it was focused on making things faster in a few different things. And I know that you've also done some work on different indexing is the indexing that you're talking about the Vgram indexing that you were looking at early on?

**Alexander Korotkov:**  
Yes, yes. Yes. Vgram indexing. Yes. It's one of my earlier early extensions.

**Matt Yonkovit:**  
Okay. So as you started to look at those early things, started to see patterns around things that needed to get fixed. And maybe tell us about where your current passion kind of came from which, right now, you're very focused on that the core of the database and some of the limitations that have been there since you got started even?

**Alexander Korotkov:**  
Yes, probably my base to these problems started even before contribution progress, because when I start, just started getting involved in the database, when I read regarding relational theory and SQL, my first question was, how does the database perform? When there are many roles? Right? So if, for instance, you have a table, your query works fast, when there are 1000 rows, but what if there are a million rows? And millions of rows? And how, how much performance is? How much is performance degradation there? No, but it's, it's nice to keep performance degradation and some constraints. It's not okay if your time if your query latency increases linearly with data volume. It would be not OK. And, and so I learned about indexes, I was aware that there are some in-memory data structures like so binary tree hash and so on. But I have learned that there are special data structures for external memory, like B plus tree, implemented Postgres. And so on, but when I started to use Postgres, it probably was Postgres 7.4. So it was quite early, an early version. And, and vacuum, there was an issue item, that person probably already had after vacuum. But it was even not as good as now. This is why I started to think about MVCC. I'm an engineer who is a researcher, everything. Everything I get into the fence, like in my childhood, I, when I get a toy car, and I try to disassemble it, and explore each part, try to assemble it back, and so on. And MVCC was a mechanism was, which caught my eye from the beginning because it's when you just work at a skill level. It's just like magic. Okay, so you can, you can do things concurrently, but you still looking for a consistent snapshot when you observed it the first time. It's magic as a human. It's nonblocking.

**Matt Yonkovit:**  
Yep, yes. Yeah. Oh, in those early days with vacuum and those who are listening who don't quite know the method behind this, data in Postgres is marked for deletion. But the data is still there, and the vacuum process comes back and cleans it up. And the early days, that was a very, very disruptive process that slowed things down. So it would definitely block and lock things quite a bit.

**Alexander Korotkov:**  
Yes, yes. Yes, that's it. And I already and already early days, I have started to think about what are possible design decisions? Because it's not only marking all the role versions as deleted , but now the issues that arose are identified. Right. And if you update some, if you update some row, you have a new version, and you have to insert into every index to make new index entries, which refers to new teeth. And this was no, that's a significant slowdown. And I have started to think about it long before. Long before Uber posted about ratification and so on, as I started about that, that we could, that if you have some role identifier even changed, due to update, then we don't have to insert to every index, but we probably should do immediate, delete, for an old or older version of modified the index. And then I started to think, about these design issues, how we can design it differently, and what consequences do we have? So it's like properties, where you can pick some of them , and you can pick every, every flow from them. So you can try to combine and find the best possible combination, the best possible combination for a typical workload, so there is no combination which would be perfect for every workload is the clearly impossible due to the theory of optimization and so on, and so far, but what would be the best combination for, for workload for typical workload, because Postgres was what, for instance, Postgres in BCC was never designed from scratch, the initial version of Postgres from Berkeley, has an innovative concept of heap innovative time I like, in the late 90s and early 80s.

**Matt Yonkovit:**  
A lot of that, in a lot of that same early philosophy, has been kept in Postgres, correct?

**Alexander Korotkov:**  
Yes, yes. Its early, early philosophy is that heap append-only structure. So you always have all the history of changes. You can do time travel, and so on. And, thanks it's append-only it doesn't meet the right lock. Because it's, you don't do any modification of old data on append. So it's like the lock, by itself. And index doesn't need recovery science, you can lose them on a system crash and just rebuild was that was the original Postgres concept. That appears to be not very practical for technical use cases, right. So not every database can keep all the history of changes, right, you see, obviously, right and the to rebuild every index on system crash, this is also not a good option. And this is why in early Postgres open source work, all of this was redesigned. But the concept of append-only heap becomes a concept of MVCC. So it wasn't its start to don't be able to give you time travel for arbitrary to go so far in the past , but to provide you MVCC. And in order to keep a heap into some no restrictions, it becomes not append-only, but a vacuum, start cleaning some gaps in a heap and the gaps were fueled by new tuples. That was how it transformed. But it's happened like, a little bit accidentally. It was the initial design, and it didn't work well. And it was fixed in a most straightforward way. That's, that's what's happened.

**Matt Yonkovit:**  
Well, I think in a lot of cases, whether it's a database or a piece of technology, starting off a project, there are certain things that work because of the size of the database or the size of the user base, it works, okay. But then as things start to escalate, and get larger and larger, then you start to expose the limitations of that design. In the case of Postgres, when you were back in the Postgres 7 days hundreds of gigs might have been like, oh, my gosh, that's a very large database. Now, you're talking potentially terabytes to petabytes of data, and the scale of the problem becomes a magnitude worse. So when you do have to go back and clean up the holes, it's different to clean up the holes on a system that's 1020 gigs than it is 100 terabytes. And I think that's, that's one of those things that early designs, you can get away with keeping things in the background and keeping things simple, and just making adjustments on top, but then over time, that just becomes less tenable.

**Alexander Korotkov:**  
Yes, yes. And also, in early design, you should keep in mind that Postgres was a research project by work and research project, it's not only valuable to get some solution, which would be best in practice, but for a research project, it's valuable just to do things differently, and achieve some different results. That doesn't always have to be practical, yes. Just, it could just improve our vision, and so on. So it's a little bit different goals for research and for industry, but for Postgres is quite a unique way. So not unique, but not so frequent way when something which was started as a research and the same code base, not just the same ideas, but the same code base gets improved into a very popular industrial product. That's a case of Postgres.

**Matt Yonkovit:**  
And yeah, Postgres has been popular for years and years now, and it is making its way into the enterprise. Why haven't some of these design issues been fixed before now? Any ideas? Or any thoughts on that? Why have some of the limitations that exist in things that could be optimized haven't been redone?

**Alexander Korotkov:**  
I think it's because there is an image it's a network of design decisions, with interrelations. And if you want to pick another decision, in one point, it affects other design decisions in another field, because it has many, many connections. And at the end of the day, you have to redesign the whole network.

**Matt Yonkovit:**  
Yeah. It's like a piece of cloth , and you pull a thread and the thread just keeps on coming undone for the rest of the whole thing. And it's just a lot of additional work because it's not easy to fix those things. I got it. Okay, that makes

**Alexander Korotkov:**  
Yes. And I think that issue is that there was no desperate enough person to do this.

**Matt Yonkovit:**  
Well, everybody likes performance. Right. So I mean, I don't know if it's desperation. But I think that yeah, I understand if it's working, it's sometimes better just to leave things alone until it's a problem.

**Alexander Korotkov:**  
Not everybody likes performance. But what people are trying to do is just to try to pick some design decisions, one of them, and even if it's a little bit, even, it's a conflict with others, try to insert some notes to make it possible. But to redesigning the whole network require some inspiration. I think.

**Matt Yonkovit:**  
Now, what so what you've been working on now, with OrioleDB is a way to fix some of those limitations. Is it an extension?

**Alexander Korotkov:**  
Yes, yes, yes, it's correct. But it requires some, patches to improve the Postgres system's ability to add some missing hooks, and it becomes too possible in an extension, but it's a little bit tricky. Extension, which duplicates some, is no duplicate but provides. Don't reuse this. Many Postgres subsystems. For instance. What if we have currently table access method API its returns souls that it expects that your implementation would likely use Postgres buffer manager that it will implement, or at the hip login at the block level, it is also intended that you will use existing index access methods with the API and so on so many, actually, there are many, many restrictions, what OrioleDB does, patches, which. This brings more work, which you can do on the extension side. So it extends the table access method API, so that you can deal with indexes on your side. So you don't realize the Postgres executor for that. And it removes the constraints that you should use the double identifier to identify the double versions, and so on. And that's why OrioleDB does things very differently from Postgre's built-in engine. Okay, what's your question?

**Matt Yonkovit:**  
So OrioleDB right now, is it still in a pre-production state? So you would call it more of a beta or an alpha? What's the state of it? Because I know that the code is up on GitHub.

**Alexander Korotkov:**  
Yes, the code is on GitHub. But yes, it's not for production. Yeah. Yeah, I talked about attracting some interest to the project. We are attracting some testing. And we encouraged people to sponsor this. Yes, but it's not yet in production. Yeah, fixing this if you have some issues, right now. Okay. Okay.

**Matt Yonkovit:**  
So with something like that work that you're doing, part of the challenge with any sort of performance testing, but especially in something that is trying to rewrite some of that core storage engine type functionality is testing at scale and testing with large datasets with large workloads, what sort of tools and how are you doing that testing? Because that's often difficult to get something that tests at scale

**Alexander Korotkov:**  
I think I don't have something special in this field. So we were keeping in touch with users from the early, very early stage of development. And we got some feedback from them. Ask them to test the early OrioleDB version on their workload, as it is one aspect. And another aspect is user two, we did a lot of benchmarking on one artificial, artificial data to check some particle engine issues and compare it to positive so no, there is no silver bullet in this, I think. So there are multiple options, and multiple things you can do, and the more you do in this field, the better results you'll have.

**Matt Yonkovit:**  
Yeah, I think it's one of the more difficult things when you're developing or enhancing databases, especially under the hood, is certain workloads can perform well, or better, and other workloads perform not so well, depending on the changes you make. And it's interesting, the trade-offs that people end up making because we see a lot of new, Postgres compatible technologies that are evolving and showing up in the ecosystem. But sometimes they only work for a certain type of query workload or work best with certain conditions. So it's, it's often difficult to find a happy medium to solve as many general workloads as possible. And so that's why I was asking about testing. That's it. Yes.

**Alexander Korotkov:**  
This is actually a reason for alpha release. Yes, we encourage people to try OrioleDB for their workload and share feedback. Yeah, yeah. Because if you're in some if you're dealing with small wins in some small system, I don't know, if you walk in just with your thoughts of sorts of your colleagues, and few beta customers you're kind of limited. If you are open to the world, if you will do an open-source release, then people can come and give you more, more feedback. So it's probably there are some workloads we didn't have in mind. Right? Probably, we can already handle it better. And probably we can, there are some things we can do easily to improve some workload. So-called low-hanging fruits. We didn't think about it. But also, there could be some workload, which we handled worse, and we didn't think about it. So to better understand the niche for OrioleDB, we are relying on feedback from the community. So the community of users.

**Matt Yonkovit:**  
Okay, okay. Great. And for those who do want to test it out check the GitHub web page, it's just OrioleDB. And there are the alpha out there and instructions on how to get started with that and test it out. And, Alexander, is there certain things you're looking for help on maybe help to either test review or help with contributions?

**Alexander Korotkov:**  
We encourage everything you mentioned. So Okay, yes, testing and benchmarking are good. contribution by code could be problematic for newbies. But if, if somebody wants to do this, please do. We will provide you with assistance. And also, sponsorship of our open source work is very welcome.

**Matt Yonkovit:**  
Okay, great. And Alexander is going to be at Percona live and we're going to be talking specifically about OrioleDB. So we would encourage you if you have a chance to stop by his talk, listen to the work that he's doing and see how you can get involved. Alexander, I wanted to thank you for coming on the podcast today. I appreciate the time. And it's exciting to hear about some work and some of the things you're fixing.

**Alexander Korotkov:**  
Yes, thank you very much. Thank you very much for inviting me. And please visit my talk if the subject is interesting for you. Thank you.

**Matt Yonkovit:**  
Yeah. And Alexander, as you progress, and as you've got more results, and as you start to release come closer to release. Come on back on and tell us about the progress and some of the things that you're seeing.

**Alexander Korotkov**
Sure, sure.

**Matt Yonkovit**
Great. All right. Thanks a bunch, everybody. We'll see you next time.


