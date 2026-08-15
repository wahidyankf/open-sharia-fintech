# Example 12 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-Process | Select-Object -First 5 Id, ProcessName, CPU
# => The displayed values are observations; inspect errors before drawing conclusions.

