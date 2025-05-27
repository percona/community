# PostgreSQL 18 - top enterprise features (fast read)

So the ~[Beta1 is available for PostgreSQL 18](https://www.postgresql.org/about/news/postgresql-18-beta-1-released-3070/)~ and while not all the ~[features](https://www.postgresql.org/docs/18/release-18.html)~ have to make it to GA, we can surely hope they do!


![PostgreSQL 18 is coming!](blog/2025/05/pg18img.png)

![](2025-05-27-PostgreSQL_18_-_top_enterprise_features_%28fast_read%29/2025-05-22_15-59-43.png)
Taking a close look at ~[what’s coming](https://www.postgresql.org/docs/18/release-18.html)~, here below is the selection of what excites me in particular:
### 1. OAuth 2.0 authentication support
→ Finally aligns with modern enterprise SSO and identity standards (e.g., Okta, Azure AD). A major win for security teams and regulatory compliance.
### 2. Logical replication from standbys now with conflict logging
→ Now you can replicate from replicas not only primary nodes and thanks to conflict logging troubleshooting issues moves closer to what the users have been asking for. It’s a big step toward robust, native, HA-friendly logical replication. Not yet there, but on the right path!
### 3. Asynchronous I/O (AIO)
→ Modern async reads improve performance, especially under heavy parallel workloads. Foundation for future IO improvements, and also a feature that scratches an itch for a lot of cloud deployments.
### 4. Faster & safer major upgrades
→ pg_upgrade ****enhancements like ****parallel upgrade checks (--jobs), safer upgrades (--swap), and planner stats carried forward = faster version adoption and smoother upgrades for large clusters.
### 5. Observability++
→ Enhanced EXPLAIN statement and pg_stat_io improvements enhance understanding and optimize I/O behavior across tables, indexes, and WAL. This reduces the need for external monitoring tools.
# Other Notable Features
While these are the top mentions, the goodies are not limited to only these. Some smaller improvements are just as exciting. Looking at these, the top interesting ones for me are:
* **New** extension_control_path **Server Variable** → Enables operators to manage PostgreSQL extensions via **Kubernetes image volumes** (~[Kubernetes 1.33 image volumes](https://kubernetes.io/blog/2025/04/29/kubernetes-v1-33-image-volume-beta/)~) without modifying the base image. → Huge win for immutable image strategies and GitOps-friendly operator design.
* Easier online constraints management → Add new NOT NULL constraints without locking large tables using NOT VALID → Use NOT ENFORCED foreign keys and CHECK to model relationships without runtime overhead
* **Smarter index maintenance (bottom-up deletion)** → Reduces bloat, lowers vacuum overhead.
* **SQL/JSON path support + JSON performance gains** → Enables document-style querying at scale.
* **Better insights into queries and vacuum** → EXPLAIN now includes buffer usage in subplans, triggers, and functions which helps spot slow parts → pg_stat_all_tables now tracks how much time vacuum and autovacuum take per table
* **Indexing improvements** → Parallel GIN builds help speed up full-text and vector searches key for hybrid full-text and vector search → B-tree skip scans make range and selective queries faster

# What enterprises would want in PostgreSQL 19+
There is already a lot to like in this release, but based on what we hear from users, customers, and our own teams, here is what is still high on the list.
First up and this one’s close to home is that we’d love to see the Transparent Data Encryption (TDE) patches from Percona Server for PostgreSQL make their way upstream. That would allow users to benefit from pg_tde directly in Community PostgreSQL Server.
The rest of the list is a mix of long standing asks and forward looking ideas. It is a wishlist for sure, but one we hope to help make real over time:
* **Built-in Logical Conflict Resolution Algorithms** → Support for conflict-handling strategies (e.g., last-write-wins, column-level rules) would simplify bidirectional replication and eliminate the need for custom frameworks, opening the door for fully open-source multi-master setups.
* **Logical failover orchestration** → Seamless promotion and failover in logical topologies, with less reliance on external tooling. This would be great from the perspective of both Kubernetes deployments as well as the ease of use for HA solutions out there.
* **Better integration with external auth systems** → Automatic PostgreSQL user creation based on OAUTH/LDAP roles at login, reducing operational burden for large-scale identity management and central access control.
* **Pluggable or columnar storage support** → Native support or better extension hooks for OLAP and hybrid workloads, closing the gap with cloud-native alternatives like Citus or Redshift.
* **Sharding to provide horizontal scaling** → Transparent sharding is a highly desired capability that becomes critical as workloads scale. While not always needed on day one, having built-in sharding means teams can grow without reinventing the wheel. Lack of it makes horizontal scaling complex, requiring more expertise and introducing higher operational overhead for DBA teams.


