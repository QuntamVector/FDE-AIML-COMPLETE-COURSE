# ============================================================
# Install Chocolatey + Python 3.14
# Run this PowerShell script as Administrator
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Chocolatey + Python 3.14 Installation" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# ------------------------------------------------------------
# 1. Check Administrator privileges
# ------------------------------------------------------------

Write-Host "`n[1/6] Checking Administrator privileges..." -ForegroundColor Yellow

$currentPrincipal = New-Object Security.Principal.WindowsPrincipal(
    [Security.Principal.WindowsIdentity]::GetCurrent()
)

if (-not $currentPrincipal.IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator
)) {
    Write-Host "ERROR: Please run PowerShell as Administrator." -ForegroundColor Red
    exit 1
}

Write-Host "Administrator privileges confirmed." -ForegroundColor Green


# ------------------------------------------------------------
# 2. Check / Install Chocolatey
# ------------------------------------------------------------

Write-Host "`n[2/6] Checking Chocolatey installation..." -ForegroundColor Yellow

if (Get-Command choco -ErrorAction SilentlyContinue) {

    Write-Host "Chocolatey is already installed." -ForegroundColor Green

}
else {

    Write-Host "Chocolatey not found. Installing Chocolatey..." -ForegroundColor Yellow

    Set-ExecutionPolicy Bypass -Scope Process -Force

    [System.Net.ServicePointManager]::SecurityProtocol =
        [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

    Invoke-Expression (
        (New-Object System.Net.WebClient).DownloadString(
            'https://community.chocolatey.org/install.ps1'
        )
    )

    Write-Host "Chocolatey installation completed." -ForegroundColor Green
}


# ------------------------------------------------------------
# 3. Refresh PATH
# ------------------------------------------------------------

Write-Host "`n[3/6] Refreshing environment variables..." -ForegroundColor Yellow

$env:Path = [System.Environment]::GetEnvironmentVariable(
    "Path",
    "Machine"
) + ";" + [System.Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {

    $chocoPath = "$env:ChocolateyInstall\bin"

    if (Test-Path $chocoPath) {
        $env:Path += ";$chocoPath"
    }
}

Write-Host "Environment refreshed." -ForegroundColor Green


# ------------------------------------------------------------
# 4. Verify Chocolatey
# ------------------------------------------------------------

Write-Host "`n[4/6] Verifying Chocolatey..." -ForegroundColor Yellow

choco --version

Write-Host "Chocolatey is ready." -ForegroundColor Green


# ------------------------------------------------------------
# 5. Install Python 3.14
# ------------------------------------------------------------

Write-Host "`n[5/6] Installing Python 3.14..." -ForegroundColor Yellow

# Remove older Python package if you specifically want
# Chocolatey to manage Python.
#
# Uncomment the following line if required:
# choco uninstall python -y

choco install python --version=3.14.0 -y --no-progress

Write-Host "Python 3.14 installation completed." -ForegroundColor Green


# ------------------------------------------------------------
# 6. Refresh PATH again and verify Python
# ------------------------------------------------------------

Write-Host "`n[6/6] Verifying Python installation..." -ForegroundColor Yellow

$env:Path = [System.Environment]::GetEnvironmentVariable(
    "Path",
    "Machine"
) + ";" + [System.Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

Write-Host "`nPython version:" -ForegroundColor Cyan
python --version

Write-Host "`nPip version:" -ForegroundColor Cyan
python -m pip --version

Write-Host "`nPython location:" -ForegroundColor Cyan
where.exe python

Write-Host "`n============================================" -ForegroundColor Green
Write-Host " Installation completed successfully!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green