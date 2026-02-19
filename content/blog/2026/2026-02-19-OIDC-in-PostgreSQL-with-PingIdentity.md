---
title: "PostgreSQL 18 OIDC Authentication with Ping Identity using pg_oidc_validator"
date: "2026-02-19T00:00:00+00:00"
tags: ['PostgreSQL', 'OIDC', 'Security', 'PingIdentity', 'pg_oidc_validator']
categories: ['PostgreSQL']
authors:
  - mohit_joshi
images:
  - blog/2026/02/ping-oidc-banner.png
---

PostgreSQL 18 introduced native OAuth 2.0 authentication support, marking an important step towards modern, centralized identity-based access control. However, since every identity provider implements OpenID Connect (OIDC) slightly differently, PostgreSQL delegates token validation to external validator libraries. This is where Percona's pg_oidc_validator extension comes in - it bridges PostgreSQL with any OIDC-compliant Identity Provider.

There are several Identity and Access Management (IAM) solutions available today that enable Single Sign-On (SSO) using OAuth 2.0 and OpenID Connect. In an earlier blog by my colleague Fernando, [PostgreSQL OIDC Authentication with pg_oidc_validator](https://www.percona.com/blog/postgresql-oidc-authentication-with-pg_oidc_validator/), he demonstrated how PostgreSQL 18 canbe integrated with Keycloak using pg_oidc_validator. In this post, we explore the same concept using Ping Identity (PingOne).

Ping Identity is widely used in enterprise environments for Identity and Access management. If you are in such an environment, integrating PostgreSQL directly with Ping Identity can provide access control.

This blog is intended for PostgreSQL users, DBAs and customers who want to evaluate or deploy OIDC authentication using pg_oidc_validator. The goal is to provide a practical step-by-step walk-through to get a working setup.

We will cover the following topics as part of this blog:

-   Setting up PingOne environment

-   Install PostgreSQL 18 from Packages

-   Configure PostgreSQL for OAuth/OIDC authentication

-   Test login using an OIDC flow

# Setting up PingOne environment

1.  Register a new [account](https://www.pingidentity.com/en/account/register.html)

![](blog/2026/02/ping-account-register.png)

2.  Fill in the details to complete the profile

![](blog/2026/02/ping-profile.png)

3.  Next step is to Sign-In into the Ping Identity [account](https://www.pingidentity.com/en/account/sign-on.html)

![](blog/2026/02/ping-sign-on.png)

4.  Log in to the Ping Identity Administrator Console and create a new environment by clicking on the + sign

![](blog/2026/02/ping-admin-console.png)

5.  Provide an environment name and click on Finish

![](blog/2026/02/ping-environment.png)

6.  Once the environment is created, click on Manage environment.

![](blog/2026/02/ping-manage-environment.png)

7.  Add a new Application, select the type as **Device Authorization** and click on Save.

![](blog/2026/02/ping-new-application.png)

8.  Upon successful creation, we will see generated **Client ID** and **Issuer ID**. The Issuer ID can be copied from under the *Connection Details* section. Enable the toggle so that the application is Active.

![](blog/2026/02/ping-created-application.png)

9.  The next step is to add a new user. Goto **Directory -\> Users** and click on + sign.

    For our exercise, we are creating a user called **employees.** In some Identity Providers (IdPs), it is possible to customize the ID token and control how certain claims (including the **sub** - subject claim) are generated or mapped. However, it is important to note that, currently in PingOne, the **sub** (subject) claim for the default OpenID Connect resource cannot be customized. The value of **sub** is generated and managed internally by PingOne and cannot be altered, mapped or derived from another attribute (such as email or username). As a result, PostgreSQL must be configured to work with the **sub** value exactly as issued by PingOne.

![](blog/2026/02/ping-create-user.png)

10. Enable the user by turning the toggle "ON" and set a password.![](blog/2026/02/ping-enable-user.png)


# Install PostgreSQL 18 from Packages

Since OAuth support is only available starting with PostgreSQL 18, we need a PostgreSQL server of at least this version.In the guide, we will install PostgreSQL 18 using Percona's official packages.

**Note:**

1.  Ensure that the [percona-release](https://docs.percona.com/percona-software-repositories/installing.html) is already installed and configured on your system. You can refer to the official Percona documentation for setup instructions.

2.  For this exercise, the steps are demonstrated on Ubuntu 24.04, so Debian-based (.deb) packages and apt are being used.

**Enable the PostgreSQL 18 repository**
```bash
sudo percona-release enable-only ppg-18.2 release
sudo apt update
```

**Install PostgreSQL 18**
```bash
sudo apt install -y percona-postgresql-18
```

**Install OAuth Support for libpq**
```bash
sudo apt install libpq-oauth
```

# Configure PostgreSQL for OAuth/OIDC authentication

**Install pg_oidc_validator**
```bash
sudo apt install percona-pg-oidc-validator18
```
**Creating the test database**

Imagine the following use case:

-   Imagine a company that regularly generates promotional discount codes and stores them in a table called "dcode" inside a database named "promo".

-   A new discount code is generated and added to this table every day.

-   The company wants all employees to be able to access the latest code whenever needed.

-   For simplicity in this demonstration, employees retrieve the code by connecting to the database and querying the table directly.

-   To avoid managing individual database accounts for every employee, access is not tied toseparate user credentials.

-   Instead, authentication to the database is handled through the company's SSO system, allowing employees to connect using their existing corporate identity.

```text
                  +------------------+
                  |   Ping Identity  |
                  |      (SSO)       |
                  +---------+--------+
                            |
                            | Authenticates
                            |
                  +---------v--------+
                  |     employees    |  (DB Role)
                  +---------+--------+
                            |
                            | SELECT
                            |
                  +---------v--------+
                  |   promo database |
                  |------------------|
                  |      dcode       |
                  +------------------+
```

**Let's connect to PostgreSQL:**
```bash
sudo -u postgres psql
```

**Create a database:**
```sql
CREATE DATABASE promo;
\c promo
```

**Add a table to store the discount code:**
```sql
CREATE TABLE dcode (code varchar(10), GENERATED_AT TIMESTAMP default now());
INSERT INTO dcode (code) VALUES ('SAVENOW');
```
**Create the access user:**
```sql
CREATE ROLE employees WITH LOGIN;
GRANT SELECT ON dcode TO employees;
```

**Configure OAuth access in PostgreSQL:**

Finally, in order for users to connect using OAuth and authenticate through the Ping Identity server, we need to create an identity map and add an entry for such access on PostgreSQL's authentication configuration file.

Edit the identity mapping configuration file and add an entry, which we will call *oidc*, mapping connections originated by a system user identified with a sub ID. For this exercise, we allow any string to match
```bash
vim /etc/postgresql/18/main/pg_ident.conf

# MAPNAME SYSTEM-USERNAME DATABASE-USERNAME
oidc /^(.*)$ employees
```
Next, edit the authentication configuration file. The configuration file *pg_hba.conf* acts as a sort of firewall for connections. With the below line, we are instructing PostgreSQL to allow all connections coming from any network that attempt to access the database promo as user employees using the new authentication method *oauth*. We are also indicating that the authentication provider is Ping Identity and the scope is *openid*.

**Note:** 
  1. Place this entry after the existing local rules and just before the replication rules in pg_hba.conf. PostgreSQL evaluates pg_hba.conf from top to bottom, and the first matching rule is applied. Putting the OAuth rule earlier ensures that connections to database promo as user employees use OAuth instead of falling back to password authentication.

  2. In production environments, restrict the IP range instead of using *0.0.0.0/0*

  3. The oauth_issuer is the **Issuer ID** which we copied earlier during PingOne environment setup.

```bash
vim /etc/postgresql/18/main/pg_hba.conf

# TYPE DATABASE USER ADDRESS METHOD
host promo employees 0.0.0.0/0 oauth issuer=https://auth.pingone.com.au/64935f69-5a0a-4b69-a8bd-46967d218303/as scope=openid map=oidc
```


**Enabling the pg_oidc_validation extension**

Edit the postgresql.conf and add below lines
```bash
vim /etc/postgresql/18/main/postgresql.conf

oauth_validator_libraries = 'pg_oidc_validator'
pg_oidc_validator.authn_field = sub
```

In this configuration, we instruct pg_oidc_validator to use the sub claim from the OIDC token as the authenticated identity.

The sub claim is defined by the OpenID Connect specification as a stable and unique identifier for a user within an Identity Provider (IdP). It is intended to uniquely represent a user and remain consistent across authentication sessions.

PostgreSQL does not interpret or transform this value. The validator extracts the configured claim and PostgreSQL simply compares it against a database role or an entry in pg_ident.conf. If the value does not match the expected role or mapping, authentication will fail, even if the token itself is valid.

It is also important to note that PostgreSQL is not limited to using the sub claim. The pg_oidc_validator extension can be configured to use any claim present in the ID token. For example, if your IdP includes the user's email in the token, you could instead configure:

```text
pg_oidc_validator.authn_field = email
```

However, whether a claim is present in the token depends on the scopes requested during authentication. Scopes control what identity information the Identity Provider includes in the token. Common examples include:

-   openid - ensures a valid identity token with a sub claim
-   email - includes the user\'s email address
-   profile - includes basic profile details like name and username

If a claim is not included in the requested scope, it will not appear in the token, and PostgreSQL will not be able to use it for authentication or identity mapping. Therefore, when changing authn_field to use a different claim, ensure that the corresponding scope is requested and that the claim is actually present in the issued token.

**Note**: PingIdentity does not allow customized tokens for the default resource - **OpenID Connect**. We can only use pg_oidc_validator.authn_field = sub


**Reload the configuration**

```bash
sudo -u postgres psql
SELECT pg_reload_conf();
```

**Monitor the server logs**
```bash
tail -f /var/log/postgresql/postgresql-18-main.log
```

# Test login using an OIDC flow

**Connecting to the database:**

For this quick connection test, we use psql to connect to the promo database as the employees user, explicitly specifying the host IP along with the **oauth_issuer** and **client_id**.
```bash
psql 'host=127.0.0.1 user=employees dbname=promo oauth_issuer=https://auth.pingone.com.au/64935f69-5a0a-4b69-a8bd-46967d218303/as oauth_client_id=1e892f71-09d7-4ed6-a534-0dc888d39c7c'
```
By connecting via the host IP address rather than the local socket, PostgreSQL treats this as a host-based connection, ensuring that the OAuth configuration in pg_hba.conf is applied and that the authentication request is redirected to PingIdentity for validation.

We will see a prompt on the console with the URL and activation code.You will notice an activation code **XXXX-XXX.** Example shown below:
```text
Visit https://auth.pingone.com.au/64935f69-5a0a-4b69-a8bd-46967d218303/device and enter the code: 7KK7-88DK
```
Upon clicking the URL, it will prompt you to log in with the **employee\'s** user, which we created during the PingOne environment setup.

![](blog/2026/02/ping-user-login.png)

Next, it will prompt you to reset your password, then enter the activation code.

![](blog/2026/02/ping-activation-code.png)

Approve the access to the employee\'s user and that's it! We have successfully authenticated the user via OIDC

![](blog/2026/02/ping-approve-user.png)

Return to the PostgreSQL prompt and you should see that the login to the promo database is successful. You can now query the *dcode* table to fetch the discount code.

```bash
mohit.joshi@qa-hd-27527:~$ psql 'host=127.0.0.1 user=employees dbname=promo oauth_issuer=https://auth.pingone.com.au/64935f69-5a0a-4b69-a8bd-46967d218303/as oauth_client_id=1e892f71-09d7-4ed6-a534-0dc888d39c7c'
Visit https://auth.pingone.com.au/64935f69-5a0a-4b69-a8bd-46967d218303/device and enter the code: 7KK7-88DK
psql (18.2 - Percona Server for PostgreSQL 18.2.1)
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off, ALPN: postgresql)
Type "help" for help.

promo=> select * from dcode;
  code   |        generated_at
---------+----------------------------
 SAVENOW | 2026-02-13 09:40:13.109801
(1 row)
```

With the steps shown in this guide, we now have a working end-to-end setup using OIDC authentication and device flow login. From here, the same model can be extended to real-world enterprise environments with tighter network restrictions and role mapping.

If you run into issues while setting up pg_oidc_validator or integrating PostgreSQL with Ping Identity, check the [community forums](https://forums.percona.com/) first, chances are someone in the community may already have encountered a similar issue. If not, feel free to open a [discussion](https://github.com/Percona-Lab/pg_oidc_validator/issues) or raise a request for help.
