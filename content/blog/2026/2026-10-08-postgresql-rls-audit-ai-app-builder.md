---
title: "One query to audit the PostgreSQL row-level security an AI app builder wrote for you"
date: "2026-10-08T00:00:00+00:00"
tags: ['PostgreSQL', 'Supabase', 'Security', 'RLS', 'AI']
categories: ['PostgreSQL']
authors:
  - oleg_naryzhnykh
slug: postgresql-rls-audit-ai-app-builder
---

I take over apps that were made with Lovable, Bolt or v0.

The apps' databases are on Supabase. In this post I'll show you how I check and patch what the builders wrote in the database to protect its data.

TaskFlow is a demo. I wrote its schema and policies by hand, copying what Lovable and Bolt generate. The database is PostgreSQL 16.14 on my laptop, with a shim that creates the Supabase roles and `auth.uid()`.

> An insufficient database Row-Level Security policy in Lovable through 2025-04-15 allows remote unauthenticated attackers to read or write to arbitrary database tables of generated sites. NOTE: this is disputed by the Supplier because each individual customer of the Lovable platform accepts a responsibility over protecting the data of their application.
>
> [CVE-2025-48757](https://www.cve.org/CVERecord?id=CVE-2025-48757)

## What the generated policies look like

These are the policies that I reconstructed in [TaskFlow](https://github.com/works-on-my-box/lovable-rescue-case), a demo task tracker:

```sql
alter table public.tasks enable row level security;   -- and the other four tables

create policy "Enable read access for all users"
  on public.profiles for select using (true);
create policy "Users can update own profile"
  on public.profiles for update using (auth.uid() = id);

create policy "Enable read access for all users"
  on public.projects for select using (true);
create policy "Owners can update projects"
  on public.projects for update using (auth.uid() = owner_id);

create policy "Enable read access for all users"
  on public.project_members for select using (true);
create policy "Enable insert for authenticated users only"
  on public.project_members for insert to authenticated with check (true);

create policy "Team can read tasks"
  on public.tasks for select to authenticated using (true);
create policy "Team can update tasks"
  on public.tasks for update to authenticated using (true);

create policy "Enable all for authenticated users"
  on public.comments for all to authenticated using (true) with check (true);
-- plus three more in 01-schema-as-generated.sql
```

`anon` is the role of the public API key. `authenticated` is any signed-in user, and `auth.uid()` returns their id.

The generated read policy on `projects` says that every role (`anon` included) can read all rows.

In older Supabase projects, `anon` and `authenticated` are not just roles. They also hold full table privileges on tables in the `public` schema (check `\dp`).

The `service_role` key sits in the repository's `.env` file, right next to the project's URL. This key bypasses row-level security and should be rotated first.

## The audit

Let's look at how we can find out what the generated policies do. And how they leak data.

### What the query looks like

We will run just one query that goes through PostgreSQL's catalogs:

```sql
with t as (
  select c.oid, c.relname as tbl, c.relrowsecurity as rls_on
  from pg_class c
  join pg_namespace n on n.oid = c.relnamespace
  where n.nspname = 'public' and c.relkind in ('r', 'p')
), p as (
  select polrelid, polname,
         case polcmd when 'r' then 'SELECT' when 'a' then 'INSERT'
                     when 'w' then 'UPDATE' when 'd' then 'DELETE' else 'ALL' end as cmd,
         case when polroles = '{0}' then '{public}' else polroles::regrole[]::text end as roles,
         pg_get_expr(polqual, polrelid)      as using_expr,
         pg_get_expr(polwithcheck, polrelid) as check_expr
  from pg_policy
)
select t.tbl, t.rls_on, p.polname as policy, p.cmd, p.roles, p.using_expr, p.check_expr,
  concat_ws('; ',
    case when not t.rls_on
         then 'RLS OFF: every row open to any role with a grant' end,
    case when t.rls_on and p.polname is null
         then 'RLS on, no policies: the API roles see nothing (app breaks rather than leaks)' end,
    case when p.using_expr = 'true' and p.cmd in ('SELECT', 'ALL')
         then 'reads every row' end,
    case when p.using_expr = 'true' and p.cmd in ('UPDATE', 'DELETE', 'ALL')
         then 'writes or deletes every row' end,
    case when p.roles = '{public}'
         then 'no TO clause: applies to anon as well' end,
    case when p.check_expr = 'true'
         then 'WITH CHECK (true): ownership columns not enforced on write' end,
    case when p.cmd in ('UPDATE', 'ALL') and p.check_expr is null and p.using_expr <> 'true'
         then 'no WITH CHECK: USING is reused for the new row' end,
    case when coalesce(p.using_expr, '') || coalesce(p.check_expr, '') ~ 'auth\.(uid|jwt|role)\(\)'
          and coalesce(p.using_expr, '') || coalesce(p.check_expr, '') !~* '\(\s*select auth\.'
         then 'auth.*() not wrapped in (select ...): evaluated per row' end
  ) as findings
from t
left join p on p.polrelid = t.oid
order by t.tbl, p.cmd, p.polname;
```

`pg_policies` skips tables where there are no policies. So this query first checks `pg_class`, then gets the policies from `pg_policy` and adds a `findings` column for our report.

PostgreSQL 9.5 and newer has row-level security built in. You don't need any extensions.

### What it finds (6 of 12 rows, columns cut for width)

It tells us that `true` means that this policy reads or writes every row:

```text
 tbl             | policy                                     | cmd    | roles           | findings
-----------------+--------------------------------------------+--------+-----------------+---------------------------------------------------------
 comments        | Enable all for authenticated users         | ALL    | {authenticated} | reads every row; writes or deletes every row; WITH CHECK (true): ownership columns not enforced on write
 profiles        | Enable read access for all users           | SELECT | {public}        | reads every row; no TO clause: applies to anon as well
 profiles        | Users can update own profile               | UPDATE | {public}        | no TO clause: applies to anon as well; no WITH CHECK: USING is reused for the new row; auth.*() not wrapped in (select ...): evaluated per row
 project_members | Enable insert for authenticated users only | INSERT | {authenticated} | WITH CHECK (true): ownership columns not enforced on write
 tasks           | Team can read tasks                        | SELECT | {authenticated} | reads every row
 tasks           | Team can update tasks                      | UPDATE | {authenticated} | writes or deletes every row
```

There is no `TO` clause on two of these policies, which means that they apply to the `anon` role too.

On `project_members`, we have `WITH CHECK (true)`. This means that any signed-in user can add owner rows to `project_members`, and this is a bad thing.

It's also wrong that `auth.*()` isn't wrapped in a subquery for performance.

There are blind spots. The query can't check the columns (like `is_admin` on `profiles`). It can't check policies where `auth.role() = 'authenticated'`.

## Testing a policy from psql

PostgREST runs every request as one API role. The JWT claims go into transaction settings, and then it executes the query. We can do the same thing by hand:

Set the role with `set role`, and put the user ID into the `request.jwt.claims` setting.

### Example

Let's start with a test case:

Alice is the owner of project Alpha. Bob is just a member of Alpha, so he has no right to modify or delete it. Carol owns Gamma, but she has nothing to do with Alpha.

If you run `04-test-as-user.sql` from psql, you will get some output like this:

```text
=== anon: the key from the browser bundle, nobody signed in
set role anon;
 profiles | projects | members | tasks
----------+----------+---------+-------
        3 |        2 |       3 |     0

=== carol signed in (member of Gamma only)
set role authenticated;
select set_config('request.jwt.claims',
  '{"sub": "00000000-0000-0000-0000-000000000003", "role": "authenticated"}', false);

--- what she can read
 project |              title              | done
---------+---------------------------------+------
 Alpha   | Rotate the leaked service key   | f
 Alpha   | Write RLS policies for comments | f
 Gamma   | Pick a domain name              | f
 Gamma   | Set up billing                  | f

--- what she can write: someone else's task in Alpha
update public.tasks set done = true
where title = 'Rotate the leaked service key' returning title, done;
             title             | done
-------------------------------+------
 Rotate the leaked service key | t
UPDATE 1

--- make herself an owner of Alpha
insert into public.project_members (project_id, user_id, role)
values ('...00a1', '...0003', 'owner') returning *;
 project_id | user_id | role
------------+---------+-------
 ...00a1    | ...0003 | owner
INSERT 0 1

--- and an admin
update public.profiles set is_admin = true where id = auth.uid()
returning full_name, is_admin;
 full_name | is_admin
-----------+----------
 Carol     | t
UPDATE 1

--- a policy with USING but no WITH CHECK: hand her own project to alice
update public.projects set owner_id = '...0001' where name = 'Gamma'
returning name, owner_id;
ERROR:  new row violates row-level security policy for table "projects"
```

Carol's first four statements went through. But then we hit an error: new row violates row-level security policy for table "projects". This error happens because the `USING` clause is reused on policies that lack a `WITH CHECK`.

## The fix

There are some rules that I follow when fixing RLS. First, every policy names its role. Second, a row is visible if the user is a member of its project. And finally, every insert and update has `WITH CHECK`.

```sql
drop policy "Enable read access for all users"           on public.profiles;   -- and the other eleven
revoke all on public.profiles, public.projects, public.project_members, public.tasks, public.comments
  from anon, authenticated;
grant select, insert, update, delete
  on public.profiles, public.projects, public.project_members, public.tasks, public.comments
  to authenticated;
```

### "Infinite recursion" on project_members

```sql
create policy "members: read own projects" on public.project_members
  for select to authenticated
  using (project_id in (select m.project_id from public.project_members m
                        where m.user_id = (select auth.uid())));
select * from public.project_members;   -- as a signed-in user
```

```text
ERROR:  infinite recursion detected in policy for relation "project_members"
```

The reason is that `project_members` has its own RLS policies. So when I try to see if a user is a member of the project, it tries to check if they are a member. This causes infinite recursion.

The fix was to make `private.my_project_ids()` `SECURITY DEFINER` with an empty `search_path`.

```sql
create schema if not exists private;
grant usage on schema private to authenticated;
create or replace function private.my_project_ids() returns setof uuid
language sql stable security definer set search_path = '' as $$
  select project_id from public.project_members where user_id = (select auth.uid())
$$;
revoke execute on function private.my_project_ids() from public;
grant  execute on function private.my_project_ids() to authenticated;

create policy "projects: owner and members read" on public.projects
  for select to authenticated
  using (owner_id = (select auth.uid()) or id in (select private.my_project_ids()));

create policy "members: read own projects" on public.project_members
  for select to authenticated
  using (project_id in (select private.my_project_ids())
         or exists (select 1 from public.projects p
                    where p.id = project_members.project_id and p.owner_id = (select auth.uid())));
create policy "members: owner adds" on public.project_members
  for insert to authenticated
  with check (exists (select 1 from public.projects p
                      where p.id = project_members.project_id and p.owner_id = (select auth.uid())));

create policy "tasks: members update, task stays in a project of theirs" on public.tasks
  for update to authenticated
  using (project_id in (select private.my_project_ids()))
  with check (project_id in (select private.my_project_ids()));
revoke update on public.tasks from authenticated;
grant  update (title, done) on public.tasks to authenticated;
-- plus ten more in 05-fix.sql
```

### The is_admin column

I needed to revoke table-level `UPDATE`, and grant it back on `full_name` only:

```sql
revoke update on public.profiles from authenticated;
grant  update (full_name) on public.profiles to authenticated;
```

## Checking the fix

I ran the same test case again, with a fresh database. But the first time I ran `run.sh` it didn't reseed the test data. It looked like I had failed to patch the security.

```text
##### 05b-leftovers.sql: 05-fix.sql on top of what carol wrote (no reseed)
[...]
--- no policy takes back rows written under the old ones. to review on a live database:
 project | member | role
---------+--------+-------
 Alpha   | Carol  | owner

 full_name | is_admin
-----------+----------
 Carol     | t
```

After reseeding and rerunning, the results were better:

```text
=== anon: the key from the browser bundle, nobody signed in
ERROR:  permission denied for table profiles

=== carol signed in (member of Gamma only)
--- what she can read
 project |       title        | done
---------+--------------------+------
 Gamma   | Pick a domain name | f
 Gamma   | Set up billing     | f

--- someone else's task in Alpha: 0 rows, the row is not there for her
 title | done
-------+------
UPDATE 0
--- the same update, no WHERE, no RETURNING: her own two tasks
UPDATE 2
--- make herself an owner of Alpha
ERROR:  new row violates row-level security policy for table "project_members"
--- the same insert without RETURNING
ERROR:  new row violates row-level security policy for table "project_members"
--- and an admin
ERROR:  permission denied for table profiles

=== bob signed in (member of Alpha, not its owner)
[...]
--- a teammate's task: he cannot make himself its author
ERROR:  permission denied for table tasks
--- the app still works: bob starts a project of his own and adds himself to it
 name
------
 Beta
INSERT 0 1
 role
-------
 owner
INSERT 0 1
[...]
```

The audit findings were empty for all 14 policies.

## The cost

Let's see how much they cost on a large table.

```text
=== seeding: 2,000 users, 500 projects, ~4 members each, 200,000 tasks
 tasks  | memberships | my_projects
--------+-------------+-------------
 200004 |        2008 |           5
```

I look at the dashboard count (how many tasks are there) and then one page of tasks for the authenticated user. I run these tests on my laptop: 11th gen i7, PostgreSQL 16.14, `shared_buffers` is 128 MB and the cache is warm. JIT is turned off for this test.

```sql
explain (analyze, buffers, costs off) select count(*) from public.tasks;
explain (analyze, buffers, costs off)
  select * from public.tasks where project_id = :page order by created_at desc limit 10;
```

```sql
-- A: a function call per row
using (private.is_project_member(project_id))
-- B: what 05-fix.sql installs on tasks
using (project_id in (select private.my_project_ids()))
-- C: correlated EXISTS
using (exists (select 1 from public.project_members m
               where m.project_id = tasks.project_id and m.user_id = (select auth.uid())))
```

### The shape A policy

```text
 Aggregate (actual time=1064.579..1064.580 rows=1 loops=1)
   Buffers: shared hit=404515
   ->  Seq Scan on tasks (actual time=0.293..1064.294 rows=2000 loops=1)
         Filter: private.is_project_member(project_id)
         Rows Removed by Filter: 198004
         Buffers: shared hit=404515
 [...]
 Execution Time: 1064.597 ms
```

The query plan tells us that it ran the function `is_project_member(project_id)` on every row in the table.

It took 1065 ms and 404,515 buffer hits (on my machine). The first page of tasks took 0.57 ms, because it used `project_id = $1` which was leakproof and ran first.

But if I tried to run a `LIKE` search for title, it took 1073 ms because it had to call `is_project_member(project_id)` again.

### Shape B: the "project_id in (select my_project_ids())" policy

But now the dashboard count took just 13.9 ms, and the first page of tasks 0.65 ms.

```text
[...]
   ->  Index Scan using tasks_created_at_idx on tasks (actual time=0.176..0.638 rows=10 loops=1)
         Filter: ((hashed SubPlan 1) AND (project_id = '00000000-0000-0000-0002-000000000003'::uuid))
         Rows Removed by Filter: 4496
 Execution Time: 0.653 ms
```

### Correlated EXISTS

In this case, the dashboard count took 20.7 ms (with JIT turned off).

I also tried to run the query with the default `jit = on`. It was slower: 283 ms vs 20.7 ms.

```text
--- C with jit = on (the default up to PostgreSQL 18): the cost estimate crosses jit_above_cost
 Aggregate  (cost=6449848.95..6449848.96 rows=1 width=8) (actual time=269.537..269.542 rows=1 loops=1)
   ->  Seq Scan on tasks  (cost=0.00..6449598.94 rows=100002 width=0) (actual time=254.382..269.470 rows=2000 loops=1)
         Filter: (hashed SubPlan 22)
         Rows Removed by Filter: 198004
 [...]
 JIT:
   Timing: Generation 2.293 ms, Inlining 50.450 ms, Optimization 109.853 ms, Emission 93.490 ms, Total 256.087 ms
 Execution Time: 282.744 ms
```

The plan showed that the query was estimated at 6.4 million cost units. This is more than `jit_above_cost`, so it spent 256 ms just to compile the plan.

```text
--- B with jit = on: the estimate stays under jit_above_cost, nothing is compiled
 Execution Time: 16.028 ms
```

### The index

Adding an index helped a lot.

```sql
create index if not exists tasks_project_id_created_at_idx
  on public.tasks (project_id, created_at desc);
create index if not exists project_members_user_id_idx
  on public.project_members (user_id, project_id);
create index if not exists comments_task_id_idx
  on public.comments (task_id);
```

This made the first page of tasks run in 0.15 ms, because now it didn't have to filter out 4,496 rows.

```text
=== the indexes (08-indexes.sql), with shape B in place
[...]
   ->  Index Scan using tasks_project_id_created_at_idx on tasks (actual time=0.123..0.139 rows=10 loops=1)
         Index Cond: (project_id = '00000000-0000-0000-0002-000000000003'::uuid)
         Filter: (hashed SubPlan 1)
 Execution Time: 0.152 ms
```

### The (select auth.uid()) trick vs bare auth.uid()

Wrapping `auth.uid()` into a subquery is a lot faster. In this case, it was 10 ms vs 151 ms.

```text
--- using (created_by = auth.uid())
 Execution Time: 150.685 ms
--- using (created_by = (select auth.uid()))
   InitPlan 1 (returns $0)
   ->  Seq Scan on tasks (actual time=0.037..9.873 rows=400 loops=1)
         Filter: (created_by = $0)
 Execution Time: 9.910 ms
```

## What I hand back

I hand over the audit output before and after the fix. I also include Carol's transcript from when she tried to do stuff that she wasn't allowed to, the rows to review, my `05-fix.sql` script and the `08-indexes.sql` script.

I set up a GitHub Actions job that runs on every push and fails if any of my regressions fail.

The first version of this job failed because psql writes ERROR lines to stderr. But grep was reading from stdout only.

When the builder updates their schema, you will need to fix the RLS again.
