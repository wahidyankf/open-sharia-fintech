# Example 15 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 ProcessName, Id, WorkingSet64
# => The displayed values are observations; inspect errors before drawing conclusions.

