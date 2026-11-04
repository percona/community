PostgreSQL 18 lost-update release check — linked lab appendix

Companion lab for "Catch Lost Updates Before Release: A Two-Client
PostgreSQL Test on Windows."
The full harness is lost_update_psql_lab.py. It contains the fixture, all five
assertion cases and the A-blocks-B observations. Only its standard library is
required by Windows Python; the two competing psql clients and a controller
session run inside the Linux Percona container through Docker Desktop.

Recorded final-code validation: 2026-10-15T18:14:24.1203443Z through 2026-10-15T18:14:53.0113288Z.
Actual server: PostgreSQL 18.6 / Percona Server 18.6.1 (server_version_num 180006).
20 complete suites passed; all 20 native exits were 0; all 80 required A-blocks-B
observations were recorded. The unsafe result is a deliberate defect reproduction,
not a claim of application correctness. The closed-port check exited1, with no
PASS or final success report. Each expected quantity is3.

Unsafe, start 10 -> committed 2, stock 7 (correct stock would be 4).
Atomic, start 10 -> committed 2, stock 4.
Atomic, start 4 -> committed 1, stock 1.
Rollback, start 4 -> committed 1, stock 1.
Single-client insufficient, start 2 -> committed 0, stock 2.

The accepted count is changed-row reservations whose COMMIT completed. No order
or reservation ledger is stored. A provisional RETURNING followed by ROLLBACK
does not count. Multi-SKU workflows, duplicate-request idempotency and Serializable
transaction retry behavior are outside this fixture.

Automated Windows validation was AI-assisted using Codex on Jack VanSickle's
SNOW-WOLF machine. The evidence attributes that recorded run specifically; the
validator defaults to an unspecified operator for new runs and records the real
COMPUTERNAME. Use -AiAssisted only when that describes your own run.

Image tag: percona/percona-distribution-postgresql:18.6
Pinned image: percona/percona-distribution-postgresql:18.6@sha256:27a1dba816fcc4cec88f216d54e3ec86db4c1d4b16799f49800055c41606e11e
Image ID: sha256:27a1dba816fcc4cec88f216d54e3ec86db4c1d4b16799f49800055c41606e11e
Harness SHA256: 5d80c87e0ba114b5302efe2a97ac59bcdfaf3fb9f5952c853e512b7f2fada484
Validator SHA256: 3b397209a03e08c44887fa8813be9f0b3ec8f28305159307f9f5f9b2bb95c907

Prerequisites: Docker Desktop Linux containers and its desktop-linux context,
PowerShell, and an installed stable Python. The actual test used Python 3.13.2
64 bit, PowerShell 7.6.5, Windows 11 Home build 26300, Docker Desktop 4.95.0 and Engine 29.8.2.
No host PostgreSQL or pip package was installed.

Reproduce from a local copy of this lab directory (not on a shared database):

  $lock=Get-Content -Raw .\image-lock.json | ConvertFrom-Json
  docker --context desktop-linux pull $lock.pinned_ref
  if ($LASTEXITCODE -ne 0) { throw 'Pinned image pull failed' }
  & .\start_lab.ps1
  & .\validate_psql_lab.ps1 -Runs 20 -Operator 'your name or test runner'
  # Supply -AiAssisted only if applicable to the new run.
  # Keep the new evidence before cleanup.
  & .\cleanup_lab.ps1

Copy the five source/config files above, including image-lock.json. Scripts create
a new evidence/ directory; recorded-evidence/ holds the historical run and is not
overwritten. Startup uses --pull never after the explicit pull. The recorded
validation invoked startup with -RequireSnowWolf and validation with -Runs 20
-Operator 'Codex on authorized SNOW-WOLF' -AiAssisted.

The disposable name is lost-update-lab-pg18-20261015, with loopback host port 55432,
one CPU and 512 MiB. It has no host filesystem mounts. The password in the source
is a deliberately disposable fixture value; no live or personal credential is used.
Stop if the name or port is occupied. Never reuse an existing container or database.
Cleanup verifies exact container ID, name, ownership label and absence of bind
mounts before removing only that lab and its associated anonymous volumes.

Readiness probes container TCP 127.0.0.1:5432. The controller uses that internal
endpoint; this does not test a Windows libpq driver or the published host port.
Unique response markers, ON_ERROR_STOP, response deadlines, bounded Barrier/Event
waits and retrieved future results prevent database errors from becoming rejections.

If startup fails before recording lab-identity.json, docker run may have created
a stopped container. Stop and inspect only the exact proposed name and its task
label; do not reuse it or run a broad prune. Recover/verify its exact identity
before any cleanup. The recorded validation had no such startup failure.

The original lab and associated anonymous volumes were removed after evidence
capture. Recorded container IDs are historical evidence, not live targets.
Publication evidence includes all 20 original suite logs, the original run-status
and validation-summary JSON, and the original wrong-port exit record. Those files
are unchanged from the recorded validation. The supplied wrong-port traceback is
also unchanged from the reviewed copy, where local folder prefixes were redacted.
environment.txt consolidates eight historical platform/version/isolation records
and omits the local Python executable location. No version, outcome or exit code
was changed. Historical container identity, image-pull, port-binding and cleanup
receipts are omitted. The five source/config files remain byte-identical to the
tested files. SHA256.json covers only the files published in this appendix.

Official image documentation:
https://docs.percona.com/postgresql/18/docker/docker.html
Official release notes:
https://docs.percona.com/postgresql/18/release-notes/release-notes-v18.6.1.html
