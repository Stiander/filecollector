# file_collector.ps1
param(
    [switch]$simple,
    [switch]$help
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptPath "file_collector.py"

$arguments = @()
if ($simple) { $arguments += "--simple" }
if ($help) { $arguments += "--help" }

# Try to find Python in the system
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if ($pythonCmd) {
    & $pythonCmd.Source $pythonScript $arguments
}
else {
    Write-Error "Python is not found in the system. Please install Python and make sure it's in your PATH."
    exit 1
}