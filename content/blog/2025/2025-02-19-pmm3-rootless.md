---
title: "Percona Monitoring and Management 3 and rootless containers"
date: "2025-02-19T00:00:00+00:00"
tags: ['PMM', 'HELM', 'Docker']
authors:
  - sergey_pronin
images:
  - blog/2025/02/pmm3-rootless.jpg
---

In today's landscape, where security breaches are a constant concern, reducing potential attack vectors is a top priority for any organization. Percona Monitoring and Management (PMM) has established itself as a reliable solution for database performance monitoring. With [the release of PMM version 3](https://docs.percona.com/percona-monitoring-and-management/3/release-notes/3.0.0.html), Percona has significantly strengthened its security posture, notably by introducing support for rootless container deployments. This advancement directly addresses a crucial security challenge and enhances the overall robustness and reliability of PMM.

![Percona Monitoring and Management (PMM) 3.0.0](blog/2025/02/pmm3-homepage.jpg)

The inherent risks associated with root privileges are well-documented. While many applications, including those containerized, have historically relied on root access, this practice presents a substantial security vulnerability. In the event of a successful exploit, an attacker gains comprehensive control over the host system. This risk is further exacerbated in environments with outdated software or complex configurations. Essentially, while the root user offers extensive capabilities, it also represents a significant potential liability that should be carefully mitigated.

In this blog post we will look at the exact differences between PMM versions 2 and 3 and how they behave.

## Enforcing Pod Security Standards

[The Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) define three different policies to broadly cover the security spectrum. These policies are cumulative and range from highly-permissive to highly-restrictive.

To enforce restrictions on a specific namespace we will create the following YAML manifest:
```
apiVersion: v1
kind: Namespace
metadata:
  name: secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```

This YAML creates a namespace named secure-namespace. The pod-security.kubernetes.io/enforce: restricted label instructs Kubernetes to deny any pods in this namespace that violate the "restricted" PSS profile. The warn and audit labels are also very useful for monitoring and testing before fully enforcing the restricted policy.

## Deploy PMM

We will execute a series of deployments to demonstrate the difference between PMM2 and PMM3 behavior in insecure and secure environments. All files can be found in this github repository: [spron-in/blog-data/pmm3-rootless](https://github.com/spron-in/blog-data/tree/master/pmm3-rootless)

### Regular namespace

**PMM2**

```
% kubectl apply -f 01.pmm2.yaml 
statefulset.apps/pmm-server created
service/pmm-server created

% kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
pmm-server-0   1/1     Running   0          45s
```

I can connect to my PMM2 server with a Service that I created.

**PMM3**

```
% kubectl apply -f 02.pmm3.yaml 
statefulset.apps/pmm-server created
service/pmm-server created

% kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
pmm-server-0   1/1     Running   0          20s
```

I can connect to my PMM3 server with a Service that I created.

### Secure namespace

Let’s try to deploy both versions of Percona Monitoring and Management servers in a secure namespace. For both we will see the following:

```
% kubectl apply -f 01.pmm2.yaml -n secure-namespace
Warning: would violate PodSecurity "restricted:latest": allowPrivilegeEscalation != false (container "pmm-server" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (container "pmm-server" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "pmm-server" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "pmm-server" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
statefulset.apps/pmm-server created
service/pmm-server created

% kubectl -n secure-namespace get pods
No resources found in secure-namespace namespace.
```

There are no Pods created and if you describe the StatefulSet, you are going to see a similar error:

```
Warning  FailedCreate  5s (x15 over 87s)  statefulset-controller  create Pod pmm-server-0 in StatefulSet pmm-server failed error: pods "pmm-server-0" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (container "pmm-server" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (container "pmm-server" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "pmm-server" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "pmm-server" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```

The error will be the same for PMM2 and PMM3 manifests. 

### Secure namespace and security contexts

We are now going to apply Pod and Container Security Contexts to both manifests. 

Under spec.containers we add everything that Kubernetes suggested us:
```
      - name: pmm-server
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
              - ALL
          runAsNonRoot: true
          seccompProfile:
            type: 'RuntimeDefault'
```


**PMM2**

```
% kubectl -n secure-namespace apply -f 03.pmm2-secure.yaml 
statefulset.apps/pmm-server created
service/pmm-server created

% kubectl -n secure-namespace get pods
NAME           READY   STATUS   RESTARTS      AGE
pmm-server-0   0/1     Error    2 (15s ago)   28s
```

Even though the PMM2 server Pod can be created now, it is failing to start. If you check the logs, you are going to see the following:

```
% kubectl -n secure-namespace logs pmm-server-0
...
Error: Can't drop privilege as nonroot user
For help, use /usr/local/bin/supervisord -h
```

**PMM3**

```
% kubectl -n secure-namespace apply -f 04.pmm3-secure.yaml 
statefulset.apps/pmm-server created
service/pmm-server created

% kubectl -n secure-namespace get pods
NAME           READY   STATUS    RESTARTS   AGE
pmm-server-0   1/1     Running   0          32s
```

PMM3 starts just fine.


### Helm

The recommended approach to deploy PMM3 in Kubernetes is via Helm. You can find our helm charts in [percona/helm-charts](https://github.com/percona/percona-helm-charts/tree/main/charts/pmm) github repository and more in [our documentation](https://docs.percona.com/percona-monitoring-and-management/3/install-pmm/install-pmm-server/deployment-options/helm/index.html).

To deploy PMM3 in a namespace or environment with strict security (like OpenShift), you need to pass similar security context parameters. You can find how in [05.pmm3-helm.yaml](https://github.com/spron-in/blog-data/blob/master/pmm3-rootless/05.pmm3-helm.yaml) values manifest.

Then the deployment will look like this:
```
helm repo update
helm install pmm3 percona/pmm -f 05.pmm3-helm.yaml --namespace secure-namespace
```

## Conclusion

PMM 3's rootless design excels where PMM 2 falters in secure Kubernetes environments. Enforcing Pod Security Standards, we saw PMM 3 deploy successfully, while PMM 2 failed, even with security contexts. This highlights PMM 3's enhanced security, crucial for modern, hardened deployments. Using Helm simplifies secure PMM 3 deployments, ensuring robust database monitoring without compromising security.

Try out [Percona Monitoring and Management version 3](https://docs.percona.com/percona-monitoring-and-management/3/release-notes/3.0.0.html), 100% open source database observability solution, and learn more about its enhancements.

Tell us what you think in [our forum](https://forums.percona.com/c/percona-monitoring-and-management-pmm/pmm-3/84/l/new) or let us know if you are looking for [commercial support](https://www.percona.com/about/contact).