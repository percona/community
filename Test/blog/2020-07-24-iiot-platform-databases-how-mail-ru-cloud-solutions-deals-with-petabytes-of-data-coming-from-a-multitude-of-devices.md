---
title: 'IIoT platform databases - How Mail.ru Cloud Solutions deals with petabytes of data coming from a multitude of devices'
date: Fri, 24 Jul 2020 14:11:14 +0000
draft: false
tags: ['author_sergev', 'Advanced Level', 'Cache', 'ClickHouse', 'DevOps', 'IoT', 'Kubernetes', 'Kubernetes', 'Lua', 'NoSQL', 'Open Source Databases', 'SQL', 'Tarantool', 'Tools']
images: 
  - blog/2020/07/image6.png
authors:
  - andrey_sergeev
---

![IIoT platform databases - How Mail.ru Cloud Solutions](blog/2020/07/image6.png) Hello, my name is Andrey Sergeyev and I work as a Head of IoT Solution Development at [Mail.ru Cloud Solutions](https://mcs.mail.ru/). We all know there is no such thing as a universal database. Especially when the task is to build an IoT platform that would be capable of processing millions of events from various sensors in near real-time. 

Our product [Mail.ru IoT Platform](https://mcs.mail.ru/iot/) started as a Tarantool-based prototype. I’m going to tell you about our journey, the problems we faced and the solutions we found. I will also show you a current architecture for the modern Industrial Internet of Things platform. In this article we will look into:

*   our requirements for the database, universal solutions, and the CAP theorem
*   whether the database + application server in one approach is a silver bullet
*   the evolution of the platform and the databases used in it
*   the number of Tarantools we use and how we came to this

Mail.ru IoT Platform today
--------------------------

Our product Mail.ru IoT Platform is a scalable and hardware-independent platform for building Industrial Internet of Things solutions. It enables us to collect data from hundreds of thousands devices and process this stream in near real-time by using user-defined rules (scripts in Python and Lua) among other tools. 

The platform can store an unlimited amount of raw data from the sources. It also has a set of ready-made components for data visualization and analysis as well as built-in tools for predictive analysis and platform-based app development. ![Mail.ru IoT Platform set-up](blog/2020/07/image1.png) Mail.ru IoT Platform set-up[/caption] The platform is currently available for on-premise installation on customers’ facilities. In 2020 we are planning its release as a public cloud service.

Tarantool-based prototype: how we started
-----------------------------------------

Our platform started as a pilot project – a prototype with a single instance Tarantool. Its primary functions were receiving a data stream from the OPC server, processing the events with Lua scripts in real-time, monitoring key indicators on its basis, and generating events and alerts for upstream systems.

![Flowchart of the Tarantool-based prototype](blog/2020/07/image3.png) 

Flowchart of the Tarantool-based prototype[/caption]   This prototype has even shown itself in the field conditions of a multi-well pad in Iraq. It worked at an oil platform in the Persian Gulf, monitoring key indicators and sending data to the visualization system and the event log. The pilot was deemed successful, but then, as it often happens with prototypes, it was put into cold storage until we got our hands on it.

Our aims in developing the IoT platform
---------------------------------------

Along with the prototype, we got ourselves a challenge of creating a fully functional, scalable, and failsafe IoT platform that could then be released as a public cloud service. 

We had to build a platform with the following specifications:

1.  Simultaneous connection of hundreds of thousands of devices
2.  Receiving millions of events every second
3.  Datastream processing in near real-time
4.  Storing several years of raw data
5.  Analytics tools for both streaming and historic data
6.  Support for deployment in multiple data centers to maximize disaster tolerance

Pros and cons of the platform prototype
---------------------------------------

At the start of active development the prototype had the following structure:

*   Tarantool that was used as a database + Application Server
*   all the data was stored in Tarantool’s memory
*   this Tarantool had a Lua app that performed the data reception and processing and called the user scripts with incoming data

**This type of app structure has its advantages:**

1.  The code and the data are stored in one place – that enables to manipulate the data right in the application memory and get rid of extra network manipulations, which are typical for traditional apps
2.  Tarantool uses the JIT (Just in Time Compiler) for Lua. It compiles Lua code into machine code, allowing simple Lua scripts to execute at the C-like speed (40,000 RPS per core and even higher!)
3.  Tarantool is based upon cooperative multitasking. This means that every call of stored procedure runs in its own coroutine-like fiber. It gives a further performance boost for the tasks with I/O operations, e.g. network manipulations
4.  Efficient use of resources: tools capable of handling 40,000 RPS per core are quite rare

**There are also significant disadvantages:**

1.  We need storing several years of raw data from the devices, but we don’t have hundreds of petabytes for Tarantool
2.  This item directly results from advantage #1. All of the platform code consists of procedures stored in the database, which means that any codebase update is basically a database update, and that sucks
3.  Dynamic scaling gets difficult because the whole system’s performance depends on the memory it uses. Long story short, you can’t just add another Tarantool to increase the bandwidth capacity without losing 24 to 32 Gb of memory (while starting, Tarantool allocates all the memory for data) and resharding the existent data. Besides, when sharding, we lose the advantage #1 – the data and the code may not be stored in the same Tarantool
4.  Performance deteriorates as the code gets more complex with the platform progress. This happens not only because Tarantool executes all the Lua code in a single system stream, but also because the LuaJIT goes into interpreting mode instead of compiling when dealing with complex code

**Conclusion:** Tarantool is a good choice for creating an MVP, but it doesn’t work for a fully functional, easily maintained, and failsafe IoT platform capable of receiving, processing, and storing data from hundreds of thousands of devices.

Two primary problems that we wanted to solve
--------------------------------------------

First of all, there were two main issues we wanted to sort out:

1.  Ditching the concept of database + application server. We wanted to update the app code independently of the database.
2.  Simplifying the dynamic scaling under stress. We wanted to have an easy independent horizontal scaling of the greatest possible number of functions

To solve these problems, we took an innovative approach that was not well tested – the microservice architecture divided into Stateless (the applications) and Stateful (the database). 

In order to make maintenance and scaling the Stateless services out even simpler, we containerized them and adopted Kubernetes. 

![Kubernetes](blog/2020/07/image9.png) 

Now that we figured out the Stateless services, we have to decide what to do with the data.

Basic requirements for the IoT platform database
------------------------------------------------

At first, we tried not to overcomplicate things – we wanted to store all the platform data in one single universal database. Having analyzed our goals, we came up with the following list of requirements for the universal database:

1.  **ACID transactions** – the clients will keep a register of their devices on the platform, so we wouldn’t want to lose some of them upon data modification
2.  **Strict consistency** – we have to get the same responses from all of the database nodes
3.  **Horizontal scaling for writing and reading** – the devices send a huge stream of data that has to be processed and saved in near real-time
4.  **Fault tolerance** – the platform has to be capable of manipulating the data from multiple data centers to maximize fault tolerance
5.  **Accessibility** – no one would use a cloud platform that shuts down whenever one of the nodes fails
6.  **Storage volume and good compression** – we have to store several years (petabytes!) of raw data that also needs to be compressed.
7.  **Performance** – quick access to raw data and tools for stream analytics, including access from the user scripts (tens of thousands of reading requests per second!)
8.  **SQL** – we want to let our clients run analytics queries in a familiar language

Checking our requirements with the CAP theorem
----------------------------------------------

Before we started examining all the available databases to see if they meet our requirements, we decided to check whether our requirements are adequate by using a well-known tool – the CAP theorem. 

The CAP theorem states that a distributed system cannot simultaneously have more than two of the following qualities:

1.  **Consistency** – data in all of the nodes have no contradictions at any point in time
2.  **Availability** – any request to a distributed system results in a correct response, however, without a guarantee that the responses of all system nodes match
3.  **Partition tolerance** – even when the nodes are not connected, they continue working independently

![Checking our requirements with the CAP theorem](blog/2020/07/image11.png) 

For instance, the Master-Slave PostgreSQL cluster with synchronous replication is a classic example of a CA system and Cassandra is a classic AP system. 

Let’s get back to our requirements and classify them with the CAP theorem:

1.  ACID transactions and strict (or at least not eventual) consistency are C.
2.  Horizontal scaling for writing and reading + accessibility is A (multi-master).
3.  Fault tolerance is P: if one data center shuts down, the system should stand.

![ACID](blog/2020/07/image10.png) 

**Conclusion:** the universal database we require has to offer all of the CAP theorem qualities, which means that none of the existing databases can fulfill all of our needs.

Choosing the database based on the data the IoT platform works with
-------------------------------------------------------------------

Being unable to pick a universal database, we decided to split the data into two types and choose a database for each type the database will work with. 

With a first approximation we subdivided the data into two types:

1.  **Metadata** – the world model, the devices, the rules, the settings. Practically all the data except the data from the end devices
2.  **Raw data from the devices** – sensor readings, telemetry, and technical information from the devices. These are time series of messages containing a value and a timestamp

### Choosing the database for the metadata

_Our requirements_ 

Metadata is inherently relational. It is typical for this data to have a small amount and be rarely modified, but the metadata is quite important. We can’t lose it, so consistency is important – at least in terms of asynchronous replication, as well as ACID transactions and horizontal read scaling. 

This data is comparatively little in amount and it will be changed rather infrequently, so you can ditch horizontal read scaling, as well as the possible inaccessibility of the read database in case of failure. That is why, in the language of the CAP theorem, we need a CA system. 

**What usually works.** If we put a question like this, we would do with any classic relational database with asynchronous replication cluster support, e.g. PostgreSQL or MySQL. 

**Our platform aspects.** We also needed support for trees with specific requirements. The prototype had a feature taken from the systems of the RTDB class (real-time databases) – modeling the world using a tag tree. They enable us to combine all the client devices in one tree structure, which makes managing and displaying a large number of devices much easier. 

![This is how the device tree looks like](blog/2020/07/image4.png) 

This is how the device tree looks like   

This tree enables linking the end devices with the environment. For example, we can put devices physically located in the same room in one subtree, which facilitates the work with them in the future. This function is very convenient, besides, we wanted to work with RTDBs in the future, and this functionality is basically the industry standard there. 

To have a full implementation of the tag trees, a potential database must meet the following requirements:

1.  Support for trees with arbitrary width and depth.
2.  Modification of tree elements in ACID transactions.
3.  High performance when traversing a tree.

Classic relational databases can handle small trees quite well, but they don’t do as well with arbitrary trees. 

**Possible solution.** Using two databases: a graph one for the tree and the relational one for all the other metadata. 

This approach has major disadvantages:

1.  To ensure consistency between two databases, you need to add an external transaction coordinator.
2.  This design is difficult to maintain and not so reliable.
3.  As a result, we get two databases instead of one, while the graph database is only required for supporting limited functionality.

![A possible, but not a perfect solution with two databases](blog/2020/07/image7.png) 
A possible, but not a perfect solution with two databases   

**Our solution for storing metadata.** We thought a little longer and remembered that this functionality was initially implemented in a Tarantool-based prototype and it turned out very well. 

Before we continue, I would like to give an unorthodox definition of Tarantool: _Tarantool is not a database, but a set of primitives for building a database for your specific case._ 

Available primitives out of the box:

*   Spaces – an equivalent of tables for storing data in the databases.
*   Full-fledged ACID transactions.
*   Asynchronous replication using WAL logs.
*   A sharding tool that supports automatic resharding.
*   Ultrafast LuaJIT for stored procedures.
*   Large standard library.
*   LuaRocks package manager with even more packages.

Our CA solution was a relational + graph Tarantool-based database. We assembled perfect metadata storage with Tarantool primitives:

*   Spaces for storage.
*   ACID transactions – already in place.
*   Asynchronous replication – already in place.
*   Relations – we built them upon stored procedures.
*   Trees – built upon stored procedures too.

Our cluster installation is classic for systems like these – one Master for writing and several Slaves with asynchronous replications for reading scaling. 

As a result, we have a fast scalable hybrid of relational and graph databases. 

One Tarantool instance is able to process thousands of reading requests, including those with active tree traversals.

### Choosing the database for storing the data from the devices

_Our requirements_ 

This type of data is characterized by frequent writing and a large amount of data: millions of devices, several years of storage, petabytes of both incoming messages, and stored data. Its high availability is very important since the sensor readings are important for the user-defined rules and our internal services. 

It is important that the database offers horizontal scaling for reading and writing, availability, and fault tolerance, as well as ready-made analytical tools for working with this data array, preferably SQL-based. We can sacrifice consistency and ACID transactions, so in terms of the CAP theorem, we need an AP system. 

**Additional requirements.** We had a few additional requirements for the solution that would store the gigantic amounts of data:

1.  Time Series – sensor data that we wanted to store in a specialized base.
2.  Open-source – the advantages of open source code are self-explanatory.
3.  Free cluster – a common problem among modern databases.
4.  Good compression – given the amount of data and its homogeneity, we wanted to compress the stored data efficiently.
5.  Successful maintenance – in order to minimize risks, we wanted to start with a database that someone was already actively exploiting at loads similar to ours.

**Our solution.** The only database suiting our requirements was ClickHouse – a columnar time-series database with replication, multi-master, sharding, SQL support, and a free cluster. Moreover, Mail.ru has many years of successful experience in operating one of the largest ClickHouse clusters. 

But ClickHouse, however good it may be, didn’t work for us.

### Problems with the database for device data and their solution

**Problem with writing performance.** We immediately had a problem with the large data stream writing performance. It needs to be delivered to the analytical database as soon as possible so that the rules analyzing the flow of events in real-time can look at the history of a particular device and decide whether to raise an alert or not. 

**Solution.** ClickHouse is not good with multiple single inserts, but works well with large packets of data, easily coping with writing millions of lines in batches. We decided to buffer the incoming data stream, and then paste this data in batches.

![This is how we dealt with poor writing performance](blog/2020/07/image5.png) 

This is how we dealt with poor writing performance   

The writing problems were solved, but it cost us several seconds of lag between the data coming into the system and its appearance in our database. 

This is critical for various algorithms that react to the sensor readings in real-time. 

**Problem with reading performance.** Stream analytics for real-time data processing constantly needs information from the database – tens of thousands of small queries. On average, one ClickHouse node handles about a hundred analytical queries at any time. It was created to infrequently process heavy analytical queries with large amounts of data. Of course, this is not suitable for calculating trends in the data stream from hundreds of thousands of sensors.

![ClickHouse doesn’t handle a large number of queries well](blog/2020/07/image2.png) 

ClickHouse doesn’t handle a large number of queries well

**Solution.** We decided to place a cache in front of Clickhouse. The cache was meant to store the hot data that has been requested in the last 24 hours most often. 

24 hours of data is not a year but still quite a lot – so we need an AP system with horizontal scaling for reading and writing and a focus on performance while writing single events and numerous readings. 

We also need high availability, analytic tools for time series, persistence, and built-in TTL. So, we needed a fast ClickHouse that could store everything in memory. Being unable to find any suitable solutions, we decided to build one based on the Tarantool primitives:

1.  Persistence – check (WAL-logs + snapshots).
2.  Performance – check; all the data is in the memory.
3.  Scaling – check; replication + sharding.
4.  High availability – check.
5.  Analytics tools for time series (grouping, aggregation, etc.) – we built them upon stored procedures.
6.  TTL – built upon stored procedures with one background fiber (coroutine).

The solution turned out to be powerful and easy to use. One instance handled 10,000 reading RPCs, including analytic ones. 

Here is the architecture we came up with:

![Final architecture: ClickHouse as the analytic database and the Tarantool cache storing 24 hours of data. ](blog/2020/07/image8.png) 

Final architecture: ClickHouse as the analytic database and the Tarantool cache storing 24 hours of data.  

A new type of data – the state and it’s storing
-----------------------------------------------

We found a specific database for each type of data, but as the platform developed, another one appeared – the status. The status consists of current statuses of sensors and devices, as well as some global variables for stream analytics rules. 

Let’s say we have a lightbulb. The light may be either on or off, and we always need to have access to its current state, including one in the rules. Another example is a variable in stream rules – e.g., a counter of some sort. 

This type of data needs frequent writing and fast access but doesn’t take a lot of space. 

Metadata storage doesn’t suit this type of data well, because the status may change quite often and we only have one Master for writing. Durable and operating storage doesn’t work well too, because our status was last changed three years ago, and we need to have quick reading access. 

This means that the status database needs to have horizontal scaling for reading and writing, high availability, fault tolerance, and consistency on the values/documents level. We can sacrifice global consistency and ACID transactions. 

Any Key-Value or a document database should work: Redis sharding cluster, MongoDB, or, once again, Tarantool. 

Tarantool advantages:

1.  It is the most popular way of using Tarantool.
2.  Horizontal scaling – check; asynchronous replication + sharding.
3.  Consistency on the document level – check.

As a result, we have three Tarantools that are used differently: one for storing metadata, a cache for quick reading from the devices, and one for storing status data.

How to choose a database for your IoT platform
----------------------------------------------

1.  There is no such thing as a universal database.
2.  Each type of data should have its own database, the one most suitable.
3.  There is a chance you may not find a fitting database in the market.
4.  Tarantool can work as a basis for a specialized database