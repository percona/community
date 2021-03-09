---
title: 'How to Automate Minor Version Upgrades for MySQL on RDS'
date: Tue, 10 Jul 2018 12:19:11 +0000
draft: false
tags: ['renato-losio', 'Amazon RDS', 'AWS', 'devops', 'MySQL', 'RDS', 'upgrade']
---

Amazon RDS for MySQL offers the option to automate [minor version upgrades](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.html#USER_UpgradeDBInstance.MySQL.Minor) using the _minor version upgrade policy_, a property that lets you decide if Amazon is allowed to perform the upgrades on your behalf. Usually the goal is not to upgrade automatically every RDS instance but to keep up to date automatically non-production deployments. This helps you address engine issues as soon as possible and improve the automation of the deployment process. If your are using the AWS Command Line Interface (CLI) and you have an instance called _test-rds01_ it is as simple as changing```
\[--auto-minor-version-upgrade | --no-auto-minor-version-upgrade\]
```For example:```
aws rds modify-db-instance --db-instance-identifier test-rds01 --apply-immediately 
--auto-minor-version-upgrade true
```And if you use the AWS Management Console, it is just a check box.  All sorted? Unfortunately not. The main problem is that Amazon performs those upgrade only in rare circumstances. As for Amazon’s [documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.html#USER_UpgradeDBInstance.MySQL.Minor):

> Minor version upgrades only occur automatically if a minor upgrade replaces an unsafe version, such as a minor upgrade that contains bug fixes for a previous version. In all other cases, you must modify the DB instance manually to perform a minor version upgrade.

If the new version fixes any vulnerabilities that were present in the previous version, then the auto minor version upgrade will automatically take place during the next weekly maintenance window on your DB instance. In all other cases, you should manually perform the minor version upgrade. So in most scenarios, the automatic upgrade is unlikely to happen and using the auto-minor-version-upgrade  attribute is not the way to keep your MySQL running on RDS updated to the latest available minor version.

#### How to improve automation of minor version upgrades Amazon RDS for MySQL

Let’s say you want to reduce the time a newer minor version reaches your development environments or even your production ones. How can you achieve that on RDS? First of all you have to consider the delay it takes for a minor version to reach RDS that can be anything between a few weeks and a few months.  And you might even not notice that a new minor is available as it is not obvious how to be notified when it is. **What is the best way to be notified of new minor versions available on RDS MySQL?** In the past you could (even automatically) monitor the [release notes page](https://aws.amazon.com/releasenotes/?tag=releasenotes%23keywords%23amazon-rds) but the page is not anymore used for RDS. Now you have to monitor the [database announcement page](https://aws.amazon.com/new/#database-services), something that you can hardly automate. **Any way to speed up the minor version upgrades?** You can use the AWS CLI invoking the _describe-db-engine-versions_ API or write a simple Lambda function to retrieve the latest available minor version and act accordingly: you can, for example, notify your team of DBAs using Amazon Simple Notification Service (SNS) or you can automatically upgrade the instance. Let’s first see how to achieve that using the command line:```
aws --profile sandbox rds describe-db-engine-versions --engine 'mysql' --engine-version '5.7' 
--query "DBEngineVersions\[-1\].EngineVersion"
```where the -1 in the array let you filter out the very latest version of the engine available on RDS. Today the result is “5.7.21” and a simple cron job will monitor and can trigger notification for changes. Note that the same approach can be used to retrieve the latest available minor version for engines running MySQL 5.5 and MySQL 5.6. And PostgreSQL engines too. If you want to automatically and immediately upgrade your instance, the logic can be easily done in a few lines in bash with a cron on a EC2. For example, the following function requires only the database instance identifier:```
rds\_minor\_upgrade() {

  rds\_endpoint=$1
  engine\_version="5.7"

  rds\_current\_minor=$(aws rds describe-db-instances 
     --db-instance-identifier="$rds\_endpoint" --query "DBInstances\[\].EngineVersion")

  rds\_latest\_minor=$(aws rds describe-db-engine-versions -- engine 'mysql' 
      --engine-version $eng\_version --query "DBEngineVersions\[-1\].EngineVersion")

  if \[ "$rds\_latest\_minor" != "$rds\_current\_minor" \]; then
    aws rds modify-db-instance --apply-immediately --engine-version 
      $rds\_latest\_minor --db-instance-identifier $rds\_endpoint
  fi
}

```Alternatively you can write the code as a scheduled Lambda function in your favourite language. For example, using the AWS node.js SDK you can [manage RDS](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/RDS.html)  and implement the logic above using the _rds.describeDBEngineVersions_ and_rds.modifyDBInstance_ to achieve the same.```
(...)
rds.describeDBEngineVersions(params, function(err, data) {
(...)
});

(...)
var params = {
DBInstanceIdentifier: 'test-rds01', 
ApplyImmediately: true,
EngineVersion: '<new minor version>',
(...)
};
rds.modifyDBInstance(params, function(err, data) {
(...)
});
```

#### Speed up your minor upgrade!

To summarize, Amazon Web Services does not offer a real way to automatically upgrade a RDS instance to the latest available minor in the most common scenarios, but it is very easy to achieve that by taking advantage of the AWS CLI or the many SDKs. The goal is not to upgrade automatically every deployment. You would not normally use this for production deployments. However, being able to monitor the latest available minor version on RDS and apply the changes automatically for development and staging deployment can significantly reduce the time it takes to have MySQL up to date on RDS and make your upgrade process more automated. ![upgrade minor versions MySQL Amazon RDS](https://www.percona.com/community-blog/wp-content/uploads/2018/07/upgrade-minor-versions-MySQL-Amazon-RDS-300x200.jpg)