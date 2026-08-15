# Example 46 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-CimInstance Win32_Process | Select-Object -First 5 ProcessId, ParentProcessId, Name
# => The displayed values are observations; inspect errors before drawing conclusions.

