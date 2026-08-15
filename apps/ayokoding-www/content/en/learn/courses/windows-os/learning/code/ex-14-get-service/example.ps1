# Example 14 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-Service | Select-Object -First 5 Status, Name, DisplayName
# => The displayed values are observations; inspect errors before drawing conclusions.

