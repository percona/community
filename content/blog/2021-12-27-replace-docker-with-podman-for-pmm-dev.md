---
title: "How to replace `docker` with `podman` for PMM development"
date: "2021-12-27T00:00:00+00:00"
tags: ['PMM', 'docker-compose', 'goreleaser', 'docker', 'podman']
authors:
  - denys_kondratenko
images:
  - superhero.png
slug: replace-docker-with-podman-for-pmm-dev
---

Lets try to find the use cases where it is not possible or not suitable to do.

Looks like for Linux it is quite possible, but the experience could be different on MacOS or Windows.

I would use Fedora 35 distro in examples bellow, first lets install `podman` and start needed tools:
```sh
$ sudo dnf install podman docker-compose
$ systemctl --user start podman.socket
```
* we still need `docker-compose` as most of PMM tooling is built around it
* starting `podman.socket` so compose would actually talk to `podman` instead of `docker` socket

## pmm-managed

First lets try to compile and run `pmm-managed`.

### podman.socket
```sh
$ make env-up
...
  File "/usr/lib/python3.10/site-packages/docker/transport/unixconn.py", line 30, in connect
    sock.connect(self.unix_socket)
FileNotFoundError: [Errno 2] No such file or directory
...

$ systemctl --user status podman.socket
● podman.socket - Podman API Socket
     Loaded: loaded (/usr/lib/systemd/user/podman.socket; disabled; vendor preset: disabled)
     Active: active (listening) since Wed 2021-12-22 22:50:33 CET; 1h 12min ago
   Triggers: ● podman.service
       Docs: man:podman-system-service(1)
     Listen: /run/user/1000/podman/podman.sock (Stream)
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/podman.socket

$ DOCKER_HOST=unix:///run/user/1000/podman/podman.sock make env-up
$ # ^^^that or exporting env would get us to the next stage
```
`docker-compose` that is used to bring up environment couldn't connect to the docker daemon and thus failing. There is an env var to point to the right socket to talk to so lets find out the socket path and set it.

Set that var in your environment (`.bashrc` or similar) or I set it in the current session:
```sh
$ export DOCKER_HOST=unix:///run/user/1000/podman/podman.sock
```

### short-name image resolution
```sh
$ make env-up
Pulling pmm-managed-server ... error

ERROR: for pmm-managed-server  failed to resolve image name: short-name resolution enforced but cannot prompt without a TTY
ERROR: failed to resolve image name: short-name resolution enforced but cannot prompt without a TTY

$ DOCKER_HOST=unix:///run/podman/podman.sock PMM_SERVER_IMAGE=docker.io/perconalab/pmm-server:dev-latest make env-up
```
Now it has failed because the system doesn't accept the short names for images, but there is another env for it `PMM_SERVER_IMAGE`.

The short image name resolution we could tune in the system, `/etc/containers/registries.conf` says:
```
For more information on this configuration file, see containers-registries.conf(5).
#
# NOTE: RISK OF USING UNQUALIFIED IMAGE NAMES
# We recommend always using fully qualified image names including the registry
# server (full dns name), namespace, image name, and tag
# (e.g., registry.redhat.io/ubi8/ubi:latest). Pulling by digest (i.e.,
# quay.io/repository/name@digest) further eliminates the ambiguity of tags.
# When using short names, there is always an inherent risk that the image being
# pulled could be spoofed. For example, a user wants to pull an image named
# `foobar` from a registry and expects it to come from myregistry.com. If
# myregistry.com is not first in the search list, an attacker could place a
# different `foobar` image at a registry earlier in the search list. The user
# would accidentally pull and run the attacker's image and code rather than the
# intended content. We recommend only adding registries which are completely
# trusted (i.e., registries which don't allow unknown or anonymous users to
# create accounts with arbitrary names). This will prevent an image from being
# spoofed, squatted or otherwise made insecure.  If it is necessary to use one
# of these registries, it should be added at the end of the list.
```

The way to go is to alias names for example in `/etc/containers/registries.conf.d/001-shortnames-den.conf`:
```
[aliases]
  # docker
  "perconalab/pmm-server" = "docker.io/perconalab/pmm-server"
  "goreleaser/goreleaser" = "docker.io/goreleaser/goreleaser"
  "moby/buildkit" = "docker.io/moby/buildkit"
  "mongo" = "docker.io/library/mongo"
```
In this way we don't need to set `PMM_SERVER_IMAGE`:
```sh
$ make env-up
```

Please also note other aliases that I have added as I progressed through this experiment, I needed them all to run later.

### security-opt parameter
```sh
$ make env-up
...
ERROR: for pmm-managed-server  Cannot create container for service pmm-managed-server: fill out specgen: invalid --security-opt 1: "seccomp:unconfined"
https://github.com/containers/podman/blob/7dabcbd7bcf78f3b5d310ed547801106da382618/pkg/specgenutil/specgen.go#L544
```

OK, that is more interesting. In `pmm-managed` compose file:
```yaml
    security_opt:
      - seccomp:unconfined
```
I googled it and found out [this fix](https://github.com/containers/podman-compose/commit/bbaa7867399b91255859b959535fedd7c20daacc) for `podman-compose`. There they just replaced `:` with `=`.
OK, if I try that - it works:
```yaml
    security_opt:
      - seccomp=unconfined
```
It passes it correctly and podman happy.

Probably docker would be happy as well, as they support both `:` and `=`:
* https://github.com/docker/cli/blob/9de1b162f/cli/command/container/opts.go#L673
* https://github.com/docker/compose/blob/a9e8164a8d2796847c83a38a2f7cd9f19a13b940/pkg/compose/create.go#L401

Looks like devs weren't sure which one is correct or there were no standard on the date `:` was added. But looks like `=` is a correct one. So we need to test it with docker and just change.

Bellow I have changed compose file with `=`.

### Makefile not parametrized
```sh
$ make env-up
...
Creating pmm-managed-server ... done
compose.parallel.feed_queue: Pending: set()
compose.parallel.parallel_execute_iter: Finished processing: <Service: pmm-managed-server>
compose.parallel.feed_queue: Pending: set()
docker exec -it --workdir=/root/go/src/github.com/percona/pmm-managed pmm-managed-server .devcontainer/setup.py
make: docker: No such file or directory
make: *** [Makefile:12: env-devcontainer] Error 127
```

Now it couldn't find `docker` executable, it is hardcoded in the Makefile:
```
env-devcontainer:
        docker exec -it --workdir=/root/go/src/github.com/percona/pmm-managed pmm-managed-server .devcontainer/setup.py
```

So we can't just alias it in bash, but need a link:
```sh
$ sudo ln -s /usr/bin/podman /usr/bin/docker
```

Other way to do it is to use some variable in the `Makefile` to be able to take executable as a parameter.

### Success
Implementing all above:
```sh
$ make env-up
...
> supervisorctl start pmm-managed
pmm-managed: started
Done in 129.057330132
```

Actually not that bad, what we have done:
* prepared system environment: socket, env var, link, aliases
* fixed minor non-standard parameter

All of that needs to be done once and after that there is no difference on running podman, except that it runs in user mode and don't require privileged daemon ;-)

## mongodb_exporter

Lets test if we can build it using `goreleaser` with `podman` as well as let's try to bring up some more complex testing environment with `docker-compose`.

### goreleaser

https://goreleaser.com/install/#running-with-docker :
```sh
podman run --privileged --rm -v $PWD:/go/src/github.com/user/repo -v /run/user/1000/podman/podman.sock:/var/run/docker.sock -w /go/src/github.com/user/repo goreleaser/goreleaser release --snapshot --skip-publish --rm-dist
```
So we know that we have different socket already so we are passing it, as well as we already have alias for the short-name (for `goreleaser` as well as for the `buildx`). And it just works:
```sh
$ podman run --privileged --rm -v $PWD:/go/src/github.com/user/repo -v /run/user/1000/podman/podman.sock:/var/run/docker.sock -w /go/src/github.com/user/repo goreleaser/goreleaser release --snapshot --skip-publish --rm-dist
   • releasing...
...
   • building binaries
      • building                  binary=/go/src/github.com/user/repo/build/mongodb_exporter_darwin_arm64/mongodb_exporter
      • building                  binary=/go/src/github.com/user/repo/build/mongodb_exporter_darwin_amd64/mongodb_exporter
      • building                  binary=/go/src/github.com/user/repo/build/mongodb_exporter_linux_arm64/mongodb_exporter
      • building                  binary=/go/src/github.com/user/repo/build/mongodb_exporter_linux_amd64/mongodb_exporter
      • building                  binary=/go/src/github.com/user/repo/build/mongodb_exporter_linux_arm_7/mongodb_exporter
...
   • archives
      • creating                  archive=build/mongodb_exporter-88c186c.linux-arm64.tar.gz
      • creating                  archive=build/mongodb_exporter-88c186c.linux-amd64.tar.gz
      • creating                  archive=build/mongodb_exporter-88c186c.linux-arm.tar.gz
      • creating                  archive=build/mongodb_exporter-88c186c.darwin-arm64.tar.gz
      • creating                  archive=build/mongodb_exporter-88c186c.darwin-amd64.tar.gz
   • linux packages
      • creating                  arch=arm7 file=build/mongodb_exporter-88c186c.linux-arm.rpm format=rpm package=mongodb_exporter
      • creating                  arch=arm64 file=build/mongodb_exporter-88c186c.linux-arm64.deb format=deb package=mongodb_exporter
      • creating                  arch=arm64 file=build/mongodb_exporter-88c186c.linux-arm64.rpm format=rpm package=mongodb_exporter
      • creating                  arch=amd64 file=build/mongodb_exporter-88c186c.linux-64-bit.rpm format=rpm package=mongodb_exporter
      • creating                  arch=amd64 file=build/mongodb_exporter-88c186c.linux-64-bit.deb format=deb package=mongodb_exporter
      • creating                  arch=arm7 file=build/mongodb_exporter-88c186c.linux-arm.deb format=deb package=mongodb_exporter
   • calculating checksums
      • checksumming              file=mongodb_exporter-88c186c.linux-64-bit.rpm
      • checksumming              file=mongodb_exporter-88c186c.linux-amd64.tar.gz
      • checksumming              file=mongodb_exporter-88c186c.linux-64-bit.deb
      • checksumming              file=mongodb_exporter-88c186c.linux-arm64.rpm
      • checksumming              file=mongodb_exporter-88c186c.linux-arm64.tar.gz
      • checksumming              file=mongodb_exporter-88c186c.darwin-amd64.tar.gz
      • checksumming              file=mongodb_exporter-88c186c.darwin-arm64.tar.gz
      • checksumming              file=mongodb_exporter-88c186c.linux-arm.deb
      • checksumming              file=mongodb_exporter-88c186c.linux-arm64.deb
      • checksumming              file=mongodb_exporter-88c186c.linux-arm.rpm
      • checksumming              file=mongodb_exporter-88c186c.linux-arm.tar.gz
   • docker images
      • building docker image     image=percona/mongodb_exporter:0.30
      • pipe skipped              error=publishing is disabled
   • storing artifact list
      • writing                   file=build/artifacts.json
   • release succeeded after 66.48s

$ ls -la build/
total 55592
drwxr-xr-x.  8 dkondratenko dkondratenko    4096 Dec 22 23:35 .
drwxrwxr-x. 11 dkondratenko dkondratenko    4096 Dec 22 23:34 ..
-rw-------.  1 dkondratenko dkondratenko    9932 Dec 22 23:35 artifacts.json
-rw-r--r--.  1 dkondratenko dkondratenko    3931 Dec 22 23:34 config.yaml
drwx------.  2 dkondratenko dkondratenko     146 Dec 22 23:35 goreleaserdocker741570390
-rw-r--r--.  1 dkondratenko dkondratenko    1190 Dec 22 23:35 mongodb_exporter_88c186c_checksums.txt
-rw-r--r--.  1 dkondratenko dkondratenko 5555136 Dec 22 23:35 mongodb_exporter-88c186c.darwin-amd64.tar.gz
-rw-r--r--.  1 dkondratenko dkondratenko 5467991 Dec 22 23:35 mongodb_exporter-88c186c.darwin-arm64.tar.gz
-rw-r--r--.  1 dkondratenko dkondratenko 5362664 Dec 22 23:35 mongodb_exporter-88c186c.linux-64-bit.deb
-rw-r--r--.  1 dkondratenko dkondratenko 5345376 Dec 22 23:35 mongodb_exporter-88c186c.linux-64-bit.rpm
-rw-r--r--.  1 dkondratenko dkondratenko 5351467 Dec 22 23:35 mongodb_exporter-88c186c.linux-amd64.tar.gz
-rw-r--r--.  1 dkondratenko dkondratenko 4914988 Dec 22 23:35 mongodb_exporter-88c186c.linux-arm64.deb
-rw-r--r--.  1 dkondratenko dkondratenko 4902660 Dec 22 23:35 mongodb_exporter-88c186c.linux-arm64.rpm
-rw-r--r--.  1 dkondratenko dkondratenko 4908794 Dec 22 23:35 mongodb_exporter-88c186c.linux-arm64.tar.gz
-rw-r--r--.  1 dkondratenko dkondratenko 5028350 Dec 22 23:35 mongodb_exporter-88c186c.linux-arm.deb
-rw-r--r--.  1 dkondratenko dkondratenko 5015878 Dec 22 23:35 mongodb_exporter-88c186c.linux-arm.rpm
-rw-r--r--.  1 dkondratenko dkondratenko 5023920 Dec 22 23:35 mongodb_exporter-88c186c.linux-arm.tar.gz
drwxr-xr-x.  2 dkondratenko dkondratenko      30 Dec 22 23:35 mongodb_exporter_darwin_amd64
drwxr-xr-x.  2 dkondratenko dkondratenko      30 Dec 22 23:35 mongodb_exporter_darwin_arm64
drwxr-xr-x.  2 dkondratenko dkondratenko      30 Dec 22 23:35 mongodb_exporter_linux_amd64
drwxr-xr-x.  2 dkondratenko dkondratenko      30 Dec 22 23:35 mongodb_exporter_linux_arm64
drwxr-xr-x.  2 dkondratenko dkondratenko      30 Dec 22 23:35 mongodb_exporter_linux_arm_7

$ ls -la build/goreleaserdocker741570390/
total 25144
drwx------. 2 dkondratenko dkondratenko      146 Dec 22 23:35 .
drwxr-xr-x. 8 dkondratenko dkondratenko     4096 Dec 22 23:35 ..
-rw-r--r--. 1 dkondratenko dkondratenko      244 Dec 22 23:35 Dockerfile
-rwxr-xr-x. 1 dkondratenko dkondratenko 15024128 Dec 22 23:35 mongodb_exporter
-rw-r--r--. 1 dkondratenko dkondratenko  5362664 Dec 22 23:35 mongodb_exporter-88c186c.linux-64-bit.deb
-rw-r--r--. 1 dkondratenko dkondratenko  5345376 Dec 22 23:35 mongodb_exporter-88c186c.linux-64-bit.rpm

$ podman images
REPOSITORY                                 TAG              IMAGE ID      CREATED        SIZE
localhost/percona/mongodb_exporter         88c186c          23d41a482eb4  3 minutes ago  15.2 MB
localhost/percona/mongodb_exporter         0.30             23d41a482eb4  3 minutes ago  15.2 MB
```

### docker-compose

There is compose file to bring test environment for the `mongodb_exporter`. Lets try to bring it up (also notice that mongo alias was added above to resolve short-name):
```sh
$ docker-compose up

```

`links` don't work. Also in compose doc they are kind of deprecated:
* https://docs.docker.com/compose/compose-file/compose-file-v3/#links

So I just deleted all links and it works: 
```sh
$ docker-compose up
Creating mongo-cnf-1     ... done
Creating mongo-cnf-3     ... done
Creating mongo-1-3       ... done
Creating mongo-1-1       ... done
Creating mongo-2-2       ... done
Creating mongo-2-arbiter ... done
Creating mongo-2-3       ... done
Creating mongo-2-1       ... done
Creating standalone      ... done
Creating mongo-1-2       ... done
Creating mongo-cnf-2     ... done
Creating mongo-1-arbiter ... done
Creating mongo-rs2-setup ... done
Creating mongo-cnf-setup ... done
Creating mongo-rs1-setup ... done
Creating mongos          ... done
Creating mongo-shard-setup ... done
Attaching to mongo-2-arbiter, mongo-cnf-1, mongo-1-3, mongo-2-2, mongo-1-2, mongo-2-3, standalone, mongo-cnf-3, mongo-1-1, mongo-2-1, mongo-cnf-2, mongo-1-arbiter, mongo-rs2-setup, mongo-cnf-setup, mongo-rs1-setup, mongos, mongo-shard-setup

...

mongo-cnf-1          | 2021-12-23T22:53:02.806+0000 I  NETWORK  [listener] connection accepted from 10.89.0.33:58362 #56 (33 connections now open)
mongo-cnf-1          | 2021-12-23T22:53:02.807+0000 I  NETWORK  [conn56] received client metadata from 10.89.0.33:58362 conn56: { driver: { name: "NetworkInterfaceTL", version: "4.2.17" }, os: { type: "Linux", name: "Ubuntu", architecture: "x86_64", version: "18.04" } }
mongo-shard-setup    | --- Sharding Status ---
mongo-shard-setup    |   sharding version: {
mongo-shard-setup    |   	"_id" : 1,
mongo-shard-setup    |   	"minCompatibleVersion" : 5,
mongo-shard-setup    |   	"currentVersion" : 6,
mongo-shard-setup    |   	"clusterId" : ObjectId("61c4fdcc0039e75de22fa8bd")
mongo-shard-setup    |   }
mongo-shard-setup    |   shards:
mongo-shard-setup    |         {  "_id" : "rs1",  "host" : "rs1/10.89.0.16:27017,10.89.0.18:27017,10.89.0.22:27017",  "state" : 1 }
mongo-shard-setup    |         {  "_id" : "rs2",  "host" : "rs2/10.89.0.17:27017,10.89.0.19:27017,10.89.0.23:27017",  "state" : 1 }
mongo-shard-setup    |   active mongoses:
mongo-shard-setup    |         "4.2.17" : 1
mongo-shard-setup    |   autosplit:
mongo-shard-setup    |         Currently enabled: yes
mongo-shard-setup    |   balancer:
mongo-shard-setup    |         Currently enabled:  yes
mongo-shard-setup    |         Currently running:  no
mongo-shard-setup    |         Failed balancer rounds in last 5 attempts:  0
mongo-shard-setup    |         Migration Results for the last 24 hours:
mongo-shard-setup    |                 No recent migrations
mongo-shard-setup    |   databases:
mongo-shard-setup    |         {  "_id" : "config",  "primary" : "config",  "partitioned" : true }
mongo-shard-setup    |
mongo-shard-setup    | bye
mongos               | 2021-12-23T22:53:02.833+0000 I  NETWORK  [conn14] end connection 10.89.0.35:40380 (0 connections now open)
mongo-shard-setup exited with code 0
mongos               | 2021-12-23T22:53:03.806+0000 I  CONNPOOL [TaskExecutorPool-0] Connecting to 10.89.0.24:27017
mongos               | 2021-12-23T22:53:03.806+0000 I  CONNPOOL [TaskExecutorPool-0] Connecting to 10.89.0.21:27017
mongo-cnf-2          | 2021-12-23T22:53:03.807+0000 I  NETWORK  [listener] connection accepted from 10.89.0.33:47564 #31 (20 connections now open)
mongo-cnf-2          | 2021-12-23T22:53:03.808+0000 I  NETWORK  [conn31] received client metadata from 10.89.0.33:47564 conn31: { driver: { name: "NetworkInterfaceTL", version: "4.2.17" }, os: { type: "Linux", name: "Ubuntu", architecture: "x86_64", version: "18.04" } }
mongo-cnf-3          | 2021-12-23T22:53:03.807+0000 I  NETWORK  [listener] connection accepted from 10.89.0.33:54550 #28 (17 connections now open)
mongo-cnf-3          | 2021-12-23T22:53:03.809+0000 I  NETWORK  [conn28] received client metadata from 10.89.0.33:54550 conn28: { driver: { name: "NetworkInterfaceTL", version: "4.2.17" }, os: { type: "Linux", name: "Ubuntu", architecture: "x86_64", version: "18.04" } }
^CGracefully stopping... (press Ctrl+C again to force)
Stopping mongo-2-2         ... done
Stopping mongo-1-1         ... done
Stopping mongo-cnf-1       ... done
Stopping mongo-cnf-2       ... done
Stopping mongo-2-arbiter   ... done
Stopping mongo-2-3         ... done
Stopping mongo-cnf-3       ... done
Stopping standalone        ... done
Stopping mongos            ... done
Stopping mongo-1-arbiter   ... done
Stopping mongo-1-3         ... done
Stopping mongo-2-1         ... done
Stopping mongo-1-2         ... done
```

So this case shows that compose standard isn't that stable. And those probably just could be easily removed and `podman` could be used in this case as well.

## SELinux notes

If you have SELinux enabled, as I do:
```
$ sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     actual (secure)
Max kernel policy version:      33
```

You would need some additional changes and system tunning. It is mostly related to the volume binds.

### `pmm-managed`

Compose file for `pmm-managed` has 2 volumes binded that without additional option would through errors like:

```sh
docker exec -it --workdir=/root/go/src/github.com/percona/pmm-managed pmm-managed-server .devcontainer/setup.py
/usr/bin/python2: can't open file '/root/go/src/github.com/percona/pmm-managed/.devcontainer/setup.py': [Errno 13] Permission denied
make: *** [Makefile:12: env-devcontainer] Error 2
```
and in case of `go-modules`:
```sh
go: downloading golang.org/x/perf v0.0.0-20210220033136-40a54f11e909
mkdir /root/go/pkg/mod/cache: permission denied
tools.go:37: running "go": exit status 1
make: *** [init] Error 1
Traceback (most recent call last):
  File "/root/go/src/github.com/percona/pmm-managed/.devcontainer/setup.py", line 129, in <module>
    main()
  File "/root/go/src/github.com/percona/pmm-managed/.devcontainer/setup.py", line 116, in main
    make_init()
  File "/root/go/src/github.com/percona/pmm-managed/.devcontainer/setup.py", line 75, in make_init
    "make init",
  File "/root/go/src/github.com/percona/pmm-managed/.devcontainer/setup.py", line 19, in run_commands
    subprocess.check_call(cmd, shell=True)
  File "/usr/lib64/python2.7/subprocess.py", line 542, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command 'make init' returned non-zero exit status 2
make: *** [Makefile:12: env-devcontainer] Error 1
```

Documentation for `podman-run` [clarifies it](https://docs.podman.io/en/latest/markdown/podman-run.1.html#volume-v-source-volume-host-dir-container-dir-options):
```
To change a label in the container context, you can add either of two suffixes :z or :Z to the volume mount. These suffixes tell Podman to relabel file objects on the shared volumes. The z option tells Podman that two containers share the volume content. As a result, Podman labels the content with a shared content label. Shared volume labels allow all containers to read/write content. The Z option tells Podman to label the content with a private unshared label.
```

Here we need `:Z` option:
```yaml
    volumes:
      - .:/root/go/src/github.com/percona/pmm-managed:Z
      - ./Makefile.devcontainer:/root/go/src/github.com/percona/pmm-managed/Makefile:ro
      - go-modules:/root/go/pkg/mod:Z # Put modules cache into a separate volume
```

### `mongodb-exporter`

Compose for `mongodb_exporter` also contains volume binds, but it is shared across different container abd thus needs to be binded with `:z` option:
```yaml
        volumes:
          - ./docker/scripts:/scripts:z
```
Here is additional info:
* https://docs.podman.io/en/latest/markdown/podman-run.1.html#volumes-from-container-options
* https://github.com/containers/podman/issues/10779
* https://docs.podman.io/en/latest/markdown/podman-run.1.html#volume-v-source-volume-host-dir-container-dir-options

### MongoDB SELinux

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/#std-label-install-rhel-configure-selinux


## devcontainers

If someone uses VSCode and would like to use devcontainer which `pmm-managed` supports, podman is also [supported](https://code.visualstudio.com/docs/remote/containers#_can-i-use-podman-instead-of-docker).

I do have VSCode, but I use it in flatpak. Setting up that is a little bit tricky, and I didn't manage it as I don't really care and don't want to spend time to figure it out.

But here are couple of useful links:
* https://github.com/flathub/com.visualstudio.code/issues/55
* https://gist.github.com/FilBot3/4424d312a87f7b4178722d3b5eb20212

## Summary

I don't have docker installed for a long time and don't struggle without it much. As shown above it is easy to setup the system and with minor changes and without obsolete parameters it would work for both docker and podman.

The way to go from compose files is probably k8s manifests that podman supports with `podman generate kube` and `podman play kube`. Those are more standard and widely used.
