---
title: "Node metrics available inside of a container"
date: "2023-02-06T00:00:00+00:00"
tags: ["Kubernetes", "Monitoring", "PMM", "DBaaS", "Containers"]
categories: ['Cloud', 'PMM']
authors:
  - denys_kondratenko
images:
  - blog/2023/03/Container-Denys.jpg
slug: node-metrics-container
---

Several people asked me this question: Could we get Node metrics inside of a container?

Usually, this comes from the fact that PMM or standalone people run `node_exporter` inside a container. PMM does it as a sidecar along with many other exporters to monitor DBs, and `node_exporter` comes out of the box as a default one.
So people could see accurate data on dashboards, like Memory and CPU, that `node_exporter` reads inside the container.

My first reaction to this - the data is inaccurate, and if you need Node metrics, you need to run `node_exporter` on the Node so it has proper access to the host system (VM or HW).
By inaccurate, I mean - not all data is there, and this data could be accurate only sometimes in some environments.

But once a pretty technical person asked me, I needed to respond to this person with some tech details. There was correct data from PMM client coming from the Kubernetes container about the host it was running.

One of the things I came up with that was true - you wouldn't see the host process inside a container, and thus you wouldn't see who and how is consuming memory and CPU.

I need help understanding why Memory information, CPU, and others are correct.

So I performed a small investigation to refresh my memory and learn more about namespaces, cgroups, and containers.

## node_exporter

[node_exporter documentation](https://github.com/prometheus/node_exporter#docker) says:

> The `node_exporter` is designed to monitor the host system. It's not recommended
to deploy it as a Docker container because it requires access to the host system.

>For situations where Docker deployment is needed, some extra flags must be used to allow
the `node_exporter` access to the host namespaces.

>Be aware that any non-root mount points you want to monitor will need to be bind-mounted
into the container.

>If you start container for host monitoring, specify `path.rootfs` argument.
This argument must match path in bind-mount of host root. The node\_exporter will use
`path.rootfs` as prefix to access host filesystem.

```bash
docker run -d \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```

>On some systems, the timex collector requires an additional Docker flag, --cap-add=SYS_TIME, in order to access the required syscalls.

So right away, we can see that additional privileges are needed. More interestingly, not only access to the `/proc` and `/sys` is required, but to the whole `/`. Also, some additional capabilities are needed.

If we will look briefly at the `node_exporter` code, we will indeed find different technics it uses to gather data:

- `procfs` data
- `sysfs` data
- D-Bus socket (systemd data)
- system calls (timex)
- and probably more (udev, device data and etc)

## Container

Containers and their ecosystem is quite a big topic that is described many times. Please check out "Demystifying Containers" by [Sascha Grunert](https://www.suse.com/c/author/sgrunert/) and "Building containers by hand" by [Steve Ovens](https://www.redhat.com/sysadmin/users/steve-ovens). You can find them in [Links](#links) section.

What is related to my investigation is isolation from the host, and that is mostly `namespaces` and `cgroups`.

Other systems that are limiting access to the different files and calls inside a container:

1. capabilities
2. seccomp
3. selinux/apparmor
4. additional security options

### `namespaces` and `cgroup`

Let us focus only on `procfs`, where a lot of needed monitoring information comes from. I aim to understand why we have some data in `/proc` that corresponds to the host data and some that do not.

First, `/proc` is a [special filesystem](https://www.kernel.org/doc/html/latest/filesystems/proc.html) that acts as an interface to internal data structures in the kernel. It can obtain information about the system and change certain kernel parameters at runtime (sysctl).

It is also quite an old interface that was created before any `namespaces` and `cgroup`. Many different applications expect the data there, and thus it can't be easily namespaced.

Here is what was namespaced:

1. net
2. uts
3. ipc
4. pid
5. user
6. cgroups
7. time


Same in code:

- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/fs/proc/namespaces.c#n15
- https://elixir.bootlin.com/linux/latest/source/include/linux/proc_ns.h#L27

So it means that a lot of data under, for example, `/proc/net` would be container specific. Same for other subsystems.

But the biggest difference for monitoring when `namespaces` and `cgroup` are used is that container has the access only to its own `PID` namespace. That means that even if we see all available memory or CPU, we can't tell what processes from the host system could consume that. We could only see our namespace processes.

It is tough to tell what exactly namespaced under `/proc`. It looks like all the files (not dirs) under `/proc` are directly from the host kernel.

Thus we could see many files (they aren't real files) from the host/root namespace and many that are specific to the container namespace. 

For example, here you see uts (hostname) and network namespaces differences between root and container:
```sh
#container
[root@0d514d31c0a3 opt]$ cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo: 250045720  467744    0    0    0     0          0         0 250045720  467744    0    0    0     0       0          0
  tap0: 37944098    3043    0    0    0     0          0         0   173264    2426    0    0    0     0       0          0

#host
[dkondratenko@denlen ~]$ cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo: 1674394721 1671478    0    0    0     0          0         0 1674394721 1671478    0    0    0     0       0          0
enp2s0f0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
 wwan0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
wlp3s0: 3869584887 6162652    0 88037    0     0          0         0 1639861087 3732759    0    0    0     0       0          0
cni-podman0:    3688      53    0    0    0     0          0        53    22094     163    0    0    0     0       0          0
```

As you can see, network interfaces are different (`net`) and hostnames (`uts` namespace, `0d514d31c0a3` in the container and `denlen` in the host).

## Linux Capabilities and seccomp

[Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) allow access for the unprivileged processes to perform some actions/call in the system.
In [node_exporter](#node_exporter) section, we have seen an example of the `CAP_SYS_TIME` that is needed to gather some of the data.


[seccomp](https://en.wikipedia.org/wiki/Seccomp) is a computer security facility in the Linux kernel. seccomp allows a process to make a one-way transition into a "secure" state where it cannot make any system calls except exit(), sigreturn(), read(), and write() to already-open file descriptors.

So both systems further restrict access to the data that might be needed to gather monitoring information.

Docker, Podman have default seccomp filters:

- https://github.com/moby/moby/blob/master/profiles/seccomp/default.json
- https://github.com/containers/common/blob/main/pkg/seccomp/seccomp.json

## Linux Security Modules

Security-Enhanced Linux, [SELinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) is a Linux kernel security module that provides a mechanism for supporting access control security policies, including mandatory access controls (MAC). 

[AppArmor](AppArmor) ("Application Armor") is a Linux kernel security module that allows the system administrator to restrict programs' capabilities with per-program profiles.

Both of those could further restrict access inside the container. For example, here is the part of the [apparmor](https://docs.docker.com/engine/security/apparmor/#nginx-example-profile) profile:
```
  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,
```

So it is possible to restrict access even for those root `/proc` files that provide memory and CPU information.

## Additional security options

Container runtimes and tools could further harden security.

One example is masking mount points:

- https://docs.podman.io/en/latest/markdown/podman-run.1.html#security-opt-option
- https://github.com/containers/podman/blob/ab7f6095a17bd50477c30fc8c127a8604b5693a6/pkg/specgen/generate/config_linux.go#L91

```bash
[root@0d514d31c0a3 opt]$ mount | grep proc
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
tmpfs on /proc/acpi type tmpfs (ro,relatime,context="system_u:object_r:container_file_t:s0:c11,c680",size=0k,uid=1000,gid=1000,inode64)
devtmpfs on /proc/kcore type devtmpfs (rw,nosuid,seclabel,size=4096k,nr_inodes=1048576,mode=755,inode64)
devtmpfs on /proc/keys type devtmpfs (rw,nosuid,seclabel,size=4096k,nr_inodes=1048576,mode=755,inode64)
devtmpfs on /proc/latency_stats type devtmpfs (rw,nosuid,seclabel,size=4096k,nr_inodes=1048576,mode=755,inode64)
devtmpfs on /proc/timer_list type devtmpfs (rw,nosuid,seclabel,size=4096k,nr_inodes=1048576,mode=755,inode64)
tmpfs on /proc/scsi type tmpfs (ro,relatime,context="system_u:object_r:container_file_t:s0:c11,c680",size=0k,uid=1000,gid=1000,inode64)
proc on /proc/asound type proc (ro,relatime)
proc on /proc/bus type proc (ro,relatime)
proc on /proc/fs type proc (ro,relatime)
proc on /proc/irq type proc (ro,relatime)
proc on /proc/sys type proc (ro,relatime)
proc on /proc/sysrq-trigger type proc (ro,relatime)
```
>The default masked paths are /proc/acpi, /proc/kcore, /proc/keys, /proc/latency_stats, /proc/sched_debug, /proc/scsi, /proc/timer_list, /proc/timer_stats, /sys/firmware, and /sys/fs/selinux. The default paths that are read-only are /proc/asound, /proc/bus, /proc/fs, /proc/irq, /proc/sys, /proc/sysrq-trigger, /sys/fs/cgroup.

And indeed, masking memory information is straightforward:

```bash
podman run --detach --rm --replace=true --name=pmm-server -p 4443:443/tcp --security-opt=mask=/proc/meminfo:/proc/vmstat docker.io/percona/pmm-server:2
```

## Summary

Kubernetes support most of the above technics as well. And different Kubernetes platforms have different security hardness.

My knowledge at the beginning of this road needed to be deeper, but the conclusion stays the same - don't assume that any data inside the container is related to the host.

Looking at the technics, I didn't know before and an overall trend of hardening security for the container, my conclusion would be - it is incorrect to assume that `node_exporter` could read and provide any meaningful data about the host within the container.

Container runtimes, tools, systems, and platforms provide the full capability to shut down, fake, and abstract any data or access that `node_exporter` needs. And we couldn't control those - assume you have incorrect data.

## Links

### `procfs`

- https://www.kernel.org/doc/html/latest/filesystems/proc.html
- https://fabiokung.com/2014/03/13/memory-inside-linux-containers/

### `cgroup`

- https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- https://www.man7.org/linux/man-pages/man7/cgroups.7.html

### `namespaces`

- https://man7.org/linux/man-pages/man7/namespaces.7.html
- https://www.man7.org/linux/man-pages/man7/user_namespaces.7.html

### Containers

- https://www.suse.com/c/author/sgrunert/:
  * https://www.suse.com/c/demystifying-containers-part-i-kernel-space/
  * https://www.suse.com/c/demystifying-containers-part-iv-container-security/

- https://www.redhat.com/sysadmin/users/steve-ovens: 
  * https://www.redhat.com/sysadmin/7-linux-namespaces
  * https://www.redhat.com/sysadmin/building-container-namespaces
  * https://www.redhat.com/sysadmin/mount-namespaces
  * https://www.redhat.com/sysadmin/pid-namespace

### Linux Capabilities and Seccomp

- https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html
- https://man7.org/linux/man-pages/man7/capabilities.7.html
- https://docs.docker.com/engine/security/seccomp/
- https://github.com/moby/moby/blob/master/profiles/seccomp/default.json
- https://github.com/containers/common/blob/main/pkg/seccomp/seccomp.json

### Linux Security Modules

- https://docs.docker.com/engine/security/apparmor/
- https://docs.docker.com/engine/security/apparmor/#nginx-example-profile

### Kubernetes security

- https://kubernetes.io/docs/concepts/workloads/pods/user-namespaces/
- https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
- https://kubernetes.io/docs/concepts/security/pod-security-standards/
- https://kubernetes.io/docs/tutorials/security/apparmor/
- https://kubernetes.io/docs/tutorials/security/seccomp/
- https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/
- https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/
