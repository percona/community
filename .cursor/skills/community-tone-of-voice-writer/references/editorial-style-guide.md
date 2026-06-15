# Percona Editorial Style Guide
# v3. 2024-01

This is the authoritative style reference for all Percona content, including community content.
Apply every rule in this guide. When in doubt, default to AP Style unless a Percona exception
is noted below.

---

## Percona and Percona software naming rules

### Percona (the company)
- Always capitalized.
- Employees are Perconians.
- Avoid making Percona possessive when referring to products and solutions: Percona software, not Percona's software.
- Possessive is fine in general references: Percona's future, Percona's own Cindy Neely.

### Percona Blog
- Capitalize Blog when it follows Percona. Lowercase when used generally: our blog.

---

## Services

### General rules for all services
- Capitalize umbrella terms: Percona Support, Percona Consulting, Percona Managed Services.
- Capitalize when referring to the team: Contact the Managed Services team.
- Lowercase when used generally: MySQL support from Percona.
- Always spell out the full name on first and final mention and in CTAs.
- Link to the respective service page on first mention.

### Percona Support for [DBMS]
Write out in full. Never write Percona DBMS Support or Percona [DBMS] Database Support.
- Percona Support for MySQL
- Percona Support for MongoDB
- Percona Support for MariaDB
- Percona Support for PostgreSQL

### Percona Support for DBaaS
Write in full. Never spell out DBaaS as Database as a Service when referring to this offering.

### Percona Managed Services (PMDS)
Write out in full. When referring to a specific technology:
- Percona Managed Services for MySQL
- Percona Managed Services for PostgreSQL
- Percona Managed Services for MongoDB
Do not write "MongoDB Managed Services" when talking specifically about the Percona offering.

### Percona Consulting
Write out in full. Capitalize Consultants when referring to Percona Consultants. Lowercase when used generally.

### Percona Experts
Capitalize Experts when following Percona. Lowercase when used generally.

---

## Software and solutions

### General rules for all solutions
- Capitalize every word except conjunctions.
- No preceding article: Percona Server for MySQL, not the Percona Server for MySQL.
- Do not generalize: Percona Monitoring and Management (PMM), not "our monitoring and management solution."
- Link to the solution page (not documentation) on first mention.
- Include a short description unless you intend to describe further.
- Always spell out the full name on final mention and in CTAs.
- Software is always "freely available," never "free."
- Use "solution" not "product."

### Percona Everest
- Always use the full name: Percona Everest. Never Everest, never abbreviated.
- Never preceded by an article: not "the Percona Everest solution."
- Never referred to as a DBaaS solution. Always defined as a cloud-native database platform.
- Description: Percona Everest is a cloud-native database platform that provides automated database provisioning and management, eliminating the need for in-house development.

### Percona Monitoring and Management (PMM)
- Write out in full on first mention with abbreviation: Percona Monitoring and Management (PMM).
- Subsequent mentions can use PMM.
- Never use the "&" symbol — always write "and."
- Exception for length: PMM can be used without spelling out, as long as it is defined somewhere in the piece.

### Percona Operators
- Write out in full on first mention. Always capitalize.
- They are not "Percona Kubernetes Operators." Kubernetes is not part of the product name.
- Individual solutions: Percona Operator for PostgreSQL, Percona Operator for MongoDB, Percona Operator for MySQL.
- Percona Operator for MySQL variants: based on Percona XtraDB Cluster / based on Percona Server for MySQL. Note: "based" is lowercase.

### Percona XtraDB Cluster (PXC)
- Write out in full on first mention with abbreviation: Percona XtraDB Cluster (PXC).
- Never un-stylize: not "extra cluster" or similar.
- PXC can be used on subsequent mentions after abbreviation is introduced.

### Percona XtraBackup
- Write out in full. Do not un-stylize.

### Percona Server for MySQL / Percona Server for MongoDB
- Write out in full, including the full database name.
- PSMDB is searchable: always write Percona Server for MongoDB (PSMDB) on first mention.

### Percona Distribution for [DBMS]
- Percona Distribution for MySQL
- Percona Distribution for MongoDB
- Percona Distribution for PostgreSQL
- Write out in full, including the full database name.

### Percona Backup for MongoDB
- Write out on first mention. Can abbreviate to PBM after introduction.

### Percona XtraDB Cluster and Percona Distribution for MySQL based on Percona XtraDB Cluster
- See Percona XtraDB Cluster above.

### Percona Pro Builds
- Capitalize. Pluralized. Never "professional builds."
- Do not refer to as "our Pro Builds" or "Percona's Pro Builds."

### Percona Server for MongoDB Pro
- Always capitalize and write in full. Never abbreviate.

### PostgreSQL
- Always write PostgreSQL (not Postgres) when referring to a Percona solution or service.
- Percona Distribution for PostgreSQL — not Percona Distribution for Postgres.
- Postgres is acceptable on second mention for general (non-Percona) references.

### Percona Account
- Always capitalize. Your Percona Account or a Percona Account.

### Percona Advisors
- Always capitalize. Write in full when referring to the collective offering.
- Specific types (Security Advisors, Performance Advisors) can drop Percona after the concept is introduced.

---

## Key industry terminology

### Open source
- Never hyphenated. Never: open-source solutions. Always: open source solutions.
- Lowercase except in title case or at the start of a sentence.

### Cloud
- Lowercase except in title case or as part of a proper name.

### Database
- Never capitalized except in title case or at the start of a sentence.
- If abbreviating to DB, define on first mention: database (DB).

### Database Administrator (DBA)
- Always capitalize. Spell out on first mention with abbreviation if using later.
- Plural: DBAs (lowercase s).

### Database as a Service (DBaaS)
- Capitalize Database and Service in the full term. Never hyphenate.

### High availability
- Do not capitalize. Abbreviate to HA only after first mention with abbreviation included.

### Kubernetes Operator(s)
- Always capitalized.

### On-premises
- Always hyphenated. Never on-premise or on-prem.
- The "p" is never capitalized. The "o" is capitalized only at the start of a sentence or in a title.

### On demand
- Not hyphenated standalone: sessions are available on demand.
- Hyphenated as a modifier: the on-demand streaming service.

### End of Life
- Capitalize and follow with (EOL) on first reference: End of Life (EOL).

### Software as a Service (SaaS)
- Capitalize Software and Service in the full term. Never hyphenate. Abbreviation SaaS is well known enough to use without defining.

### Lock-in / lock in
- Lock-in: noun, hyphenated — vendor lock-in.
- Lock in: verb, not hyphenated — the vendor will lock in your data.

### Query Analytics
- Capitalize when referring to the PMM dashboard. Lowercase as a general term.
- May abbreviate to QAN after first mention with abbreviation included.

### Private and public DBaaS
- Lowercase private and public except at the start of a sentence or in a title.

---

## AP Style — key rules and Percona exceptions

### Percona follows AP Style with these exceptions:
- **Open source:** Never hyphenated (AP would hyphenate as a modifier).
- **"with" in titles:** Always lowercase — "Databases Run Better with Percona," not "With."
- **Oxford comma:** Always use the serial comma — expertise, services, and solutions.
- **Job titles:** Always capitalize, including common titles. CEO is fine without spelling out.
- **Em dashes:** Used with spaces to offset an aside — "Percona Everest — which debuted in 2024 — offers customers …"

### AP Style rules that apply:
- Spell out numbers zero through nine. Use numerals for 10 and above.
- Units of measure take numerals even below 10.
- Numbers over three digits get commas.
- Spell out fractions: two-thirds, not ⅔.
- Use the % symbol. Don't spell out percent (except at the start of a sentence).
- Spell out day of week and month in a sentence: February 2, not Feb. 2.
- Time: 7:00 a.m., 7:30 p.m. Always include minutes. Specify time zones.
- One space between sentences, always.
- Do not use ampersands unless part of a brand name.
- Subheads and subtitles in sentence case.
- Buttons and CTAs in sentence case.
- Email subject lines in sentence case.

---

## Grammar and punctuation

### Commas
- Oxford comma always: expertise, services, and solutions.

### Dashes and hyphens
- Hyphen (-) without spaces: links words into a phrase or indicates range — product-led, Monday-Wednesday.
- Em dash (—) with spaces: offsets an aside — "Percona Everest — which debuted in 2024 — offers customers …"

### Ampersands
- Do not use unless part of a brand name (Ben & Jerry's). Especially never in Percona Monitoring and Management.

### Sentence length
- Most sentences should be under 30 words. Vary length deliberately.
- If a sentence lists three or more items, consider a bullet list instead.

### Contractions
- Use them. They are vital to a conversational style.

### Semicolons
- Use sparingly. An em dash usually works better.

### Exclamation marks
- Acceptable in social media, emails, and newsletters. Not in white papers or technical reports.
- Do not overuse. Never as a substitute for a more powerful sentence.

### Ellipsis
- Three periods only. Space before and after. No spaces between the three periods.

### Apostrophes
- Possessives for plural nouns ending in "s": add apostrophe only — the Percona Consultants' advice.

### Active vs. passive voice
- Use active voice most of the time.
- Passive voice is acceptable when the actor is unimportant and the result is what matters:
  Percona Toolkit is designed to solve X (passive, acceptable) vs. We designed Percona Toolkit to solve X (active, but "we" is not the point).

---

## Word choices — use these correctly

### Use "use," not "utilize" or "leverage"
When you mean use, write use. Utilize and leverage are pretentious and can carry unintended connotations.

### replica (never slave)
Use replica for node, server, database, or cluster type. Never use the word slave.

### affect vs. effect
- Affect is a verb: storms can affect database availability.
- Effect is a noun: the effects of the storm.

### after vs. following
Use after when you mean after. Following can imply adherence to something and creates ambiguity.

### ensure vs. assure vs. insure
- Insure: insurance references only.
- Ensure: guarantee — steps were taken to ensure accuracy.
- Assure: give confidence — she assured us the statement was accurate.
- Use "help ensure" or "help assure" to avoid overpromising.

### farther vs. further
- Farther: physical distance.
- Further: extension of time or degree.

### if vs. whether
- If: conditional.
- Whether: introduces an alternative (yes or no). If you can add "or not" coherently, use whether.

### last vs. past
- Past refers to an immediately preceding time period: the past two years.
- Last means final. "The last two years" implies there will be no more years.

### complement vs. compliment
- Complement: completeness or supplementing.
- Compliment: praise.

### between vs. from/to/through
- Between excludes the endpoints.
- From X to Y / from X through Y includes the endpoints.

---

## Commonly miswritten words (correct spellings)

add-on (noun/adjective), add on (verb)
back end (noun), back-end (adjective)
coworker
datasheet
email (never hyphenated, never capitalized mid-sentence)
End of Life (EOL)
eBook
front end (noun), front-end (adjective)
homepage
internet (lowercase)
login (noun/adjective), log in (verb)
machine learning
online (lowercase)
on-premises (always hyphenated, never on-prem)
opt-in (noun/adjective), opt in (verb)
out of the box / out-of-the-box (hyphenate only as modifier)
pop-up (noun/adjective), pop up (verb)
runtime
signup (noun/adjective), sign up (verb)
single point of failure (SPOF) / single points of failure
third party (noun), third-party (adjective)
URL
website
white paper (two words)
WiFi

---

## American English spelling

Use American English. Key differences:
- behavior (not behaviour)
- canceled, canceling (not cancelled, cancelling)
- center (not centre)
- color (not colour)
- gray (not grey)
- license (not licence)
- maximize, minimize, organize, realize, recognize, specialize (not -ise endings)
- analog (not analogue)
- program (not programme)

---

## PostgreSQL extension spellings

Always follow the style accepted by the PostgreSQL community. Verify against official repositories and PGXN.

Correct spellings for commonly used extensions:
- pgvector
- timescale
- PostGIS
- pgpool-II
- pg_stat_monitor
- pg_repack
- pgaudit, pgaudit_set_user
- pgBackRest
- pgbadger
- PgBouncer
- wal2json
- Patroni
- repmgr
- barman
- HAProxy
- Keepalived
- plProfiler
- WAL-e/WAL-g
- pgadmin 4
- pg_partman
- dblink
- Oracle_fdw
- pg_cron
- pg_hint_plan
- Postgres Contrib Modules
- Postgres Client/Server Utilities

---

## Bullet list rules

- Items should follow the same grammatical structure.
- Each item begins with the same or similar part of speech.
- Items should be of comparable length.
- Either all items end with a period (complete sentences) or none do (incomplete phrases).
- Items do not end with semicolons.
- The second-to-last item does not end with a conjunction.
- Introductory sentence is short, clear, and ends with a colon.
- Lists rarely go deeper than two levels.

---

## Acronyms

- Spell out in full on first mention. Include abbreviation in parentheses if using later.
- When speaking, annunciate each individual letter using standard U.S. English pronunciation.
  Example: QAN = Query Analytics on first mention. Spoken as Q-A-N (Cue-Ay-En).

---

## People, places, and things

### Quoting someone
Use present tense in blog posts and case studies to imply an ongoing relationship.

### Names
First and last name on first mention. First name only on subsequent mentions.

### United States cities and states
Spell out in full. Do not abbreviate. U.S. cities accompanied by state name, except for major cities listed in AP Style.

### International
Spell out all city, state, and country names. EU can be abbreviated after first mention (no periods needed).

### Slang and colloquialisms
Avoid. Percona has an international audience.
