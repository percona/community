---
title: 'Easy and Effective Way of Building External Dictionaries for ClickHouse with Pentaho Data Integration Tool'
date: Thu, 02 Aug 2018 16:09:26 +0000
draft: false
tags: ['author_timur', 'ClickHouse', 'data warehouse', 'MySQL', 'Open Source Databases', 'tools']
---

![pentaho pdt with clickhouse](https://www.percona.com/community-blog/wp-content/uploads/2018/08/pentaho-clickhouse-300x160.jpg)In this post, I provide an illustration of how to use Pentaho Data Integration (PDI) tool to set up external dictionaries in MySQL to support ClickHouse. Although I use MySQL in this example, you can use any PDI supported source.

ClickHouse
----------

ClickHouse is an open-source column-oriented DBMS (columnar database management system) for online analytical processing. Source: [wiki](https://en.wikipedia.org/wiki/ClickHouse).

Pentaho Data Integration
------------------------

Information from the Pentaho [wiki](https://wiki.pentaho.com/display/EAI/Pentaho+Data+Integration+%28Kettle%29+Tutorial): Pentaho Data Integration (PDI, also called Kettle) is the component of Pentaho responsible for the Extract, Transform and Load (ETL) processes. Though ETL tools are most frequently used in data warehouses environments, PDI can also be used for other purposes:

*   Migrating data between applications or databases
*   Exporting data from databases to flat files
*   Loading data massively into databases
*   Data cleansing
*   Integrating applications

PDI is easy to use. Every process is created with a graphical tool where you specify what to do without writing code to indicate how to do it; because of this, you could say that PDI is _metadata oriented_.

External dictionaries
---------------------

You can add your own dictionaries from various data sources. The data source for a dictionary can be a local text or executable file, an HTTP(s) resource, or another DBMS. For more information, see "[Sources for external dictionaries](https://clickhouse.yandex/docs/en/dicts/external_dicts_dict_sources/#dicts-external_dicts_dict_sources)". ClickHouse:

*   Fully or partially stores dictionaries in RAM.
*   Periodically updates dictionaries and dynamically loads missing values. In other words, dictionaries can be loaded dynamically.

The configuration of external dictionaries is located in one or more files. The path to the configuration is specified in the [dictionaries\_config](https://clickhouse.yandex/docs/en/operations/server_settings/settings/#server_settings-dictionaries_config) parameter. Dictionaries can be loaded at server startup or at first use, depending on the [dictionaries\_lazy\_load](https://clickhouse.yandex/docs/en/operations/server_settings/settings/#server_settings-dictionaries_lazy_load) setting. Source: [dictionaries](https://clickhouse.yandex/docs/en/query_language/dicts/).

### Example of external dictionary

In two words, dictionary is a key(s)-value(s) mapping that could be used for storing some value(s) which will be retrieved using a key. It is a way to build a "star" schema, where _dictionaries are dimensions_: ![example external dictionary](https://www.percona.com/community-blog/wp-content/uploads/2018/08/example-external-dictionary.jpg) Using dictionaries you can lookup data by key(customer\_id in this example). Why do not use tables for simple JOIN? Here is what documentation says:

> If you need a JOIN for joining with dimension tables (these are relatively small tables that contain dimension properties, such as names for advertising campaigns), a JOIN might not be very convenient due to the bulky syntax and the fact that the right table is re-accessed for every query. For such cases, there is an "external dictionaries" feature that you should use instead of JOIN. For more information, see the section "External dictionaries".

> ##### Main point of this blog post:
> 
> > Demonstrating filling a MySQL table using PDI tool and connecting this table to ClickHouse as an external dictionary. You can create a scheduled job for loading or updating this table.

Filling dictionaries during the ETL process is a challenge. Of course you can write a script (or scripts) that will do all of this, but I've found a better way. Benefits:

*   Self-documented: you see what exactly PDI job does;
*   Easy to modify(see example below)
*   Built-in logging
*   Very flexible
*   If you use the [Community Edition](https://wiki.pentaho.com/display/COM/Community+Edition+Downloads) you will not pay anything.

Pentaho Data Integration part
-----------------------------

You need a UI for running/developing ETL, but it's not necessary to use the UI for running a transformation or job. Here's an example of running it from a Linux shell(read PDI’s docs about jobs/transformation):```
${PDI\_FOLDER}/kitchen.sh -file=${PATH\_TO\_PDI\_JOB\_FILE}.kjb \[-param:SOMEPARAM=SOMEVALUE\]

${PDI\_FOLDER}/pan.sh -file=${PATH\_TO\_PDI\_TRANSFORMATION\_FILE}.ktr \[-param:SOMEPARAM=SOMEVALUE\]
```Here is a PDI transformation. In this example I use three tables as a source of information, but you can create very complex logic: ![PDI transformation](https://www.percona.com/community-blog/wp-content/uploads/2018/08/pdi-transformation.png)

### “Datasource1” definition example

![datasource definition example](https://www.percona.com/community-blog/wp-content/uploads/2018/08/datasource-definition-example.png) Dimension lookup/update is a step that updates the MySQL table (in this example, it could be any database supported by PDI output step). It will be the source for ClickHouse's external dictionary: ![dimension lookup update id ](https://www.percona.com/community-blog/wp-content/uploads/2018/08/dimension-lookup-update-id-1.png) Fields definition:![dimension fields definition](https://www.percona.com/community-blog/wp-content/uploads/2018/08/dimension-lookup-update-fields-2.png) Once you have done this, you hit the “SQL” button and it will generate the DDL code for D\_CUSTOMER table. You can manage the algorithm of storing data in the step above: update or insert new record(with time\_start/time\_end fields). Also, if you use PDI for ETL, then you can generate a "technical key" for your dimension and store this key in ClickHouse, this is a different story… For this example, I will use “id” as a key in the ClickHouse dictionary. The last step is setting up external dictionary in ClickHouse's server config.

### The ClickHouse part

External dictionary config, in this example you'll see that I use MySQL:```
<dictionaries>
<dictionary>
    <name>customers</name>
    <source>
      <!-- Source configuration -->
      <mysql>
      <port>3306</port>
      <user>MySQL\_User</user>
      <password>MySQL\_Pass</password>
      <replica>
          <host>MySQL\_host</host>
          <priority>1</priority>
      </replica>
      <db>DB\_NAME</db>
      <table>D\_CUSTOMER</table>
      </mysql>
    </source>
    <layout>
      <!-- Memory layout configuration -->
	<flat/>
    </layout>

    <structure>
        <id>
		<name>id</name>
	</id>

    <attribute>
        <name>name</name>
                <type>String</type>
                <null\_value></null\_value>
        </attribute>

    <attribute>
        <name>address</name>
                <type>String</type>
                <null\_value></null\_value>
    </attribute>

    <!-- Will be uncommented later
    <attribute>
        <name>phone</name>
                <type>String</type>
                <null\_value></null\_value>
    </attribute>
    -->

   </structure>

    <lifetime>
            <min>3600</min>
            <max>86400</max>
    </lifetime>

</dictionary>
</dictionaries>

```Creating the fact table in ClickHouse: ![Create table in ClickHouse](https://www.percona.com/community-blog/wp-content/uploads/2018/08/table-in-ClickHouse.png) Some sample data: ![Sample data](https://www.percona.com/community-blog/wp-content/uploads/2018/08/sample-data.png) Now we can fetch data aggregated against the customer name: ![aggregated data with customer name](https://www.percona.com/community-blog/wp-content/uploads/2018/08/aggregated-data-with-customer-name.png)

### Dictionary modification

Sometimes, it happens that you need to modify your dimensions. In my example I am going to add phone number to the “customers” dictionary. Not a problem at all. You update your datasource in PDI job: ![dictionary modification add new field ](https://www.percona.com/community-blog/wp-content/uploads/2018/08/dictionary-modification.png) Open the “Dimension lookup/update” step and add the _phone_ field: ![Add a field ](https://www.percona.com/community-blog/wp-content/uploads/2018/08/add-a-field.png) And hit the SQL button. ![alter table statement](https://www.percona.com/community-blog/wp-content/uploads/2018/08/alter-data-statement.png) Also add the “phone” field in ClickHouse’s dictionary config:```
   <attribute>
       <name>phone</name>
               <type>String</type>
               <null\_value></null\_value>
   </attribute>
```ClickHouse will update a dictionary on the fly and we are ready to go—if not please check the logs. Now you can run the query without a modification of fact\_table: ![query without modifying fact](https://www.percona.com/community-blog/wp-content/uploads/2018/08/query-without-modifying-fact.png) Also, note that PDI job is an XML file that could be put under version source control tools, so it is easy to track or rollback if needed. Please do not hesitate to ask if you have questions!