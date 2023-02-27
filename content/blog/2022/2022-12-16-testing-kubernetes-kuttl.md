---
title: "Testing Kubernetes with KUTTL"
date: "2022-12-16T00:00:00+00:00"
draft: false
tags: ['PMM', 'DBaaS', 'KUTTL', 'testing']
authors:
  - andrew_minkin
slug: 'testing-kubernetes-with-kuttl'
images:
  - blog/2022/12/K8S-KUTTL.jpg
---

Automated testing is the only way to be sure that your code works. Enabling automated testing can be hard and we say a lot of tools to write automated tests in the industry since the beginning. Some veterans in the industry may remember Selenium,  Cucumber frameworks that help automate testing in the browser. However, testing in Kubernetes can be hard.

In Percona we deal with Kubernetes and have different operators to automate the management of databases. It requires testing.  A lot of testing. We have different frameworks to help us with it

1. Codecept.js to write UI tests for PMM. Also, we use a playwright for some cases.
2. We have tools to help us with API testing as well as automating some routines by running bash commands during the test step.

However, those frameworks are not applicable to test Kubernetes workloads as well as Kubernetes operators. I've been working in the PMM integrations team for six months and saw different approaches to automate testing for PMM/DBaaS. We have a Go test library with wrappers around kubectl and codecept.js for end-to-end tests for the User Interface.

## What challenges do we have?

Well, to be sure that a database cluster creation works we need to automate the following steps

1. Installation of operators to Kubernetes cluster
2. Test integration with version service to respect compatibility matrix.
3. Create a database cluster and wait once it'll be available
4. Do some assertions against Kubernetes as well as UI.

The main pain point here is that we need to wait up to 10-15 minutes for each step and we can't have different test cases to cover as many cases as we can. Yet we can achieve some performance benefits by paralleling workloads, still, it requires learning Javascript and testing framework to work with it. We had some architectural changes recently and moved from our custom gRPC API to create and manage database clusters to an operator that runs on top of other operators and converts K8s' Custom Resource from generic format to operator specific. We had a couple of options for this new project and after research, we chose kuttl as a framework for integration/e2e testing.

## What is KUTTL anyway and why should I care?

KUTTL is the KUbernetes Test TooL. It's written in Go and provides a declarative way to test Kubernetes operators using Kubernetes primitives. It's easy to start kuttling. Let's take a deeper look. I'll use [dbaas-operator](https://github.com/percona/dbaas-operator) as an example. DBaaS-operator is an operator that has a simple and generic Custom Resource Definition available to create Percona Server MongoDB or Percona XtraDB Cluster instances in kubernetes. It uses underlying operators as a dependencies. We have the following structure

```
e2e-tests
├── kind.yml
├── kuttl-eks.yml
├── kuttl.yml
└── tests
    └── pxc
        ├── 00-assert.yaml
        ├── 00-deploy-operators.yaml
        ├── 01-assert.yaml
        ├── 01-deploy-pxc.yaml
        ├── 02-assert.yaml
        ├── 02-upgrade-pxc.yaml
        ├── 03-assert.yaml
        ├── 03-restart-pxc.yaml
        ├── 04-delete-cluster.yaml
        ├── 05-assert.yaml
        ├── 05-create-cluster.yaml
        ├── 06-assert.yaml
        ├── 06-scale-up-pxc.yaml
        ├── 07-assert.yaml
        ├── 07-scale-down-pxc.yaml
        └── 08-delete-cluster.yaml

2 directories, 19 files
```

Let's discuss these YAML files more

1. kind.yml contains settings to run [Kind](https://kind.sigs.k8s.io/)
2. kuttl.yml has all required settings for Kuttl framework and kuttl-eks.yml has some EKS specific configurations
3. tests folder has test steps and assertions

## Kind and KUTTL settings

Let's discuss Kind and kuttl settings and I'll start with KUTTL first

```yaml
apiVersion: kuttl.dev/v1beta1
kind: TestSuite
kindConfig: e2e-tests/kind.yml  # Path to Kind config that will be used to create Kind clusters
crdDir: config/crd/bases        # Path to a directory that contains CRD files. Kuttl will apply them before running tests
artifactsDir: /tmp/             # Path to a directory to store artifacts such as logs and other information
testDirs:
- e2e-tests/tests               # Path to directories that have test steps
```

Kind config is quite easy

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:5000"]
    endpoint = ["http://kind-registry:5000"]
```

The aforementioned config will use local registry and will create 3 k8s worker nodes controlled by control plane

## Writing tests
At the first glance, kuttling can be easy because it uses Kubernetes primitives as a test step and assertion but I had a couple of problems to test my operator. Let's take a look at a couple of examples. Since dbaas-operator depends on PXC operator we need to prepare our environment for testing. Let's write first test that installs PXC operator and ensures that it was installed.

```
cat e2e-tests/tests/pxc/00-deploy-pxc-operator.yml

apiVersion: kuttl.dev/v1beta1
kind: TestStep
timeout: 10 # Timeout for the test step
commands:
  - command: kubectl apply -f https://raw.githubusercontent.com/percona/percona-xtradb-cluster-operator/v${PXC_OPERATOR_VERSION}/deploy/bundle.yaml -n "${NAMESPACE}"
```

KUTTL test steps easily extensible with [commands](https://kuttl.dev/docs/testing/reference.html#commands). One can run even scripts as a prerequisite for a test case. PXC operator installs CRDs and creates a deployment and here's an example of assertion.

```
cat e2e-tests/tests/pxc/00-assert.yml

apiVersion: kuttl.dev/v1beta1
kind: TestAssert
timeout: 120  # Timeout waiting for the state
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: perconaxtradbclusters.pxc.percona.com
spec:
  group: pxc.percona.com
  names:
    kind: PerconaXtraDBCluster
    listKind: PerconaXtraDBClusterList
    plural: perconaxtradbclusters
    shortNames:
    - pxc
    - pxcs
    singular: perconaxtradbcluster
  scope: Namespaced
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databaseclusters.dbaas.percona.com
spec:
  group: dbaas.percona.com
  names:
    kind: DatabaseCluster
    listKind: DatabaseClusterList
    plural: databaseclusters
    shortNames:
    - db
    singular: databasecluster
  scope: Namespaced
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: percona-xtradb-cluster-operator
status:
  availableReplicas: 1
  observedGeneration: 1
  readyReplicas: 1
  replicas: 1
  updatedReplicas: 1
```

Our first test is ready and one needs to run `kubectl kuttl test --config ./e2e-tests/kuttl.yml` to run kuttl.

## More advanced tests

We need to run our operator first to be able to work with resources and test it. KUTTL recomends configure it via `TestSuite` by the following example

```yaml
apiVersion: kuttl.dev/v1beta1
kind: TestSuite
...
commands:
  - command: ./bin/manager
...
```
However, since dbaas-operator depends on underlying operators it needs to work correctly even if they are not present in a Kubernetes cluster. It has the following logic in the controller

```
// SetupWithManager sets up the controller with the Manager.
func (r *DatabaseReconciler) SetupWithManager(mgr ctrl.Manager) error {
	fmt.Println(os.Getenv("WATCH_NAMESPACE"))
	unstructuredResource := &unstructured.Unstructured{}
	unstructuredResource.SetGroupVersionKind(schema.GroupVersionKind{
		Group:   "apiextensions.k8s.io",
		Kind:    "CustomResourceDefinition",
		Version: "v1",
	})
	controller := ctrl.NewControllerManagedBy(mgr).
		For(&dbaasv1.DatabaseCluster{})
	err := r.Get(context.Background(), types.NamespacedName{Name: pxcCRDName}, unstructuredResource)
	if err == nil {
		if err := r.addPXCToScheme(r.Scheme); err == nil {
			controller.Owns(&pxcv1.PerconaXtraDBCluster{})
		}
	}
	err = r.Get(context.Background(), types.NamespacedName{Name: psmdbCRDName}, unstructuredResource)
	if err == nil {
		if err := r.addPSMDBToScheme(r.Scheme); err == nil {
			controller.Owns(&psmdbv1.PerconaServerMongoDB{})
		}
	}
	return controller.Complete(r)
}
```

The `controller.Owns` sets up a controller to watch specified resources and once they were changed it'll run a reconciliation loop to sync changes. Also, it checks that operator is present in the cluster by checking that deployment and CRDs are available. It means that to make the operator work correctly in tests we need to choose from the following options

1. Restart operator once upsteam operator was installed by sending `HUP` signal
2. Run operator only after underlying operator is present in a cluster

Hence, I moved command as the next step before creating a cluster. You can see it below

```
cat e2e-tests/tests/pxc/01-deploy-pxc.yml

apiVersion: kuttl.dev/v1beta1
kind: TestStep
timeout: 10
commands:
  - script: WATCH_NAMESPACE=$NAMESPACE ../../../bin/manager
    background: true
---
apiVersion: dbaas.percona.com/v1
kind: DatabaseCluster
metadata:
  name: test-cluster
spec:
  databaseType: pxc
  databaseImage: percona/percona-xtradb-cluster:8.0.23-14.1
  databaseConfig: |
    [mysqld]
    wsrep_provider_options="debug=1;gcache.size=1G"
  secretsName: pxc-sample-secrets
  clusterSize: 1
  loadBalancer:
    type: haproxy
    exposeType: ClusterIP
    size: 1
    image: percona/percona-xtradb-cluster-operator:1.11.0-haproxy
  dbInstance:
    cpu: "1"
    memory: 1G
    diskSize: 15G
```

Note: `command` supports only simple commands and does not fully support env variables. It supports only $NAMESPACE, $PATH and $HOME. However, `script` solves the problem of setting `WATCH_NAMESPACE` environment variable.

In nutshell, the test step above does two things:

1. Runs the operator
2. Creates a database cluster

The assertion checks that kubernetes cluster has the `DatabaseCluster` object with `ready` status as well as PXC cluster with the same status.

```yaml

apiVersion: kuttl.dev/v1beta1
kind: TestAssert
timeout: 600
---
apiVersion: dbaas.percona.com/v1
kind: DatabaseCluster
metadata:
  name: test-cluster
spec:
  databaseType: pxc
  databaseImage: percona/percona-xtradb-cluster:8.0.23-14.1
  databaseConfig: |
    [mysqld]
    wsrep_provider_options="debug=1;gcache.size=1G"
  secretsName: pxc-sample-secrets
  clusterSize: 1
  loadBalancer:
    type: haproxy
    exposeType: ClusterIP
    size: 1
    image: percona/percona-xtradb-cluster-operator:1.11.0-haproxy
  dbInstance:
    cpu: "1"
    memory: 1G
    diskSize: 15G
---
apiVersion: pxc.percona.com/v1
kind: PerconaXtraDBCluster
metadata:
  name: test-cluster
spec:
  allowUnsafeConfigurations: true
  crVersion: 1.11.0
  haproxy:
    enabled: true
    image: percona/percona-xtradb-cluster-operator:1.11.0-haproxy
    serviceType: ClusterIP
    size: 1
  pxc:
    configuration: |
      [mysqld]
      wsrep_provider_options="debug=1;gcache.size=1G"
    expose: {}
    image: percona/percona-xtradb-cluster:8.0.23-14.1
    livenessProbes: {}
    readinessProbes: {}
    resources:
      requests:
        cpu: "1"
        memory: 1G
    serviceType: ClusterIP
    sidecarResources: {}
    size: 1
    volumeSpec:
      persistentVolumeClaim:
        resources:
          requests:
            storage: 15G
  secretsName: pxc-sample-secrets
  updateStrategy: SmartUpdate
  upgradeOptions:
    apply: 8.0-recommended
    schedule: 0 4 * * *
status:
  ready: 2
  size: 2
  state: ready
```

## Caveats and notes

I had problems running tests in Kind. They were flaky because PXC operator can't expose metrics and had problems with liveness probe. I haven't figured out how to fix it but as a workaround I use minikube to run tests

```
	minikube start --nodes=4 --cpus=2 --memory=4g --apiserver-names host.docker.internal --kubernetes-version=v1.23.6
	minikube kubectl -- config view --flatten --minify > ~/.kube/test-minikube
	KUBECONFIG=~/.kube/test-minikube kubectl kuttl test --config ./e2e-tests/kuttl.yml
```

## Further steps
There's always room for improvement and I have these steps in mind

1. Use docker images and OLM bundles as a way to run the operator for tests. This will be the best way to simulate a production like environment.
2. Add more advanced tests for database clusters such as running queries, try loading data as well as capacity testing. It's easily achivable with kuttl
