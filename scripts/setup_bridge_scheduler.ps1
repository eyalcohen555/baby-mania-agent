# BabyMania Bridge — Windows Task Scheduler Setup
# Registers a logon-triggered task that starts bridge.py automatically.

$TaskName   = "BabyMania Bridge AutoStart"
$ProjectDir = "C:\Projects\baby-mania-agent"
$BatFile    = $ProjectDir + "\start-bridge.bat"

# Verify bat file exists
if (-not (Test-Path $BatFile)) {
    Write-Error ("NOT FOUND: " + $BatFile + " - abort.")
    exit 1
}

# Action
$CmdArg = '/c "' + $BatFile + '"'
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument $CmdArg -WorkingDirectory $ProjectDir

# Trigger: at logon of current user
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

# Settings
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 2) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -MultipleInstances IgnoreNew

# Principal: current user, interactive
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# Register
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force | Out-Null

Write-Host "STATUS: REGISTERED"
Write-Host ("TASK NAME: " + $TaskName)
Write-Host ("TRIGGER: At logon - " + $env:USERNAME)
Write-Host ("ACTION: cmd.exe " + $CmdArg)
Write-Host ("WORKING DIR: " + $ProjectDir)

# Verify
$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($task) {
    Write-Host ("VERIFY: Task found - State=" + $task.State)
    Write-Host "RESULT: PASS"
} else {
    Write-Host "VERIFY: Task NOT found"
    Write-Host "RESULT: FAIL"
    exit 1
}
