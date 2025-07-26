---
title: "Percona pg_tde: A Security Review Reveals Robust Encryption"
date: "2025-07-24T00:00:00+00:00"
tags: ["Percona", "pg_tde", "PostgreSQL", "Encryption", "Security", "Compliance", "Open Source"]
categories: ['PostgreSQL']
authors:
  - kai_wagner
images:
  - blog/2025/07/pg-tde-security-audit.jpg
---

At Percona, we are committed to providing robust and secure database solutions. We recently engaged Longterm Security for an in-depth review of our Transparent Data Encryption (TDE) feature for PostgreSQL, known as **pg_tde**. This comprehensive assessment included a cryptographic design evaluation, an application security review for coding errors, and extensive fuzz testing. We're excited to share the key takeaways from this engagement, highlighting both pg_tde's strengths and areas for continued improvement.

---

## Strong Foundations in Compliance

A major highlight of the review is pg_tde's excellent alignment with leading **compliance requirements**. Our TDE implementation is well-suited to meet the stringent demands of standards like **PCI-DSS, HIPAA, GDPR, and SOC2**. This is largely due to its adherence to best practices outlined by ECRYPT-CSA, BSI, and NIST, particularly concerning key reuse, master key management, initialization vectors, randomness generation, and various counter modes (CBC, CTR, GCM).

The sole exception identified for full compliance is CNSA (formerly NSA Suite B), which specifically mandates a 256-bit key size for AES. While pg_tde currently supports AES-128, which is widely considered future-proof and meets most compliance needs for data lifetimes beyond 10 years, adding **AES-256 support remains a key recommendation** to meet the demands of government and high-security environments.

While technical work continues on managing temporary files and potentially swappable memory, it’s important to note that compliance standards—such as PCI DSS—generally permit the use of temporary files for encrypting sensitive data like PAN. That said, we understand the practical risks involved and are actively working to mitigate them.

---

## No Major Vulnerabilities Uncovered

After a comprehensive security engagement, we are pleased to report that **no major vulnerabilities have been found within pg_tde**. This outcome is a testament to the robust design principles and meticulous implementation that underpin pg_tde, validating our continuous investment in secure development.

The highest priority issue they found (**LTS-1: Temporary Files Not Subject to Encryption**) was actually something we already knew about and being on our roadmap, while we documented ways to lessen the risk. Our team is also actively tackling another known issue (**LTS-3**) where sensitive data or encryption keys might end up on your disk if your system uses "swap memory." As of today, we do not recommend using SWAP, but we’re actively looking into making it work as well. The other issues they pointed out (**LTS-4 through LTS-7**) are more like helpful suggestions for making things even more robust, rather than actual vulnerabilities.

Here's a quick overview of the findings:

| Issue | Severity | Status | Title |
|---|---|---|---|
| LTS-1 | Medium | Already Known | Temporary Files Not Subject to Encryption |
| LTS-2 | Low | Reported | Disable Core Dumps when pg_tde is active |
| LTS-3.1 | Low | Already Known | palloc memory may be swapped to disk, storing customer data |
| LTS-3.2 | Low | Already Known | palloc memory may be swapped to disk, storing key material from pg_tde |
| LTS-4 | Informational | Informative | Privileged postgres users with file read access may disclose encryption keys from memory |
| LTS-5 | Informational | Reported | Keyring_vault.c: Invalid JSON response can lead to NULL dereference |
| LTS-6 | Informational | Informative | Consider HKDF with Principal Key Usage |
| LTS-7 | Informational | Reported | Document how to securely deploy keyring authentication credentials to systems without storing to disk |
| LTS-8 | Informational | Reported | AES-GCM-SIV is available in very new OpenSSL versions as an alternative key wrapping algorithm |

---

## Always Improving: What's Next for pg_tde around security?

The review also helped us pinpoint a few areas where we can make pg_tde even stronger, especially when it comes to handling memory and exploring advanced encryption techniques:

* **Tackling Swap Memory and Core Dumps:** We're working on ways to prevent sensitive data and encryption keys from potentially leaking to your disk through swap memory or "core dumps" (which happen when a program crashes). We recommend using encrypted swap partitions and turning off core dumps when pg_tde is active. We're also looking into using special memory allocators that keep key material from being swapped out.
* **More Encryption Options:** To meet even more compliance needs and give you more choices, we're considering adding support for a wider range of encryption ciphers, including AES-CBC-256, AES-CTR-256, AES-GCM-256, ChaCha20-Poly1305, and AES-XTS-256. The 256-bit AES key sizes, in particular, will help us achieve CNSA compliance.
* **Smarter Key Management (HKDF with Principal Key Usage):** To boost security even further and protect against theoretical key-reuse attacks, we're evaluating the use of HKDF (HMAC-based Key Derivation Function). This would add an extra layer of protection by creating unique keys for different situations.
* **Securely Handling Your Keyring Credentials:** It's super important that your keyring authentication credentials (like Vault tokens or KMIP keys) are never stored in plain text on your disk. We're putting together clear guidelines for secure deployment, recommending solutions that keep credentials only in memory or use hardware-backed keystores. We'll also advise against putting credentials in command-line arguments.
* **Keeping an Eye on New Algorithms (AES-GCM-SIV):** We're aware of a newer encryption algorithm called AES-GCM-SIV, which is available in very recent OpenSSL versions. While it's not yet FIPS-140-3 compliant and might be a bit slower, it offers better protection against certain types of attacks, and we're definitely keeping it on our radar for future consideration.
* **Preparing for Post-Quantum Cryptography:** The cryptographic landscape is evolving rapidly, with post-quantum encryption (PQC) algorithms on the horizon. As these new algorithms are expected to be more resource-intensive, pg_tde's granular table-level encryption will be crucial for efficiently managing performance overheads, ensuring your data remains secure without compromising application responsiveness in a post-quantum world. We are actively monitoring these ciphers' development and standardization.

---

## Our Commitment to Security

The security review by Longterm Security has been incredibly valuable. It's not only confirmed pg_tde's strong capabilities but also given us a clear roadmap for future development. We're really proud of how secure pg_tde is, which you can see in its readiness for compliance and the fact that no major vulnerabilities were found. Our ongoing efforts to address the identified issues, even the low-priority ones, show just how committed we are to constantly improving and providing you with the most secure database solutions out there.

We're committed to building a secure and reliable data encryption solution, and your feedback plays a vital role in shaping its future. [**Try it out!**](https://docs.percona.com/pg-tde/index/index.html)

If you want to work directly with the code/test/build, take a look at the [GitHub project](https://github.com/percona/postgres/tree/TDE_REL_17_STABLE/). For issues, report them via [Jira](https://jira.percona.com/browse/PG) or go to our [Forum](https://forums.percona.com/c/postgresql/pg-tde-transparent-data-encryption-tde/82) to ask questions. For detailed deployment guidelines and best practices, take a look at our [documentation](https://docs.percona.com/pg-tde/index/index.html). We’re looking forward to any feedback and collaboration around making PostgreSQL secure.
