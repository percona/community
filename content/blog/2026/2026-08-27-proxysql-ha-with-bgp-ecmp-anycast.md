---
title: "ProxySQL HA with BGP ECMP Anycast"
date: "2026-08-27T11:00:00+00:00"
tags: ['MySQL', 'ProxySQL', 'Opensource', 'BGP', 'Percona Server', 'DevOps']
categories: ['MySQL']
authors:
  - isobel_smith
  - marno_krahmer
images:
  - blog/2026/08/proxysql-ha-with-bgp-ecmp-anycast-cover.jpeg
slug: proxysql-ha-with-bgp-ecmp-anycast
---

# ProxySQL HA with BGP ECMP Anycast

When setting up a new database for an application, high availability (HA) is one of the main priorities. Let's assume for this example that you chose to use a Percona XtraDB (PXC) cluster to host your database.
But how does the application know which PXC node is healthy and can receive application traffic? Introducing a cluster of ProxySQLs can solve this problem, as ProxySQL will healthcheck the database nodes and route the application traffic to the healthy nodes.
However, now the HA problem comes up again: how does the application know which ProxySQL host is healthy?


Putting "one more component" in front of your servers to make them highly available just shifts the problem up by one layer.
From making the database HA, to making ProxySQL HA, to needing to make HAProxy HA and so on…


At some point, you may land on the common HA strategy, keepalived, but BGP ECMP is a powerful alternative worth considering.


## What is BGP, what is ECMP?

As a brief summary, Border Gateway Protocol (BGP) is a routing protocol which operates over TCP. Equal-Cost Multi-Path (ECMP) defines that we want the traffic to be loadbalanced equally across the given routes.
Routers acting as BGP speakers are configured to accept routes for defined IP ranges and Autonomous System (AS) numbers, storing information about the networks that the router can reach in a Routing Information Base (RIB) table.
To benefit from Anycast, we will assign both/all ProxySQL nodes the same virtual IP address. BGP is then used to let the router know multiple routes to reach that IP. Configuring ECMP will cause the router to balance the traffic over these routes.

User defined health checks are executed by a BGP-speaking daemon, such as ExaBGP, running on the host to ensure that the router has the correct information about the status of a route.
As soon as a health check fails, ExaBGP will trigger a BGP update to withdraw the route. The router will remove the entry from its RIB table and stop forwarding packets to that host.
The traffic will be redistributed to the remaining healthy ProxySQL nodes.

For a more in depth guide about BGP please refer to [Cisco press](https://www.ciscopress.com/articles/article.asp?p=2738462&seqNum=2).

## How ECMP based on BGP works

For our setup we can't have the applications connect to the normal IPs of the ProxySQL nodes, as these are assigned to one node and fixed.
Instead we need a single separate anycast IP (let's take 10.5.200.1/32) that we can assign to both ProxySQL nodes. This IP will be assigned to the loopback interface and has to be of a separate network, not overlapping with the IP-Range the normal ProxySQL node IPs are from.

When a packet with the destination set to the ProxySQL anycast IP (10.5.200.1) arrives at the router, the router checks its internal routing table to determine the next hop for the packet.
The router will see the two ProxySQL nodes in the cluster as potential next hop (as they both have the same anycast IP) and will pick one of the ProxySQL nodes, based on ECMP, to forward the packet to.
In ECMP the next hop is dynamically decided based on a 5-tuple hash from the packet header fields:


`{ source IP address | destination IP address | protocol | source port | destination port }`


Because the IP address and ports are in the hash, this ensures that the packets belonging to the same TCP stream are kept on the same path, to prevent packets of the same TCP connection ending up on multiple ProxySQL nodes.

You can visualise the setup like this:

![Diagram](blog/2026/08/proxysql-ha-with-bgp-ecmp-anycast-diagram.png)

By doing so, we have achieved high availability by leveraging BGP ECMP to loadbalance traffic in an active/active configuration across the ProxySQL nodes.
Additionally, the application config can be simplified, as only the single anycast IP (or DNS record for that IP) needs to be used for the ProxySQL cluster, and the logic of routing will be handled by the router.
Failures of a ProxySQL host are automatically handled by ExaBGP; a BGP update is sent to the router, and the route to the failed ProxySQL is withdrawn. The router redirects traffic to the remaining healthy ProxySQL, with no manual interventions required.
Extra infrastructure components (such as internal loadbalancers) can be avoided, eliminating additional network hops and improving network latency.

## Alternative strategies for using BGP with databases

Of course, a ProxySQL cluster is not the only way to leverage BGP ECMP in order to achieve high availability for your databases. Some other strategies could be to use it for read-replica routing, local traffic routing, or for routing towards loadbalancers (e.g. haproxy).

### Routing towards the database loadbalancer

Using BGP ECMP does not mean that you have to forego a database loadbalancer. You can configure your database servers to sit behind a database loadbalancer,
such as HAproxy or ProxySQL, and implement BGP ECMP in order to route traffic towards the loadbalancers and operate them highly available as true active/active pair.
If one of the loadbalancer instances dies, then BGP automatically takes care of routing the traffic to the remaining healthy peers for you.

### Read replica routing

You can use BGP ECMP to distribute MySQL-Connections over multiple read replicas without using any Loadbalancer / ProxySQL at all. This saves you the additional latency and network hops of using a loadbalancer/ProxySQL.
If you need to ensure that you do not read from a replica which is lagging behind or has stopped replicating, you can implement this logic in the BGP health checks.

### BGP Local Preference

If you have a multi-datacenter setup, you can choose to use local preference to keep traffic localised within the same datacenter. For example if you have an application server and a proxysql host in one datacenter (datacenter A), and an application server and proxysql host in a second datacenter (datacenter B),
you can tell the router to send traffic from the application to the proxysql within the same datacenter. The advantage of this is that it keeps network latency low, and avoids cross-site transit. Configuring this in BGP means that the application does not need to be aware of which datacenter it is running in. The BGP router handles localised routing for you.
If the local route would disappear, then the BGP router would automatically divert traffic from the application in datacenter A to the proxysql in the datacenter B.

![Diagram BGP local preference](blog/2026/08/proxysql-ha-with-bgp-ecmp-anycast-lpref.png)


## Advantages of BGP

* One advantage of BGP over keepalived is that your anycast-nodes don't need to be in the same subnet (especially useful for multi-datacenter setups). Keepalived instead requires the nodes to be part of the same Layer 2 Network.
* BGP ECMP supports active/active, unlike keepalived which only supports active/passive architectures.
* In BGP, the router has the overview of which node is healthy or unhealthy. In keepalived this knowledge resides in the keepalived process running on the node itself.
  As long as the nodes running keepalived can see each other, keepalived thinks everything is fine, but the nodes might have lost connection to the router.
  Whereas with BGP, health checks ensure that BGP is aware of the state of the route. In case there would be a network problem that would make the node unreachable, the route would disappear from the router.
* You can horizontally scale the nodes with BGP.
* BGP Local preference allows you to automatically route traffic within a datacenter, without the application needing to configure logic like “use ProxySQL-A when running in datacenter-A, otherwise ProxySQL-B.”
* You can set BGP to eliminate additional hops of infrastructure components, for example connecting to a pool of read replicas, without needing to connect over a loadbalancer.

## Caveats with BGP

BGP ECMP is not connection-state aware, so if instances disappear/die or new instances join and the RIB table is rebuilt, the hashing algorithm will most likely forward packets for existing connections to a different instance than before. As that instance will not be aware of this TCP-Connection, it will send an RST-packet and the application will have to re-open its database connection.

In the next post, we will explain the technical details of setting up BGP ECMP for our ProxySQL cluster using OPNsense as Router.
