# Example 40 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-Process -Id $PID | Select-Object Id, ProcessName, WorkingSet64
# => The displayed values are observations; inspect errors before drawing conclusions.

