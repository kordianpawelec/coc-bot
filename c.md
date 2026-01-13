🔴 IMMEDIATE EMERGENCY RESPONSE REQUIRED:
STEP 1: DISCONNECT FROM INTERNET NOW!
powershell

# Disable network adapters (temporarily)
Get-NetAdapter | Disable-NetAdapter -Confirm:$false

# Or run this command:
ipconfig /release

STEP 2: BOOT INTO SAFE MODE (Required):
powershell

# Schedule Safe Mode boot on next restart
bcdedit /set {current} safeboot network
Write-Host "RESTART YOUR COMPUTER NOW into Safe Mode with Networking"
Write-Host "After restart, run the commands below in Safe Mode"

STEP 3: IN SAFE MODE, RUN THESE COMMANDS:
powershell

# 1. Check for rootkit/hidden processes
Get-Process | Where-Object {$_.Name -eq "vmware-vmx"} | Stop-Process -Force

# 2. Check Task Scheduler for malicious tasks
Get-ScheduledTask | Where-Object {
    $_.TaskName -match "vmware|update|python|py" -and 
    $_.Author -notmatch "Microsoft|VMware"
} | Unregister-ScheduledTask -Confirm:$false

# 3. Check Startup programs
Get-CimInstance Win32_StartupCommand | Where-Object {
    $_.Command -match "vmware" -or $_.Command -match "\.vbs" -or $_.Command -match "\.js"
} | ForEach-Object {
    Write-Host "Suspicious startup: $($_.Name) - $($_.Command)"
}

# 4. Check Registry for persistence
$regPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
)

foreach ($path in $regPaths) {
    if (Test-Path $path) {
        Get-ItemProperty $path | Select-Object * -ExcludeProperty PS* | ForEach-Object {
            $_.PSObject.Properties | Where-Object {
                $_.Value -match "vmware" -or 
                $_.Value -match "powershell.*hidden" -or
                $_.Value -match "\.vbs" -or
                $_.Value -match "\.js"
            } | ForEach-Object {
                Write-Host "Suspicious registry entry in $path : $($_.Name) = $($_.Value)"
                # Remove-ItemProperty -Path $path -Name $_.Name -Force
            }
        }
    }
}

STEP 4: MALWARE REMOVAL IN SAFE MODE:
powershell

# 1. Download and run Malwarebytes ADWCleaner
Write-Host "Download: https://www.malwarebytes.com/adwcleaner"
Write-Host "Run it and remove all detected threats"

# 2. Download and run Norton Power Eraser
Write-Host "Download: https://support.norton.com/sp/en/us/home/current/solutions/v6038"
Write-Host "Run it to detect aggressive threats"

#

