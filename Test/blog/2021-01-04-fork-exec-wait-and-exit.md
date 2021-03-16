---
title: "fork, exec, wait and exit"
date: Mon, 04 Jan 2021 16:06:48 +0000
draft: false
images:
  - blog/2021/01/prozesswechsel.png
authors:
  - koehntopp
---


This is the [english version of a 2007 article](https://isotopp.github.io/2007/01/07/fork-exec-wait-und-exit.html). In [de.comp.os.unix.linux.misc](news:de.comp.os.unix.linux.misc) somebody asked:

> *   Are commands in a script executed strictly sequentially, that is, will the next command only be executed when the previous command has completed, or will the shell **automatically** start the next command if the system has spare capacity?
> *   Can I change the default behavior - whatever it may be - in any way?

If you are looking into the fine manual, it may explain at some point that the shell starts each command in a separate process. Then you may continue your thought process and ask what that actually means. As soon as you get to this stage, you may want to have a look at the Unix process lifecycle.

Processes and programs
----------------------

A program in Unix is a sequence of executable instructions on a disk. You can use the command _size_ to get a very cursory check of the structure and memory demands of the program, or use the various invocations of _objdump_ for a much more detailed view. The only aspect that is of interest to us is the fact that a program is a sequence of instructions and data (on disk) that may potentially be executed at some point in time, maybe even multiple times, maybe even concurrently. Such a program in execution is called a process. The process contains the code and initial data of the program itself, and the actual state at the current point in time for the current execution. That is the memory map and the associated memory (check /proc/_pid_/maps), but also the program counter, the processor registers, the stack, and finally the current root directory, the current directory, environment variables and the open files, plus a few other things (in modern Linux for example, we find the processes cgroups and namespace relationships, and so on - things became a lot more complicated since 1979). In Unix processes and programs are two different and independent things. You can run a program more than once, concurrently. For example, you can run two instances of the _vi_ editor, which edit two different texts. Program and initial data are the same: it is the same editor. But the state inside the processes is different: the text, the insert mode, cursor position and so on differ. From a programmers point of view, “the code is the same, but the variable values are differing”. A process can run more than one program: The currently running program is throwing itself away, but asks that the operating system loads a different program into the same process. The new program will inherit some reused process state, such as current directories, file handles, privileges and so on. All of that is done in original Unix, at the system level, with only four syscalls:

*   `fork()`
*   `exec()`
*   `wait()`
*   `exit()`


Usermode and Kernel
-------------------


![Usermode and Kernel](https://isotopp.github.io/uploads/prozesswechsel.png) 

_Context switching: Process 1 is running for a bit, but at (1) the kernel interrupts the execution and switches to process 2. Some time later, process 2 is frozen, and we context switch back to where we left off with (1), and so on. For each process, this seems to be seamless, but it happens in intervals that are not continous._ Whenever a Unix process does a system call (and at some other opportunities) the current process leaves the user context and the operating system code is being activated. This is privileged kernel code, and the activation is not quite a subroutine call, because not only is privileged mode activated, but also a kernel stack is being used and the CPU registers of the user process are saved. From the point of view of the kernel function, the user process that has called us is inert data and can be manipulated at will. The kernel will then execute the system call on behalf of the user program, and then will try to exit the kernel. The typical way to leave the kernel is through the scheduler. The scheduler will review the process list and current situation. It will then decide into which of all the different userland processes to exit. It will restore the chosen processes registers, then return into this processes context, using this processes stack. The chosen process may or may not be the one that made the system call. In short: Whenever you make a system call, you may (or may not) lose the CPU to another process. That’s not too bad, because this other process at some point has to give up the CPU and the kernel will then return into our process as if nothing happened. Our program is not being executed linearly, but in a sequence of subjectively linear segments, with breaks inbetween. During these breaks the CPU is working on segments of other processes that are also runnable.

fork() and exit()
-----------------

In traditional Unix the only way to create a process is using the `fork()` system call. The new process gets a copy of the current program, but new process id (pid). The process id of the parent process (the process that called `fork()`) is registered as the new processes parent pid (ppid) to build a process tree. In the parent process, `fork()` returns and delivers the new processes pid as a result. The new process also returns from the `fork()` system call (because that is when the copy was made), but the result of the `fork()` is 0. So `fork()` is a special system call. You call it once, but the function returns twice: Once in the parent, and once in the child process. `fork()` increases the number of processes in the system by one. Every Unix process always starts their existence by returning from a `fork()` system call with a 0 result, running the same program as the parent process. They can have different fates because the result of the `fork()` system call is different in the parent and child incarnation, and that can drive execution down different `if()` branches. In Code:

```
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

main(void) {
        pid\_t pid = 0;

        pid = fork();
        if (pid == 0) {
                printf("I am the child.\\n");
        }
        if (pid > 0) {
                printf("I am the parent, the child is %d.\\n", pid);
        }
        if (pid < 0) {
                perror("In fork():");
        }

        exit(0);
}
```  
Running this, we get:

```
kris@linux:/tmp/kris> make probe1
cc     probe1.c   -o probe1
kris@linux:/tmp/kris> ./probe1
I am the child.
I am the parent, the child is 16959.
```
We are defining a variable `pid` of the type `pid_t`. This variable saves the `fork()` result, and using it we activate one (“I am the child.”) or the other (“I am the parent”) branch of an if(). Running the program we get two result lines. Since we have only one variable, and this variable can have only one state, an instance of the program can only be in either one or the other branch of the code. Since we see two lines of output, two instances of the program with different values for `pid` must have been running. If we called `getpid()` and printed the result we could prove this by showing two different pids (change the program to do this as an exercise!). The `fork()` system call is entered once, but left twice, and increments the number of processes in the system by one. After finishing our program the number of processes in the system is as large as before. That means there must be another system call which decrements the number of system calls. This system call is `exit()`. `exit()` is a system call you enter once and never leave. It decrements the number of processes in the system by one. `exit()` also accepts an exit status as a parameter, which the parent process can receive (or even has to receive), and which communicates the fate of the child to the parent. In our example, all variants of the program call `exit()` - we are calling `exit()` in the child process, but also in the parent process. That means we terminate two processes. We can only do this, because even the parent process is a child, and in fact, a child of our shell. The shell does exactly the same thing we are doing:

```
bash (16957) --- calls fork() ---> bash (16958) --- becomes ---> probe1 (16958)

probe1 (16958) --- calls fork() ---> probe1 (16959) --> exit()
   |
   +---> exit()
```

`exit()` closes all files and sockets, frees all memory and then terminates the process. The parameter of `exit()` is the only thing that survives and is handed over to the parent process.

wait()
------

Our child process ends with an `exit(0)`. The 0 is the exit status of our program and can be shipped. We need to make the parent process pick up this value and we need a new system call for this. This system call is `wait()`. In Code:
```
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/wait.h>

main(void) {
        pid\_t pid = 0;
        int   status;

        pid = fork();
        if (pid == 0) {
                printf("I am the child.\\n");
                sleep(10);
                printf("I am the child, 10 seconds later.\\n");
        }
        if (pid > 0) {
                printf("I am the parent, the child is %d.\\n", pid);
                pid = wait(&status);
                printf("End of process %d: ", pid);
                if (WIFEXITED(status)) {
                        printf("The process ended with exit(%d).\\n", WEXITSTATUS(status));
                }
                if (WIFSIGNALED(status)) {
                        printf("The process ended with kill -%d.\\n", WTERMSIG(status));
                }
        }
        if (pid < 0) {
                perror("In fork():");
        }

        exit(0);
}
```
And the runtime protocol:
```
kris@linux:/tmp/kris> make probe2
cc     probe2.c   -o probe2
kris@linux:/tmp/kris> ./probe2
I am the child.
I am the parent, the child is 17399.
I am the child, 10 seconds later.
End of process 17399: The process ended with exit(0).
```
The variable `status` is passed to the system call `wait()` as a reference parameter, and will be overwritten by it. The value is a bitfield, containing the exit status and additional reasons explaining how the program ended. To decode this, C offers a number of macros with predicates such as `WIFEXITED()` or `WIFSIGNALED()`. We also get extractors, such as `WEXITSTATUS()` and `WTERMSIG()`. `wait()` also returns the pid of the process that terminated, as a function result. `wait()` stops execution of the parent process until either a signal arrives or a child process terminates. You can arrange for a SIGALARM to be sent to you in order to time bound the `wait()`.

The `init` program, and Zombies
-------------------------------

The program `init` with the pid 1 will do basically nothing but calling `wait()`: It waits for terminating processes and polls their exit status, only to throw it away. It also reads `/etc/inittab` and starts the programs configured there. When something from `inittab` terminates and is set to `respawn`, it will be restarted by `init`. When a child process terminates while the parent process is not (yet) waiting for the exit status, `exit()` will still free all memory, file handles and so on, but the `struct task` (basically the `ps` entry) cannot be thrown away. It may be that the parent process at some point in time arrives at a `wait()` and then we have to have the exit status, which is stored in a field in the `struct task`, so we need to retain it. And while the child process is dead already, the process list entry cannot die because the exit status has not yet been polled by the parent. Unix calls such processes without memory or other resouces associated _Zombies_. Zombies are visible in the process list when a process generator (a forking process) is faulty and does not `wait()` properly. They do not take up memory or any other resouces but the bytes that make up their `struct task`. The other case can happen, too: The parent process exits while the child moves on. The kernel will set the ppid of such children with dead parents to the constant value 1, or in other words: `init` inherits orphaned processes. When the child terminates, `init` will `wait()` for the exit status of the child, because that’s what `init` does. No Zombies in this case. When we observe the number of processes in the system to be largely constant over time, then the number of calls to `fork()`, `exit()` and `wait()` have to balanced. This is, because for each `fork()` there will be an `exit()` to match and for each `exit()` there must be a `wait()` somewhere. In reality, and in modern systems, the situation is a bit more complicated, but the original idea is as simple as this. We have a clean fork-exit-wait triangle that describes all processes.

exec()
------

So while `fork()` makes processes, `exec()` loads programs into processes that already exist. In Code:
```
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/wait.h>

main(void) {
        pid\_t pid = 0;
        int   status;

        pid = fork();
        if (pid == 0) {
                printf("I am the child.\\n");
                execl("/bin/ls", "ls", "-l", "/tmp/kris", (char \*) 0);
                perror("In exec(): ");
        }
        if (pid > 0) {
                printf("I am the parent, and the child is %d.\\n", pid);
                pid = wait(&status);
                printf("End of process %d: ", pid);
                if (WIFEXITED(status)) {
                        printf("The process ended with exit(%d).\\n", WEXITSTATUS(status));
                }
                if (WIFSIGNALED(status)) {
                        printf("The process ended with kill -%d.\\n", WTERMSIG(status));
                }
        }
        if (pid < 0) {
                perror("In fork():");
        }

        exit(0);
}
```
The runtime protocol:
```
kris@linux:/tmp/kris> make probe3
cc     probe3.c   -o probe3

kris@linux:/tmp/kris> ./probe3
I am the child.
I am the parent, the child is 17690.
total 36
-rwxr-xr-x 1 kris users 6984 2007-01-05 13:29 probe1
-rw-r--r-- 1 kris users  303 2007-01-05 13:36 probe1.c
-rwxr-xr-x 1 kris users 7489 2007-01-05 13:37 probe2
-rw-r--r-- 1 kris users  719 2007-01-05 13:40 probe2.c
-rwxr-xr-x 1 kris users 7513 2007-01-05 13:42 probe3
-rw-r--r-- 1 kris users  728 2007-01-05 13:42 probe3.c
End of process 17690: The process ended with exit(0).
```
Here the code of `probe3` is thrown away in the child process (the `perror("In exec():")` is not reached). Instead the running program is being replaced by the given call to `ls`. From the protocol we can see the parent instance of `probe3` waits for the `exit()`. Since the `perror()` after the `execl()`is never executed, it cannot be an `exit()` in our code. In fact, `ls` ends the process we made with an `exit()` and that is what we receive our exit status from in our parent processes `wait()` call.

The same, as a Shellscript
--------------------------

The examples above have been written in C. We can do the same, in `bash`:
```
kris@linux:/tmp/kris> cat probe1.sh
#! /bin/bash --

echo "Starting child:"
sleep 10 &
echo "The child is $!"
echo "The parent is $$"
echo "$(date): Parent waits."
wait
echo "The child $! has the exit status $?"
echo "$(date): Parent woke up."

kris@linux:/tmp/kris> ./probe1.sh
Starting child:
The child is 18071
The parent is 18070
Fri Jan  5 13:49:56 CET 2007: Parent waits.
The child 18071 has the exit status 0
Fri Jan  5 13:50:06 CET 2007: Parent woke up.
``` 

The actual bash
---------------

We can also trace the shell while it executes a single command. The information from above should allow us to understand what goes on, and see how the shell actually works.
```
kris@linux:~> strace -f -e execve,clone,fork,waitpid bash
kris@linux:~> ls
clone(Process 30048 attached
child\_stack=0, flags=CLONE\_CHILD\_CLEARTID|CLONE\_CHILD\_SETTID|SIGCHLD,
child\_tidptr=0xb7dab6f8) = 30048
\[pid 30025\] waitpid(-1, Process 30025 suspended
 <unfinished ...>
\[pid 30048\] execve("/bin/ls", \["/bin/ls", "-N", "--color=tty", "-T", "0"\],
\[/\* 107 vars \*/\]) = 0
...
Process 30025 resumed
Process 30048 detached
<... waitpid resumed> \[{WIFEXITED(s) && WEXITSTATUS(s) == 0}\], WSTOPPED
WCONTINUED) = 30048
--- SIGCHLD (Child exited) @ 0 (0) ---
...
```
Linux uses a generalization of the original Unix `fork()`, named `clone()`, to create child processes. That is why we do not see `fork()` in a Linux system to create a child process, but a `clone()` call with some parameters. Linux also uses a specialized variant of `wait()`, called `waitpid()`, to wait for a specific pid. Linux finally uses the `exec()` variant `execve()` to load programs, but that is just shuffling the paramters around. At the end of `ls` (PID 30048) the process 30025 will wake up from the `wait()` and continue.

Original Code, what Windows does, and what Microsoft thinks about Linux
-----------------------------------------------------------------------

This text is based on [a USENET article](http://groups.google.com/group/de.comp.os.unix.linux.misc/msg/4035c67415f9bc09) I wrote a long time ago. [Here](https://minnie.tuhs.org/cgi-bin/utree.pl?file=V7/usr/src/cmd/sh/xec.c) is the original C-code of the original `sh` from 1979, with the `fork()` system call. Search for `case TFORK:`. Also, check out the programming style of Mr. Bourne - this is C, even if it does not look like it. The [original 2007 blog article](https://isotopp.github.io/2007/01/07/fork-exec-wait-und-exit.html), has a followup article [on Windows CreateProcess()](https://isotopp.github.io/2007/01/07/fork-und-exec-vs-createprocess.html), which has not been translated. When implementing `fork()` in Windows as part of the WSL 1, Microsoft ran into a lot of problems with the syscall, and wrote an article about how they hate it, and why they think their `CreateProcessEx()` (in Unix: `spawn()`) would be better. The [PDF](https://www.microsoft.com/en-us/research/uploads/prod/2019/04/fork-hotos19.pdf) makes a number of good points, but is still wrong. :-)

First published on [https://blog.koehntopp.info/](https://blog.koehntopp.info/) and syndicated here with permission of the author.