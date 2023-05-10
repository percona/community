---
title: 'Going back to the original node_exporter in PMM'
date: "2021-10-21T15:00:00+00:00"
tags: ['node_exporter', 'exporter', 'pmm']
authors:
  - carlos_salguero
images:
  - blog/2021/10/directory.png
slug: going-back-to-original-pmm-node-exporter
---

This is my first (I hope) post about something no so usual in our regular posts about technology.

Usually we discuss new features, talk about how to do something but even for me, a Percona developer, sometimes it is hard to know where and what to touch in PMM. There are many components, many abstractions, parts that send messages to remote APIs or agents, the PMM agent, the PMM API (pmm-managed), the command line client (pmm-admin) and all the external exporters.

In this post, I will try to show how to implement the replacement of the current node_exporter we use in PMM to move back to the original one.

## What this post is about?

In the next paragraphs, I'll try to explain the basics of how PMM works. My intention is to walk you trough the internals of the PMM API and PMM agent, how do the communicate and how to make some code changes.
There are many places to contact us to get help if you need to, but nowadays, [forums.percona.com](https://forums.percona.com/) is the fastest place to get answers.
I will try to keep things clear and simple, but this is a technical post so, there will be some code.

## Why do we use a different node_exporter?

Probably going back in time we could find many other reasons, like maintainability, or the ability to use custom builds but one of the things that lacked in the first exporters was the support for basic authentication. In PMM, all exporters metrics are password protected and since there was no support for that in the past and we needed it as part of our specification, PMM exporters use a common HTTP module called `exporter_shared`. In that module, the HTTP server supports basic authentication and some other features as well but time has passed, Prometheus exporters are much much mature and now  the Prometheus [exporter-toolkit package](https://github.com/prometheus/exporter-toolkit/tree/v0.1.0/https) has support for TLS, HTTP2, cyphers, basic auth, etc.

##  How PMM works.

As mentioned before, there are many components in PMM. The one in charge to start internal and external exporters and run commands is `pmm-agent`. Internal exporters are the ones built in into `pmm-agent`, mostly for Query Analytics and running commands like `EXPLAIN`, `SHOW TABLES`, etc.
Also, `pmm-agent` has an internal `supervisor` that, like the popular Python's [supervisord](http://supervisord.org/) project, run processes (agents) and manage them.

How does pmm-agent know which parameters should be used to run each exporter? That's where `pmm-managed` gets involved. `pmm-managed` is the PMM API server and it is the one that sends and receive commands from the UI or the command line client, prepare the messages and deliver them to the proper `pmm-agent`.

As a general rule, all agents are defined in `pmm-managed`'s `services/agents` directory.   

![directory](../assets/blog/2021/10/directory.png)

In our case, we want to modify how we start the `node_exporter` so we need to modify the [services/agents/node.go](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go) file.
The [nodeExporterConfig](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go#L31) is defined as follows:

```go
func nodeExporterConfig(node *models.Node, exporter *models.Agent) *agentpb.SetStateRequest_AgentProcess 
```

and the returned structure is defined in the pmm repository which has all the definitions for PMM. 
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

Currently, our node_exporter fork receives the user name and password used for the exporter's basic auth via the [HTTP_AUTH](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go#L135-L137) environment var:

```go
  Env: []string{
  	fmt.Sprintf("HTTP_AUTH=pmm:%s", exporter.AgentID),
  },
```

From the Prometheus exporter-toolkit package, we can see it receives the configuration information via a file specified with the `--web.config` parameter and the config example tell us we also need to encrypt the password

```yaml
# Usernames and hashed passwords that have full access to the web
# server via basic authentication. If empty, no basic authentication is
# required. Passwords are hashed with bcrypt.
basic_auth_users:
  [ <string>: <secret> ... ]
```

so, we need to update the `nodeExporterConfig` function to:

1. Update the parameters sent to [pmm-agent](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/node.go#L130-L138) to make the exporter receive the new configuration file.
2. Update the node config response to include the new files and remove unused env vars.
3. Last but not least, update the tests. 

In first place, we need to create a new configuration file and make  the`node_expoter`use but, how? The node exporter runs on the client server but pmm-managed runs on pmm server so, at first glance, it is not as easy as writing a file and updating the parameters but it is. We can spy on other exporter's config definition to see how are they receiving the TLS certificate files and we can do the same for the web.config file. Let's take a look at the mysql_exporter.

The [mysqlExporterConfig](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/mysql.go#L33) method returns all the paremeters needed to call the node exporter. The [TextFiles](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/mysql.go#L131) parameter is being built [here](https://github.com/percona/pmm-managed/blob/PMM-2.0/services/agents/mysql.go#L100-L113) and for each file there is an exporter's file parameter. For example, for the `--mysql.ssl-ca-file=` parameter it receives:

```
tdp.Left+" .TextFiles.tlsCa "+tdp.Right
```

This might look complicates but **tdp** stands for **T**emplate **D**elimiter **P**air and it is just a helper to choose the correct delimiters in case this value id used in a template and the rest is just a parameter, in this case, the TLS CA file (the file contents, not just the name).

## Implementing the changes.

### 1. Return files for node_exporter type

The current node_exporter in PMM is a fork that doesn't use the exporter-toolkit package for the http server, it uses Percona's exporter_shared instead so, to make the upstream exporter behave like the forked one, we need to create a pass a file for the `--web.config` parameter having the Basic Authentication parameters we use to protect the metrics exposition.

In pmm-managed agent_model's [Files()](https://github.com/percona/pmm-managed/blob/PMM-2.0/models/agent_model.go#L562) function, we need to return the list of files for `NodeExporterType` and we are going to write a new function to build the config file (`buildWebConfigFile`).

`webConfigFilePlaceholder` is just a string constant used to identify the different files that can be passed to the agents.

```
const (
	.
	.
	.
	// webConfigFile is the Prometheus HTTP Toolkit's web.config file.
	// It the basic auth parameters we need to set for node exporter.
	// All other exporters are using exporter shared but after going back to the upstream
	// version of node_exporter, we need to pass this file to pmm-agent.
	webConfigFilePlaceholder = "webConfigPlaceholder"
)
```

```
	case NodeExporterType:
		return map[string]string{
			webConfigFilePlaceholder: s.buildWebConfigFile(s.GetAgentPassword()),
		}
```

The `buildWebConfigFile` returns the file content needed to specify user and password for the exporter's basic auth.

According to the [documentation](https://github.com/prometheus/exporter-toolkit/tree/v0.1.0/https),the password must be encrypted so, our function receives a plain-test password and return the configuration file contents with the password encrypted with bcrypt.

```
func (s *Agent) buildWebConfigFile(password string) string {
	buf, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	if err != nil {
		log.Fatal(err, "cannot encrypt basic auth password")
	}

	content := "basic_auth_users:" + "\n" +
		"    pmm:" + string(buf) + "\n"

	return content
}
```

### 2. Update the node service

In `services/agents/node.go` there is a `nodeExporterConfig` which is called to get the exporter configuration.

The new implementation should get the files the exporter is going to use and remove the now unused environment variables. 

The code will look like this:

```
	files := exporter.Files()
	for k := range files {
		switch k {
		case "webConfigPlaceholder":
			// see https://github.com/prometheus/exporter-toolkit/tree/v0.1.0/https
			args = append(args, "--web.config="+tdp.Left+" .TextFiles.webConfigPlaceholder "+tdp.Right)
		default:
			continue
		}
	}

	sort.Strings(args)

	return &agentpb.SetStateRequest_AgentProcess{
		Type:               inventorypb.AgentType_NODE_EXPORTER,
		TemplateLeftDelim:  tdp.Left,
		TemplateRightDelim: tdp.Right,
		Args:               args,
		Env:                []string{},
		TextFiles:          files,
	}
```

### 3. Updating tests

Since we changed the response for the `nodeExporterConfig` method and now we are returning files and removed the environment vars, tests will fail.

We need to update the tests at `services/agents/node_test.go` to reflect the changes. I am not going to get into the details because they are trivial but I do want to mention that since the encrypted password is not always the same (because of the nature of the function) I am just comparing that we are returning a file from the Files() method (`agent_model.go`).

If you never ran the test for pmm-managed let me quickly show the the only 2 steps needed:

1. make env-up
2. make env TARGET=test

With those 2 commands, you will be able to run all the tests in the suite to ensure the changes won't break anything.


I hope I was able to explain at least the basics about how to make changes in PMM.
Remember you can contact us at community-team@percona.com ans we will be glad to answer your questions.

