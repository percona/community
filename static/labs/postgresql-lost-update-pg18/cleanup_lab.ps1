$ErrorActionPreference = 'Stop'
$Evidence = Join-Path $PSScriptRoot 'evidence'
$identity = Get-Content -Raw -LiteralPath (Join-Path $Evidence 'lab-identity.json') | ConvertFrom-Json
$cid = $identity.container_id
if ($cid -notmatch '^[0-9a-f]{64}$') { throw 'Invalid recorded container ID' }
$label = docker --context desktop-linux inspect $cid --format '{{index .Config.Labels "codex.percona.task"}}'
if ($LASTEXITCODE -ne 0 -or $label -ne $identity.owner_label -or $label -ne 'percona-snowwolf-20261015-pg18') { throw 'Lab ownership verification failed' }
$name = docker --context desktop-linux inspect $cid --format '{{.Name}}'
if ($LASTEXITCODE -ne 0 -or $name -ne '/lost-update-lab-pg18-20261015') { throw 'Unexpected container name' }
$mountJson = docker --context desktop-linux inspect $cid --format '{{json .Mounts}}'
if ($LASTEXITCODE -ne 0) { throw 'Mount inventory failed' }
$mounts = @($mountJson | ConvertFrom-Json)
if (@($mounts | Where-Object { $_.Type -eq 'bind' }).Count -ne 0) { throw 'Unexpected host mount; do not remove automatically' }
$volumes = @($mounts | Where-Object { $_.Type -eq 'volume' } | ForEach-Object { $_.Name })
docker --context desktop-linux rm -f -v $cid *> (Join-Path $Evidence 'cleanup-output.txt')
$removeCode = $LASTEXITCODE
if ($removeCode -ne 0) { throw 'Disposable container removal failed' }
docker --context desktop-linux inspect $cid *> (Join-Path $Evidence 'cleanup-container-check.txt')
$absentCode = $LASTEXITCODE
if ($absentCode -eq 0) { throw 'Container still exists after cleanup' }
$volumeChecks = @()
foreach ($volume in $volumes) {
    docker --context desktop-linux volume inspect $volume *> $null
    $volumeChecks += [ordered]@{name=$volume;inspect_exit_code=$LASTEXITCODE}
    if ($LASTEXITCODE -eq 0) { throw 'An associated volume remains; retain its identity' }
}
$record = [ordered]@{
    container_id=$cid;container_name=$name;owner_label=$label
    removed_owned_container=$true;remove_exit_code=$removeCode;post_remove_inspect_exit_code=$absentCode
    anonymous_volumes=$volumeChecks;cleanup_utc=(Get-Date).ToUniversalTime().ToString('o')
    scope='Only this task-created lab container and its associated anonymous volumes'
}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Evidence 'cleanup.json')
Get-Content -LiteralPath (Join-Path $Evidence 'cleanup.json')
