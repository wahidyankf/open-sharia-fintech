# Example 13 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-Process -Name powershell -ErrorAction SilentlyContinue | Select-Object Id, ProcessName
# => The displayed values are observations; inspect errors before drawing conclusions.

