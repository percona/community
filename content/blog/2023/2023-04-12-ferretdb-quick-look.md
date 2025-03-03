---
title: "FerretDB - A Quick Look"
date: "2023-04-12T00:00:00+00:00"
draft: false
tags: ["FerretDB", "MongoDB", "Databases", "Opensource"]
categories: ['PostgreSQL', "MongoDB", "Community"]
authors:
  - david_stokes
images:
  - blog/2023/04/Ferret-1200.jpg
---

There is an old saying that what looks like a duck and quacks like a duck is probably a duck.  But what looks like MongoDB and acts like MongoDB could be FerretDB! To greatly simplify the technology behind this project, FerretDB speaks, or quacks, MongoDB but stores the data in PostgreSQL. PostgreSQL has had a rich JSON data environment for years and FerrtDB takes advantage of this capability. This is a truly Open Source MongoDB alternative and was released under the Apache 2.0 license.

FerretDB has been in development for a while, but they [announced](https://blog.ferretdb.io/ferretdb-1-0-ga-opensource-mongodb-alternative/) the first Generally Available Release of their product recently. 

In the announcement is a quick "How To Get Started" section which details how to get FerretDB running with the help of Docker.  As can be seen below, this is a very simple process.

```
$  docker run -d --rm --name ferretdb -p 27017:27017 ghcr.io/ferretdb/all-in-one
Unable to find image 'ghcr.io/ferretdb/all-in-one:latest' locally
latest: Pulling from ferretdb/all-in-one
f1f26f570256: Pull complete 
1c04f8741265: Pull complete 
dffc353b86eb: Pull complete 
18c4a9e6c414: Pull complete 
81f47e7b3852: Pull complete 
5e26c947960d: Pull complete 
a2c3dc85e8c3: Pull complete 
17df73636f01: Pull complete 
713535cdf17c: Pull complete 
52278a39eea2: Pull complete 
4ded87da67f6: Pull complete 
05fae4678312: Pull complete 
56b4f4aeea2d: Pull complete 
68c486387c4f: Pull complete 
5eb3eee800a9: Pull complete 
8e5dd809e820: Pull complete 
d3e85fce5b45: Pull complete 
e6810cdbd43b: Pull complete 
Digest: sha256:072312577c1daf469ac77d09284a638dea98b63f4f4334fd54959324847b93aa
Status: Downloaded newer image for ghcr.io/ferretdb/all-in-one:latest
58f00a86bad172674479f3663563af274e0dd3d15249029a403d0c85039b7ab5
```

Now that FerretDB is ready, we can use the MondoDB shell to speak to it.  

```
$ docker exec -it ferretdb mongosh
```

```
Current Mongosh Log ID: 6435963392d12db06bdb7ecc
Connecting to:      mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0
Using MongoDB:      6.0.42
Using Mongosh:      1.8.0

(the remaining output was omitted for brevity)
```

Entering some very basic MongoDB commands work as expected. Well, for the most part. 

```
test> db
test
test> show collections;

test> db.createCollection('test');
{ ok: 1 }
test> show collections;
test
```
```
test> db.test.insert({name: "Dave", state: "Texas"});
DeprecationWarning: Collection.insert() is deprecated. Use insertOne, insertMany, or bulkWrite.
{
  acknowledged: true,
  insertedIds: { '0': ObjectId("6435ac52c4a22ac27f30e2a2") }
}
test> db.test.insertOne({name: "Dave", state: "Texas"});
{
  acknowledged: true,
  insertedId: ObjectId("6435ac5dc4a22ac27f30e2a3")
}
test> db.test.find();
[
  {
    _id: ObjectId("6435ac52c4a22ac27f30e2a2"),
    name: 'Dave',
    state: 'Texas'
  },
  {
    _id: ObjectId("6435ac5dc4a22ac27f30e2a3"),
    name: 'Dave',
    state: 'Texas'
  }
]
test> 
```

I expected that the inset on the deprecated ’insert’ command would not create a document but I was wrong.  It took me a moment to realize that the ‘insert’ and ‘insertOne’ commands both worked after looking at the different ObjectIds. 
But what do we know about the server itself? Issuing a serverStatus commands confirms we are talking to the FerretDB server. 

```
test> db.runCommand({serverStatus: 1});
{
  host: '58f00a86bad1',
  version: '6.0.42',
  process: 'ferretdb',
  pid: Long("10"),
  uptime: 6277.435694035,
  uptimeMillis: Long("6277435"),
  uptimeEstimate: Long("6277"),
  localTime: ISODate("2023-04-11T18:59:46.488Z"),
  freeMonitoring: { state: 'undecided' },
  metrics: {
    commands: {
      ping: { total: Long("1"), failed: Long("0") },
      getFreeMonitoringStatus: { total: Long("1"), failed: Long("0") },
      create: { total: Long("1"), failed: Long("0") },
      insert: { total: Long("3"), failed: Long("0") },
      atlasVersion: { total: Long("1"), failed: Long("1") },
      getLog: { total: Long("1"), failed: Long("0") },
      buildInfo: { total: Long("1"), failed: Long("0") },
      getCmdLineOpts: { total: Long("1"), failed: Long("0") },
      listCollections: { total: Long("2"), failed: Long("0") },
      ismaster: { total: Long("611"), failed: Long("0") },
      find: { total: Long("4"), failed: Long("0") },
      getParameter: { total: Long("1"), failed: Long("1") },
      hello: { total: Long("1"), failed: Long("0") },
      unknown: { total: Long("5"), failed: Long("0") }
    }
  },
  ok: 1,
  catalogStats: {
    collections: 210,
    capped: 0,
    timeseries: 0,
    views: 0,
    internalCollections: 0,
    internalViews: 0
  }
}
test> 
```

## Summary
    
FerretDB is a MongoDB protocol server built upon PostgreSQL. Those unhappy with the change in MongoDB’s license change away from open source now have another path they can follow. I will have a full session at [Percona Live](https://www.percona.com/live/conferences) on [FerretDB](https://www.ferretdb.io/) where I will delve into how complete of an option this is for those desiring an open solution.  
