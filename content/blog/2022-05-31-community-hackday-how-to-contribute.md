---
title: "How and Why Contribute to Communities"
date: "2022-05-30T00:00:00+00:00"
tags: ['PMM' , 'minikube', 'CSI', 'kubernetes', 'k8s', 'operator' ]
authors:
  - denys_kondratenko
images:
  - blog/2022/5/how_and_why_contirbute.jpg
slug: csi-minikube-multinode
---

## Why

Lets start with a simple question "Why to contribute?".

In our day to day development's and user's life we use tons of OSS (open source) software. Ppl develop that software together to have ability to use them in more standard and open way, so they spend less time negotiating on interfaces and tools (and that is not the main reason, one of the reasons for OSS).

As any sustainable process, OSS development also needs not only users but contributors to be able to move project forward as well as to sustain bugs, time and new tech trends. As users we have different use cases that might not be yet implemented but could be very valuable for other users.

As an example I use `minikube` for the development and testing of [PMM DBaaS solution](https://docs.percona.com/percona-monitoring-and-management/using/dbaas.html). That tool allows me to run Kubernetes (k8s) locally and run [Percona operators](https://www.percona.com/software/percona-kubernetes-operators) with help of DBaaS.

One of the great `minikube` features is to run real multi-node k8s clusters (see this [blog post](https://percona.community/blog/2021/12/20/pmm-minikube-postgres/) for details):
```sh
$ minikube start --nodes=4 --cpus=4 --memory=8G
...
$ kubectl get nodes
NAME           STATUS   ROLES                  AGE     VERSION
minikube       Ready    control-plane,master   2d22h   v1.22.3
minikube-m02   Ready    <none>                 2d22h   v1.22.3
minikube-m03   Ready    <none>                 2d22h   v1.22.3
minikube-m04   Ready    <none>                 2d22h   v1.22.3
```

I usually run integration test with `--driver=kvm` and some simple sanity tests with `--driver=podman`.

During my testing I found out that I can't deploy operators with DBaaS on `minikube` multi-node cluster and I found similar [Jira issue about it](https://jira.percona.com/browse/K8SPXC-879):
```console
$ kubectl get pods
NAME                                               READY   STATUS                  RESTARTS     AGE
percona-server-mongodb-operator-fcc5c8d6-rphcs     1/1     Running                 0            3h11m
percona-xtradb-cluster-operator-566848cf48-zm28g   1/1     Running                 0            3h11m
pmm-0                                              1/1     Running                 0            8m19s
test-haproxy-0                                     2/3     Running                 0            9s
test-pxc-0                                         0/2     Init:CrashLoopBackOff   1 (5s ago)   9s
$ kubectl logs test-pxc-0 pxc-init
++ id -u
++ id -g
+ install -o 2 -g 2 -m 0755 -D /pxc-entrypoint.sh /var/lib/mysql/pxc-entrypoint.sh
install: cannot create regular file '/var/lib/mysql/pxc-entrypoint.sh': Permission denied
```

So that is Why - ability to use `minikube` to test operator's DB deployments.

## Community Hackdays

Percona engineering management came with idea of dedicating a Focus day (we have those in Percona :) to community contributions. That was a great initiative, even if community contribution is our routine (we do it day to day when needed), having dedicated day is a nice way to educate others on how to do it on a good set of examples.

I run with my `minikube` multi-node issue as an example of both day to day work and what could be achieved during one community hackday.

### Day to day community hacking

`minikube` issue affects me as a developer so I spent a day to investigate it and half a day to find out workaround and next steps.

First I spent quite a time to understand what is going on and if that issue of `minikube` or DBaaS, or maybe operator's issue. It was interesting detective work and I found out that it is indeed `minikube` related issue and similar issue already exists in GitHub: [kubernetes/minikube #12360](https://github.com/kubernetes/minikube/issues/12360).

I have described my findings in [this comment](https://github.com/kubernetes/minikube/issues/12360#issuecomment-1123247475) and later found workaround that enables me and my colleagues to continue to use `minikube` in [multi-node setup](https://github.com/kubernetes/minikube/issues/12360#issuecomment-1123794143).

That was day to day community hacking, I also spent a little time to find out how to fix it correctly and joined [Minikube Triage party](https://minikube.sigs.k8s.io/docs/contrib/triage/) to discuss the issue (sorry folks, still need to find time to join it regularly and help with triaging).

And there I left it to the next opportunity to contribute.

### Hackday

Opportunity presented itself quite quickly with new Community Hackday initiative and I decided that it would be a great time to fix part of the issue as the complete fix would take longer than a day.

First step in fixing [kubernetes/minikube #12360](https://github.com/kubernetes/minikube/issues/12360) is to fix [kubernetes-csi/csi-driver-host-path](https://github.com/kubernetes-csi/csi-driver-host-path) to support unprivileged containers.

So I took it for the day and here describe my progress...

## Contributing to the community project

So your first help on how to contribute usually are [README.md](https://github.com/kubernetes-csi/csi-driver-host-path/blob/master/README.md) and [CONTRIBUTING.md](https://github.com/kubernetes-csi/csi-driver-host-path/blob/master/CONTRIBUTING.md).

I started with forking the repo on GH (GitHub) UI and cloning it locally:
```sh
$ git clone git@github.com:denisok/csi-driver-host-path.git
```

First what I would like to do is to compile the code, create container and reproduce the issue.

```sh
$ cd csi-driver-host-path

$ make container

./release-tools/verify-go-version.sh "go"

======================================================
                  WARNING

  This projects is tested with Go v1.18.
  Your current Go version is v1.16.
  This may or may not be close enough.

  In particular test-gofmt and test-vendor
  are known to be sensitive to the version of
  Go.
======================================================

mkdir -p bin
# os_arch_seen captures all of the $os-$arch-$buildx_platform seen for the current binary
# that we want to build, if we've seen an $os-$arch-$buildx_platform before it means that
# we don't need to build it again, this is done to avoid building
# the windows binary multiple times (see the default value of $BUILD_PLATFORMS)
export os_arch_seen="" && echo '' | tr ';' '\n' | while read -r os arch buildx_platform suffix base_image addon_image; do \
	os_arch_seen_pre=${os_arch_seen%%$os-$arch-$buildx_platform*}; \
	if ! [ ${#os_arch_seen_pre} = ${#os_arch_seen} ]; then \
		continue; \
	fi; \
	if ! (set -x; cd ./cmd/hostpathplugin && CGO_ENABLED=0 GOOS="$os" GOARCH="$arch" go build  -a -ldflags ' -X main.version=v1.8.0-6-g50b99a39 -extldflags "-static"' -o "/home/dkondratenko/Workspace/github/csi-driver-host-path/bin/hostpathplugin$suffix" .); then \
		echo "Building hostpathplugin for GOOS=$os GOARCH=$arch failed, see error(s) above."; \
		exit 1; \
	fi; \
	os_arch_seen+=";$os-$arch-$buildx_platform"; \
done
+ cd ./cmd/hostpathplugin
+ CGO_ENABLED=0
+ GOOS=
+ GOARCH=
+ go build -a -ldflags ' -X main.version=v1.8.0-6-g50b99a39 -extldflags "-static"' -o /home/dkondratenko/Workspace/github/csi-driver-host-path/bin/hostpathplugin .
docker build -t hostpathplugin:latest -f Dockerfile --label revision=v1.8.0-6-g50b99a39 .
STEP 1/7: FROM alpine
STEP 2/7: LABEL maintainers="Kubernetes Authors"
--> Using cache 9172a5d022e2a2550bcb0f6f7faa0b6a2126dcf7c1a0266924f4989370fbf80e
--> 9172a5d022e
STEP 3/7: LABEL description="HostPath Driver"
--> Using cache 532cdc0c943df037d70368de6b7e90adb39dda3c6f9d7645c7ca6a9bd8d50abd
--> 532cdc0c943
STEP 4/7: ARG binary=./bin/hostpathplugin
--> Using cache 762a2b09549d02f9cd3d1dd8220c1b6890ae48efc155ae7aff276ae53bf7836b
--> 762a2b09549
STEP 5/7: RUN apk add util-linux coreutils && apk update && apk upgrade
--> Using cache 4bd7cf3998cc06cfdc780d3abdf6cedc452170ad93cf46cd3f4d12a8f5f97f09
--> 4bd7cf3998c
STEP 6/7: COPY ${binary} /hostpathplugin
--> a8e75bbeab1
STEP 7/7: ENTRYPOINT ["/hostpathplugin"]
COMMIT hostpathplugin:latest
--> b0014a637af
Successfully tagged localhost/hostpathplugin:latest
b0014a637af31632b48f39def813637ad0d83d11d008d5b89edb52f28498b805

$ podman images
REPOSITORY                                 TAG              IMAGE ID      CREATED         SIZE
<none>                                     <none>           1ec47f8d8558  46 seconds ago  35.6 MB
localhost/hostpathplugin                   latest           f36f889fb57b  2 minutes ago   35.6 MB
```

It appears to be super easy, I had Go 1.18 and podman already setup on my machine.

So I have an image and now need to reproduce the issue. I need k8s cluster, setup CSI driver and upload my custom container:

```sh
$ minikube start --nodes=2 --cpus=2 --memory=2G

$ minikube addons disable storage-provisioner
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌑  "The 'storage-provisioner' addon is disabled"

$ kubectl delete storageclass standard
storageclass.storage.k8s.io "standard" deleted

$ cd deploy/kubernetes-distributed/

[kubernetes-distributed]$ ./deploy.sh
applying RBAC rules
curl https://raw.githubusercontent.com/kubernetes-csi/external-provisioner/v3.1.0/deploy/kubernetes/rbac.yaml --output /tmp/tmp.yXGWmlOXv9/rbac.yaml --silent --location
kubectl apply --kustomize /tmp/tmp.yXGWmlOXv9
serviceaccount/csi-provisioner created
role.rbac.authorization.k8s.io/external-provisioner-cfg created
clusterrole.rbac.authorization.k8s.io/external-provisioner-runner created
rolebinding.rbac.authorization.k8s.io/csi-provisioner-role-cfg created
clusterrolebinding.rbac.authorization.k8s.io/csi-provisioner-role created
csistoragecapacities.v1beta1.storage.k8s.io:
   No resources found in default namespace.
deploying with CSIStorageCapacity v1beta1: true
deploying hostpath components
   ./hostpath/csi-hostpath-driverinfo.yaml
csidriver.storage.k8s.io/hostpath.csi.k8s.io created
   ./hostpath/csi-hostpath-plugin.yaml
        using           image: k8s.gcr.io/sig-storage/csi-provisioner:v3.1.0
        using           image: k8s.gcr.io/sig-storage/csi-node-driver-registrar:v2.5.0
        using           image: k8s.gcr.io/sig-storage/hostpathplugin:v1.7.3
        using           image: k8s.gcr.io/sig-storage/livenessprobe:v2.6.0
daemonset.apps/csi-hostpathplugin created
   ./hostpath/csi-hostpath-storageclass-fast.yaml
storageclass.storage.k8s.io/csi-hostpath-fast created
   ./hostpath/csi-hostpath-storageclass-slow.yaml
storageclass.storage.k8s.io/csi-hostpath-slow created
   ./hostpath/csi-hostpath-testing.yaml
        using           image: docker.io/alpine/socat:1.7.4.3-r0
service/hostpath-service created
statefulset.apps/csi-hostpath-socat created

$ kubectl patch storageclass csi-hostpath-fast -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
storageclass.storage.k8s.io/csi-hostpath-fast patched

```

There I have k8s cluster with 2 nodes, disabled standard `minikube` storage-provisioned (which doesn't support multi-node) deleted `storageclass` that was working with that storage-provisioner and setup CSI hostpathplugin. Also enabled `default` flag on the `storageclass` for hostpathplugin so it would provision PVCs for me.

Lets create test manifest `perm_test.yaml` to reproduce the issue:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  labels:
    app: perm-test
  name: perm-test
spec:
  replicas: 1
  serviceName: perm-test
  selector:
    matchLabels:
      app: perm-test
  template:
    metadata:
      labels:
        app: perm-test
    spec:
      securityContext:
        fsGroup: 65534
        runAsGroup: 65534
        runAsNonRoot: true
        runAsUser: 65534
      containers:
        - image: busybox
          name: perm-test
          command: ["/bin/sh"]
          args:
            - "-c"
            - |
              touch /mnt/perm_test/file_test && echo passed && sleep 3600 && exit 0
              echo failed
              exit 1
          volumeMounts:
            - mountPath: /mnt/perm_test
              name: perm-test
  volumeClaimTemplates:
    - metadata:
        name: perm-test
      spec:
        accessModes: [ "ReadWriteOnce" ]
        resources:
          requests:
            storage: 1G
```

And test it to see that we really have a problem with unprivileged container:
```sh
$ kubectl apply -f perm_test.yaml
statefulset.apps/perm-test created

$ kubectl logs perm-test-0

touch: /mnt/perm_test/file_test: Permission denied
failed

$ kubectl get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE           NOMINATED NODE   READINESS GATES
csi-hostpath-socat-0       1/1     Running   0          24h     10.244.1.13   minikube-m02   <none>           <none>
csi-hostpathplugin-fnhvr   4/4     Running   0          2m27s   10.244.0.24   minikube       <none>           <none>
csi-hostpathplugin-w5rxt   4/4     Running   0          2m30s   10.244.1.55   minikube-m02   <none>           <none>
perm-test-0                0/1     Error     0          2m18s   10.244.1.56   minikube-m02   <none>           <none>
```

If we put `sleep 3600` before `exit 1` we actually could jump into the container and inspect the permissions:
```sh
$ kubectl exec --stdin --tty perm-test-0 -- sh

$ id
uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)

$ stat /mnt/perm_test 
File: /mnt/perm_test 
Size: 40 Blocks: 0 IO Block: 4096 directory 
Device: 10h/16d Inode: 82570 Links: 2 
Access: (0755/drwxr-xr-x) Uid: ( 0/ root) Gid: ( 0/ root) 
Access: 2022-05-27 13:21:56.905860356 +0000 
Modify: 2022-05-27 13:21:56.905860356 +0000 
Change: 2022-05-27 13:21:56.905860356 +0000
```

As we see that directory has `Access: (0755/drwxr-xr-x)` and when we would like to write to it we have not enough permissions for `nobody` user and file creation fails. We also could see that there are couple of pods running for the CSI plugin that actually provision PV/Cs.

Clean up:

```sh
$ kubectl delete -f perm_test.yaml
$ kubectl delete pvc perm-test-perm-test-0
```

I did code changes to add more logging to understand the program flow better and to see when the permissions would change if they actually.
During changes I learned a little bit on [glog](https://github.com/google/glog#verbose-logging) and that it has `-v=5` in arguments for containers, so Info level by default.

Lets create new image with those changes which we upload to the minikube and modify DeamonSet (csi driver):

```sh
$ make container
$ rm hostpath.tar
$ podman save --format docker-archive -o hostpath.tar localhost/hostpathplugin
Copying blob 4fc242d58285 done
Copying blob 89f8b151f422 done
Copying blob 57a9469e70ba done
Copying config 29ba4a1533 done
Writing manifest to image destination
Storing signatures

$ minikube image load ./hostpath.tar

$ minikube image ls
...
docker.io/localhost/hostpathplugin:latest
...

$ kubectl set image ds/csi-hostpathplugin hostpath=localhost/hostpathplugin:latest
```

Another way to modify DeamonSet is to run edit `$ kubectl edit ds csi-hostpathplugin`, and change something. For example I was changing `-v=6` and back to `-v=5` so it would restart all containers with new image (that I uploaded).

> **stuck**: I actually spent 2h trying to understand why I don't see logs that I have added, and that actually led me to learn `glog`, but it was quite simple. By default `kubectl logs csi-hostpathplugin-w5rxt` shows logs for default container, not for hostpath. So I just needed to path right parameters `kubectl logs csi-hostpathplugin-w5rxt -c hostpath` 

Adding volume to the pod happens in couple of stages, `hostpath.go` creates directory on a needed node and `nodeserver.go` publishes this volume to the pod by `bind` mounting target pod `mount` directory to the volume directory created by `hostpath.go`.
Please check [Spec](https://github.com/container-storage-interface/spec/blob/master/spec.md).

It actually showed me that permission didn't change from stage to stage but weren't setup correctly on dir creation:
```go
	case state.MountAccess:
		err := os.MkdirAll(path, 0777)
		if err != nil {
			return nil, err
		}
```

I have mode log before and after it, as it looked 0777 should be right one (allowing everyone to rwx on the directory):
```console
I0527 19:09:38.234437       1 hostpath.go:177] VolumePath: /csi-data-dir/8dc9889d-ddf0-11ec-b319-7e80679203b2 AccessType: 0
I0528 07:07:57.543195       1 hostpath.go:187] mode info: -rwxr-xr-x for user: 0 group: 0
```

So actually mode is 0755 instead of 0777 as requested in MkdirAll, and documentation clarifies:
```
MkdirAll creates a directory named path, along with any necessary parents, and returns nil, or else returns an error. 
The permission bits perm (before umask) are used for all directories that MkdirAll creates. 
If path is already a directory, MkdirAll does nothing and returns nil.
```

Lets check umask for the root user (`minikube ssh -n minikube-m02`):
```sh
$ umask
0022

$ getfacl --default /tmp/hostpath-provisioner/
getfacl: Removing leading '/' from absolute path names
# file: tmp/hostpath-provisioner/
# owner: root
# group: root

$ getfacl /tmp/hostpath-provisioner/
getfacl: Removing leading '/' from absolute path names
# file: tmp/hostpath-provisioner/
# owner: root
# group: root
user::rwx
group::r-x
other::r-x
```

mkdir syscall actually accounts mask, which is 022. Or even mask is ignored as ACL from parent dir could be propagated:
* https://man7.org/linux/man-pages/man2/mkdir.2.html
* https://man7.org/linux/man-pages/man2/umask.2.html

In my case there are no default ACLs but umask is set to 022 so: (0777 & ~0022 & 0777) actually gives us 0755.

```sh
$ umask
0022

$ getfacl --default /tmp/hostpath-provisioner/
getfacl: Removing leading '/' from absolute path names
# file: tmp/hostpath-provisioner/
# owner: root
# group: root

$ getfacl /tmp/hostpath-provisioner/
getfacl: Removing leading '/' from absolute path names
# file: tmp/hostpath-provisioner/
# owner: root
# group: root
user::rwx
group::r-x
other::r-x
```

So that was it, we need to get rid of a mask and proposed fix is:
```go
		if err = os.Chmod(path, 0777); err != nil {
			glog.V(4).Infof("Couldn't change volume permissions: %w", err)
		}
```

Cleaned up once again, compiled, created and pushed container. Tested it - It works!

I created the branch on my fork, pushed it to my repo and followed PR procedure to create [kubernetes-csi/csi-driver-host-path #356](https://github.com/kubernetes-csi/csi-driver-host-path/pull/356).

That was the end of my Hackday and one step in solving issue in more general way.

## Value

The excersise has a lot of value for me and Percona. I learned a lot of new things about k8s PV/PVC provisioning and CSI. For Percona we enabled development (devs and ci/cd) to run deployments on multi-node k8s local clusters.

And hopefully for everyone else who needs to run unprivilege containers in multi-node with PVC.

All together ppl developing OSS projects to benefit from each other and use better inovating Open-Source Software as well as to have a lot of fun :) .
