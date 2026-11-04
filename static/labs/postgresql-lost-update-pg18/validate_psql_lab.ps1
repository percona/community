param([int]$Runs=20,[string]$Operator='Unspecified operator',[switch]$AiAssisted)
$ErrorActionPreference='Stop'
if ($Runs -lt 1) { throw 'Runs must be positive' }
$Evidence=Join-Path $PSScriptRoot 'evidence'
$Harness=Join-Path $PSScriptRoot 'lost_update_psql_lab.py'
$Python=(Get-Command python -ErrorAction Stop).Source
if (Test-Path -LiteralPath (Join-Path $Evidence 'psql-run-status.json')) { throw 'Preserve existing suite records before rerunning' }
$started=(Get-Date).ToUniversalTime().ToString('o')
& $Python -m py_compile $Harness
$compileCode=$LASTEXITCODE
if ($compileCode -ne 0) { throw 'Harness compilation failed' }
$records=@()
$blockingTotal=0
$expected=@('BUG_REPRODUCED unsafe start=10 committed=2 stock=7','PASS atomic start=10 committed=2 stock=4','PASS atomic start=4 committed=1 stock=1','PASS rollback start=4 committed=1 stock=1','PASS insufficient start=2 committed=0 stock=2','ALL EXPECTED CONDITIONS MET')
foreach ($i in 1..$Runs) {
    $log=Join-Path $Evidence ('psql-run-{0:D2}.txt' -f $i)
    & $Python $Harness *> $log
    $code=$LASTEXITCODE
    $lines=@(Get-Content -LiteralPath $log)
    $blocking=@($lines | Where-Object { $_ -like 'BLOCKING *' }).Count
    $records += [ordered]@{run=$i;exit_code=$code;blocking_pairs=$blocking;log=(Split-Path $log -Leaf)}
    $records | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Evidence 'psql-run-status.json')
    if ($code -ne 0) { throw "Failed PostgreSQL18 run $i; inspect $log" }
    if ($blocking -ne 4) { throw 'Incomplete overlap evidence' }
    foreach ($line in $expected) { if ($lines -cnotcontains $line) { throw "Missing expected outcome: $line" } }
    $blockingTotal += $blocking
    Write-Output "Completed PostgreSQL18 measured run $i/$Runs, exit=$code, blocking_pairs=$blocking"
}
$oldPort=[Environment]::GetEnvironmentVariable('LU_LAB_CONTAINER_PORT','Process')
try {
    $env:LU_LAB_CONTAINER_PORT='5433'
    $failureLog=Join-Path $Evidence 'psql-wrong-port.txt'
    & $Python $Harness *> $failureLog
    $failureCode=$LASTEXITCODE
    $failureCode | Set-Content -LiteralPath (Join-Path $Evidence 'psql-wrong-port-exit.txt')
    if ($failureCode -eq 0) { throw 'Wrong port unexpectedly succeeded' }
    if ((Get-Content -Raw -LiteralPath $failureLog) -match 'PASS |BUG_REPRODUCED|ALL EXPECTED CONDITIONS MET') { throw 'Connection failure reported a passing outcome' }
} finally { [Environment]::SetEnvironmentVariable('LU_LAB_CONTAINER_PORT',$oldPort,'Process') }
& $Python -c "import sys,platform; print(sys.version); print(platform.architecture()[0]); print(sys.executable)" *> (Join-Path $Evidence 'python-version.txt')
if ($LASTEXITCODE -ne 0) { throw 'Python version capture failed' }
$summary=[ordered]@{
    started_utc=$started;finished_utc=(Get-Date).ToUniversalTime().ToString('o')
    operator=$Operator;windows_host=$env:COMPUTERNAME;ai_assisted_automated_windows_testing=[bool]$AiAssisted
    transport='Windows Python standard library controlling existing Linux-container psql clients'
    server_major=18;server_version_num=[int](Get-Content -Raw -LiteralPath (Join-Path $Evidence 'server-version-num.txt')).Trim()
    harness=(Split-Path $Harness -Leaf);harness_sha256=(Get-FileHash -LiteralPath $Harness -Algorithm SHA256).Hash.ToLowerInvariant()
    validator_sha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    measured_complete_suites=$records.Count;successful_suites=@($records | Where-Object { $_.exit_code -eq 0 }).Count
    observed_blocking_pairs=$blockingTotal;wrong_port=$failureCode;compilation_exit=$compileCode
}
$summary | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Evidence 'psql-validation-summary.json')
Get-Content -LiteralPath (Join-Path $Evidence 'psql-validation-summary.json')
