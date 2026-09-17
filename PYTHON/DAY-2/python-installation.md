```
Absolutely. Here is a complete PowerShell script that:

Checks whether PowerShell is running as Administrator
Installs Chocolatey if it is not already installed
Refreshes the environment
Installs Python 3.14 through Chocolatey
Verifies Python and pip
Displays the installed versions

Save this as install-python.ps1.
```

## Open PowerShell as Administrator, then:
```
Set-ExecutionPolicy Bypass -Scope Process -Force
.\install-python.ps1
```

## If you specifically need the latest Python 3.14.x, rather than exactly 3.14.0, I recommend using:
```
choco install python314 -y --no-progress
```

