---
title: 'Going back to the original node_exporter in PMM'
date: Mon 31 Aug 2021 00:00:00 +0000
draft: true
tags: ['node_exporter', 'exporter', 'pmm']
authors:
  - carlos_salguero
images:
  - blog/2018/04/safety-2890768_640.jpg
slug: going-back-to-original-pmm-node-exporter
---

This is my first (I hope) post about something not so usual in our regular posts about technology.
Usually we discuss new features, talk about how to do something, but even for me, a Percona developer, sometimes it is hard to know where and what to touch in PMM. There are many components, many abstractions, parts that send messages to remote APIs or agents, the PMM agent, the PMM API (`pmm-managed`), the command line client (`pmm-admin`) and all the external exporters.

In this post, I will try to show how to implement the replacement of the current node_exporter we use in PMM to move back to the original one.

## Apologies in advance

Usually I don't write blog posts. (I am a developer, I don't even write documentation!)
I'll try to be as clear as possible and as interesting as possible but writing about coding might not be exciting for most people.
My motivation in writing this post is to try to encourage people to submit patches and enhancements to PMM, and to help others that want to start participating in the project.
There are many places to contact us to get help, if you need to, but nowadays, [Discord](http://per.co.na/discord) is the fastest place to get answers.

## Why do we use a different node_exporter?

Probably going back in time we could find many other reasons, like maintainability, or the ability to use custom builds, but one of the things that was lacking in the first exporters was the support for basic authentication. In PMM, all exporters metrics are password protected, and since there was no support for that in the past and we needed it as part of our specification PMM exporters use a common HTTP module called `exporter_shared`. In that module, the HTTP server supports basic authentication, and some other features as well, but time has passed. Prometheus exporters are much more mature and now the Prometheus [exporter-toolkit package](https://github.com/prometheus/exporter-toolkit/tree/v0.1.0/https) has support for TLS, HTTP2, cyphers, basic auth, etc.

## Some theory

As mentioned before, there are many components in PMM. The one 'in charge' to start internal and external exporters and run commands is `pmm-agent`. Internal exporters are the ones built into `pmm-agent`, mostly for Query Analytics and for running commands like `EXPLAIN`, `SHOW TABLES`, etc.
Also, `pmm-agent` has an internal `supervisor` that, like the popular Python's [supervisord](http://supervisord.org/) project, run processes (agents) and manages them.

How does `pmm-agent` know which parameters should be used to run each exporter? That's where `pmm-managed` gets involved. `pmm-managed` is the PMM API server and it is the one that sends and receives commands from the UI or the command line client, prepares the messages and delivers them to the proper `pmm-agent`.

As a general rule, all agents are defined in `pmm-managed`'s `services/agents` directory.

![directory](../assets/blog/2021/08/directory.png)

In our case, we want to modify how we start the `node_exporter` so we need to modify the [services/agents/node.go](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go) file.
The [nodeExporterConfig](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go#L31) is defined as follows:

```go
func nodeExporterConfig(node *models.Node, exporter *models.Agent) *agentpb.SetStateRequest_AgentProcess
```

and the returned structure is defined in the `pmm` repository which has all the definitions for PMM.
The [AgentProcess](https://github.com/percona/pmm/blob/PMM-2.0/api/agentpb/agent.proto#L54-L62) message has these fields:

```go
message AgentProcess {
  inventory.AgentType type = 1;
  string template_left_delim = 2;
  string template_right_delim = 3;
  repeated string args = 4;
  repeated string env = 5;
  map<string, string> text_files = 6;
  repeated string redact_words = 7;
}
```

Currently, our `node_exporter` fork receives the user name and password used for the exporter's basic auth via the [HTTP_AUTH](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go#L135-L137) environment var:

```go
Env: []string{
    fmt.Sprintf("HTTP_AUTH=pmm:%s", exporter.AgentID),
},
```

From the Prometheus `exporter-toolkit` package, we can see it receives the configuration information via a file specified with the `--web.config` parameter and the config example tell us we also need to encrypt the password.

```
# Usernames and hashed passwords that have full access to the web
# server via basic authentication. If empty, no basic authentication is
# required. Passwords are hashed with bcrypt.
basic_auth_users:
  [ <string>: <secret> ... ]
```

So, we need to update the `nodeExporterConfig` function to:

1. Update the parameters sent to [pmm-agent](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go#L130-L138) to make the exporter receive the new configuration file.
2. Remove the unused environment variables.
3. Last but not least, update the tests.

In first place, we need to create a new configuration file and make the `node_exporter` use it, but how? The node exporter runs on the client server but `pmm-managed` runs on PMM Server so, at first glance, it is not as easy as writing a file and updating the parameters—but it is. We can spy on another exporter's config definition to see how are they receiving the TLS certificate files, and we can do the same for the `web.config` file. Let's take a look at the `mysql_exporter`.

The [mysqlExporterConfig](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/mysql.go#L33) method returns all the parameters needed to call the node exporter. The [TextFiles](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/mysql.go#L131) parameter is being built [here](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/mysql.go#L100-L113) and for each file there is an exporter's file parameter. For example, for the `--mysql.ssl-ca-file=` parameter it receives:

```
tdp.Left+" .TextFiles.tlsCa "+tdp.Right
```

This might look complicated but **tdp** stands for **T**emplate **D**elimiter **P**air and it is just a helper to choose the correct delimiters in case this value id is used in a template and the rest is just a parameter, in this case, the TLS CA file (the file contents, not just the name).

## Lets begin

### 1. Return files for node_exporter type

In the `agent_model` [Files()](https://github.com/percona/pmm-managed/blob/PMM-2.0/models/agent_model.go#L562) function, we need to return the list of files for `NodeExporterType` and a new function to build the config file (`buildWebConfigFile`).

```go
case NodeExporterType:
    return map[string]string{
        webConfigFilePlaceholder: s.buildWebConfigFile(s.GetAgentPassword()),
    }
```

`webConfigFilePlaceholder` is just a string constant used to identify the different files that can be passed to the agents.

## 2.
