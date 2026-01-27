---
id: "1597e92e-f772-4d99-9d5b-ad7aad597112"
title: "How Transparent Data Encryption is built in MySQL and Percona Server ?"
layout: single
speakers:
  - robert_golebiowski
talk_url: "https://fosdem.org/2020/schedule/event/security_how_transparent_data_encryption_is_built_in_mysql_and_percona_server/"
presentation_date: "2020-01-31"
presentation_date_end: ""
presentation_time: "11:30 PM"
talk_year: "2020"
event: "FOSDEM 2020"
event_status: "Done"
event_date_start: "2020-02-01"
event_date_end: "2020-02-02"
event_url: "https://fosdem.org/2020/"
event_location: "Belgium"
talk_tags: ['MySQL', 'Open Source']
slides: ""
video: "https://archive.fosdem.org/2020/schedule/event/security_how_transparent_data_encryption_is_built_in_mysql_and_percona_server/"
---
## Abstract

How Transparent Data Encryption is built in MySQL and Percona Server ? - keyrings – what are they used for ? What is the difference between using a server back-end (keyring_vault) versus file back-end (keyring_file). How it affects server startup and why? Why per server separation is needed in Vault Server?
- How Master Key encryption works ? How it is build on page level ? How do we know which key we should fetch to decrypt a table ? How do we know that used key is the correct one ? How do we make sure that we can decrypt a table when we need it ?
- What crypto algorithms are used ?
- How Master Key rotation works ? Why is it needed ?
- What is KEYRING encryption and what are encryption threads?
- How binlog encryption works in 5.7 and how it works in 8.0 ?
- How undo log/redo log encryption works ?