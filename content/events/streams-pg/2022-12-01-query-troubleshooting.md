---
title: 'End of the Year Session: Query Troubleshooting - Percona Community PostgreSQL
  Live Stream & Chat - December 1st'
description: 'Join us at Percona Community Live Stream. We will have End of the year
  session: Query troubleshooting with database experts on Thursday, December 1st at
  10:00 AM EST / 04:00 PM CET / 08:30 PM IST'
draft: false
images:
- events/streams-pg/PG-Stream-Dave-Chino-December.jpg
speakers:
- charly_batista
- mario_garcia
- edith_puclla
- david_gonzalez
- jobin_augustine
- muhammad_usama
date: '2022-12-01'
tags: ["Postgres", "Stream"]
events_year: ["2022"]
events_tag: ["PostgreSQL"]
events_category: ["Speaking"]
---
![Percona Community PostgreSQL Live Stream & Chat](events/streams-pg/PG-Stream-Dave-Chino-December.jpg)
 
This session will be our final one in 2022. We will celebrate it and also discuss **query troubleshooting**in Postgres with Percona database experts.
 
## VIDEO
 
{{% youtube youtube_id="0PtiAVBzOnU" %}}{{% /youtube %}}

 
## TRANSCRIPT


**Edith Puclla:**
Hello, everyone. I think we are online, right?

**Charly Batista:**   
Yes, we are live.

**Edith Puclla:** 
So welcome to our Percona meetup. We have our special guests for this meeting. This is the end of the year meeting. So we are going to celebrate that. And for today we have Charly Batista, who is the tech lead, Postgres tech lead in Percona. So glad to have you, Charly here.

**Charly Batista:**  
Thanks. Thanks, everybody. It's been an amazing year. Right. So we are coming to the end of the year. And we had many sessions, right, where we talked about a lot of things. We talked about replication, high availability, proxy, caching, it's been quite exciting. And I hope we've been helped and people out there to get on board on this amazing world that is Postgres, right. So we always try to bring some different topics, something that can be useful during the life of a DBA. And today's topic, the idea is to talk about troubleshooting, right, especially kernel troubleshooting. Who never had a performance issue, who never had a query that was running this low when those things right. The idea today is to talk about those things. We also have Jobin here. Hey, Jobin, how are you doing? Can you hear me? We also Usama. Nice to have you here. 

**Muhammad Usama:**
Very, very excited. Like this is the last of this year, I guess. 

**Charly Batista:**   
Yeah. We should do more discussions like the one today, right? To make things more interesting, because the last ones that we've been stringing here was more like a monologue. And then you have more people, so it's quite interesting. And actually, I have a challenge for you guys. Let me share my screen here. Because I kind of have a challenge for you guys. But where is my screen? Can you guys see it properly? It's too small.

**Muhammad Usama:**
Yeah, I can see the terminal.

**Charly Batista:** 
It's not small, right. The font size.

**Muhammad Usama:**
Let me put on the glasses.

**Edith Puclla:**
Could you type something? 

**Charly Batista:**
I think it's good. Excellent. Okay, yeah, looks good. Looks good. Nice. So what is the problem that I have for you guys today? So today we have cube tables here. I'm most interested in this database, we want to pay attention on this table mapper and table meta object. They're quite simple tables. So let me describe the table meta. Looks like I have a problem. Oh, sorry..

**Edith Puclla:**
A little bit more. Please, if you can zoom a little bit more. Yes. Thank you so much.

**Charly Batista:**
Adam, all right. Okay. All right. So this is the table meta. I basically have three columns here, the ID, the parent, and then the underneath, right. So it's pretty simple. And in fact, it doesn't have even much rows here. If we select here, we have 20 rows. full table, just three columns, and 20 rows. So whatever select that we do here, enabled by me here. So if I do is select star from meta, it should be quite fast, right? Because it's just there's more people. But we have another thing, but we have a nice one here. So if I check this one, it's also a very small table. It's not a large table. As we see, we have the ID of this table here. We have the ID of the table meta. So the table meta is the parent of this table, we have the name, and we have some data, JSON. Well, first things when I what I like to do is to sort of draw a diagram of my database when I'm trying to troubleshoot, right. And actually, I have it here. And now I have the buttons to show back. So I have it here. But it's these, okay.

So you can see this diagram, right? So, as you're seeing this diagram here, maybe this is simple tables, I have the table meta that is has a self reference, and the table object, it's like a cube, a cube of objects, right. So the parent can have sub cubes in those sub skills they have the objects, the elements actually inside of those, those cubes. And we have one select. Let me go back to the terminal. Keep that in mind. Keep that one in mind because we have this my select here, let me get my select here. It looks a lot larger and actually has a syntax error because I'm like copy and paste. Interesting. Let me copy and paste again. Just give me a second.

So, I have this a lot. It looks complex. Don't get afraid because of the size of the SELECT. What matters is the result. And as you can see here, it's pretty small. It's very slow, it will finish eventually. Okay, it took 21 seconds to finish. And this is just a report. So we have the ID of the elements, the map, as you can see here, my map object ID one, the name is metal one, it has zero items in the cube, because it's the parent. So the application does not allow the parents to put anything inside the cube, only the children. But as we can see, here, the children can have children's, so those are grandchildren, right? So we have the grandparent, the parent, and the children here of this object, for example. And this is what that selected us. But the problem is the accused, the customer is complaining that it's taking 21 seconds to execute this a lot. And they run this a lot. A lot of times during the day. So if you tried to run it again, it took again, take 21 seconds. So even caching here, on my database is not working. And caching was the topic of last session. Right. So my question for you guys, including you, sir, manager, been everybody here? How we can improve the performance of the SELECT? What will you guys do as the first step to start troubleshooting the problem here? Anybody?

**Jobin Augustine:**
So for a start, I will open the code and try to implement heretical theory's syntax in the code.

**Charly Batista:**
So the problem in the application not in this alone, is that

**Jobin Augustine:**
In the Postgres server Yeah. From I don't know, the Curie exactly, but I think something like CD or like the intermediate results, like intermediate table could be helpful in this case. 

**Charly Batista:**
That's fine. Oh, I'm taking notes of the guest the options - an intermediate table. But the problem of an intermediate table is we need to change the logic on the application by the logic… 

**Jobin Augustine:**
By intermediate table, I mean something like CTE theories.

**Charly Batista:**
Okay. But this one uses one already. Keep my post here, let me get through to post. I see people commenting a lot. We try to open the YouTube, I think we are on YouTube, right? But we try to open YouTube here and both the current.

**Edith Puclla:**
YouTube, there are no questions.

**Charly Batista:**
Yeah, but I just want to post the query on the YouTube. Okay. Okay, let me just open here, my YouTube, that's gonna be interesting, because I'm probably going to hear myself and it's always awkward when you hear yourself you know, or at least for me. Oh, I opened Okay, YouTube link here. Just give me a second. Okay, say something, Charly. Well, it will break the format. And it won't let me pause because it's 200 characters max. And that's about it, isn't it? I gotta do something better. I have a cup. So I got a post on Reddit. So on YouTube, I post a comment there. That is the GitHub page. So if you guys open this, get this this this page here that I just posted on YouTube. Did you see you get the query there. So the last query is the one that I'm executing here. Right. So let's, let me say now what I will, I will do. So, as I mentioned, first thing, usually that I do is to draw the diagram of the neighborhood. So luckily, this one is very simplistic one, so I want to use paper. And they draw. And I'm gonna draw a diagram here that I have the table. But this table mat, the head ID, then has spotted this for now is what it's interesting. And then we have an audit table, that is the table. A call object has ID, and also has parents. And this table here has a self reference. So this is you guys sit at me hide my, my face here. Okay, let me just share for a second. So you guys can see here, right? I just stopped sharing. So this is usually the first step that I do. So, and then go back to my window. One thing that I also do is check what are the indexes, we have that. So if I show up here, my table meta, I'll see that I have a primary key. We have a primary key here. And that's it. We don't have any more index, I have constraints here. But constraints, they are not indexes. So I only have the primary key on this, this table method. Okay, if I check the option, we'll see that I also only have the primary key. Well, that's the first problem that I see. Like, I don't have a key under the columns that we might be using. So, and that sounds looks like a problem for me. I cannot tell if it is really a problem, because I only see on the tables, what it looks like to be a problem, right? And how can I be sure if it's a problem? Or if it's not a problem? What can I do to check if adding an index could help in this query without adding an index? Because if I add an index here, it's gonna take time depends on the application, the application gonna I'm gonna suffer performance issues and all this kind of stuff. What can I do to check these things here? If if adding an index would be interesting?

**Jobin Augustine:**
So let's explain that query and see what happens.

**Charly Batista:**
Let's explain the query. So database here, it's, it's messy. Let me open a editor here because it's messing up here with when I paste the query here.

Okay, the only thing that I did was to add that line, right. And I got a run here, see, just added explain and the query is basically the same. So okay, we have an unexplained here I'll try to okay, this is what we got from the exploit. My goodness, but it's going on with my terminal here. It's not helping much. My configuration is having problems here. So what my explain says here is that we have a city, right? We have a city here, Name Map, a hierarchy, the city those this a recursive union those a sequential scan that has a super query sequential scan inside, and then has a hash join and all this kind of stuff. But how can I start interpreting this information here? We try to make it better. Okay. How can I start interpreting this information here? How does it work? I think that it is a very important thing, right? When we want to use whatever tool that we use, we need to understand how the tool works, right? And unexplained on any database, including Postgres is a very powerful tool. And understand how to extract information from an explain is very important. And one interesting thing on the explain on post quiz is that it's not top down. It doesn't start on top, just like I was reading, or is not done top, actually, the itemization here, tell us what are executed first, right? So the things that are more to the right, are the ones that are executed first. And sometimes you can have two things executed in parallel. Postgres has the ability to make operations in parallel. For example, seems that those operations here they been executed in parallel, right. So we have a sequential scan on the table meta object. And this is a very important thing sequential scan. It's usually an expensive operation, we usually do not want to do a sequential scan, what is a sequential scan? Sequential scan is when some it reads the table the whole table from the beginning to end. And how can we prevent the sequential scan, Jobin?

**Jobin Augustine:** 
We can force or turn off the secrecy, enable signals off and try whether the plan is better or not.

**Charly Batista:**
That was a bit confusing to me. Can you explain a bit more?

**Jobin Augustine:**
We can have a session level setting. Set Enable setting.

**Charly Batista:**
We can disable the sequential scan, right, we can force. 
Okay. Okay, we disabled the sequential scan for this session. Right? Yeah. Even if it was not for the session, so let's try to do an EXPLAIN again. Okay.
 
What I what is the other option that the database has? If the database is on the sequential scan? What is the other option for the database run? It should use an index, right?

**Muhammad Usama:** 
Yeah. So I think we should give a give an option to the planner to have two scans and depend like based on the cost, it can select the better one. So right now without an index, I think the sequential scan is the only option. I'm going to disable it. That's that's not a very

**Charly Batista:**
Good point. Remember that what I said, we have no indexes here. And look, the key that it's using in this object is meta underlying ID, right? And it's doing a sequential scan here, right to join those. So as you mentioned, to someone probably if we create an index on Is this key here that's been used to solve? We might improve things, right? So let's try to create this index trade index. I'm just gonna give it a name ID. And the column name. Is the table. 

Okay, it's taken some time, because you said one thing that I didn't do. I didn't show you guys how many objects how many roles we have in this table. Remember, I only showed them the order the first table. And that was a purpose. Because this is the largest state that we have here. Let's let me do a select count. From this table is large, we have here one, we have 10 million rows here in this table. So this is the table that is causing all the problems, right? All the data with the troubles is here. And that's why our explain here shows us and now look what happened here. It's using an index scan, we have a change, right? We have a change. We didn't check anything else. We only check it out the first one here. And this is change our change. It's something it's using an index scan. Let me let's change that be true back to the default, just to see if they explain, you're probably still…

Even with the parameter on now, the database believes this is cheaper to the index, right. But one thing that I would like to point here is the EXPLAIN that we are using here, this just explained. It's an estimation, right? So it doesn't necessarily mean that this is what will happen. But the database is telling you the Optimizely follow. I'm checking the data that they have their own statistics. And based on the statistics that I have, I believe this is the best way to run your query. This is what the database is telling us, I believe this is the best way to run your code. But it doesn't say if I look, I got to run exactly these way things can change during the execution, because database can figure out something is not as tender. And so things might change. But having something or a change in here. It gives us hope. So let's give it a try. Let me copy. Let me just. Okay, I just execute this one here and remove them explain. And let's see how long it's gonna take.

Looks like it didn't help much. Right? It was it 16 seconds. So if we go back here from the last execution, when we had to read this, this query in cache, let's go back, go back. It was around 17 seconds, right? I lost the history here. But it was around 17 seconds, from 20 to 17 seconds just because of the cache. So it dropped it from 17 to 16 seconds. It doesn't mean it doesn't look like much better. Right? So the mix might have improved a little bit. Let me just execute again. But it doesn't seem to be that efficient. I got to even do one thing here. I got to run a vacuum analyze on that table to try to update the statistics shouldn't be needed, just in case. So let me run here. You guys have statistics and everything. So let me run again. And we'll see it's around 16 to 15 seconds, it's pretty consistent. Okay, that was the first attempt of optimization, we created the index and still pretty slow if I said to my customer this, but they got a copy by load, you drop it from 17 to six to 15 seconds. So didn't help much. What next we can do we can keep going to explain right let's, let's go back to that explain. So, what can we do to improve here.

**Muhammad Usama:** 
So I believe we could look at the operations which are which which which are causing which have the highest costs. So, that is there to desert a patient we want to like, optimize first.

**Charly Batista:**
Good point, that's a very, very good point. Going back here, it's from what is from the right to the left, right. So here it's doing creating the city here, but don't see anything expensive. So the creative city to be doing this category doesn't seem to be anything expensive. If we go here, on this top branch, let's put this way we have two branches, this first branch and the second branch, they run in parallel, if we go to the stop branch here doesn't seem to be pretty cheap, right? The operations here pretty cheap. So probably what's causing the expensive look because that we have here is this second branch. Okay, let's go this first operation here that's doing the scan it's using the index it's fine. The cost started increasing here look, even you're using the index it's an expensive operation because we have 10 million rows right so it's looking it's such an older roll because of the query as you saw we don't have any work walls on the ground. So it needs to read all the rules and just to scanning the index the cost is already high and then it's doing a mess marriage right join him and when he does the magic right, I hear the cost skyrocket see it goes for around 600,000 to 6 million of cost it's skyrocket exponentially. So looks like these operations here is the one that's causing the problem can we get extra information from those things or is this is all the information that we get from postcards.

Yeah, we can do better right we can we can do an explain analyze good point explain analyze we can also share the buffers right to see if we have any buffers or or anything related right. And we can ask the database to give a vote of whatever you know database let tell us let's explain people what this analyzes here those things do so then allies it will actually run the query right and this is important to know because if I had, for example, a drop table or after the for insert here, we want to first you start a transaction right because right now we are not running on transactions. So if I do an EXPLAIN analyze, in a deleted if you actually execute the Delete in the database, if I do unexplained arise in a drop table, it will actually drop the table. Right next metalize runs the query on the database and then collects all the information during the execution time during the time difference Friday. And if anything here interferes or destroys or do anything with the data, we definitely need to restart the session. Right? So then after the EXPLAIN, we do a rollback. That's not our case. But it's always a good practice to have here a put this in, in a transaction. Right? So it wasn't hard. Around here, as an example, and see, it's taking a lot more time now to execute the query. Because it's doing, it's really executing the query. It's collecting the data. It's pulling everything. So it will take more than the 15 seconds that it took before. Cross all this instrumentation and all those kinds of things. It takes time, CPU time, it takes memory and all the things from the databases. So let's wait a little bit. And, Jobin, out of curiosity, because it happened too often in support to help customer from shooting credits performance.

**Jobin Augustine:** 
I'm not too frequently. But yeah, there are cases where common patterns. So what is the developer tendency to copy and paste? Instead of writing from scratch, the tables and joining them, they'll be copying some of the sub queries and putting into another query. So, end of the day, they'll get a very big query. And another common problem is excessive use of views. So the all the complexities will be hiding behind.

**Charly Batista:**
A user view, right? Yeah, I've seen I've seen both. So you have just a file of the query, but instead of having one table, you have a view of 1000? Instruction, right? Yeah. I seen that one. Usama, you know, what would be nice for one of our streams? To do an overview inside of database, you know, to do a debug to see where are the points that the credit pass by inside of the code in the database? It's quite interesting, right? So it gives people a different view of approach hold on how the database works internally. I don't have to be a nice one. No, I want to invite you to do such a session.

**Muhammad Usama:** 
Sure, sure. Sure. I'm up for it. Nice.

**Charly Batista:**
All right, we got it here. So just go to the end. See, we have a lot more information, a lot more information here. Great. And that mean? Let's try to organize it, we have the first branch here, the first branch, again, this first branch doesn't seem to be anything expensive. See, the final cost of the branch here is 477. It's okay. We can ignore that for now. But the second branch, still that very expensive cost, right? So it's, it's, it's really high. 

**Muhammad Usama:** 
The EXPLAIN analyze, you can actually see the actual time taken by for this particular oppression. So rather than cause we can jump to the actual time as well.

**Charly Batista:**
That's another good point. That's a really good point. And another interesting point that we can see are the buffers, right? If we're hitting keeping that in memory buffer, or if we're going to the disk too often. And looks like we're actually we're hitting the buffers here. Right? So it doesn't seem to be a problem of just a specific disk IO. C. And the thing is, you mentioned is yes, it's a good point. We have the time here that most of the time was, was taken here. We can see from zero blah, blah, blah, 35 to 16 million milliseconds. 16 seconds, right? It was just one loop here, one operation. And this is one thing that we need to pay attention because sometimes I don't have it. I don't see it here. Sometimes we we see one operation. Let's say we see this sort operation here. and it takes like just a few, a few milliseconds. And then the next operation on top takes seconds. And doesn't make sense, right? So you have one here. And the next one that suppose it just to be the adding time from the previous one plus its own time. If you if you sum the time, it doesn't make any sense. And the thing is, the database might do iterations of the same operation. For example, in this case, here, this index scan, it only needed one loop, one iteration, to collect all the data. So all the data was collected in one iteration, it went that with this, whatever it needs to go with everything needed to do one operation, sometimes it needs to do 234 10 many operations, and the time that we will see here is the time and the cost of one of that operation. So we need to multiply the amount of time or demo the cost that we have here. By how many loops it did in that iteration. To finish the job here, in our case is just one. And we can clearly see here, see, it's 11 seconds here. Up this one is, it was very cheap. So this is our problem, this one is actually started to be a problem. And in this query, this specific part here, everything that anytime that any of those things, I always see that the amount of data that's being collected is the problem is actually the problem here. And we added an index, and it didn't help much, because we're still collecting like 10 million rolls, we still need to get all those objects to put here. We need to join, see this is the problematic thing here. The join here, this joy is used as the index that we had to do the JOIN and this JOIN with 10 million rows here, it's been the problem. And I don't see any way that we can add more index or anything that we can optimize here. Do you guys see anything?

**David Gonzalez:** 
I don't know, maybe we could try to convert this index scan into an Index Only Scan, maybe. Because the index scan at the end is doing to access right to the index and to the hip. And the Index Only Scan called retrieve all the data from the index itself with not the second, the second access to the hip. But at the end, is that a lot of data? So be better or at the end?

**Charly Batista:**
Yeah, well, welcome aboard, David. Nice to have you here. And that's a good point. That's a really good point. How can we do an Index Only Scan here?

**David Gonzalez:**  
Yeah, as we can see here, from the output of the EXPLAIN, we see the output line, right? So what we are getting from the index are those columns, the object ID made an ID, object name and object data. So we can include those columns in the index definition with the include clouds, and that are gonna add that status to the meta object.

**Charly Batista:**
Right, we have the object ID. We have the form the same type of object ID map ID. Name and data. Yeah. Yes.

**David Gonzalez:** 
Yeah. Okay. Yeah, well, that doesn't maybe make no more sense because we are going to end.

**Charly Batista:**
Yeah, but that's a good point that he that you put on them. Like, let's let's say for example, if we can find a way to do not collect those, those columns here, right, let's say we only need to two columns from our SELECT. We don't need the odd ones. Yeah, we could find we could create the index with only Those, those columns and the PostgreSQL, we go to the index and extract the information from the index only, it doesn't need to go to the table. That's the heap, right? It's the need to go to the table and to select. And usually that's really fast. That's very fast. Because especially if we have like, let's say, a table with 2013 columns, right, so it's a lot more expensive to go to the, to the table, if we could go only to the index. That's that's a really good point. Well, it doesn't solve our problem here. Because our payments, it's quite small, right? So it doesn't apply for this example. But that's, that's a really good point. And thanks for reminding that one. I was missing that point. Yeah. Anything else? Guys?

I see the problems because we have too many minerals, right? Too many objects, then means we always go to those STEM units and think, can we make those in parallel? But can we force a database to do something in parallel? And maybe, let's not only go back to the select, let's try to simplify that select a little bit. So let me remove the comments. So it'll make things a bit simpler. And just okay, instead of going here, let me share actually order what is the sharing thing? Let me stop sharing. Yep. And I will share editing the SELECT what is it? Can't find. Okay, so you can see my Visual Studio here, right? Just need to improve the font size just a second. I will do that just by setting its font, font size, I think the teens is it good? Can you read it? So yeah, it's it's good because here we can edit things and make it simpler. Okay, this is our our select this is our select that we are executing that I just removed the debit comments. How does it work here, we have a recursion here right so we have these many select this is the domain select, I can do one nice thing here, I can run my terminal, let me just increase the font size of the terminal. Now we never remember how to increase the font size of the terminal usually more to the end. Okay. So the nice thing here with with this studio code is because I just can just run the terminal here. And we can execute the selection. Well, this is my first select. What we first select does is to get all the parents, right, it's just get all the powers. If you see here, my select which method parent is new, those are the real real parents, they ID 123. So they don't have any parent, right? They're the grand grand grand grand plan. It's the top of hierarchy, right so I get this a lot here. And then this record C will loop through this a lot and execute the second select For example, to just let me copy this, here, just to give you an example, we actually copied everything.

But what it got to do is to run this a lot. So for meta, this meta hierarchy is the name that I gave you, right, that's just the result of the select, we can just get this a lot and do it hope that works. 

One is that might be, okay. If you start building the things, it will get the parent and then we'll select to get the children of that one. And then it will get bowls here, and the next iteration, the next loop, it will get the children's, the grandchildren's and the grand so as many we have here in the hierarchy, it to just show one of our and then I just joined by the end with the last ones to get everything and do the order by so the secret here of is this guide, and that we are looping using these one, two loops inside of the circle. Basically, this is what the recursion though. And it's super nice, because we're creating a loop it's like a while a for loop inside of a salon. Right? It's the concept of of CTS and using those things was requisite. Very, it's quite interesting. It's super cool. Or at least I I think it's super cool. Because we can we can do a loop here without any programming language. And, but, look we still didn't solve the problem, right? We still didn't didn't solve the thing about the the problem of the number of rooms. What if instead, I do deselect here outside, remember that we select all the here what it does is it selects all the parents and the children here. And after select all the parents and children, we still have another left join. Where's our m o n ID, it's the joint here. See the joins outside. What happens if instead of those things, I actually do something a little bit different. Like for example I have here an order CT let's say you do a select mapper ID This is the one thing we need I come from meta object.

For what I'm doing here  I'm asking the database to count all the objects that we have to remember those 10 million rows instead of I joined the 10 million rows first and count later and trying to count first and then join later right now we have two cities looks even more complicated, right? What goes on here and this we're gonna do an auditor work because they want to join the two cities that I have the city one, I want to get the ID of this difference that we have i also want the hierarchy and the main conference required main because you want to put all of them I go on for less here, the portal because if it's new, I want you to show zero and my from gonna be from the PCT, right CTP. I call this one and this one. Okay. Looks good. All right. Does it work? Is it proven run.

So, let's try to see. So the recap here is what I did is one as well as all the the the explain the analyze all the time, it was showing me that the biggest problem was the joint because it was joint then minerals. Right. So here we need to to count the number of objects that we have in each cube instead of joy first and counting later. 

See, this is exactly the same result that we had with the same board about exactly the same thing. But we drop it from 1517 seconds to less than a second without changing anything. Because both 17 seconds we will have created an index right so and the thing we did here we use it that explain that a little back here to explain why I always fight with this tool.

This is backwards expert. So they explain help us to understand that do join him see this Smash, right join that was caused by these joint outside here is life drawing here was the biggest problem. So we needed to find a way to optimize these joints, these joints here, it takes all the 10 million rules as the expenses mentioned, here we go $9 Lancel all the time meaning rules, do one loop in one thread only. And takes almost all the times in this example here it takes 16 seconds. The idea was, let's try to finalize an operation, let's try to make it smarter. So instead of joining with the 10 million rules, let's try to get the 10 million rows in the into the sun because see, the count is though is not outside. This is where the count is down here. Let's do the count first. And then when we get the result of the count, what we do, we join with the the city that creates the hierarchy. But now we do not have the median objects and more, we have a lot less probably we have plenty of both the I don't recall how many objects we have. And let's explain that select the new select here but the copy the new talent here.

Let me explain this one here. It will take some time. Actually explain usually takes a lot more than that the query execution itself. Remember, this query executes in milliseconds less than a second. But the EXPLAIN took a lot more time. And let's see what was the magic here?

It does. Let go. Yeah, this is the expensive one is this expensive branch. This is one stock that's been sent back. Let's go down here go down. Oh, now we see what something different here. Now we see workers. And we see Fallout index only scanning. So they were able to do an Index Only Scan. Changing that the CT. That is great. It is right. It is great, because so it did and it didn't follow. And in my configuration, I only have two workers, I could have more because I have a 16 CPU cores here on this box. But anyway, on the configuration only have to work and doing the work in parallel. See, the cost here is a lot less is smaller, because it's doing an Index Only Scan even if we sum up the cost here, that was around 11 to 12,000. It's a lot less than the five to 600,000 that we had the other one to do the full index scan and everything, right. And then when it grows to do the accounting and everything is out seduce the pilot. So the only thing we needed to do here is the approach of the salon. Right? We tried an index, it didn't work, we tried to force using the index, it didn't work, we thought about doing the Index Only Scan. Initially, we didn't have an option because we use all the rows with the columns or the columns here. So if we create an index with all the columns of the table, just leave the table alone, right? You don't need all the things changing the approach instead of doing the join first, but going in there and doing the counting first, an ad To the whole counting up while the joy made the whole difference. So, in this optimization without changing the configuration hat or anything, it just made the Select 15 times faster, at least 15 times. How much money? Do you need to spend on Google Cloud? Amazon call whatever cloud to make a hat or 15,015 times faster? It's a lot of money.

It's a lot of money. So we're not, we didn't only help the customer here, on up to make an application faster, we also help with the cost, we're here to save money. And this is an example of the power of credit optimization that a lot of people a lot of today's out there, when they think about characterization, doesn't work. It doesn't work, therefore, you know, why? What's the game this was like, just to do, to give it 30-40% improvement on the credit. We can make it like 1520 times faster. And it will be super expensive if we do that this improvement, using hacker and audit things like this? Yes, do you guys have any comments, thoughts? 

**Edith Puclla:**
Really great talk. Appreciate your time and your support for this. If it's a good practice to optimize the quality? I am writing it in the same times at the beginning.

**Charly Batista:**
No, I don't think so. I don't think so. The approach that I take is, make things work first, right? Make it work slowly, whatever, make it work as fast as you can, when it's working. When it's getting the data that you need, you have a baseline. Okay, it's sort of like the first one was working, it was getting the data, it was solving a problem, okay? But it was too slow. Right. So from that baseline, we can start optimization. If you start trying to optimize the query before even you get value and everything when it guesses, you want to guess oh, if I create, just like index breaking. It's, it's a terrible practice to when you're designing your database, put index everywhere. Right, it's really bad practice, because index, they're not for free. And actually, they're not cheap. Every time that you write on the database that we're doing sort of an update or delete the index, they need to be updated, and it's expensive. So pre optimization, most of the times is not a good practice. So make things work. Okay, in designing my database, I created those tables. So obviously, you got to put your primary keys. So you want to you want to put your reference, like the foreign keys, but like foreign keys, they're not indexes, they're just references. You don't need to put to give index to all of them. Some foreign keys we just give you if you can ignore, like, in our example, here, the index is which was just obsolete. So we can go for this right here. We can go and remove that index. It won't make much of a difference. Right? Yeah. Thank you. Yes.

**Jobin Augustine:**
Yeah, one common problem with the development practices is they will be developing with some say 100 records. And the original quarry will be running very fast. It takes milliseconds. And they won't realize the problem until the records increases. 2000 10,000 means the bad query degrade for a time, heavily. So it's a degradation is exponential. As the number of records increases, so in last 20 years, this is one of the most frequently asked questions by most of the developers when they joined the call. You do was working earlier suddenly.

**Charly Batista:**  
It was working so well before, last Friday's was working super well, today is super slow

**Jobin Augustine:** 
what happened? What happened? So the aging is something which we need to account. So the same code, the same SQL degrades over a period of time. It's just like humans aging, the more fat we accumulate.

**Charly Batista:** 
You get slower, right?  Exactly. And yeah, this is a good point, it's a very good point. Because sometimes your application is working for 10 years, no problem at all, everything is fast. And then out of nowhere, know how to change, no coatings, nothing has changed, nothing has changed, it's blue, explodes and stop became super slow. You reached the limit, right? So that design has limited application is age. And then sometimes it's even the data distribution changes. Like, you access the table, always, most of the time the first thing that was involved is 1000 rows, and then the tables is increasing. And suddenly, instead of getting always the same 1000, few 1000 rolls now need to get million rows because the data just shifted, distribute, the distribution just changed. And that happens, right? And it's actually it's quite common. And this is a problem that's really hard to troubleshoot, really hard to find. Because Oh, my goodness. So the code is the same, the parameters are the same, the data is similar, but I still have 10 million rows. But now instead of 10 million rows from state A or state B, and we have all shifted all over the states. And now we need to join a lot of things and collect, just because the big change in the distribution of the data is statistically changing your exports. And this is one of the most complex and difficult situations, we get run when troubleshooting performance issues. When like nothing changes, everything is the same even the number for most, it's sort of the same and things export like this

**David Gonzalez:** 
Thank you, Charly for the chat was very interesting to see the red steel's doing this process to optimize the quality, the definitely is a good example of the things you will be done. And also, I totally agree with the idea that you should try to reduce the size of the data set before joining. I will try to do that. And I have seen a couple of scenarios with that situation where for example, the query is doing a large list of joints, one after the other, and you end with a huge list of joints. And yeah, you have a huge list of where it's something equal to these were something major these were some Well, something that I have seen that works well is to move the word part of the filtering part of the coding within the JOIN clause, because you pull the join on the column equals two and the other column where filtering equals to the value that you want. So, instead of joining all the data set, and then filtering those what you want filter from the beginning, when you are doing the join and that also is a good way to improve this kind of situation and reduce the size of the data set to join.

**Jobin Augustine:** 
And be careful about that. There are cases where that produces different results that we can it's a good idea.

**Charly Batista:**  
And that there are two cases actually that I see when this happens because the join the condition of the giant, you can explicitly put them on the giant claws or you can put on the workflow right. So, the optimizer is smart enough when they get this they then find that the joint and put the clause there. So, usually people coming from Oracle order databases, they have this is very common practice to not use the giant expression that just will Babel comma table and then on the word that they put all the join us so this is one thing but also there is a technique that you can isolate the Giants first, like, force the database to to do the join, or force. In our case, we just use one of those techniques that are more than one smarter one. We just use it one technique that we force it the database to do the operation we want in these examples the county and after them to do the job. Right. And yeah, the only concern is what job he mentioned that if we are not careful enough, we can change the results of the people's query. But one thing is sometimes changing the result is not a bad thing. Sometimes the old query is wrong. So we need to analyze, we need to understand the problem, what we're trying to solve, we need to understand what is the data we want to see, to first identify, Okay, is the old Cray accurate? It is correct. Yeah. If it's correct, then okay. Yeah, we got to just try to optimize, but sometimes the old Cray actually is doing wrong. And this new one with the different results, right? It's fixing the things. But yeah, it can happen. And, and there are many, many different techniques to do those things. This one using CT is one of them. One thing that I liked with like CT and window functions, for example, is because using window functions or CT, you can isolate the operation, right, we can just start the operation. Let's say you accounted for some of you can do only that operation first. And then join with those that the other things this is possible, this is a possibility. So but yeah, we need to understand that the problem that the original query to make sure we were not the result. Yeah. We'll have more questions. All right. That was great. It's nice to have you all here. You know, it's not having just a monologue, we have interaction is so much better, so much better. I hope I can have you guys here during the night, the next sessions. So we all learn all these things. Thanks, guys. Thanks, you're watching us it was another long session. So I was trying to make it faster but was not fast enough. But it was great. I hope you guys enjoyed it.

**Edith Puccla:**
Thank you so much for being here. Thank you. Bye.


Follow us on [Twitter](https://twitter.com/PerconaBytes) and stay tuned to all upcoming meetups.