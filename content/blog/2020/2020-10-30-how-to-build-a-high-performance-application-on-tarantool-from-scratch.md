---
title: 'How to build a high-performance application on Tarantool from scratch'
date: Fri, 30 Oct 2020 14:44:18 +0000
draft: false
tags: [ 'Advanced Level', 'Code', 'DevOps', 'Lua', 'Open Source Databases', 'Programming', 'Tarantool', 'Tools']
authors: 
  - mons_anderson
images:
  - blog/2020/10/image5.png
slug: how-to-build-a-high-performance-application-on-tarantool-from-scratch
aliases:
    - /blog/how-to-build-a-high-performance-application-on-tarantool-from-scratch/
---

![tarantool start](blog/2020/10/image1.jpg) 

I came to Mail.ru Group in 2013, and I required a queue for one task. First of all, I decided to check what the company had already got. They told me they had this Tarantool product, and I checked how it worked and decided that adding a queue broker to it could work perfectly well. I contacted Kostja Osipov, the senior expert in Tarantool, and the next day he gave me a 250-string [script](https://github.com/mailru/tntlua/commit/f879dfb6981dc82287b7243074ca6cc9c6038369) that was capable of managing almost everything I needed. Since that moment, I have been in love with Tarantool. It turned out that a small amount of code written with a quite simple script language was capable of ensuring some totally new performance for this DBMS. Today, I’m going to tell you how to instantiate your own queue in Tarantool 2.2. At that moment, I enjoyed a simple and fast queue broker Beanstalkd. It offered a user-friendly interface, task status tracking by connection (client’s disconnection returned the task into the queue), as well as practical opportunities for dealing with delayed tasks. I wanted to make something like that. Here is how the service works: there is a queue broker that accepts and stores tasks; there are clients: producers sending tasks (put method); and consumers taking tasks up (take method). ![tarantool 1](blog/2020/10/image3-1.png) This is how one task’s lifecycle looks like. The task is sent with the put method and then goes to the ready state. The take operation changes the task’s status to taken. The taken task can be acknowledged (ack) and removed or changed back to ready (release-d). ![tarantool 2](blog/2020/10/image2-1.png) Procession of delayed tasks can be added: ![tarantool 3](blog/2020/10/image5.png)

**Neighborhood setup**
----------------------

Today, Tarantool is also a LuaJIT interpreter. To start working with it, an entry point is required – an initial file init.lua. After that a box.cfg()shall be called – it starts the DBMS internals. For local development, you only have to connect and start the console. Then create and run a file as follows:
```
require'strict'.on()
box.cfg{}

require'console'.start()
os.exit()
```
The console is interactive and can be instantly put to use. There is no need to install and/or set up multiple tools and learn to use them. It only takes to write 10 to 15 strings of code on any local machine. Another advice from me is to use the strict mode. Lua language is quite easy on the variable declaration, and this mode to a certain extent will help you with error management. If you build Tarantool on your own in the DEBUG mode, the strict mode will be on by default. Let’s run our file with Tarantool:
```
tarantool init.lua
```
You’ll see something like:
```
2020-07-09 20:00:11.344 [30043] main/102/init.lua C> Tarantool 2.2.3-1-g98ecc909a
2020-07-09 20:00:11.345 [30043] main/102/init.lua C> log level 5
2020-07-09 20:00:11.346 [30043] main/102/init.lua I> mapping 268435456 bytes for memtx tuple arena...
2020-07-09 20:00:11.347 [30043] main/102/init.lua I> mapping 134217728 bytes for vinyl tuple arena...
2020-07-09 20:00:11.370 [30043] main/102/init.lua I> instance uuid 38c59892-263e-42de-875c-8f67539191a3
2020-07-09 20:00:11.371 [30043] main/102/init.lua I> initializing an empty data directory
2020-07-09 20:00:11.408 [30043] main/102/init.lua I> assigned id 1 to replica 38c59892-263e-42de-875c-8f67539191a3
2020-07-09 20:00:11.408 [30043] main/102/init.lua I> cluster uuid 7723bdf4-24e8-4957-bd6c-6ab502a1911c
2020-07-09 20:00:11.425 [30043] snapshot/101/main I> saving snapshot `./00000000000000000000.snap.inprogress'
2020-07-09 20:00:11.437 [30043] snapshot/101/main I> done
2020-07-09 20:00:11.439 [30043] main/102/init.lua I> ready to accept requests
2020-07-09 20:00:11.439 [30043] main/104/checkpoint_daemon I> scheduled next checkpoint for Thu Jul  9 21:11:59 2020
tarantool>
```

**Writing a queue**
-------------------

Let’s create a file queue.lua to write our app. We can add all of it right to init.lua, but working with an independent file is handier. Now, connect the queue as a module from the init.lua file:
```
require'strict'.on()

box.cfg{}

queue = require 'queue'

require'console'.start()
os.exit()

```
All the following modifications will be made in queue.lua. As we’re making a queue, we need a place to store the task data. Let’s create a space – a data table. It can be made optionless, but we’re going to add something at once. For regular restart we have to indicate that a space shall be created only in case it doesn’t exist (if_not_exists). Another thing – in Tarantool, you can indicate the field format with content description (and it is a good idea to do so). I’m going to take a very simple structure for the queue. I’ll need only task id-s, their statuses, and some random data. Data can’t be used with a primary index, so we create an index in accordance with id. Make sure the field type of the format and the index match.
```
box.schema.create_space('queue',{ if_not_exists = true; })

box.space.queue:format( {
    { name = 'id';     type = 'number' },
    { name = 'status'; type = 'string' },
    { name = 'data';   type = '*'      },
} );

box.space.queue:create_index('primary', {
   parts = { 1,'number' };
   if_not_exists = true;
})

```
Then, we make a global queue table that will contain our functions, attributes, and methods. First of all, we bring out two functions: putting a task (put) and taking a task (take). The queue will show states of the tasks. For status indication, we’ll make another table. Numbers or strings can be used as values, but I like one-symbol references – they can be semantically relevant, and they take little place to be stored. First of all, we create two statuses: R=READY and T=TAKEN.
```
local queue = {}

local STATUS = {}
STATUS.READY = 'R'
STATUS.TAKEN = 'T'

function queue.put(...)

end

function queue.take(...)

end

return queue

```
How do we make put? Easy as pie. We need to generate an id and insert the data to a space with the READY status. There are many ways to generate an indicator, but we’ll take clock.realtime. It can automatically determine the message queue. However, remember that the clock is likely to readjust, causing a wrong message order. Another thing is that a task with the same value can appear in the queue. You can check if there is a task with the same id, and in case of collision you just one unit. This takes microseconds, and this situation is highly unlikely, so efficiency won’t be affected. All the arguments of the function shall be added to our task:
```
local clock = require 'clock'
function gen_id()
    local new_id
    repeat
        new_id = clock.realtime64()
    until not box.space.queue:get(new_id)
    return new_id
end

function queue.put(...)
    local id = gen_id()
    return box.space.queue:insert{ id, STATUS.READY, { ... } }
end

```
After we’ve written the put function, we can restart Tarantool and call this function instantly. The task will be added to the queue, now looking like a tuple. We can add random data and even nested structures to it. Tuples that Tarantool uses to store data are packed into the MessagePack, which facilitates storing of these structures.
```
tarantool> queue.put("hello")
---
- [1594325382148311477, 'R', ['hello']]
...

tarantool> queue.put("my","data",1,2,3)
---
- [1594325394527830491, 'R', ['my', 'data', 1, 2, 3]]
...

tarantool> queue.put({ complex = { struct = "data" }})
---
- [1594325413166109943, 'R', [{'complex': {'struct': 'data'}}]]
...

```
Everything we put remains within the space. We can take space commands to see what we have there:
```
tarantool> box.space.queue:select()
---
- - [1594325382148311477, 'R', ['hello']]
  - [1594325394527830491, 'R', ['my', 'data', 1, 2, 3]]
  - [1594325413166109943, 'R', [{'complex': {'struct': 'data'}}]]
...

```
Now, we need to learn how to take tasks. For this, we make a take function. We take the tasks that are ready for processing, i. e., the ones with the READY status. We can check the primary key and find the first ready task, but if there’re a lot of tasks to be processed this scenario won’t work. We’ll need a special index using the status field. One of the main differences between Tarantool and the key-value databases is that the former facilitates the creation of diverse indexes, almost like in relational databases: using various fields, composite ones, of different kinds. Then, we create the second index, indicating that the first field shows status. This will be our search option. The second field is id. It will put the tasks with the same status in the ascending order.
```
box.space.queue:create_index('status', {
    parts = { 2, 'string', 1, 'number' };
    if_not_exists = true;
})

```
Let’s take predefined functions for our selection. There’s a special iterator that is applied to a space as pairs. We pass a part of the key to it. Here, we have to deal with a composite index, which contains two fields. We use the first one for searching and the second one for putting things in order. We command the system to find the tuples that match the READY status in the first part of their index. And the system will present them put in order in accordance with the second part of the index. If we find anything, we’ll take that task, update it and return it. An update is required to prevent anybody with the same take call taking it. If there are no tasks, we return nil.
```
function queue.take()
    local found = box.space.queue.index.status
        :pairs({STATUS.READY},{ iterator = 'EQ' }):nth(1)
    if found then
        return box.space.queue
            :update( {found.id}, {{'=', 2, STATUS.TAKEN }})
    end
    return
end

```
Please, note that the first tuple level in Tarantool is an array. It has no names, but only numbers, and that’s why the field number used to be required at operations like update. Let’s make an auxiliary element – a table, to match the field names and numbers. To compile such a table we can use the format we’ve already written:
```
local F = {}
for no,def in pairs(box.space.queue:format()) do
    F[no] = def.name
    F[def.name] = no
end

```
For better visibility, we can correct descriptions of indexes like:
```
box.space.queue:format( {
    { name = 'id';     type = 'number' },
    { name = 'status'; type = 'string' },
    { name = 'data';   type = '*'      },
} );

local F = {}
for no,def in pairs(box.space.queue:format()) do
    F[no] = def.name
    F[def.name] = no
end

box.space.queue:create_index('primary', {
   parts = { F.id, 'number' };
   if_not_exists = true;
})

box.space.queue:create_index('status', {
    parts = { F.status, 'string', F.id, 'number' };
    if_not_exists = true;
})
```

Now we can implement take in whole:

```
function queue.take(...)
    for _,t in
        box.space.queue.index.status
        :pairs({ STATUS.READY },{ iterator='EQ' })
    do
        return box.space.queue:update({t.id},{
            { '=', F.status, STATUS.TAKEN }
        })
    end
    return
end

```
Let’s check how it works. For this, we’ll put one task and call take twice. If by that moment we have any data in the space, we can clear it with the command box.space.queue:truncate():
```
tarantool> queue.put("my","data",1,2,3)
---
- [1594325927025602515, 'R', ['my', 'data', 1, 2, 3]]
...

tarantool> queue.take()
---
- [1594325927025602515, 'T', ['my', 'data', 1, 2, 3]]
...

tarantool> queue.take()
---
...

```
The first take will return us the task we’ve put. As soon as we call take for the second time, nil is returned, because there are no more ready-tasks (with R status). To make sure, we run a select command from the space:
```
tarantool> box.space.queue:select()
---
- - [1594325927025602515, 'T', ['my', 'data', 1, 2, 3]]
...

```
The consumer taking the task shall either acknowledge its procession or release it without a procession. In the latter case, somebody else will be able to take the task. For this, two functions are used: ack and release. They receive the task’s id and look for it. If the task’s status shows it’s been taken, we process it. These functions are really similar: one removes processed tasks, and the other returns them with a ready status.
```
function queue.ack(id)
    local t = assert(box.space.queue:get{id},"Task not exists")
    if t and t.status == STATUS.TAKEN then
        return box.space.queue:delete{t.id}
    else
        error("Task not taken")
    end
end

function queue.release(id)
    local t = assert(box.space.queue:get{id},"Task not exists")
    if t and t.status == STATUS.TAKEN then
        return box.space.queue:update({t.id},{{'=', F.status, STATUS.READY }})
    else
        error("Task not taken")
    end
end

```
Let’s see how it works with all four functions. We will put two tasks and take the first of them, then releasing them. It returns to the R status. The second take call takes the same task. If we process it, it will be removed. The third take call will take the second task. The order will be observed. In case the task has been taken, it won’t be available for anybody else.
```
tarantool> queue.put("task 1")
---
- [1594326185712343931, 'R', ['task 1']]
...

tarantool> queue.put("task 2")
---
- [1594326187061434882, 'R', ['task 2']]
...

tarantool> task = queue.take() return task
---
- [1594326185712343931, 'T', ['task 1']]
...

tarantool> queue.release(task.id)
---
- [1594326185712343931, 'R', ['task 1']]
...

tarantool> task = queue.take() return task
---
- [1594326185712343931, 'T', ['task 1']]
...

tarantool> queue.ack(task.id)
---
- [1594326185712343931, 'T', ['task 1']]
...

tarantool> task = queue.take() return task
---
- [1594326187061434882, 'T', ['task 2']]
...

tarantool> queue.ack(task.id)
---
- [1594326187061434882, 'T', ['task 2']]
...

tarantool> task = queue.take() return task
---
- null
...

```
This is a properly working queue. We are already capable of writing a consumer to process the tasks. However, there is a problem. When we call take, the function instantly returns either a task or an empty string. If we write a cycle for task procession and start it, it will run unproductively, doing nothing and simply wasting the CPU.
```
while true do
    local task = queue.take()
    if task then
        -- ...
    end
end

```
To fix this, we’ll need a primitive channel. It enables message communication. In fact, it’s a FIFO queue for fiber communication. We have a fiber that puts the tasks when we access the database through the network or via the console. At the fiber, our Lua-code is executed, and it needs some primitive to inform the other fiber awaiting the task that there is a new one available. This is how a channel works: it can contain a buffer with N slots where a message can be located, even if no one is checking the channel. Another option is creating a channel without a buffer: this way, messages will be only acceptable in the slots that somebody waiting for. Let’s say, we create a channel for two buffer elements. It has two slots for put. If one consumer is waiting at the channel, it will create a third slot for put. If we are going to send messages via this channel, three put operations will be enabled without blocking, but the fourth put operation will be blocked by the fiber that sends messages via this channel. This is how an inter-fiber communication is set up. If for any chance you are familiar with channels in Go, they are literally the same there: ![tarantool 4](blog/2020/10/image4-1.png) Let’s slightly modify the take function. First of all, we add a new argument – timeout, implying we’re ready to wait for the task within a set period of time. We make a cycle to search for a ready task. If it can’t be found, the cycle will compute how long it has to wait. Now, let’s make a channel that will wait along with this timeout. While the fiber is pending at the channel (asleep), it can be woken up externally by sending a message via the channel.
```
local fiber = require 'fiber'
queue._wait = fiber.channel()
function queue.take(timeout)
    if not timeout then timeout = 0 end
    local now = fiber.time()
    local found
    while not found do
        found = box.space.queue.index.status
            :pairs({STATUS.READY},{ iterator = 'EQ' }):nth(1)
        if not found then
            local left = (now + timeout) - fiber.time()
            if left <= 0 then return end
            queue._wait:get(left)
        end
    end
    return box.space.queue
        :update( {found.id}, {{'=', F.status, STATUS.TAKEN }})
end

```
Altogether, take tries to take the task and if this is managed, the task is returned. However, if there is no task, it can be awaited for the rest of the timeout. Besides, the other party that creates the task will be able to wake this fiber up. To make the performance of various tests more convenient, we can globally connect the fiber module in the init.lua file:
```
fiber = require 'fiber'
```
Let’s see how this works without waking the fiber up. In an independent fiber, we’ll put a task with a 0.1 sec. delay, i. e. at first the queue will be empty, and the task will appear in 0.1 sec. after starting. Upon that, we’ll set up a 3 sec. timeout for the take call. After the start, take will try to find the task, and then if there’s none, it goes to sleep for 3 sec. In 3 sec. it wakes up, searches again, and finds the task.
```
tarantool> do
    box.space.queue:truncate()
    fiber.create(function()
        fiber.sleep(0.1)
        queue.put("task 3")
    end)
    local start = fiber.time()
    return queue.take(3), { wait = fiber.time() - start }
end

---
- [1594326905489650533, 'T', ['task 3']]
- wait: 3.0017817020416
...

```
Now, let’s make take wake up at the tasks’ appearance. For this, we’ll take our old put function and update it with a message sent via the channel. The message can be literally anything. Let it be true here. Previously, I demonstrated that put can be blocked if the channel lacks place. At the same time, the task producer doesn’t care if there are consumers on the other side. It shouldn’t get blocked while waiting for a consumer. So, it’s a reasonable thing to set up a zero timeout for blocking here. If there are some consumers out there, i. e., the ones who need to be messaged about the new task, we’ll wake them up. Otherwise, we won’t be able to send the message via the channel. An alternative option is to check if the channel has any active readers.
```
function queue.put(...)
    local id = gen_id()

    if queue._wait:has_readers() then
        queue._wait:put(true,0)
    end

    return box.space.queue:insert{ id, STATUS.READY, { ... } }
end

```
Now the take code is going to work in a totally different way. We create a task in 0.1 sec. and take instantly wakes up and receives it. We’ve got rid of the hot cycle that has been continuously pending, awaiting tasks. If we don’t put a task, the fiber will wait for 3 seconds.
```
tarantool> do
    box.space.queue:truncate()
    fiber.create(function()
        fiber.sleep(0.1)
        queue.put("task 4")
    end)
    local start = fiber.time()
    return queue.take(3), { wait = fiber.time() - start }
end

---
- [1594327004302379957, 'T', ['task 4']]
- wait: 0.10164666175842
...

```
We’ve tested how things work within the instance, and now let’s try some networking. First of all, let’s create a server. For that, we add the listen option to box.cfg of our init.lua file (it will be a port used for listening). At the same time, we’ll need to give permissions. Right now we’re not going to study privilege setting up in detail, but let’s make every connection have an execution privilege. To read about the rights please check [this](https://www.tarantool.io/en/doc/latest/book/box/authentication/).
```
require'strict'.on()
fiber = require 'fiber'

box.cfg{
    listen = '127.0.0.1:3301'
}
box.schema.user.grant('guest', 'super', nil, nil, { if_not_exists = true })

queue = require 'queue'

require'console'.start()
os.exit()

```
Let’s create a producer client for task generation. Tarantool already has a module that facilitates connection to another Tarantool.
```
#!/usr/bin/env tarantool

if #arg < 1 then
    error("Need arguments",0)
end

local netbox = require 'net.box'
local conn = netbox.connect('127.0.0.1:3301')

local yaml = require 'yaml'
local res = conn:call('queue.put',{unpack(arg)})
print(yaml.encode(res))
conn:close()

$ tarantool producer.lua "hi"
--- [1594327270675788959, 'R', ['hi']]
...

```
The consumer will connect, call take with a timeout, and process the result. If it receives the task, we’ll print or release it but won’t process it yet. Let’s say, we’ve received the task.
```
#!/usr/bin/env tarantool

local netbox = require 'net.box'
local conn = netbox.connect('127.0.0.1:3301')
local yaml = require 'yaml'

while true do
    local task = conn:call('queue.take', { 1 })

    if task then
        print("Got task: ", yaml.encode(task))
        conn:call('queue.release', { task.id })
    else
        print "No more tasks"
    end
end


```
But when we try to release the task, something odd happens:
```
$ tarantool consumer.lua 
Got task:
        --- [1594327270675788959, 'T', ['hi']]
...

ER_EXACT_MATCH: Invalid key part count in an exact match (expected 1, got 0)

```
Let’s delve into this matter. When the consumer will once again attempt to execute the task we’ll see that at the previous start it has taken the task but hasn’t been able to return it. Some error’s occurred, and the tasks got stuck. Such tasks become unavailable for other consumers, and there is nobody to return them to, as the code used to take them has been completed. 
```
$ tarantool consumer.lua 
No more tasks
No more tasks

```select shows that the tasks have been taken.```
tarantool> box.space.queue:select()
---
- - [1594327004302379957, 'T', ['task 3']]
  - [1594327270675788959, 'T', ['hi']]
...

```
We have several issues at once here. Let’s start with the automatic release of the tasks in case the client disconnects. Tarantool contains triggers for client connection and disconnection. If we add them, we’ll be able to learn about connection and disconnection events.
```
local log = require 'log'

box.session.on_connect(function()
    log.info( "connected %s from %s", box.session.id(), box.session.peer() )
end)

box.session.on_disconnect(function()
    log.info( "disconnected %s from %s", box.session.id(), box.session.peer() )
end)

2020-07-09 20:52:09.107 [32604] main/115/main I> connected 2 from 127.0.0.1:36652
2020-07-09 20:52:10.260 [32604] main/116/main I> disconnected 2 from nil
2020-07-09 20:52:10.823 [32604] main/116/main I> connected 3 from 127.0.0.1:36654
2020-07-09 20:52:11.541 [32604] main/115/main I> disconnected 3 from nil


```
There is this term, session id, and we can check the IP address used to connect, as well as the time of disconnection. However, calling session.peer()actually calls getpeername(2) right over the socket. That’s why at disconnection we don’t see who’s disconnected (as getpeername is called over a closed socket). Let’s do some minor hacking, then. Tarantool has a box.session.storage — a temporary table, to which anything you wish can be saved during the session lifetime. At connection, we can keep in mind the ones connected to know who’s disconnected. This will make adjustments easier.
```
box.session.on_connect(function()
    box.session.storage.peer = box.session.peer()
    log.info( "connected %s from %s", box.session.id(), box.session.storage.peer )
end)

box.session.on_disconnect(function()
    log.info( "disconnected %s from %s", box.session.id(), box.session.storage.peer )
end)

```
So, we have a client disconnection event. And we need to somehow release the tasks it has taken. Let’s introduce the term “possession of the task.” The session that has taken the task ought to answer for it. Let’s make two tables to save these data and modify the take function:
```
queue.taken = {}; -- list of tasks taken
queue.bysid = {}; -- list of tasks for the specific session

function queue.take(timeout)
    if not timeout then timeout = 0 end
    local now = fiber.time()
    local found
    while not found do
        found = box.space.queue.index.status
            :pairs({STATUS.READY},{ iterator = 'EQ' }):nth(1)
        if not found then
            local left = (now + timeout) - fiber.time()
            if left <= 0 then return end
            queue._wait:get(left)
        end
    end

    local sid = box.session.id()
    log.info("Register %s by %s", found.id, sid)
    queue.taken[ found.id ] = sid
    queue.bysid[ sid ] = queue.bysid[ sid ] or {}
    queue.bysid[ sid ][ found.id ] = true

    return box.space.queue
        :update( {found.id}, {{'=', F.status, STATUS.TAKEN }})
end

```
We’ll use this table to memorize that a certain task has been taken by a certain session. We’ll also need to modify the task returning code, ack, and release. Let’s make a single common function to check if the task is there and if it has been taken by a specific session. Then, it will be impossible to take the task under one connection and then return under another one requesting its deletion due to its procession completion.
```
local function get_task( id )
    if not id then error("Task id required", 2) end
    local t = box.space.queue:get{id}
    if not t then
        error(string.format( "Task {%s} was not found", id ), 2)
    end
    if not queue.taken[id] then
        error(string.format( "Task %s not taken by anybody", id ), 2)
    end
    if queue.taken[id] ~= box.session.id() then
        error(string.format( "Task %s taken by %d. Not you (%d)",
            id, queue.taken[id], box.session.id() ), 2)
    end
    return t
end

```
Now ack and release functions become very simple. We use them to call get_task, which checks if the task is possessed by us and if it is taken. Then we can work with it.
```
function queue.ack(id)
    local t = get_task(id)
    queue.taken[ t.id ] = nil
    queue.bysid[ box.session.id() ][ t.id ] = nil
    return box.space.queue:delete{t.id}
end

function queue.release(id)
    local t = get_task(id)
    if queue._wait:has_readers() then queue._wait:put(true,0) end
    queue.taken[ t.id ] = nil
    queue.bysid[ box.session.id() ][ t.id ] = nil
    return box.space.queue
        :update({t.id},{{'=', F.status, STATUS.READY }})
end

```
To reset statuses of all the tasks to R SQL or Lua snippet can be used:
```
box.execute[[ update "queue" set "status" = 'R' where "status" = 'T' ]]
box.space.queue.index.status:pairs({'T'}):each(function(t) 
box.space.queue:update({t.id},{{'=',2,'R'}}) end)

```
When we call the consumer again, it replies: task ID required.
```
$ tarantool consumer.lua 
Got task:
        --- [1594327004302379957, 'T', ['task 3']]
...

ER_PROC_LUA: queue.lua:113: Task id required

```
Thus, we’ve found the first problem in our code. When we work in Tarantool, a tuple is always associated with the space. The latter has a format, and the format has field names. That’s why we can use field names in a tuple. When we take it beyond the database, a tuple becomes just an array with a number of fields. If we refine the format of return from the function, we’ll be able to return not tuples, but objects with names. For this, we’ll apply the method :tomap{ names_only = true }:
```
function queue.put(...)
    --- ...
    return box.space.queue
        :insert{ id, STATUS.READY, { ... } }
        :tomap{ names_only = true }
end

function queue.take(timeout)
    --- ...
    return box.space.queue
        :update( {found.id}, {{'=', F.status, STATUS.TAKEN }})
        :tomap{ names_only = true }
end

function queue.ack(id)
    --- ...
    return box.space.queue:delete{t.id}:tomap{ names_only = true }
end

function queue.release(id)
    --- ...
    return box.space.queue
        :update({t.id},{{'=', F.status, STATUS.READY }})
        :tomap{ names_only = true }
end

return queue

```
Having replaced it, we’ll encounter another issue.
```
$ tarantool consumer.lua 
Got task:
        --- {'status': 'T', 'data': ['hi'], 'id': 1594327270675788959}
...

ER_PROC_LUA: queue.lua:117: Task 1594327270675788959ULL not taken by anybody

```
If we try to release the task the system will answer that we haven’t taken it. Moreover, we will see the same ID, but with a suffix – ULL. Here we encounter a trick of the LuaJIT extention: FFI (Foreign Function Interface). Let’s delve into this matter. We add five values to the table using various alternatives of numeral 1 designation as the keys.
```
tarantool> t = {}
tarantool> t[1] = 1
tarantool> t["1"] = 2
tarantool> t[1LL] = 3
tarantool> t[1ULL] = 4
tarantool> t[1ULL] = 5
tarantool> t
---
- 1: 1
  1: 5
  1: 4
  '1': 2
  1: 3
...

```
We would expect them to be displayed as 2 (string + number) or 3 (string + number + LL). But when displayed, all the keys will appear in the table separately: we will still see all the values – 1, 2, 3, 4, 5. Moreover, at serialization, we won’t see any difference between regular, signed, or unsigned numbers.
```
tarantool> return t[1], t['1'], t[1LL], t[1ULL]
---
- 1
- 2
- null
- null
...

```
However, the most amusing thing happens when we try to extract data from the table. It goes well with regular Lua-types (number and string), but it doesn’t with LL (long long) and ULL (unsigned long long). They are a separate type of cdata, intended for working with C language types. When saving into a Lua table, cdata is hashed by address, not by value. Two numbers, no matter if they are the same in value, simply have different addresses. And when we add ULL to the table, we can’t extract them using the same value. That’s why we’ll have to change our queue and key possession a bit. This is a forced move, but it will enable random modification of our keys in the future. Somehow, we need to transform our key into a string or a number. Let’s take the MessagePack. In Tarantool, it’s used to store tuples, and it will pack our values just like Tarantool itself does. With this pack, we’ll transform a random key into a string that will become a key to our table.
```
local msgpack = require 'msgpack'

local function keypack( key )
    return msgpack.encode( key )
end

local function keyunpack( data )
    return msgpack.decode( data )
end

```
Then we add the key package to take and save it into the table. In the function get_task we need to check if the key has passed in a correct format, and if not, we change it to int64. After that, we use keypack to pack the key to the MessagePack. As this packed key will be required by all the functions that use it, we’ll return it from get_task, so that ack and release could use it and clean it out from the sessions.
```
function queue.take(timeout)
    if not timeout then timeout = 0 end
    local now = fiber.time()
    local found
    while not found do
        found = box.space.queue.index.status
            :pairs({STATUS.READY},{ iterator = 'EQ' }):nth(1)
        if not found then
            local left = (now + timeout) - fiber.time()
            if left <= 0 then return end
            queue._wait:get(left)
        end
    end

    local sid = box.session.id()
    log.info("Register %s by %s", found.id, sid)
    local key = keypack( found.id )
    queue.taken[ key ] = sid
    queue.bysid[ sid ] = queue.bysid[ sid ] or {}
    queue.bysid[ sid ][ key ] = true

    return box.space.queue
        :update( {found.id}, {{'=', F.status, STATUS.TAKEN }})
        :tomap{ names_only = true }
end

local function get_task( id )
    if not id then error("Task id required", 2) end
    id = tonumber64(id)
    local key = keypack(id)
    local t = box.space.queue:get{id}
    if not t then
        error(string.format( "Task {%s} was not found", id ), 2)
    end
    if not queue.taken[key] then
        error(string.format( "Task %s not taken by anybody", id ), 2)
    end
    if queue.taken[key] ~= box.session.id() then
        error(string.format( "Task %s taken by %d. Not you (%d)",
            id, queue.taken[key], box.session.id() ), 2)
    end
    return t, key
end

function queue.ack(id)
    local t, key = get_task(id)
    queue.taken[ key ] = nil
    queue.bysid[ box.session.id() ][ key ] = nil
    return box.space.queue:delete{t.id}:tomap{ names_only = true }
end

function queue.release(id)
    local t, key = get_task(id)
    queue.taken[ key ] = nil
    queue.bysid[ box.session.id() ][ key ] = nil
    if queue._wait:has_readers() then queue._wait:put(true,0) end
    return box.space.queue
        :update({t.id},{{'=', F.status, STATUS.READY }})
        :tomap{ names_only = true }
end

```
As we have a disconnection trigger, we know that a certain session has disconnected – the one possessing certain keys. We can take all the keys from that session and automatically return them to their initial state — ready. Besides, this session may contain some tasks awaiting to be take-n. Let’s mark them in the session.storage for the tasks not to be taken.
```
box.session.on_disconnect(function()
    log.info( "disconnected %s from %s", box.session.id(), box.session.storage.peer )
    box.session.storage.destroyed = true

    local sid = box.session.id()
    local bysid = queue.bysid[ sid ]
    if bysid then
        while next(bysid) do
            for key, id in pairs(bysid) do
                log.info("Autorelease %s by disconnect", id);
                queue.taken[key] = nil
                bysid[key] = nil
                local t = box.space.queue:get(id)
                if t then
                    if queue._wait:has_readers() then queue._wait:put(true,0) end
                    box.space.queue:update({t.id},{{'=', F.status, STATUS.READY }})
                end
            end
        end
        queue.bysid[ sid ] = nil
    end
end)

function queue.take(timeout)
    if not timeout then timeout = 0 end
    local now = fiber.time()
    local found
    while not found do
        found = box.space.queue.index.status
            :pairs({STATUS.READY},{ iterator = 'EQ' }):nth(1)
        if not found then
            local left = (now + timeout) - fiber.time()
            if left <= 0 then return end
            queue._wait:get(left)
        end
    end

    if box.session.storage.destroyed then return end

    local sid = box.session.id()
    log.info("Register %s by %s", found.id, sid)
    local key = keypack( found.id )
    queue.taken[ key ] = sid
    queue.bysid[ sid ] = queue.bysid[ sid ] or {}
    queue.bysid[ sid ][ key ] = found.id

    return box.space.queue
        :update( {found.id}, {{'=', F.status, STATUS.TAKEN }})
        :tomap{ names_only = true }
end

```
For testing purposes, tasks can be taken as a group:
```
tarantoolctl connect 127.0.0.1:3301 <<< 'queue.take()'

```
At adjustment, you might see that you’ve taken the tasks, thus dropping the queue, but at restart the tasks aren’t possessed by anybody (because all connections were interrupted when you switched off), but they get the taken status. That’s why we’ll update our code with status modification at startup. Thus, the database will be started, releasing all the tasks taken.
```
while true do
    local t = box.space.queue.index.status:pairs({STATUS.TAKEN}):nth(1)
    if not t then break end
    box.space.queue:update({ t.id }, {{'=', F.status, STATUS.READY }})
    log.info("Autoreleased %s at start", t.id)
end

```
Now we have a queue ready for operation.

**Adding delayed procession**
-----------------------------

Thereat, we only have to add delayed tasks. For that, let’s add a new field and a relevant index. We’re going to use this field to store the time when a certain task’s state should be changed. To this end, we’re modifying the put function and adding a new status: W=WAITING.
```
box.space.queue:format( {
    { name = 'id';     type = 'number' },
    { name = 'status'; type = 'string' },
    { name = 'runat';  type = 'number' },
    { name = 'data';   type = '*'      },
} )

box.space.queue:create_index('runat', {
    parts = { F.runat, 'number', F.id, 'number' };
    if_not_exists = true;
})

STATUS.WAITING = 'W'

```
As we are flip-flopping the pattern, and as this is a development mode, let’s clear the previous pattern (via the console):
```
box.space.queue.drop()
box.snapshot()

```
Now, let’s restart our queue. Then, we add support of delay in put and release. If delay is passed on, the task’s status shall be changed to WAITING, and we have to define when it is subject to the procession. Another thing we need is a processor. For this, we can use background fibers. At any moment we can create a fiber that isn’t associated with any connections and works in the background. Let’s make a fiber that will work infinitely and await the nearest tasks.
```
function queue.put(data, opts)
    local id = gen_id()

    local runat = 0
    local status = STATUS.READY

    if opts and opts.delay then
        runat = clock.realtime() + tonumber(opts.delay)
        status = STATUS.WAITING
    else
        if queue._wait:has_readers() then
            queue._wait:put(true,0)
        end
    end

    return box.space.queue
        :insert{ id, status, runat, data }
        :tomap{ names_only=true }
end

function queue.release(id, opts)
    local t, key = get_task(id)
    queue.taken[ key ] = nil
    queue.bysid[ box.session.id() ][ key ] = nil

    local runat = 0
    local status = STATUS.READY

    if opts and opts.delay then
        runat = clock.realtime() + tonumber(opts.delay)
        status = STATUS.WAITING
    else
        if queue._wait:has_readers() then queue._wait:put(true,0) end
    end

    return box.space.queue
        :update({t.id},{{ '=', F.status, status },{ '=', F.runat, runat }})
        :tomap{ names_only = true }
end

```
If a time comes for some of the tasks, we modify it, changing its status from waiting to ready and also notifying the clients that might be awaiting a task. Now, we put a delayed task. Call take, make sure that there are no ready tasks. Call it again with a timeout, which fits into the task’s appearance. As soon as it appears, we see it’s been done by the fiber queue.runat.
```
queue._runat = fiber.create(function()
    fiber.name('queue.runat')
    while true do
        local remaining

        local now = clock.realtime()
        for _,t in box.space.queue.index.runat
            :pairs( { 0 }, { iterator = 'GT' })
        do
            if t.runat > now then
                remaining = t.runat - now
                break
            else
                if t.status == STATUS.WAITING then
                    log.info("Runat: W->R %s",t.id)
                    if queue._wait:has_readers() then queue._wait:put(true,0) end
                    box.space.queue:update({ t.id }, {
                        {'=', F.status, STATUS.READY },
                        {'=', F.runat, 0 },
                    })
                else
                    log.error("Runat: bad status %s for %s", t.status, t.id)
                    box.space.queue:update({ t.id },{{ '=', F.runat, 0 }})
                end
            end
        end

        if not remaining or remaining > 1 then remaining = 1 end
        fiber.sleep(remaining)
    end
end)

```

**Monitoring**
--------------

Never forget about monitoring the queue, because it can extend too much or even run out. We can count the number of tasks with every status in the queue and start sending the data to monitoring.
```
function queue.stats()
    return {
        total   = box.space.queue:len(),
        ready   = box.space.queue.index.status:count({STATUS.READY}),
        waiting = box.space.queue.index.status:count({STATUS.WAITING}),
        taken   = box.space.queue.index.status:count({STATUS.TAKEN}),
    }    
end


tarantool> queue.stats()
---
- ready: 10
  taken: 2
  waiting: 5
  total: 17
...

tarantool> local clock = require 'clock' local s = clock.time() local r = queue.stats() return r, clock.time() - s
---
- ready: 10
  taken: 2
  waiting: 5
  total: 17
- 0.00057339668273926
...

```
Such monitoring will work quite fast as long as there are not too many tasks. The normal state of the queue is empty. But suppose we have a million tasks. Our stats function still shows the correct value but works rather slowly. The issue is caused by the index:count call — this is always a full scan by index. Let’s cash the values of the counters.
```
queue._stats = {}
for k,v in pairs(STATUS) do
    queue._stats[v] = 0LL
end

for _,t in box.space.queue:pairs() do
    queue._stats[ t[F.status] ] = (queue._stats[ t[F.status] ] or 0LL)+1
end

function queue.stats()
    return {
        total   = box.space.queue:len(),
        ready   = queue._stats[ STATUS.READY ],
        waiting = queue._stats[ STATUS.WAITING ],
        taken   = queue._stats[ STATUS.TAKEN ],
    }
end

```
Now, this function will work very fast regardless of the number of records. We only have to update the counters at any operations. Prior to every operation, we have to reduce one value and increase the other. We also can manually set updates of the functions, but errors and contradictions are possible. Luckily, Tarantool has triggers for spaces that are capable of tracing any changes in the space. You can even manually execute space:update or space:delete – the trigger will take that into account, too. The trigger will account for all the statuses according to the value used in the database. At the restart, we’ll once account for the values of all the counters.
```
box.space.queue:on_replace(function(old,new)
    if old then
        queue._stats[ old[ F.status ] ] = queue._stats[ old[ F.status ] ] - 1
    end
    if new then
        queue._stats[ new[ F.status ] ] = queue._stats[ new[ F.status ] ] + 1
    end
end)

```
There is one more operation that can’t be traced in the space directly but affects its content: space:truncate(). To monitor the clearing of the space a special space trigger can be used — _truncate.
```
box.space._truncate:on_replace(function(old,new)
    if new.id == box.space.queue.id then
        for k,v in pairs(queue._stats) do
            queue._stats[k] = 0LL
        end
    end
end)

```
After that everything will work accurately and consistently. Statistics can be sent over the network. Tarantool has convenient non-blocking sockets that can be used rather low-level, almost like in C. To demonstrate how it works let send the metrics in a Graphite format using UDP:
```
local socket = require 'socket'
local errno = require 'errno'

local graphite_host = '127.0.0.1'
local graphite_port = 2003

local ai = socket.getaddrinfo(graphite_host, graphite_port, 1, { type = 'SOCK_DGRAM' })
local addr,port
for _,info in pairs(ai) do
   addr,port = info.host,info.port
   break
end
if not addr then error("Failed to resolve host") end

queue._monitor = fiber.create(function()
    fiber.name('queue.monitor')
    fiber.yield()
    local remote = socket('AF_INET', 'SOCK_DGRAM', 'udp')
    while true do
        for k,v in pairs(queue.stats()) do
            local msg = string.format("queue.stats.%s %s %sn", k, tonumber(v), math.floor(fiber.time()))
            local res = remote:sendto(addr, port, msg)
            if not res then
                log.error("Failed to send: %s", errno.strerror(errno()))
            end
        end
        fiber.sleep(1)
    end
end)

```
or using TCP:
```
local socket = require 'socket'
local errno = require 'errno'

local graphite_host = '127.0.0.1'
local graphite_port = 2003

queue._monitor = fiber.create(function()
    fiber.name('queue.monitor')
    fiber.yield()
    while true do
        local remote =  require 'socket'.tcp_connect(graphite_host, graphite_port)
        if not remote then
            log.error("Failed to connect to graphite %s",errno.strerror())
            fiber.sleep(1)
        else
            while true do
                local data = {}
                for k,v in pairs(queue.stats()) do
                    table.insert(data,string.format("queue.stats.%s %s %sn",k,tonumber(v),math.floor(fiber.time())))
                end
                data = table.concat(data,'')
                if not remote:send(data) then
                    log.error("%s",errno.strerror())
                    break
                end
                fiber.sleep(1)
            end
        end
    end
end)

``` 
**Hot code reloading**
----------------------
An important feature of the Tarantool platform is hot code reloading. It is rarely required in regular apps, but when you have Gigabytes of data stored in the database and every reload takes time, hot reloading is quite helpful.  When Lua loads some code on require, the content of the file is interpreted, and the returned result is cashed in the system table package.loaded under the module’s name. Subsequent require calls of the same module won’t read the file again but will return its cached value. To make Lua reinterpret and redownload the file you just have to delete the relevant record from package.loaded[...] and call require again. You need to memorize what the runtime has preloaded because there won’t be files for reloading of inbuilt modules. The simplest code snippet for reload procession looks like:
```
require'strict'.on()
fiber = require 'fiber'

box.cfg{
    listen = '127.0.0.1:3301'
}
box.schema.user.grant('guest', 'super', nil, nil, { if_not_exists = true })

local not_first_run = rawget(_G,'_NOT_FIRST_RUN')
_NOT_FIRST_RUN = true
if not_first_run then
   for k,v in pairs(package.loaded) do
      if not preloaded[k] then
         package.loaded[k] = nil
      end
   end
else
   preloaded = {}
   for k,v in pairs(package.loaded) do
      preloaded[k] = true
   end
end

queue = require 'queue'

require'console'.start()
os.exit()

```
As the code reload is a typical and regular task, we already have a set module [package.reload](https://github.com/moonlibs/package-reload), which we use in most of the apps. It memorizes the file used to download data, the modules that were preloaded, and then provides a convenient call for reload initiation: package.reload().
```
require'strict'.on()
fiber = require 'fiber'

box.cfg{
    listen = '127.0.0.1:3301'
}
box.schema.user.grant('guest', 'super', nil, nil, { if_not_exists = true })

require 'package.reload'

queue = require 'queue'

require'console'.start()
os.exit()

```
To make the code reloadable, you should write it in a slightly different way. Mind that the code can be executed repeatedly. At first, it is executed at the first start, and subsequently, it is executed at reloading. We have to clearly process this situation.
```
local queue = {}
local old = rawget(_G,'queue')
if old then
    queue.taken = old.taken
    queue.bysid = old.bysid
    queue._triggers = old._triggers
    queue._stats = old._stats
    queue._wait = old._wait
    queue._runch = old._runch
    queue._runat = old._runat
else
    queue.taken = {}
    queue.bysid = {}
    queue._triggers = {}
    queue._stats = {}
    queue._wait = fiber.channel()
    queue._runch = fiber.cond()
    while true do
        local t = box.space.queue.index.status:pairs({STATUS.TAKEN}):nth(1)
        if not t then break end
        box.space.queue:update({ t.id }, {{'=', F.status, STATUS.READY }})
        log.info("Autoreleased %s at start", t.id)
    end
    for k,v in pairs(STATUS) do
        queue._stats[v] = 0LL
    end
    for _,t in box.space.queue:pairs() do
        queue._stats[ t[F.status] ] = (queue._stats[ t[F.status] ] or 0LL)+1
    end
    log.info("Perform initial stat counts %s", box.tuple.new{ queue._stats })
end

```
Besides, you need to remember about trigger reloading. If you leave the issue as is, every reload will cause the installation of an additional trigger. However, triggers support an indication of the old function, so the installation of the trigger returns it. That’s why we’ll just save the installation result to a variable and pass it on as an argument. At the first start, there will be no variable, and a new trigger will be installed. However, at subsequent loading, the trigger will be replaced.
```
queue._triggers.on_replace = box.space.queue:on_replace(function(old,new)
    if old then
        queue._stats[ old[ F.status ] ] = queue._stats[ old[ F.status ] ] - 1
    end
    if new then
        queue._stats[ new[ F.status ] ] = queue._stats[ new[ F.status ] ] + 1
    end
end, queue._triggers.on_replace)

queue._triggers.on_truncate = box.space._truncate:on_replace(function(old,new)
    if new.id == box.space.queue.id then
        for k,v in pairs(queue._stats) do
            queue._stats[k] = 0LL
        end
    end
end, queue._triggers.on_truncate)

queue._triggers.on_connect = box.session.on_connect(function()
    box.session.storage.peer = box.session.peer()
    log.info( "connected %s from %s", box.session.id(), box.session.storage.peer )
end, queue._triggers.on_connect)

queue._triggers.on_disconnect = box.session.on_disconnect(function()
    log.info( "disconnected %s from %s", box.session.id(), box.session.storage.peer )
    box.session.storage.destroyed = true

    local sid = box.session.id()
    local bysid = queue.bysid[ sid ]
    if bysid then
        while next(bysid) do
            for key, id in pairs(bysid) do
                log.info("Autorelease %s by disconnect", id);
                queue.taken[key] = nil
                bysid[key] = nil
                local t = box.space.queue:get(id)
                if t then
                    if queue._wait:has_readers() then queue._wait:put(true,0) end
                    box.space.queue:update({t.id},{{'=', F.status, STATUS.READY }})
                end
            end
        end
        queue.bysid[ sid ] = nil
    end
end, queue._triggers.on_disconnect)

```
Another essential element at reloading is fibers. A fiber is started in the background, and we don’t control it in any way. It has while ... true written, and it never stops and doesn’t reload on its own. To communicate with it we’ll need a channel or rather a fiber.cond: condition variable. There are several different approaches to fiber reload. For example, the old ones can be deleted with the fiber.kill call, but this is not a very consistent take on the issue, as we may call kill at the wrong time. This is why we usually use the fiber generation attribute: the fiber proceeds working only in the generation it has been created. At code reload, the generation changes and the fiber clearly ends. Moreover, we can prevent the simultaneous operation of several fibers, checking the status of the previous generation fiber.
```
queue._runat = fiber.create(function(queue, gen, old_fiber)
    fiber.name('queue.runat.'..gen)

    while package.reload.count == gen and old_fiber and old_fiber:status() ~= 'dead' do
        log.info("Waiting for old to die")
        queue._runch:wait(0.1)
    end

    log.info("Started...")
    while package.reload.count == gen do
        local remaining

        local now = clock.realtime()

        for _,t in box.space.queue.index.runat
            :pairs( {0}, { iterator = 'GT' })
        do
            if t.runat > now then
                remaining = t.runat - now
                break
            else
                if t.status == STATUS.WAITING then
                    log.info("Runat: W->R %s",t.id)
                    if queue._wait:has_readers() then queue._wait:put(true,0) end
                    box.space.queue:update({ t.id }, {
                        { '=', F.status, STATUS.READY },
                        { '=', F.runat, 0 },
                    })
                else
                    log.error("Runat: bad status %s for %s", t.status, t.id)
                    box.space.queue:update({ t.id },{{ '=', F.runat, 0 }})
                end
            end
        end

        if not remaining or remaining > 1 then remaining = 1 end
        queue._runch:wait(remaining)
    end

    queue._runch:broadcast()
    log.info("Finished")
end, queue, package.reload.count, queue._runat)
queue._runch:broadcast()

```
And in the end, at code reload you get an error saying the console is already on. This is how this situation can be dealt with:
```
if not fiber.self().storage.console then
    require'console'.start()
    os.exit()
end

```

**Let’s summarize**
-------------------

We’ve written a working network queue with delayed processing, automatic task return by means of triggers, statistics forwarding in Graphite using TCP, and explored quite a few issues. With average state-of-the-art hardware, such a queue will easily support the transmission of 20+ thousand messages per second. It contains about 300 code strings and can be compiled in a day, document studies included. Final files: **queue.lua:**
```
local clock = require 'clock'
local errno = require 'errno'
local fiber = require 'fiber'
local log = require 'log'
local msgpack = require 'msgpack'
local socket = require 'socket'

box.schema.create_space('queue',{ if_not_exists = true; })

box.space.queue:format( {
    { name = 'id';     type = 'number' },
    { name = 'status'; type = 'string' },
    { name = 'runat';  type = 'number' },
    { name = 'data';   type = '*'      },
} );

local F = {}
for no,def in pairs(box.space.queue:format()) do
    F[no] = def.name
    F[def.name] = no
end

box.space.queue:create_index('primary', {
   parts = { F.id, 'number' };
   if_not_exists = true;
})

box.space.queue:create_index('status', {
    parts = { F.status, 'string', F.id, 'number' };
    if_not_exists = true;
})

box.space.queue:create_index('runat', {
    parts = { F.runat, 'number', F.id, 'number' };
    if_not_exists = true;
})

local STATUS = {}
STATUS.READY = 'R'
STATUS.TAKEN = 'T'
STATUS.WAITING = 'W'

local queue = {}
local old = rawget(_G,'queue')
if old then
    queue.taken = old.taken
    queue.bysid = old.bysid
    queue._triggers = old._triggers
    queue._stats = old._stats
    queue._wait = old._wait
    queue._runch = old._runch
    queue._runat = old._runat
else
    queue.taken = {}
    queue.bysid = {}
    queue._triggers = {}
    queue._stats = {}
    queue._wait = fiber.channel()
    queue._runch = fiber.cond()
    while true do
        local t = box.space.queue.index.status:pairs({STATUS.TAKEN}):nth(1)
        if not t then break end
        box.space.queue:update({ t.id }, {{'=', F.status, STATUS.READY }})
        log.info("Autoreleased %s at start", t.id)
    end

    for k,v in pairs(STATUS) do queue._stats[v] = 0LL end
    for _,t in box.space.queue:pairs() do
        queue._stats[ t[F.status] ] = (queue._stats[ t[F.status] ] or 0LL)+1
    end
    log.info("Perform initial stat counts %s", box.tuple.new{ queue._stats })
end

local function gen_id()
    local new_id
    repeat
        new_id = clock.realtime64()
    until not box.space.queue:get(new_id)
    return new_id
end

local function keypack( key )
    return msgpack.encode( key )
end

local function keyunpack( data )
    return msgpack.decode( data )
end

queue._triggers.on_replace = box.space.queue:on_replace(function(old,new)
    if old then
        queue._stats[ old[ F.status ] ] = queue._stats[ old[ F.status ] ] - 1
    end
    if new then
        queue._stats[ new[ F.status ] ] = queue._stats[ new[ F.status ] ] + 1
    end
end, queue._triggers.on_replace)

queue._triggers.on_truncate = box.space._truncate:on_replace(function(old,new)
    if new.id == box.space.queue.id then
        for k,v in pairs(queue._stats) do
            queue._stats[k] = 0LL
        end
    end
end, queue._triggers.on_truncate)

queue._triggers.on_connect = box.session.on_connect(function()
    box.session.storage.peer = box.session.peer()
end, queue._triggers.on_connect)

queue._triggers.on_disconnect = box.session.on_disconnect(function()
    box.session.storage.destroyed = true
    local sid = box.session.id()
    local bysid = queue.bysid[ sid ]
    if bysid then
        log.info( "disconnected %s from %s", box.session.id(), box.session.storage.peer )
        while next(bysid) do
            for key, id in pairs(bysid) do
                log.info("Autorelease %s by disconnect", id);
                queue.taken[key] = nil
                bysid[key] = nil
                local t = box.space.queue:get(id)
                if t then
                    if queue._wait:has_readers() then queue._wait:put(true,0) end
                    box.space.queue:update({t.id},{{'=', F.status, STATUS.READY }})
                end
            end
        end
        queue.bysid[ sid ] = nil
    end
end, queue._triggers.on_disconnect)

queue._runat = fiber.create(function(queue, gen, old_fiber)
    fiber.name('queue.runat.'..gen)

    while package.reload.count == gen and old_fiber and old_fiber:status() ~= 'dead' do
        log.info("Waiting for old to die")
        queue._runch:wait(0.1)
    end

    log.info("Started...")
    while package.reload.count == gen do
        local remaining

        local now = clock.realtime()

        for _,t in box.space.queue.index.runat
            :pairs( {0}, { iterator = 'GT' })
        do
            if t.runat > now then
                remaining = t.runat - now
                break
            else
                if t.status == STATUS.WAITING then
                    log.info("Runat: W->R %s",t.id)
                    if queue._wait:has_readers() then queue._wait:put(true,0) end
                    box.space.queue:update({ t.id }, {
                        { '=', F.status, STATUS.READY },
                        { '=', F.runat, 0 },
                    })
                else
                    log.error("Runat: bad status %s for %s", t.status, t.id)
                    box.space.queue:update({ t.id },{{ '=', F.runat, 0 }})
                end
            end
        end

        if not remaining or remaining > 1 then remaining = 1 end
        queue._runch:wait(remaining)
    end

    queue._runch:broadcast()
    log.info("Finished")
end, queue, package.reload.count, queue._runat)
queue._runch:broadcast()

local graphite_host = '127.0.0.1'
local graphite_port = 2003
queue._monitor = fiber.create(function(gen)
    fiber.name('queue.mon.'..gen)
    fiber.yield()
    while package.reload.count == gen do
        local remote =  require 'socket'.tcp_connect(graphite_host, graphite_port)
        if not remote then
            log.error("Failed to connect to graphite %s",errno.strerror())
            fiber.sleep(1)
        else
            while package.reload.count == gen do
                local data = {}
                for k,v in pairs(queue.stats()) do
                    table.insert(data,string.format("queue.stats.%s %s %sn",k,tonumber(v),math.floor(fiber.time())))
                end
                data = table.concat(data,'')
                if not remote:send(data) then
                    log.error("%s",errno.strerror())
                    break
                end
                fiber.sleep(1)
            end
        end
    end
end, package.reload.count)

function queue.put(data, opts)
    local id = gen_id()

    local runat = 0
    local status = STATUS.READY
    if opts and opts.delay then
        runat = clock.realtime() + tonumber(opts.delay)
        status = STATUS.WAITING
    else
        if queue._wait:has_readers() then
            queue._wait:put(true,0)
        end
    end

    return box.space.queue
        :insert{ id, status, runat, data }
        :tomap{ names_only=true }
end

function queue.take(timeout)
    if not timeout then timeout = 0 end
    local now = fiber.time()
    local found
    while not found do
        found = box.space.queue.index.status
            :pairs({STATUS.READY},{ iterator = 'EQ' }):nth(1)
        if not found then
            local left = (now + timeout) - fiber.time()
            if left <= 0 then return end
            queue._wait:get(left)
        end
    end

    if box.session.storage.destroyed then return end

    local sid = box.session.id()
    log.info("Register %s by %s", found.id, sid)
    local key = keypack( found.id )
    queue.taken[ key ] = sid
    queue.bysid[ sid ] = queue.bysid[ sid ] or {}
    queue.bysid[ sid ][ key ] = found.id

    return box.space.queue
        :update( {found.id}, {{'=', F.status, STATUS.TAKEN }})
        :tomap{ names_only = true }
end

local function get_task( id )
    if not id then error("Task id required", 2) end
    id = tonumber64(id)
    local key = keypack(id)
    local t = box.space.queue:get{id}
    if not t then
        error(string.format( "Task {%s} was not found", id ), 2)
    end
    if not queue.taken[key] then
        error(string.format( "Task %s not taken by anybody", id ), 2)
    end
    if queue.taken[key] ~= box.session.id() then
        error(string.format( "Task %s taken by %d. Not you (%d)",
            id, queue.taken[key], box.session.id() ), 2)
    end
    return t, key
end

function queue.ack(id)
    local t, key = get_task(id)
    queue.taken[ key ] = nil
    queue.bysid[ box.session.id() ][ key ] = nil
    return box.space.queue:delete{t.id}:tomap{ names_only = true }
end

function queue.release(id, opts)
    local t, key = get_task(id)
    queue.taken[ key ] = nil
    queue.bysid[ box.session.id() ][ key ] = nil

    local runat = 0
    local status = STATUS.READY

    if opts and opts.delay then
        runat = clock.realtime() + tonumber(opts.delay)
        status = STATUS.WAITING
    else
        if queue._wait:has_readers() then queue._wait:put(true,0) end
    end

    return box.space.queue
        :update({t.id},{{'=', F.status, status },{ '=', F.runat, runat }})
        :tomap{ names_only = true }
end

function queue.stats()
    return {
        total   = box.space.queue:len(),
        ready   = queue._stats[ STATUS.READY ],
        waiting = queue._stats[ STATUS.WAITING ],
        taken   = queue._stats[ STATUS.TAKEN ],
    }
end

return queue

```**init.lua:**```
require'strict'.on()
fiber = require 'fiber'
require 'package.reload'

box.cfg{
    listen = '127.0.0.1:3301'
}
box.schema.user.grant('guest', 'super', nil, nil, { if_not_exists = true })

queue = require 'queue'

if not fiber.self().storage.console then
    require'console'.start()
    os.exit()
end

```