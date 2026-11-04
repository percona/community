param([switch]$RequireSnowWolf)
$ErrorActionPreference = 'Stop'
$Name = 'lost-update-lab-pg18-20261015'
$Owner = 'percona-snowwolf-20261015-pg18'
$Evidence = Join-Path $PSScriptRoot 'evidence'
$lock = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'image-lock.json') | ConvertFrom-Json
if ($lock.requested_tag -ne 'percona/percona-distribution-postgresql:18.6' -or $lock.pinned_ref -notmatch '^percona/percona-distribution-postgresql:18\.6@sha256:[0-9a-f]{64}$') { throw 'Unexpected image lock' }
if ($RequireSnowWolf -and $env:COMPUTERNAME -ne 'SNOW-WOLF') { throw 'This validation targets SNOW-WOLF' }
New-Item -ItemType Directory -Force -Path $Evidence | Out-Null
if (Test-Path -LiteralPath (Join-Path $Evidence 'lab-identity.json')) { throw 'Existing lab identity; preserve it before a new run' }
$existing = docker --context desktop-linux ps -a --filter 'name=^/lost-update-lab-pg18-20261015$' --format '{{.ID}}'
if ($LASTEXITCODE -ne 0) { throw 'Container inventory failed' }
if ($existing) { throw 'Lab name exists; do not reuse or remove it automatically' }
if (Get-NetTCPConnection -LocalPort 55432 -State Listen -ErrorAction SilentlyContinue) { throw 'Lab port 55432 is occupied' }
$mode = docker --context desktop-linux info --format '{{.OSType}}'
if ($LASTEXITCODE -ne 0 -or $mode -ne 'linux') { throw 'Linux container mode required' }
$actualImage = docker --context desktop-linux image inspect $lock.pinned_ref --format '{{.Id}}'
if ($LASTEXITCODE -ne 0 -or $actualImage -ne $lock.image_id) { throw 'Locked image unavailable or changed; do not pull automatically' }
$cid = docker --context desktop-linux run --pull never --name $Name --label "codex.percona.task=$Owner" --restart no --memory 512m --cpus 1 -d -p 127.0.0.1:55432:5432 -e POSTGRES_PASSWORD=lab-only-disposable -e POSTGRES_DB=lost_updates $lock.pinned_ref
if ($LASTEXITCODE -ne 0) { throw 'Disposable container start failed' }
$identity = [ordered]@{
    container_id=$cid;container_name=$Name;owner_label=$Owner;docker_context='desktop-linux'
    image_tag=$lock.requested_tag;image_id=$lock.image_id;pinned_ref=$lock.pinned_ref
    repo_digests=@($lock.repo_digest);created_utc=(Get-Date).ToUniversalTime().ToString('o')
}
$identity | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Evidence 'lab-identity.json')
$ready=$false
for ($i=0;$i -lt 60;$i++) {
    docker --context desktop-linux exec $cid pg_isready -h 127.0.0.1 -p 5432 -U postgres -d lost_updates
    if ($LASTEXITCODE -eq 0) { $ready=$true;break }
    Start-Sleep -Seconds 1
}
docker --context desktop-linux logs $cid *> (Join-Path $Evidence 'startup-container-log.txt')
if ($LASTEXITCODE -ne 0) { throw 'Container log capture failed' }
if (-not $ready) { throw 'Database did not become TCP-ready; keep failed startup evidence' }
$binding=docker --context desktop-linux inspect $cid --format '{{json .NetworkSettings.Ports}}'
if ($LASTEXITCODE -ne 0) { throw 'Port verification failed' }
$binding | Set-Content -LiteralPath (Join-Path $Evidence 'port-binding.json')
$ports=$binding | ConvertFrom-Json
if ($ports.'5432/tcp'.Count -ne 1 -or $ports.'5432/tcp'[0].HostIp -ne '127.0.0.1' -or $ports.'5432/tcp'[0].HostPort -ne '55432') { throw 'Unexpected published endpoint' }
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $Evidence 'windows.json')
$PSVersionTable | Out-String | Set-Content -LiteralPath (Join-Path $Evidence 'powershell.txt')
docker --context desktop-linux version *> (Join-Path $Evidence 'docker-version.txt')
if ($LASTEXITCODE -ne 0) { throw 'Docker version capture failed' }
docker --context desktop-linux exec $cid psql --version *> (Join-Path $Evidence 'psql-version.txt')
if ($LASTEXITCODE -ne 0) { throw 'Client version capture failed' }
docker --context desktop-linux exec $cid psql -X -v ON_ERROR_STOP=1 -U postgres -d lost_updates -c 'SELECT version();' *> (Join-Path $Evidence 'server-version.txt')
if ($LASTEXITCODE -ne 0) { throw 'Server version capture failed' }
docker --context desktop-linux exec $cid psql -X -At -v ON_ERROR_STOP=1 -U postgres -d lost_updates -c 'SHOW server_version_num;' *> (Join-Path $Evidence 'server-version-num.txt')
if ($LASTEXITCODE -ne 0) { throw 'Server major-version capture failed' }
$number=[int](Get-Content -Raw -LiteralPath (Join-Path $Evidence 'server-version-num.txt')).Trim()
if ($number -lt 180000 -or $number -ge 190000) { throw 'Wrong server major version' }
docker --context desktop-linux exec $cid psql -X -v ON_ERROR_STOP=1 -U postgres -d lost_updates -c 'SHOW default_transaction_isolation;' *> (Join-Path $Evidence 'server-isolation.txt')
if ($LASTEXITCODE -ne 0) { throw 'Isolation capture failed' }
Get-Content -LiteralPath (Join-Path $Evidence 'lab-identity.json')
Get-Content -LiteralPath (Join-Path $Evidence 'server-version.txt')
