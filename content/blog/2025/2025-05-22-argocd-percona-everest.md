---
title: "Deploy Open Source Databases with Extended Monitoring on Kubernetes using Argo CD for GitOps-Driven Management"
date: "2025-05-19T00:00:00+00:00"
tags: ['PMM', 'Kubernetes', 'MySQL', 'MongoDB', 'Percona', 'Opensource']
categories: ['PMM', 'Cloud', 'MySQL', 'MongoDB', 'PostgreSQL']
authors:
  - daniil_bazhenov
images:
  - blog/2025/05/BugReportApril2025.jpg
---

Kubernetes has become the de-facto platform for orchestrating applications, and managing databases on Kubernetes efficiently is a critical challenge. Percona Everest emerges as a powerful solution that streamlines the deployment and management of open-source database distributions such as **MongoDB, PostgreSQL, and MySQL**, offering a user-friendly UI and a robust API for database operations. It leverages Kubernetes operators to automate database lifecycle operations, including deployment, scaling, updating, backing up, and restoring. Beyond core database management, Everest provides integrated monitoring capabilities through **Percona Monitoring and Management (PMM)**, offering comprehensive visibility into database performance and health.

Percona Everest utilizes Helm charts for installation, simplifying its deployment processes, and these charts have undergone several iterations of improvements. The official Percona Helm Charts are readily available in the [percona/percona-helm-charts](https://github.com/percona/percona-helm-charts/tree/main) repository. Furthermore, Percona has generously provided specific [recommendations for deploying Everest with Argo CD](https://github.com/percona/percona-helm-charts/blob/main/charts/everest/docs/argocd.md), which serves as a foundation for our GitOps approach.

For this guide, I've prepared a GKE cluster and installed Argo CD according to its [official documentation](https://argo-cd.readthedocs.io/en/stable/getting_started/). With our Kubernetes environment and GitOps tooling in place, let's dive into deploying Percona Everest.


### Argo CD: A Declarative GitOps Workflow

Argo CD employs a declarative GitOps workflow where application state is defined in Git. It continuously monitors Git repositories and the Kubernetes cluster, automatically reconciling discrepancies to ensure the cluster's state matches the declared Git source. This approach provides consistent, auditable, and easily revertible deployments.

Crucially, this setup directly utilizes official Percona Helm charts, avoiding custom chart creation. Storing these manifests in Git also enables robust change tracking and collaboration.

### Understanding the GitOps Manifests

Our GitOps deployment hinges on two primary Argo CD `Application` manifests: `everest.yaml` and `everest-db.yaml`. These manifests, prepared based on Percona's recommendations and tailored with specific parameters, are located in my repository: [https://github.com/dbazhenov/argocd-percona-everest](https://github.com/dbazhenov/argocd-percona-everest).

Now, let's look at the manifests:

1.  **`apps/everest.yaml`:**
    This manifest defines the core Percona Everest UI and its foundational components, including integration with **Percona Monitoring and Management (PMM)**. Crucially, this chart deploys the Operator Lifecycle Manager (OLM) components and a `CatalogSource` which will be used by the database operators.

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: everest
      namespace: argocd # Namespace where your Argo CD application is defined
    spec:
      destination:
        namespace: everest-system # Target namespace for Everest components within the cluster
        server: https://kubernetes.default.svc
      project: default
      source:
        repoURL: https://percona.github.io/percona-helm-charts/
        chart: everest
        targetRevision: 1.6.0 # Or HEAD for the latest version of the chart
        helm:
          parameters:
          - name: server.service.type
            value: "LoadBalancer"  # Exposes the main Everest UI service externally via a load balancer
          - name: upgrade.preflightChecks
            value: "false"  # Disables preflight upgrade checks for smoother updates
          - name: dbNamespace.enabled
            value: "false"  # Prevents creation of a separate namespace for the database (as everest-db handles operators)
          # PMM Configuration Parameters
          - name: pmm.enabled
            value: "true" # Enables the deployment of Percona Monitoring and Management (PMM) components
          - name: pmm.service.type
            value: "LoadBalancer" # Exposes the PMM service externally via a load balancer
          # If you have an external PMM server, you would configure its details here.
          # Otherwise, the chart will attempt to deploy a PMM server within your cluster.
          # - name: pmm.server.url
          #   value: "https://your-external-pmm-server-ip"
          # - name: pmm.server.username"
          #   value: "admin"
          # - name: pmm.server.password
          #   value: "your-pmm-password"
      syncPolicy:
        automated:
          prune: false  # Prevents deletion of critical resources during sync
          selfHeal: true  # Ensures ArgoCD automatically fixes any drifted configurations
        syncOptions:
        - CreateNamespace=true  # Automatically creates namespaces if they do not exist
        - RespectIgnoreDifferences=true  # Ignores changes in certain Kubernetes objects to avoid unwanted updates
        - ServerSideApply=true  # Enables server-side apply to prevent sync issues with Custom Resource Definitions (CRDs)
      ignoreDifferences:
      # The JWT key is randomly generated if `server.jwtKey` is not set.
      # This prevents ArgoCD from marking it as out-of-sync on each sync.
      - group: ""
        jsonPointers:
        - /data
        kind: Secret
        name: everest-jwt
        namespace: everest-system
      # If `server.initialAdminPassword` is not set, the chart generates a random password.
      # This prevents ArgoCD from marking the Secret as out-of-sync.
      - group: ""
        jsonPointers:
        - /data
        kind: Secret
        name: everest-accounts
        namespace: everest-system
      # If OLM (Operator Lifecycle Manager) is deployed without cert-manager,
      # the below TLS certificates are randomly generated. This prevents sync issues.
      - group: ""
        jsonPointers:
        - /data
        kind: Secret
        name: packageserver-service-cert
        namespace: everest-olm
      # APIService CA bundles and annotations are automatically updated.
      # Ignoring differences prevents unnecessary sync failures.
      - group: apiregistration.k8s.io
        jqPathExpressions:
        - .spec.caBundle
        - .metadata.annotations
        kind: APIService
        name: v1.packages.operators.coreos.com
    ```

2.  **`apps/everest-db.yaml`:**
    This manifest utilizes the `everest-db-namespace` Helm chart. It is responsible for creating the dedicated `databases` namespace and deploying the **Percona Database Operators** (for MongoDB, PostgreSQL, and Percona XtraDB Cluster) within it. It's configured to automatically approve OLM `InstallPlans` for these operators, ensuring a seamless, automated deployment without manual intervention.

    **Crucially, the `destination.namespace` parameter within this manifest defines the Kubernetes namespace where the Percona database operators will be installed, and consequently, where Percona Everest will create and manage your database instances.**

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: everest-db # Name of the Argo CD Application
      namespace: argocd
    spec:
      project: default
      source:
        repoURL: https://percona.github.io/percona-helm-charts/
        chart: everest-db-namespace # Using the everest-db-namespace chart
        targetRevision: 1.6.0 # Match the version of your main everest chart for compatibility
        helm:
          parameters:
            # Enable / Disable operators within this namespace
          - name: psmdb.enabled
            value: "true" # Enable Percona Server for MongoDB operator
          - name: pg.enabled
            value: "true" # Enable Percona Operator for PostgreSQL
          - name: pxc.enabled
            value: "true" # Enable Percona XtraDB Cluster operator
            # Set automatic install plan approval for operators in this namespace
          - name: psmdb.installPlanApproval
            value: "Automatic"
          - name: pg.installPlanApproval
            value: "Automatic"
          - name: pxc.installPlanApproval
            value: "Automatic"
      destination:
        server: https://kubernetes.default.svc
        namespace: databases # <-- This is the namespace where Percona Everest will create and manage databases
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
        - ServerSideApply=true
    ```

### Deploying Percona Everest with Argo CD

Once you've reviewed the manifests, you're ready to deploy.

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/dbazhenov/argocd-percona-everest.git
    cd argocd-percona-everest
    ```

2.  **Deploy the Everest Core Application:**

    ```bash
    kubectl apply -f apps/everest.yaml -n argocd
    ```

3.  **Deploy the Everest Database Operators Application:**

    ```bash
    kubectl apply -f apps/everest-db.yaml -n argocd
    ```

Here's an overview of the deployed applications in the Argo CD UI immediately after applying the manifests:

![Argo CD Applications Dashboard](blog/2025/05/argocd-apps.png)
*Fig 1: Argo CD Applications Dashboard displaying 'everest' and 'everest-db' applications as Healthy and Synced.*

### Monitoring Deployment Progress

Argo CD will now start syncing these applications. You can monitor their status using the Argo CD CLI:

```bash
argocd app list
argocd app get everest
argocd app get everest-db
```

Allow a few minutes for the cluster to provision resources and operators to start. You should observe both applications transition to a **`STATUS Synced`** and **`HEALTH Healthy`**.

A detailed view of the `everest-db` application within Argo CD provides insight into the deployed operator components:

![Argo CD:Detailed resource topology of the everest-db](blog/2025/05/argocd-everest.png)
*Fig 2: Detailed resource topology of the 'everest-db' application in Argo CD, illustrating the successful deployment of Percona database operators via OLM Subscriptions.*

To further verify the successful deployment of the operators, you can check their pods and ClusterServiceVersions (CSVs) in the `databases` namespace:

```bash
kubectl get pods -n databases
kubectl get csv -n databases
```

You should see the operator pods running and their ClusterServiceVersions (CSVs) in a **`Succeeded`** phase.

### Accessing Percona Everest and PMM UIs

Once the applications are **`Healthy`**, you can access the Everest and PMM UIs.

By default, the `everest.yaml` configures the Everest and PMM services to use **`LoadBalancer`** type. This means your cloud provider (e.g., GKE in my setup) will attempt to provision external IP addresses for these services.

If you are running on a local cluster (like Minikube/Kind) or if your cloud provider doesn't support `LoadBalancer` services, you might not get an external IP. In such cases, or if you prefer to access them without an external IP, you can change the service type to **`ClusterIP`** in `apps/everest.yaml` and use `kubectl port-forward`.

To change the service type:
Edit `apps/everest.yaml` and modify these lines under `helm.parameters`:

```yaml
      - name: server.service.type
        value: "ClusterIP" # Change from "LoadBalancer"
      # ...
      - name: pmm.service.type
        value: "ClusterIP" # Change from "LoadBalancer"
```

After modifying the file, run `kubectl apply -f apps/everest.yaml -n argocd` again.

-----

1.  **Get Everest UI Admin Password:**

    ```bash
    kubectl get secret everest-accounts -n everest-system -o jsonpath='{.data.SUPERUSER_PASSWORD}' | base64 --decode
    ```

2.  **Get PMM Admin Password:**

    ```bash
    kubectl get secret pmm-secret -n everest-system -o jsonpath='{.data.PMM_ADMIN_PASSWORD}' | base64 --decode
    ```

3.  **Access the UIs:**

      * **If using `LoadBalancer` (default):**
        Retrieve the external IP addresses for the services:

        ```bash
        kubectl get svc -n everest-system
        ```

        Look for the **`everest`** and **`pmm`** services. If they show an **`EXTERNAL-IP`**, use that to access the UIs in your browser.

          * **For Everest UI:** Navigate to `https://<EXTERNAL-IP_OF_EVEREST_SVC>:8080`
          * **For PMM UI:** Navigate to `http://<EXTERNAL-IP_OF_PMM_SVC>` (PMM typically uses port 80/443 for its UI).

      * **If using `ClusterIP` (or for local access via port-forward):**
        Use `kubectl port-forward` to temporarily expose the services to your local machine:

        ```bash
        # For Everest UI (adjust ports if necessary)
        kubectl port-forward svc/everest -n everest-system 8080:8080

        # For PMM UI (adjust ports if necessary)
        kubectl port-forward svc/pmm -n everest-system 8081:80
        ```

        Then, navigate to `https://localhost:8080` for Everest and `http://localhost:8081` for PMM.

### Database Management and Monitoring

With the Percona Everest UI accessible and the database operators running, you can now provision and manage your database instances. For demonstration purposes, I've created four test databases using the Everest UI.

Here's an example of the Percona Everest UI dashboard, showcasing the managed database clusters:

![Argo CD: Percona Everest UI](blog/2025/05/argocd-percona-everest.png)
*Fig 3: Percona Everest UI displaying a list of managed database clusters (MongoDB, MySQL, PostgreSQL).*

And here's a view of the PMM dashboard, providing integrated monitoring for the deployed databases:

![Argo CD: Percona Monitoring and Management (PMM)](blog/2025/05/argocd-everest-pmm.png)
*Fig 4: Percona Monitoring and Management (PMM) dashboard providing insights into monitored database services and instances within the Everest environment.*

### Conclusion

This post walked through the GitOps deployment of Percona Everest and PMM on Kubernetes using Argo CD. By leveraging Percona's robust Helm charts and Argo CD's declarative reconciliation, we've achieved an automated and transparent setup for managing database infrastructure. The seamless integration of database operators and PMM through Everest provides a powerful platform for operational excellence.

I encourage you to try out this setup in your own environment and share your experiences and insights!