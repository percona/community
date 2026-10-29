---
title: "A New KMIP Library in C++, and the Only Free One"
date: "2026-10-29T09:00:00+00:00"
draft: false
description: "Percona open sourced kmipclient, a new KMIP library in C++ with a clean, spec-first architecture built to replace a hard-to-extend C implementation."
tags: ['KMIP', 'Encryption', 'Security', 'C++', 'Open Source', 'MySQL', 'Percona Server for MySQL']
categories: ['MySQL', 'Community']
authors:
  - oleksiy_lukin
images:
  - blog/2026/10/kmipclient-new-kmip-library-cover.png
slug: kmipclient-new-kmip-library-in-cpp
---

Percona has open sourced `kmipclient`, a new KMIP library in C++ for applications that need to talk to a key management system over a standard protocol instead of a single vendor's proprietary API.

Encryption is one of the fundamental tools for protecting sensitive data. But encryption is only part of the problem. The keys that unlock that data need to be protected separately from the data itself.

If an attacker gets access to both the encrypted data and the keys required to decrypt it, encryption does not buy much. That is a bit like taping your house key to the front door: the lock is real, but it is not doing much work. Keeping keys under their own administrative and security boundary also makes key rotation, access control, auditing, and revocation easier to manage.

This is why dedicated **key management systems (KMS)** exist. A KMS keeps cryptographic keys in a separate security domain and gives applications controlled access to them, so an application can store encrypted data while the keys stay under the control of the key management infrastructure.

There is another problem, though: different KMS products expose different APIs.

The **Key Management Interoperability Protocol (KMIP)** addresses that by defining a standard protocol for communication between applications and key management systems. KMIP is developed by the [KMIP Technical Committee at OASIS](https://www.oasis-open.org/committees/kmip/) (the Organization for the Advancement of Structured Information Standards), which publishes the KMIP specifications, profiles, and test cases. The protocol has evolved through several versions, from KMIP 1.0 through 1.4 and the 2.x series, with [KMIP 3.0 now in development](https://docs.oasis-open.org/kmip/kmip-spec/v3.0/kmip-spec-v3.0.html).

Several open source KMIP implementations already exist, in Python, Go, and C. We searched extensively and found none of them native C++: `libkmip` itself is a C library, and the handful of C++-adjacent projects out there are either proprietary SDKs or early-stage work with no C++ bindings yet. What was missing was a modern, freely available native C++ implementation with a clean API, current KMIP support, and an architecture that would make further development reasonably painless.

So we built one. `kmipclient` is built on top of its own protocol library, `kmipcore`, and tested against five independent KMIP-capable servers.

## Why build a new KMIP library in C++

At the time, Percona was already maintaining and extending an existing KMIP implementation: a fork of `libkmip`, a C library, wrapped in a thin C++ layer called `kmippp`. (The old code is still there, on the [`legacy-libkmip` branch](https://github.com/percona/kmipclient/tree/legacy-libkmip), for anyone curious about the starting point.) It worked, but extending it was not much fun.

The problem was not that KMIP is difficult to implement. The problem was the shape of the C data model. `libkmip` allocates and frees every request and response type through its own dedicated pair of functions, so adding one KMIP operation means writing a new alloc function, a new free function, and a new parse function, then wiring all three into a C++ wrapper on top. Every small feature turned into a little archaeology dig: find the right allocator, find its matching free function, and hope you freed the thing you actually allocated. The specification implementation was minimal, and even a small addition was expensive to make correctly.

Adding support for the KMIP **Activate** and **Deactivate** operations was a good example. The work meant reading the specification, adding the missing functionality to `libkmip`, and then adding a matching wrapper in `kmippp`. Three layers, for one operation.

That was the point where it became clear: this was costing more in support and development than it should.

What was needed was simple to describe: code that was easier to understand, maintain, test, and extend, without fighting the architecture at every step. So a small weekend project started, not to replace the existing implementation immediately, but to see what a clean, maintainable, extensible native C++ KMIP implementation could look like.

The weekend project grew.

## Splitting the protocol from the client

One of the early decisions was to separate the **KMIP protocol** from the **client** that talks to a server.

`kmipcore` is the protocol library. It holds the KMIP data model, the objects, requests and responses, and the TTLV (Tag-Type-Length-Value) serialization and parsing that KMIP uses on the wire. It has no networking code at all.

`kmipclient` is the client library built on top of `kmipcore`. It provides the higher-level API applications use, handles the communication layer, and adds features such as a thread-safe connection pool.

Networking and logging are both dependency injection points rather than fixed choices. Networking is abstracted behind a replaceable `NetClient` interface, with an OpenSSL-based implementation provided out of the box. Logging follows the same pattern: a `Logger` interface emits structured records that an application can route into its own logging sink instead of one bolted on by the library. Either way, an application can plug `kmipclient` into networking and logging infrastructure it already runs, rather than standing up a parallel one just for this library.

This separation turned out to matter more than expected. `kmipcore` can be tested on its own, with no KMS and no network connection involved. `kmipclient` can then concentrate on the practical problems of talking to a real server. And because `kmipcore` represents the KMIP protocol itself rather than any one client's needs, the same library could also become the foundation for a KMIP server implementation later.

The diagram below shows what that split replaced. The old stack needed three layers in C and C++ to reach `component_keyring_kmip`, Percona Server for MySQL's keyring component for KMIP. The new stack needs one: `kmipcore`, with `kmipclient` sitting on top of it.

![Old C stack (libkmip, kmip_bio, kmippp, three layers) versus new C++ stack (kmipcore, kmipclient, one layer) feeding into Percona Server for MySQL's component_keyring_kmip](blog/2026/10/kmipclient-architecture-old-vs-new.svg)

*Old stack on the left, new stack on the right. `kmipcore` is where new KMIP operations actually get implemented.*

A separate `utils` module, still in progress, is growing alongside the two libraries to hold key and X.509 certificate handling and other shared helpers that do not belong in either the protocol or the client layer.

The first time a new operation took an afternoon instead of a week, the split already felt worth it.

## The specification comes first

KMIP is a fairly large and detailed protocol, and interoperability depends on implementing what the specification says, not just what happens to work against one particular server.

The [KMIP specification](https://www.oasis-open.org/committees/kmip/) was the primary source of truth throughout the project. `kmipclient` supports [KMIP 1.4](https://docs.oasis-open.org/kmip/spec/v1.4/kmip-spec-v1.4.html) and [KMIP 2.0](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/kmip-spec-v2.0.html), including protocol negotiation, while still letting an application select a protocol version explicitly when it needs to.

Real KMS implementations are useful for testing, but interoperability testing validates a specification-based implementation. It is not a replacement for reading the specification. A server accepting what you send does not prove that what you sent was correct according to KMIP, only that this particular server tolerated it.

## Designed to be extended

Fully implementing the KMIP specification is a project of its own, and that was never the near-term goal. The practical goal was narrower: implement what is needed today, while keeping the cost of implementing the next piece of the specification as low as possible.

This is where the split between protocol and client pays off. KMIP objects and operations map directly to C++ types, and adding a new operation mostly means implementing the corresponding protocol objects in `kmipcore`, rather than touching several layers of an older C implementation and a separate C++ wrapper on top of it.

The top-level API is aimed at engineers who care about the result, not the protocol or the cryptography underneath it: activate a key, fetch one, rotate one, without reading the KMIP specification or knowing what a wrapping algorithm is. The protocol details are still there underneath, for the few call sites that actually need them.

The library also supports batching multiple request and response items into a single exchange, which high-level operations use directly. `op_get_key()`, for example, sends a Get and a Get Attributes request as one batch and returns both the key material and its attributes from a single round trip:

```cpp
auto key = client.op_get_key(id);
std::cout << "Key: 0x";
print_hex(key->value());
std::cout << "Attributes:" << std::endl;
for (const auto &[attr_name, attr_value] :
     key->attributes().as_string_map()) {
  std::cout << "  " << attr_name << ": " << attr_value << std::endl;
}
```

*From `kmipclient/examples/example_get.cpp`.*

High-level operations stay just as direct for simpler calls. Activating a key, for instance, is a single method call that returns the server-confirmed key ID or throws:

```cpp
std::string KmipClient::op_activate(const std::string &id) const {
  auto request = make_request_message();
  const auto batch_item_id =
      request.add_batch_item(kmipcore::ActivateRequest(id));

  kmipcore::secure_bytes response_bytes;
  io->do_exchange(
      request.serialize(), response_bytes, request.getMaxResponseSize()
  );

  kmipcore::ResponseParser rf(response_bytes, request);
  return rf
      .getResponseByBatchItemId<kmipcore::ActivateResponseBatchItem>(
          batch_item_id
      )
      .getUniqueIdentifier();
}
```

*From `kmipclient/src/KmipClient.cpp`.*

The library also provides lower-level protocol access for applications that need something more specialized than the high-level API covers.

## From a weekend project to production

Testing turned the prototype into a library other teams could depend on.

The test suite has two layers. Unit tests exercise the protocol and data model on their own, including serialization, parsing, and specification-conformance checks. Integration tests then run against five independent KMIP server implementations: [PyKMIP](https://github.com/OpenKMIP/PyKMIP) (open source), [Cosmian KMS](https://github.com/Cosmian/kms) (source-available), HashiCorp Vault Enterprise, Fortanix Data Security Manager, and Thales CipherTrust Manager.

![Diagram showing unit tests feeding into integration tests, which split into an automated CI pipeline running Cosmian KMS on every commit, and a manual QA pass running all five KMIP servers on every release](blog/2026/10/kmipclient-testing-pipeline.svg)

Cosmian KMS runs in CI, so the integration suite exercises it on every change. CI started out against PyKMIP; the switch to Cosmian KMS came later, driven by its more complete coverage of the KMIP 2.0 specification. Cosmian KMS is source-available rather than open source: its code is public under the Business Source License (BUSL-1.1), which grants free use for non-production work like a CI pipeline outright, free production use up to two vCPUs, and converts to the Mozilla Public License (MPL) 2.0, an open source license, four years after each version's publication.

The other four servers are not practical to spin up on every commit, so Percona's QA engineers run the full integration suite against all five servers by hand after each update, in addition to the automated CI run. Every `kmipclient` release is verified against all five this way, which gives an interoperability matrix and catches regressions that unit tests and CI alone would miss.

`kmipclient` now backs `component_keyring_kmip` in [Percona Server for MySQL's KMIP keyring component](https://docs.percona.com/percona-server/8.0/using-kmip.html), shipping in the 8.4.10 and 8.4.11, 9.7.1 and 9.7.2, and 26.10 releases, with an MTR (MySQL Test Run) suite that exercises it against a Cosmian KMS instance in Docker. It is a general-purpose KMIP client library, though: MySQL was its first important user, not the reason it exists. Teams who previously set up Percona Server for MySQL with HashiCorp Vault Enterprise's KMIP secrets engine through [our earlier keyring plugin walkthrough](https://www.percona.com/blog/using-percona-server-for-mysql-8-0-and-percona-xtrabackup-8-0-with-hashicorp-vault-enterprise-kmip-secrets-engine/) are now running on top of this library.

## Growing through real-world contributions

The project stopped being a one-person exercise early on.

Thanks are due to several Percona engineers who helped along the way: colleagues from the MongoDB team gave an early hand with KMIP itself and with getting test servers running; colleagues from the PostgreSQL team contributed fixes and improvements covering secure handling of sensitive data, protocol correctness, and network robustness; colleagues from the MySQL team reviewed the library's design, API, and usability; and colleagues from the QA team have done extensive testing of both the library and the MySQL KMIP keyring built on it, across all five supported KMIP servers.

Contributions crossing three product teams and QA, for a library that started as a weekend project on one engineer's laptop, says something about how real integration work exposes problems that are hard to find alone. The code gets reviewed, exercised, and occasionally broken in ways a single developer's test environment rarely produces, which is one of the more effective forms of testing there is.

## How AI fit into the process

A significant part of the implementation was done with AI coding assistance, mainly GitHub Copilot. The architecture and API were designed by hand first; AI did a lot of the repetitive implementation work afterward.

The approach was deliberately incremental. The KMIP specifications went in first, so the protocol itself was the primary source of truth, not an impression of what the existing C code already did. The existing C library went in next, for practical context on functionality already in use. Then came a hand-written prototype with the new API, interfaces, stubs, and implementation skeletons already defined.

From there, the process followed a pattern: explain the architecture and goals, check that the model's understanding matched, have it write documentation, then read that documentation back and fix the inconsistencies it surfaced. Development plans came next, broken into a rough work breakdown, followed by the API itself through several rounds of review and revision. Implementation went step by step, function by function, with every step checked rather than accepted on faith.

AI also served as an additional code-review pass: a colleague ran the implementation through several different models for a second set of perspectives. That is not a substitute for human engineering judgment, though. Another colleague reviewed the complete library the traditional way, looking past individual pieces of code at the overall design, API, usability, and maintainability.

AI did a lot of the typing. It did not design the system or make the engineering calls.

There is an irony worth admitting here. Extending `libkmip` by hand, allocator by allocator, is exactly what made the old architecture feel so expensive in the first place. That kind of grind, hunting down the right alloc function and its matching free function, is precisely the work an AI assistant handles well today. Started now, with these tools already in hand, the choice might not be to write a new library at all. It might be to keep extending the old one.

## What's next for kmipclient

The project is not done. A few things are already in motion: folding shared helpers into the `utils` module and tidying up the key-related API, extending the operation API further, rounding out X.509 certificate support, and filling in more of the KMIP specification. A secure memory de-allocation change is currently in review, and memory allocation and general performance work is next on the list.

None of that changes the underlying goal: implement what applications need now, while keeping the next addition to the specification cheap.

## Try the new KMIP library in C++

`kmipclient` is a native, open source C++ implementation of KMIP, built on `kmipcore`, its underlying protocol library. It started as a weekend project aimed at making KMIP development in C++ easier to understand, test, and extend. It has since become a production component in Percona Server for MySQL, tested against five independent KMIP server implementations, with contributions from engineers across three product teams.

It still is not an attempt to implement every corner of the KMIP specification at once. It is a foundation for the functionality applications need today, built so the next piece costs less than the last one did.

Building it requires a C++20 compiler, CMake 3.10 or newer, and OpenSSL. The `kmipclient` keeps the same dual Apache-2.0/BSD license that `libkmip` used, out of respect for `libkmip`'s original author and for the projects already depending on that license.

The project is open source and available on GitHub: **[percona/kmipclient](https://github.com/percona/kmipclient)**. Issues, questions, and contributions are welcome.

And, as is usually true of software, it is not quite finished yet.

---

## Related reading

- [KMIP keyring component in Percona Server for MySQL](https://docs.percona.com/percona-server/8.0/using-kmip.html)
- [Setting up Percona Server for MySQL with HashiCorp Vault Enterprise's KMIP secrets engine](https://www.percona.com/blog/using-percona-server-for-mysql-8-0-and-percona-xtrabackup-8-0-with-hashicorp-vault-enterprise-kmip-secrets-engine/)
- [kmipclient on GitHub](https://github.com/percona/kmipclient)
