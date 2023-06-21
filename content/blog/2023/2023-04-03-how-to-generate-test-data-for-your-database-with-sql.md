---
title: 'How To Generate Test Data for Your Database With SQL'
date: "2023-03-30T00:00:00+00:00"
draft: false
tags: ['SQL']
authors:
  - maksim_gramin
images:
  - blog/2023/04/00-chat-gpt-generates-test-data.jpg
---

Recently, I've noticed several posts on the Percona Community blog about test data generation. This is a great trend, as such data enables us to test applications more easily and efficiently and detect problems before they appear in production. [One](https://percona.community/blog/2022/12/13/how-to-generate-data-with-pagila-in-percona-distribution-for-postgresql/) article was devoted to the Pagila standard DB schema and [another](https://percona.community/blog/2023/01/09/how-to-generate-test-data-for-your-database-project-with-python/) to generating test data with Python. I've decided to continue this tradition and write an article about generating data using SQL. For our experimental schema, we'll use Pagila, but we'll generate much more data than it currently has.

And of course, in the current climate, we have no choice but to start with ChatGPT. We will politely ask the bot to generate data for the Pagila (publicly available sample database schema):

![ChaGPT respects referential integrity and prudently starts with reference tables](blog/2023/04/00-chat-gpt-generates-test-data.jpg)

As a result, we will obtain several valid SQL scripts in the correct order. However, we may need to request additional details, such as ensuring that all tables are included. On the one hand, this is useful and may already suffice for some cases. On the other hand, there are numerous nuances during data generation, such as specific data distribution and proximity to the subject area. Explaining all of these nuances to the bot may be challenging and labor-intensive. Plus, for sure we will need to generate a large amount of data, and in a very limited time and for private corporate schemas… So let’s roll up our sleeves and go through all the basic steps of generating data from scratch using good old SQL.


## Generate rows

As we know, SQL was designed for working with real data stored in tables. However, the SQL:1999 standard introduced [recursive queries](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL), which allow, among other things, to generate an arbitrary number of rows without referring to any particular table. At the same time, different DBMSs may have their own (often more convenient) constructs for generating rows:

```sql
-- Standard SQL:1999 way
with recursive tmp (r) as (
  select 0 union all
  select r+1 from tmp
   where r < 365)
select r from tmp

-- PostgreSQL
select generate_series
  from generate_series(1, 365)

-- Oracle
select level
  from dual
connect by level <= 365
```


## Generate values

So, we already have rows, and now we need data for these rows. To the best of my knowledge, SQL standard does not provide a way to generate random values. However, most DBMSs have their own methods for doing so. With a little tinkering, we can obtain some random data that is remotely similar to real names, emails, dates, and so on. Let’s create 1000 employees for the `employee` table without leaving your warm SQL-console:

```sql
-- PostgreSQL
insert into employee(id, first_name, last_name, 
                     years_of_experience, email, order_date, is_student)
select generate_series
     , md5(random()::text)
     , md5(random()::text)
     , floor(random() * 99)::int
     , md5(random()::text) || '@gmail.com'
     , now() - (random() * (interval '90 days')) 
     , case when random() > 0.5 then true else false end
  from generate_series(1, 1000)
```


## Generate lifelike values

Thus, we can already generate tons of messy data, which in many cases will be quite enough. But we will not rest on our laurels and will try to generate something closer to real data. Let’s start with one of the most popular task: generating real people’s names. One simple and effective solution is to prepare two sets with common first and last names, respectively, and join them using a Cartesian join. I was impressed by [this](https://gist.github.com/jbnv/ca5a7829927a6b8f2308) GitHub gist:

```sql
-- PostgreSQL
select first_name
     , last_name
  from (select unnest(array['Adam',/*...*/'Susan']) as first_name) as f
 cross join
       (select unnest(array['Matthews',/*...*/'Hancock']) as last_name) as l
 order by random()
```

We were able to generate 1392 unique full names by joining 48 first names and 29 last names. This is a good start, and the same technique can be applied to generate other types of data, such as emails, addresses and so on, by wrapping it in a stored function or using a templating engine like [Jinja](https://palletsprojects.com/p/jinja/) for ease of use. We can also use numerous third-party advanced random data generation services and try to load the generated data into our database (e.g., in CSV format like [Fake Name Generator](https://www.fakenamegenerator.com/)). Some of them will even be able to generate a ready-made SQL script for you (like the [Generatedata](https://generatedata.com/generator) service):

```sql
insert into persons (name, company, address, email)
values
  ('Berk Cotton','Tempus Eu Ligula Incorporated','Ap #633-4301 Tempus, St.','interdum.libero.dui@icloud.ca'),
  ('Ahmed Sandoval','Nullam Lobortis Foundation','P.O. Box 902, 9630 Convallis Rd.','magna.suspendisse@google.edu'),
  ('Hedy Mcbride','Risus Nulla Limited','5235 Lacinia Avenue','donec.felis@icloud.com'),
  ('Kermit Mcintosh','Erat Associates','278-141 Pellentesque St.','vel.faucibus@icloud.ca'),
  ('Susan Berg','Mauris Institute','Ap #876-781 Vehicula Street','ipsum.nunc@protonmail.ca');
```

The problem of generating data is not new, and there are many popular general-purpose libraries available for generating high-quality fake primitives such as names, addresses, and companies for various programming languages (e.g. [Java](https://github.com/DiUS/java-faker), [Python](https://github.com/joke2k/faker), [JS](https://github.com/faker-js/faker), [Ruby](https://github.com/faker-ruby/faker), etc.). Fortunately, some databases allow you to work with these libraries and generate more realistic data using SQL queries. For example, [PostgreSQL Faker](https://gitlab.com/dalibo/postgresql_faker) allows you to generate more realistic data using SQL queries like this:

```sql
select faker.name()
     , faker.company()
     , faker.address()
     , faker.email()
  from generate_series(1, 5)
```

And that’s not all. Extensions such as [faker_fdw](https://github.com/guedes/faker_fdw) provide a true relational way to generate data, using tables, joins, and other relational features:

```sql
select p.name
     , c.company
     , a.address
     , i.ascii_email 
  from (select row_number() over() as id, p.* from person p limit 5) p
  join (select row_number() over() as id, a.* from address a limit 5) a on a.id = p.id
  join (select row_number() over() as id, c.* from company c limit 5) c on c.id = p.id
  join (select row_number() over() as id, i.* from internet i limit 5) i on i.id = p.id
```


## Unique values

Although our data is random, this does not mean that there are no requirements for it. For example, we may only need unique data for certain columns (e.g. `id`, `isbn`, `code`, etc.). There are several ways to achieve this. For instance, many DBMSs support the `upsert` concept based on the values of one or more columns (clauses like `merge`, `on conflict`, etc.):

```sql
-- PostgreSQL
create table orders (code varchar(4) primary key, operation_date date);

insert into orders
select substr(md5(random()::text), 1, 4) as code
     , now() - (random() * (interval '90 days')) as operation_date 
  from generate_series(1, 1000)
    on conflict (code) do nothing
```

We can also eliminate duplicate values during generation with the help of the `distinct` clause or analytical functions:

```sql
-- PostgreSQL
select code
     , operation_date
  from (select code
             , operation_date
             , row_number() over (partition by code order by operation_date) as rn
      from (select substr(md5(random()::text), 1, 4) as code
                 , now() - (random() * (interval '90 days')) as operation_date 
              from generate_series(1, 1000)) s) s
 where rn=1
```

The disadvantage of the two previous solutions is that we may end up with fewer rows than specified. For greater accuracy, we can use the unique data generation tools built into the DBMS, such as sequences, generators, UUIDs, etc.:

```sql
-- PostgreSQL
select gen_random_uuid()
select nextval('film_film_id_seq')

-- PostgreSQL Faker
select faker.unique_name()
     , faker.unique_address()
  from generate_series(1, 10)
```


## Repeatable randomness

In specific cases, it may be necessary to generate the same random data on every run. This is particularly useful for running tests. To achieve this, many DBMSs and libraries allow you to set the initial value (seed) of the random generator:

```sql
-- PostgreSQL
select setseed(0.5);

-- Oracle
exec dbms_random.seed(42);

-- PostgreSQL Faker
select faker.seed(4321);
```


## Avatars

We may need to generate not only textual data, but also images, such as avatars. There are many special services with APIs for avatar generation, ranging from funny cartoons to real people photos (e.g. [dicebear.com](https://www.dicebear.com/), [api.multiavatar.com](https://api.multiavatar.com/), [randomusers](https://xsgames.co/randomusers/)). Let’s try to generate some people with random avatars using the captivating [robohash.org](http://robohash.org/) service:

```sql
select name
     , format('https://robohash.org/%s?set=set%s',
              replace(name, ' ', '_'),
              set_number) as avatar
  from (select trunc(random() * 4 + 1) as set_number
             , faker.name()
          from generate_series(1, 3)) s
```

![robohash](blog/2023/04/01-robohash.png)


## Let’s generate something real

It’s time to do something useful! To conduct our experiments, we require a “guinea pig” database. Let’s use the wonderful and well-known [Pagila](https://github.com/devrimgunduz/pagila) sample database, which we already used with ChatGPT at the very beginning of the post. In fact, Pagila already has data, but it is quite small — a maximum of 16k in just a couple of tables. So we will generate a lot of data ourselves for the empty schema with the help of pure SQL:

![The main part of the Pagila schema for our exercises](blog/2023/04/02-pagila-part-of-schema.png)

To make our SQL generation scripts simpler and more readable, and the generated data more realistic, we will use the [PostgreSQL Faker](https://gitlab.com/dalibo/postgresql_faker) Postgres extension in our SQL queries. Fortunately, there is an easy way to obtain this extension by using a Docker image:

```bash
docker run \
  -p 5432:5432 \
  --env POSTGRES_PASSWORD=postgres \
  registry.gitlab.com/dalibo/postgresql_faker
```

Also, don’t forget to connect to the database and register the extension:

```bash
docker exec \
  -it pagila-faker sh -c \
  "psql -U postgres -d postgres \
    -c \"create schema faker;\" \
    -c \"create extension faker schema faker cascade;\" \
  "
```

And set up Pagila’s schema, using only the [pagila-schema.sql](https://github.com/devrimgunduz/pagila/blob/master/pagila-schema.sql) script without any data:

```bash
git clone https://github.com/devrimgunduz/pagila.git
cd pagila
docker cp ./pagila-schema.sql pagila-faker:/docker-entrypoint-initdb.d/pagila-schema.sql

docker exec -it pagila-faker sh -c \
  "psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/pagila-schema.sql"
```


## References

So let’s start with the easiest stuff — reference tables. In our case, these are things like tables of countries, languages, and so on. In such a situation, we can combine the `generate_series` and `faker.unique_country` functions (or `unique_language_name`, or any other suitable function from the PostgreSQL Faker extension):

```sql
insert into country(country)
select faker.unique_country()
  from generate_series(1, 20) as id
```

A more complex case is the `city` reference table because the `city` table depends on the `country` table. It would be great if each country had a different number of cities, as is usually the case in reality. To achieve this, we can perform a `cross join` between the `country` table and a sequence of 1000 rows, and then randomly filter out some of the data, 90% in our case:

```sql
insert into city(city, country_id)
select faker.unique_city()
     , country_id
  from country
 cross join generate_series(1, 1000)
 where random() > 0.9
```

As a result, we get around 2000 cities with different distributions by country:


| country_id |     country      | cities_per_country | cities |
|------------|------------------|--------------------|--------|
|         27 | Guinea           |                118 |   1943 |
|         32 | Suriname         |                108 |   1943 |
|         40 | Marshall Islands |                107 |   1943 |
|         25 | Romania          |                103 |   1943 |
|         36 | Micronesia       |                103 |   1943 |


## Generate related data

Okay, now comes the fun part — generating data for the `staff` table. This table has two parent tables, `store` and `address`, and we need to generate their random combinations somehow. The first thing that comes to mind is using a `cross join` (as we did already with small reference tables). However, in this case, we may end up with a very slow query, because the Cartesian product of two large tables will generate a huge number of rows that still have to be sorted in random order (and only after that can we cut off the extra rows). Fortunately, the SQL:2003 standard introduces the `tablesample` clause. This allows us to read not the entire table, but only a part of it as a percentage. The `Bernoulli` sampling method ensures that all blocks of the table are scanned and only some random records are read, which leads to a quite uniform distribution of randomly selected rows. This way, we can subtract only a portion of the random rows from the `store` and `address` tables, say 1%, and then confidently perform a `cross join` between them:

```sql
insert into staff(first_name, ..., password)
select faker.first_name()
     , ...
     , faker.password()
  from (select a.address_id
             , s.store_id
          from store s tablesample bernoulli(1)
         cross join address a tablesample bernoulli(1)
         limit 50000) s
```


## Generate time-series data

We often need to store time-series data in our tables. [TimescaleDB](https://www.timescale.com/) has published three impressive articles ([one](https://www.timescale.com/blog/how-to-create-lots-of-sample-time-series-data-with-postgresql-generate_series/), [two](https://www.timescale.com/blog/generating-more-realistic-sample-time-series-data-with-postgresql-generate_series/), [three](https://www.timescale.com/blog/how-to-shape-sample-data-with-postgresql-generate_series-and-sql/)) devoted to generating such data using SQL. However, in this post, we will only focus on generating `rental_date` values based on the current row number for the `rental` table:

```sql
insert into rental(rental_date, inventory_id, customer_id, staff_id)
select current_date - (((row_number() over())::text) || ' minute')::interval
     , ...
  from (select ...
          from inventory i tablesample bernoulli(1) 
         cross join customer c tablesample bernoulli(1)
         cross join staff s tablesample bernoulli(1)
         limit 1000000) s
```


## Data multiplication

In some cases, we need to generate data from scratch, which is what we have done so far. But in other cases, we need to generate new data based on existing data while preserving current distributions and relationships. Let’s try to increase the number of cities in the `city` table by four times while maintaining the percentage of cities in each country. The idea is very simple: count the number of cities for each country, multiply it by 3, and generate this number of new cities for each country:

```sql
insert into city(city, country_id)
select unnest(array(select faker.unique_city()
                      from generate_series(1, c.cities_count*3) as id)) as city
     , country_id
  from (select country_id
             , count(1) as cities_count
          from city
         group by country_id
         order by country_id) c
```

As you can see, there are many more cities, but the top 5 countries have remained the same:


| country_id |     country      | cities_per_country | cities |
|------------|------------------|--------------------|--------|
|         27 | Guinea           |                472 |   7772 |
|         32 | Suriname         |                432 |   7772 |
|         40 | Marshall Islands |                428 |   7772 |
|         25 | Romania          |                412 |   7772 |
|         36 | Micronesia       |                412 |   7772 |

This is a viable option for generating data based on existing data, but in some cases, we may need more advanced methods, such as interpolation, prediction/extrapolation, or even machine learning. Perhaps we will discuss this separately in one of the following posts.


## Sewing it all together

The full set of scripts is available in this GitHub repository. Among other things, you can find a `docker-compose.yaml` file there, which will allow you to easily set up a test database and run generation scripts for it with just a few commands:

```bash
git clone https://github.com/mgramin/pagila-data-generation
cd pagila-data-generation
docker-compose up
```


## There’s still a long way to go…

On the one hand, we have described many useful tools and generated a lot of synthetic data for our schema. But on the other hand, we will face many other problems and challenges:

- Different database schemas. Our current SQL scripts are rigidly tied to the Pagila database schema. We will have to rewrite the scripts every time for each new supported schema.
Schema Migrations. We will also need to update the scripts every time we migrate the schema.
- Complex Schemas. In the Pagila database, we have about two dozen tables, but in real life, we usually encounter schemas with hundreds and thousands of tables, and complex dependencies between them.
- Data Quality. In this article, we did not imposed strict requirements on the quality and properties of the synthesized data. But in real life, it’s different. We may need a specific distribution of values for certain parameters, localization of values, and much more.
- Specific Data Types. In addition to text, dates, and numeric values (which we have worked with in this post), various DBMSs support many other more complex data types. These include object types, domains, and JSON, among others, which may also need to be processed during generation.
- Performance issues.


## But not so bad

Fortunately, there are many ready-made solutions that can solve the aforementioned problems in various ways (an incomplete list can be found and supplemented [here](https://github.com/mgramin/awesome-db-tools#generators)). We will attempt to generate data for our schema using the [Synthesized TDK](https://docs.synthesized.io/tdk/latest/?utm_source=percona&utm_medium=devrel&utm_campaign=datagen) tool. TDK is a YAML-based tool, and for a quick start, we only need to prepare a small configuration file in YAML format and specify the mode and expected number of rows:

```yaml
default_config:
  mode: GENERATION
  target_row_number: 100_000
```

This configuration is already sufficient to generate test data for both a small Pagila database and for real production schemas with hundreds of tables and relationships. TDK will determine and apply the necessary generation parameters independently depending on the mode, type of columns, and initial data. As a result, TDK will scan all the tables and their data in the input database and generate 100K rows for each table in the output database, taking into account the type of each column and the existing distribution.

However, we can change the default behavior of TDK by adding custom instructions to the configuration file. Suppose we want movies that are suitable for the whole family (MPAA-rating G — General Audiences) to be the majority. To achieve this, we will add additional configurations to our configuration file to generate the values of the `film.rating` column with a specific distribution:

```yaml
tables:
  - table_name_with_schema: "public.film"
    target_row_number: 10_000
    transformations:
      - columns: ["rating"]
        params:
          type: "categorical_generator"
          categories:
            type: string
            values: ["G",  "PG", "PG-13", "R", "NC-17"]
          probabilities: [0.5, 0.2, 0.1, 0.1, 0.1]
```

By applying this configuration, we can achieve the specified distribution among 10,000 films:


| rating | count | ratio |
|--------|-------|-------|
| G      |  5006 |    50 |
| PG     |  1997 |    19 |
| NC-17  |  1048 |    10 |
| PG-13  |   976 |     9 |
| R      |   973 |     9 |

We can also further configure the generation of addresses, names, strings, various sequences, and much more. You can read more about this in the [documentation](https://docs.synthesized.io/tdk/latest/user_guide/reference/transformations?utm_source=percona&utm_medium=devrel&utm_campaign=datagen) on transformation types. TDK also provide easy integration with [CI/CD pipelines](https://github.com/marketplace/actions/run-synthesized-tdk) and [Testcontainers](https://synthesized.medium.com/how-synthesized-can-help-populate-your-testcontainers-databases-8168aa7a668). And for an even easier start, we have prepared a small demo — [pagila-tdk-generation](https://github.com/synthesized-io/pagila-tdk-generation.git). It can be run with just a couple of commands using docker-compose:

```bash
git clone https://github.com/synthesized-io/tdk-docker-demo
cd tdk-docker-demo
docker-compose run tdk
```

As a result, two PostgreSQL instances will be created, with port `6000` forwarded for the input database and port `6001` for the output database. The Pagila schema will be installed on each of them, and the TDK will be launched to generate data using a more advanced [configuration](https://github.com/synthesized-io/pagila-tdk-generation/blob/main/config.yaml). Once the TDK completes its work, control will return to the command line, and we can connect to the output database to examine the synthesized data (using `6001` port and `postgres` as the username, password, and database name).


## Conclusion

In this post, we have demonstrated how easy it is to generate test data for a database using SQL and its extensions. With these tools, we were able to create a set of SQL scripts that generate test data for the Pagila schema. You can use these scripts as a basis for creating your own scripts for your own databases. However, as your database schema grows and your data quality requirements become more complex, maintaining and developing these scripts can become difficult and expensive. Fortunately, there are many ready-made solutions available, one of which is Synthesized TDK, which we examined in this post.
