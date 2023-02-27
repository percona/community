---
title: '7 Checks to Successfully Upgrade MongoDB Replica Set in Production'
date: Wed, 29 Aug 2018 10:23:20 +0000
draft: false
tags: ['author_atishandhare', 'MongoDB', 'Open Source Databases', 'replica set', 'upgrade']
authors:
  - atish_a
images:
  - blog/2018/08/checklist-for-the-upgrade-of-MongoDB-replica-set.jpg
slug: 7-checks-successfully-upgrade-mongodb-replica-set-production
---

MongoDB ships powerful features in each release. The new release brings new features while revisions add bug fixes, security patches or improvements to existing features. To bring most out these [releases](https://docs.mongodb.com/manual/release-notes/3.6/) to your plate you should always consider upgrading your MongoDB deployments. 

![checklist for the upgrade of MongoDB replica set](blog/2018/08/checklist-for-the-upgrade-of-MongoDB-replica-set.jpg)

Planning your database upgrade can avoid the nightmares caused due to _database-upgrade-gone-wrong_ or avoid _not-so-simple_ rollbacks in your production database. Grab a cup of coffee and sit back. This blog post explains the few important to have items on your checklist to plan MongoDB replica set upgrades.


1\. Data Compatibility First
----------------------------

It is important to identify the data compatibility between your current MongoDB version and the version planned to upgrade. MongoDB sometimes introduces changes to configurations, metadata, protocol version, [validations](https://docs.mongodb.com/manual/release-notes/3.4-compatibility/#stricter-validation-of-collection-and-index-specifications), [indexes ](https://docs.mongodb.com/manual/reference/limits/#indexes)or options. The best way to identify such differences is to go through release specific compatibility [changes](https://docs.mongodb.com/manual/release-notes/3.4-compatibility/#stricter-validation-of-collection-and-index-specifications) and measure the impact.

2\. Is your Driver Compatible?
------------------------------

The driver compatibility [matrix](https://docs.mongodb.com/ecosystem/drivers/driver-compatibility-reference/#node-js-driver-compatibility) lists the versions of MongoDB and language-specific versions that are compatible with those versions. The newer version of MongoDB can introduce the changes that affect compatibility with the older version. Familiarise yourself with release specific driver compatibility changes and implement what matters.

3\. Follow Upgrade Path
-----------------------

To upgrade the newer version of MongoDB you must have already upgraded to the previous major version release series. For example, if you want to upgrade to version 4.0, you must have already upgraded to version 3.6. If you're running version 3.4 and planning to upgrade to version 4.0, you must upgrade MongoDB to stable release series 3.6. 

Wait, there's something more that can change the upgrade plan: if you wish to consider the possibility of a downgrade, it is recommended that you downgrade to the latest revision of the version you would want to downgrade to. This may prompt you to change your upgrade plan in this order:

*   Upgrade your current MongoDB version to the latest revision of current release series
*   Go to check 1 and plan your upgrade

4\. Feature Compatibility Flags
-------------------------------

Starting from version 3.4, MongoDB introduced feature compatibility flags(_some serious stuff goes here)_ 

[setFeatureCompatibilityVersion](https://docs.mongodb.com/manual/reference/command/setFeatureCompatibilityVersion/#dbcmd.setFeatureCompatibilityVersion) allows you to set the features those are _incompatible_ with the previous versions ON or OFF. 

For example, MongoDB 3.4 introduced backward-incompatible features such as Views, Decimal Type, Collation and Case-Insensitive Indexes. To enable these features in MongoDB 3.4 you must set the FeatureCompatibilityVersion to 3.4 while upgrading from version 3.2. To upgrade to a newer version of MongoDB, you must have the feature compatibility flag set as previous release series.

5\. Rehearse the Upgrade in Non-Production
------------------------------------------

Now that you're prepared, you can upgrade the MongoDB replica set in rolling fashion. This upgrade will involve the DB upgrade, driver upgrades and application code that is compatible with this driver version and DB version. To minimize the impact, upgrade secondaries in a replica set first, followed by stepping down a primary and its upgrade. 

_Test your downgrade path:_ Prepare for downgrading in the test environment. A MongoDB replica set must follow the downgrade path from the path to be upgraded to, to the latest revision of the currently used release series.

6\. Allow a Burn-in Period
--------------------------

You need to enable compatibility flags after the replica set upgrade. But let it take some time. Once you've verified that everything is all set and there is little likelihood of needing to downgrade, you can set the feature compatibility flags as mentioned in check 4.

7\. Upgrade MongoDB Tools
-------------------------

Once you've successfully upgraded to a newer version, upgrade the mongodb tools used to connect your deployment.

*   Upgrade the mongo shell to the same version as the MongoDB deployment
*   Upgrade mongodump and mongorestore versions used in your backup and restore scripts. Use the same version of mongodump/mongorestore to backup/restore deployment of the same version on MongoDB.

_The content in this blog is provided in good faith by members of the open source community. The content is not edited or tested by Percona, and views expressed are the authors' own. When using the advice from this or any other online resource **test** ideas before applying them to your production systems, and **always **secure a working back up._