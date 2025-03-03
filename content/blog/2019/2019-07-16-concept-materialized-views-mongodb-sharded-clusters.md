---
title: 'The Concept of Materialized Views in MongoDB Sharded Clusters'
date: Tue, 16 Jul 2019 10:14:41 +0000
draft: false
tags: ['MongoDB']
authors:
  - antonios_giannopoulos
images:
  - blog/2019/07/MongoDB-materialized-views.jpg
slug: concept-materialized-views-mongodb-sharded-clusters
---

In one of my past [blogs](https://www.objectrocket.com/blog/mongodb/enhance-your-organization-security-with-mongodb-views/) I explained the contribution of MongoDB® views in organization security. In this blog, I will take it one step further and I will try to approach the concept of a materialized view in MongoDB. In computing, a materialized view is a database object that contains the results of a query (definition taken from Wikipedia). If you are already familiar with MongoDB views (or you read my [blog](https://www.objectrocket.com/blog/mongodb/enhance-your-organization-security-with-mongodb-views/)), you are now probably wondering why I am calling the MongoDB views materialized while it's well known that they are computed on the fly? Well, the answer is that in this blog, I am not going to discuss the built-in view capabilities of MongoDB – which by the way are not materialized –but for a technique on how to build, maintain and use a materialized views in a MongoDB sharded cluster.

![MongoDB materialized views](blog/2019/07/MongoDB-materialized-views.jpg)

MongoDB materialized views use case
-----------------------------------

Before I begin with the implementation details, I will analyze a use case that is a perfect fit for a materialized view. The use case will help you also understand why the concept of materialized views can be really useful on a sharded cluster. I am not stating that materialized views aren’t useful on replica-sets, it's just sometimes a covering index can substitute a materialized view. In a sharded cluster, a sharded collection receives two types of queries: targeted and scatter-gather. 

Targeted queries use the shard key on the query predicates. Most of the time these queries have to access only one shard before returning results to the driver, as the shard key routes the request properly. Scatter-gather queries are the exact opposite, they have to access each and every shard to return results for a query. Scatter-gather is not ideal. At a small scale, they are not considered as a major issue, and as a matter of fact, some queries maybe be faster with scatter-gather (divide and conquer) but what happens if half of the application queries are scatter-gather? This is not an uncommon scenario, as a collection may have two popular query patterns that their query predicates don’t overlap. For example, a collection with document structure {`_id`, `_a`, `_b`, `_c`}, and the application queries 50% on `_id` and 50% on `_a`. If you choose {`_id:1` or `_id:` hashed} as the shard key, queries on a will be scattered gather and vice-versa.

How materialized views might help... and some challenges
--------------------------------------------------------

Materialized views can help us overcome the “evil” scatter-gather queries. For the above scenario, we will create a satellite collection with {`_id`, `_a`} where we are going to copy both fields from our main collection `{_id, _a, _b, _c}`. The only difference is that the satellite collection will be sharded on `{_a:1}` or `{_a:hashed}`. A query on `_a`, will first hit the satellite collection, fetch the associated `_id` and use it to query the main collection. 

At this point, you will be wondering why two queries are better than one. Well, you have to think of what is happening within the database layer during a query on `_a`. If you have N shards the mongos have to send the read request on all N shards. Some shards may return zero results but the database would have already wasted resources to execute the query. If you perform two queries, your database will execute exactly two queries, and only two shards will be busy with the “read transaction”. 

However, I must be frank, I am describing the perfect world and the ideal use case. What if the query on `_a` returns more than one result? It’s a challenge, then, to identify where one query against the main collection is better than a read transaction on both satellite-main collections. If `_a` tends to be unique our approach should be better but in cases where it returns a high number of documents – more than half of the number of shards (N/2) – maybe it is not a good solution. 

Another challenge is the way we are going to populate the satellite collection. We can treat it, like a cache, query for an `_a` and if you can’t find it on the satellite collection then add it from the main one. If `_a` is immutable we can construct the satellite collection in the background, dump/restore or using custom code. During the “initial sync”, we must not forget to track for changes, either using change streams or oplog or custom code in the application tier. If `_a` is immutable you will need an upsert operation in the satellite collection for any new inserts operation in the main collection and replay any remove operations that happen in main. That's also the way to keep both collections in sync after you finish with the “initial sync”. If `_a` is not immutable, you have to propagate the related updates as well. That's more tricky, it actually means you have to modify the shard key value. In MongoDB 4.2 it is allowed (thanks to distributed transactions), but all version prior to 4.2 it will give you an exception if you attempt it. An update on `_a` on the main collection should be replayed as an insert followed by a delete on the satellite collection. 

The challenges list doesn’t stop here. We have to consider the case, that `_a` may not a good shard key (may create hotspots, poor cardinality). Also, consider the extra storage and extra writes that will happen to your cluster. A materialized view is not good approach to every use case but is very handy when the fields are not changing very often (ideally at all) and they have decent cardinality (ideally unique).

MongoDB 4.2
-----------

As I was writing this post, MongoDB 4.2 went from development to release candidate. MongoDB 4.2 is a game-changer when it comes to materialized views, as it offers built-in support for it. The $merge  operator (from the aggregation framework) can be used to create a materialized view. The database will take the responsibility to build and maintain the view – I see some smiles already – but it comes with a few restrictions too. In the future, and when 4.2 goes GA, I will expand this post to include the $merge operator.

-- 

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors’ own. When using the advice from this or any other online resource, please **test** ideas before applying them to your production systems, and **always **secure a working back up._

_Photo by [Erol Ahmed](https://unsplash.com/@erol?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/leaves?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_